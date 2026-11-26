import logging

from google import genai
from google.genai import errors as genai_errors

from app.ai.errors import AIServiceError
from app.core import config

logger = logging.getLogger(__name__)
_client = None

RETRYABLE_CODES = {429, 500, 502, 503, 504}  # busy or rate-limited: worth trying another model


def _get_client():
    global _client
    if _client is None:
        if not config.GEMINI_API_KEY:
            raise AIServiceError("GEMINI_API_KEY is not set in backend/.env")
        _client = genai.Client(api_key=config.GEMINI_API_KEY)
    return _client


def complete(prompt: str) -> str:
    """Send a prompt, get text back. The only file that knows which provider we use."""
    if not config.LLM_MODEL:
        raise AIServiceError("LLM_MODEL is not set in backend/.env")

    models = [config.LLM_MODEL]
    if config.LLM_FALLBACK_MODEL and config.LLM_FALLBACK_MODEL != config.LLM_MODEL:
        models.append(config.LLM_FALLBACK_MODEL)

    last_exc = None
    for model in models:
        try:
            response = _get_client().models.generate_content(model=model, contents=prompt)
            return response.text or ""
        except AIServiceError:
            raise
        except genai_errors.APIError as exc:
            last_exc = exc
            if exc.code in RETRYABLE_CODES:
                logger.warning("Model %s unavailable (%s), trying next", model, exc.code)
                continue
            logger.exception("LLM request failed")  # 400/401/404: retrying another model won't help
            raise AIServiceError("The AI request was rejected. Check LLM_MODEL and GEMINI_API_KEY.") from exc
        except Exception as exc:
            logger.exception("LLM request failed")
            raise AIServiceError(
                "The AI service is unavailable or rate-limited. Try again in a minute."
            ) from exc

    raise AIServiceError(
        "The AI service is unavailable or rate-limited. Try again in a minute."
    ) from last_exc