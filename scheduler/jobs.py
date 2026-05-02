import asyncio
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from loguru import logger
import os

scheduler = BackgroundScheduler()
bot_app = None


def setup_scheduler(app=None):
    global bot_app
    bot_app = app
    tz = os.getenv("TZ", "America/Monterrey")
    topic_id = os.getenv("TOPIC_ID")
    if topic_id:
        topic_id = int(topic_id)

    def run_async(coro):
        asyncio.run(coro)

    scheduler.add_job(
        lambda: run_async(morning_reminder(topic_id)),
        CronTrigger(hour=9, minute=0, timezone=tz),
        id="morning_reminder",
        replace_existing=True
    )

    scheduler.add_job(
        lambda: run_async(evening_reminder(topic_id)),
        CronTrigger(hour=17, minute=0, timezone=tz),
        id="evening_reminder",
        replace_existing=True
    )

    scheduler.add_job(
        lambda: run_async(weekly_report(topic_id)),
        CronTrigger(day_of_week="sun", hour=20, minute=0, timezone=tz),
        id="weekly_report",
        replace_existing=True
    )

    scheduler.start()
    logger.info("Scheduler iniciado")


async def morning_reminder(topic_id):
    from talia.messages import REMINDER_MORNING
    logger.info("Enviando recordatorio matutino")
    if bot_app and topic_id:
        await bot_app.bot.send_message(chat_id=os.getenv("TELEGRAM_CHAT_ID"), text=REMINDER_MORNING, message_thread_id=topic_id)


async def evening_reminder(topic_id):
    from talia.messages import REMINDER_EVENING
    logger.info("Enviando recordatorio vespertino")
    if bot_app and topic_id:
        await bot_app.bot.send_message(chat_id=os.getenv("TELEGRAM_CHAT_ID"), text=REMINDER_EVENING, message_thread_id=topic_id)


async def weekly_report(topic_id):
    from talia.messages import WEEKLY_REPORT
    from db.models import Transaction
    from db.session import SessionLocal
    from sqlalchemy import func

    logger.info("Generando reporte semanal")
    if not bot_app or not topic_id:
        return

    db = SessionLocal()
    try:
        total = db.query(func.sum(Transaction.total)).scalar() or 0
        personal = db.query(func.sum(Transaction.total)).filter(Transaction.macro == "Personal").scalar() or 0
        business = db.query(func.sum(Transaction.total)).filter(Transaction.macro == "Negocio").scalar() or 0

        text = WEEKLY_REPORT.format(
            total=f"${total:.2f}",
            personal=f"${personal:.2f}",
            business=f"${business:.2f}",
            top_categories="N/A"
        )
        await bot_app.bot.send_message(chat_id=os.getenv("TELEGRAM_CHAT_ID"), text=text, message_thread_id=topic_id)
    finally:
        db.close()
