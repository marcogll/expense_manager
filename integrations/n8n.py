import os
import requests
from loguru import logger
from time import sleep


def send_to_n8n(transaction: dict, max_retries: int = 3) -> bool:
    url = os.getenv("N8N_WEBHOOK_URL")

    if not url:
        logger.error("N8N_WEBHOOK_URL no configurada")
        return False

    headers = {"Content-Type": "application/json"}

    for attempt in range(max_retries):
        try:
            response = requests.post(url, json=transaction, headers=headers, timeout=10)

            if response.status_code == 200:
                logger.info("Datos enviados a n8n exitosamente")
                return True
            logger.warning(f"Intento {attempt + 1} falló: {response.status_code} - {response.text[:100]}")
        except Exception as e:
            logger.error(f"Error enviando a n8n: {e}")

        sleep(2 ** attempt)

    logger.error(f"Falló envío a n8n después de {max_retries} intentos")
    return False
