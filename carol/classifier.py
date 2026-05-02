import os
from loguru import logger
from .schemas import Transaction, MacroCategory


CONFIDENCE_THRESHOLD = float(os.getenv("CLASSIFICATION_CONFIDENCE_THRESHOLD", 0.85))


def classify_transaction(transaction: Transaction) -> Transaction:
    if transaction.confidence_score < CONFIDENCE_THRESHOLD:
        logger.warning(f"Confianza baja: {transaction.confidence_score}")

    if not transaction.macro:
        transaction.macro = MacroCategory.PERSONAL
        transaction.subcategory = "Sin categorizar"
        transaction.confidence_score = 0.5

    return transaction
