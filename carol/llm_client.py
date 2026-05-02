import os
from dotenv import load_dotenv
from openai import OpenAI
from loguru import logger

load_dotenv()


def get_llm_client():
    provider = os.getenv("LLM_PROVIDER", "openai").lower()

    if provider == "openrouter":
        api_key = os.getenv("OPENROUTER_API_KEY")
        base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
        if not api_key:
            logger.error("OPENROUTER_API_KEY no configurada")
            raise ValueError("OPENROUTER_API_KEY requerida para OpenRouter")
        logger.info("Usando OpenRouter como proveedor LLM")
        return OpenAI(api_key=api_key, base_url=base_url), os.getenv("OPENROUTER_MODEL", "openai/gpt-4o")

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.error("OPENAI_API_KEY no configurada")
        raise ValueError("OPENAI_API_KEY requerida para OpenAI")
    logger.info("Usando OpenAI como proveedor LLM")
    return OpenAI(api_key=api_key), "gpt-4o"
