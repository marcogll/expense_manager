import os
import tempfile
from dotenv import load_dotenv
from telegram.ext import Application, MessageHandler, CommandHandler, filters
from loguru import logger
from .messages import RECEIVED, WELCOME
from carol.processor import process_image, process_text
from carol.pdf_handler import extract_text_from_pdf
from carol.voice_handler import transcribe_voice
from integrations.n8n import send_to_n8n
from carol.schemas import Transaction

load_dotenv()

TOPIC_ID = os.getenv("TOPIC_ID")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
USER_ID = os.getenv("TELEGRAM_USER_ID")

if TOPIC_ID:
    TOPIC_ID = int(TOPIC_ID)


def check_access(update) -> bool:
    if CHAT_ID and str(update.effective_chat.id) != CHAT_ID:
        return False
    if USER_ID and str(update.effective_user.id) != USER_ID:
        return False
    return True


async def start(update, context):
    if not check_access(update):
        return
    await update.message.reply_text(WELCOME, message_thread_id=TOPIC_ID)


async def handle_message(update, context):
    if not check_access(update):
        return

    message = update.message

    if message.photo:
        await process_photo(update, context)
    elif message.document:
        await process_document(update, context)
    elif message.voice:
        await process_voice(update, context)
    else:
        # Check if it's a correction first
        if not await handle_correction(update, context):
            await message.reply_text(RECEIVED, message_thread_id=TOPIC_ID)


async def process_photo(update, context):
    message = update.message
    await message.reply_text(RECEIVED, message_thread_id=TOPIC_ID)
    user_id = str(update.effective_user.id)

    photo = message.photo[-1]
    file = await context.bot.get_file(photo.file_id)

    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
        await file.download_to_drive(tmp.name)
        result = process_image(tmp.name, user_id)

        items_text = "\n".join([f"  • {i.quantity}x {i.name} - ${i.total:.2f}" for i in result.items]) if result.items else ""
        msg = (
            f"✅ **{result.store}**\n"
            f"RFC: {result.rfc or 'N/A'}\n"
            f"Fecha: {result.date}\n"
            f"Total: ${result.total:.2f}\n"
            f"Categoría: {result.macro} › {result.subcategory}\n"
            f"Confianza: {result.confidence_score:.0%}\n"
        )
        if items_text:
            msg += f"Ítems:\n{items_text}"

        await message.reply_text(msg, message_thread_id=TOPIC_ID, parse_mode="Markdown")
        send_to_n8n(result.model_dump())
        logger.info(f"Imagen procesada: {result}")
    os.unlink(tmp.name)


async def process_document(update, context):
    message = update.message
    await message.reply_text(RECEIVED, message_thread_id=TOPIC_ID)
    user_id = str(update.effective_user.id)

    doc = message.document
    file = await context.bot.get_file(doc.file_id)

    suffix = f".{doc.file_name.split('.')[-1]}" if doc.file_name else ".pdf"

    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        await file.download_to_drive(tmp.name)

        if doc.mime_type == "application/pdf":
            text = extract_text_from_pdf(tmp.name)
            result = process_text(text, user_id)
        items_text = "\n".join([f"  • {i.quantity}x {i.name} - ${i.total:.2f}" for i in result.items]) if result.items else ""
        msg = (
            f"✅ **{result.store}**\n"
            f"RFC: {result.rfc or 'N/A'}\n"
            f"Dirección: {result.address or 'N/A'}\n"
            f"Tel: {result.phone or 'N/A'}\n"
            f"Folio: {result.folio or 'N/A'}\n"
            f"Fecha ticket: {result.date} {result.time or ''}\n"
            f"Registrado: {result.registered_at[:19].replace('T', ' ') if result.registered_at else 'N/A'}\n"
            f"Total: {result.currency} ${result.total:.2f}\n"
            f"Categoría: {result.macro} › {result.subcategory}\n"
            f"Confianza: {result.confidence_score:.0%}\n"
        )
        if items_text:
            msg += f"Ítems:\n{items_text}"
            await message.reply_text(msg, message_thread_id=TOPIC_ID, parse_mode="Markdown")
            send_to_n8n(result.model_dump())
            logger.info(f"PDF procesado: {result}")
        else:
            logger.warning(f"Tipo de archivo no soportado: {doc.mime_type}")

    os.unlink(tmp.name)


async def process_voice(update, context):
    message = update.message
    await message.reply_text(RECEIVED, message_thread_id=TOPIC_ID)
    user_id = str(update.effective_user.id)

    voice = message.voice
    file = await context.bot.get_file(voice.file_id)

    with tempfile.NamedTemporaryFile(suffix=".ogg", delete=False) as tmp:
        await file.download_to_drive(tmp.name)
        text = transcribe_voice(tmp.name)
        result = process_text(text, user_id)
        items_text = "\n".join([f"  • {i.quantity}x {i.name} - ${i.total:.2f}" for i in result.items]) if result.items else ""
        msg = (
            f"✅ **{result.store}**\n"
            f"RFC: {result.rfc or 'N/A'}\n"
            f"Fecha: {result.date}\n"
            f"Total: ${result.total:.2f}\n"
            f"Categoría: {result.macro} › {result.subcategory}\n"
            f"Confianza: {result.confidence_score:.0%}\n"
        )
        if items_text:
            msg += f"Ítems:\n{items_text}"
        await message.reply_text(msg, message_thread_id=TOPIC_ID, parse_mode="Markdown")
        send_to_n8n(result.model_dump())
        logger.info(f"Voz procesada: {result}")
    os.unlink(tmp.name)


async def handle_correction(update, context):
    user_id = str(update.effective_user.id)
    text = update.message.text.lower()

    if "no, es" in text or "corregir" in text:
        if "personal" in text:
            macro = "Personal"
        elif "negocio" in text:
            macro = "Negocio"
        else:
            return False

        from carol.learner import save_exception
        from db.session import SessionLocal

        db = SessionLocal()
        try:
            # TODO: get last store from context or user session
            save_exception(db, "última_tienda", user_id, macro, "corregido")
        finally:
            db.close()

        await update.message.reply_text(f"Corregido a: {macro}", message_thread_id=TOPIC_ID)
        return True

    return False


def create_bot():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        logger.error("TELEGRAM_BOT_TOKEN no configurado")
        raise ValueError("TELEGRAM_BOT_TOKEN requerido")

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.ALL, handle_message))

    logger.info("Talia bot inicializado")
    return app
