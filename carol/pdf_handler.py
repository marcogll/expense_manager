import os
from pypdf import PdfReader
from loguru import logger


def extract_text_from_pdf(pdf_path: str) -> str:
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        logger.info(f"Texto extraído de PDF: {len(text)} caracteres")
        return text
    except Exception as e:
        logger.error(f"Error leyendo PDF: {e}")
        raise
