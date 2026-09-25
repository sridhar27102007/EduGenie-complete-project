import os
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()


@lru_cache
def get_settings():
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash").strip()
    use_local_explanation = os.getenv("USE_LOCAL_EXPLANATION", "false").lower() == "true"
    local_model = os.getenv(
        "LOCAL_EXPLANATION_MODEL",
        "MBZUAI/LaMini-Flan-T5-783M",
    ).strip()

    return {
        "api_key": api_key,
        "model": model,
        "use_local_explanation": use_local_explanation,
        "local_model": local_model,
    }


def require_api_key() -> str:
    key = get_settings()["api_key"]
    if not key:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured. Copy .env.example to .env and add your Gemini API key."
        )
    return key
