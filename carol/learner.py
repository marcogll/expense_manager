from sqlalchemy.orm import Session
from loguru import logger
from db.models import StoreRule, Exception as StoreException
from carol.schemas import Transaction, MacroCategory


def get_store_rule(db: Session, store_name: str, user_id: str = None):
    if user_id:
        exception = db.query(StoreException).filter(
            StoreException.store_name == store_name,
            StoreException.user_id == user_id
        ).first()
        if exception:
            logger.info(f"Excepción encontrada para {store_name} / user {user_id}")
            return exception

    rule = db.query(StoreRule).filter(StoreRule.store_name == store_name).first()
    if rule:
        logger.info(f"Regla encontrada para {store_name}")
        return rule

    return None


def save_store_rule(db: Session, transaction: Transaction, user_id: str = None):
    existing = db.query(StoreRule).filter(StoreRule.store_name == transaction.store).first()

    if not existing:
        rule = StoreRule(
            store_name=transaction.store,
            macro=transaction.macro.value if isinstance(transaction.macro, MacroCategory) else transaction.macro,
            subcategory=transaction.subcategory,
            confidence_score=transaction.confidence_score
        )
        db.add(rule)
        db.commit()
        logger.info(f"Nueva regla guardada para {transaction.store}")


def save_exception(db: Session, store_name: str, user_id: str, macro: str, subcategory: str):
    exception = StoreException(
        store_name=store_name,
        user_id=user_id,
        macro=macro,
        subcategory=subcategory
    )
    db.add(exception)
    db.commit()
    logger.info(f"Excepción guardada para {store_name} / user {user_id}")
