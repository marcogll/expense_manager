import os
from loguru import logger
from .llm_client import get_llm_client


def transcribe_voice(audio_path: str) -> str:
    client, _ = get_llm_client()
    
    with open(audio_path, "rb") as f:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=f
        )
    
    logger.info(f"Transcripción: {transcript.text[:50]}...")
    return transcript.text
