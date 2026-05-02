import base64
import os
from loguru import logger
from .llm_client import get_llm_client
from .schemas import Transaction

SYSTEM_PROMPT = """Eres C.A.R.O.L., un extractor de datos de tickets/facturas.
Analiza la imagen o texto y extrae TODA la información visible en formato JSON:
{
  "store": "nombre de la tienda",
  "rfc": "RFC del emisor (si aparece)",
  "address": "dirección de la tienda (si aparece)",
  "phone": "teléfono (si aparece)",
  "folio": "número de ticket/folio (si aparece)",
  "date": "YYYY-MM-DD",
  "time": "HH:MM (hora del ticket, si aparece)",
  "total": float,
  "currency": "código de moneda (MXN, USD, EUR, etc.)",
  "macro": "Personal" o "Negocio",
  "subcategory": "categoría específica (usa las listas abajo)",
  "confidence_score": float entre 0 y 1,
  "items": [{"name": "producto", "quantity": int, "unit_price": float, "total": float, "subcategory": "subcategoría"}]
}

CATEGORÍAS PERSONALES: Alimentación, Restaurantes, Transporte, Servicios, Salud, Entretenimiento, Educación, Hogar, Ropa y Calzado, Regalos, Seguros, Impuestos y Trámites, Mascotas, Flores y Plantas

CATEGORÍAS DE NEGOCIO: Refacciones, Oficina, Telecomunicaciones, Transporte y Logística, Publicidad y Marketing, Servicios Profesionales, Nómina y Prestaciones, Rentas y Servicios, Capital Gasto, Capacitación y Desarrollo, Viajes y Hospedaje, Software y SaaS

Extrae TODOS los campos visibles. Si no aparece un campo, usa null."""


def encode_image(image_path: str) -> str:
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def extract_from_image(image_path: str) -> Transaction:
    client, model = get_llm_client()
    base64_image = encode_image(image_path)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": [
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
            ]}
        ],
        response_format={"type": "json_object"}
    )

    data = response.choices[0].message.content
    logger.info(f"OCR extraído: {data}")
    return Transaction.model_validate_json(data)


def extract_from_text(text: str) -> Transaction:
    client, model = get_llm_client()

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Extrae la información de este texto: {text}"}
        ],
        response_format={"type": "json_object"}
    )

    data = response.choices[0].message.content
    logger.info(f"Texto extraído: {data}")
    return Transaction.model_validate_json(data)
