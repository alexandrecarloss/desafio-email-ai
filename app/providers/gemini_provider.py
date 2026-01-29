from app.config import GEMINI_API_KEY
from google import genai
import logging

logger = logging.getLogger(__name__)

MODELS_PRIORITY = [
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-3-flash-preview"
]

client = genai.Client(api_key=GEMINI_API_KEY)

def generate_text_with_fallback(prompt: str) -> str:
    last_error = None

    for model in MODELS_PRIORITY:
        try:
            response = client.models.generate_content(
                model=model,
                contents=prompt
            )
            logger.info(f"Modelo usado: {model}")
            return response.text.strip()
        except Exception as e:
            logger.warning(f"Falha no modelo {model}: {e}")
            last_error = e

    raise RuntimeError(f"Todos os modelos falharam: {last_error}")

