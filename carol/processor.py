from loguru import logger
from .ocr import extract_from_image, extract_from_text
from .classifier import classify_transaction
from .schemas import Transaction, MacroCategory
from .learner import get_store_rule, save_store_rule
from db.session import SessionLocal
from db.models import Transaction as TransactionDB


def process_image(image_path: str, user_id: str = None) -> Transaction:
    logger.info(f"Procesando imagen: {image_path}")

    db = SessionLocal()
    try:
        transaction = extract_from_image(image_path)
        transaction = classify_transaction(transaction)

        rule = get_store_rule(db, transaction.store, user_id)
        if rule:
            transaction.macro = rule.macro
            transaction.subcategory = rule.subcategory
            transaction.confidence_score = rule.confidence_score
        else:
            save_store_rule(db, transaction, user_id)

        # Guardar transacción en BD
        db_transaction = TransactionDB(
            store=transaction.store,
            rfc=transaction.rfc,
            address=transaction.address,
            phone=transaction.phone,
            folio=transaction.folio,
            date=transaction.date,
            time=transaction.time,
            total=transaction.total,
            currency=transaction.currency,
            macro=transaction.macro.value if isinstance(transaction.macro, MacroCategory) else transaction.macro,
            subcategory=transaction.subcategory,
            confidence_score=transaction.confidence_score,
            registered_at=transaction.registered_at
        )
        db.add(db_transaction)
        db.commit()

        return transaction
    finally:
        db.close()


def process_text(text: str, user_id: str = None) -> Transaction:
    logger.info(f"Procesando texto: {text[:50]}...")

    db = SessionLocal()
    try:
        transaction = extract_from_text(text)
        transaction = classify_transaction(transaction)

        rule = get_store_rule(db, transaction.store, user_id)
        if rule:
            transaction.macro = rule.macro
            transaction.subcategory = rule.subcategory
            transaction.confidence_score = rule.confidence_score
        else:
            save_store_rule(db, transaction, user_id)

        # Guardar transacción en BD
        db_transaction = TransactionDB(
            store=transaction.store,
            rfc=transaction.rfc,
            address=transaction.address,
            phone=transaction.phone,
            folio=transaction.folio,
            date=transaction.date,
            time=transaction.time,
            total=transaction.total,
            currency=transaction.currency,
            macro=transaction.macro.value if isinstance(transaction.macro, MacroCategory) else transaction.macro,
            subcategory=transaction.subcategory,
            confidence_score=transaction.confidence_score,
            registered_at=transaction.registered_at
        )
        db.add(db_transaction)
        db.commit()

        return transaction
    finally:
        db.close()
