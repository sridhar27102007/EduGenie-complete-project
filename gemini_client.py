from functools import lru_cache

from google import genai
from google.genai import types

from config import get_settings, require_api_key


@lru_cache
def get_client():
    # The current Google GenAI Python SDK reads the API key from the
    # GEMINI_API_KEY environment variable, but passing it explicitly makes
    # the configuration obvious for this project.
    return genai.Client(api_key=require_api_key())


def generate_text(
    prompt: str,
    *,
    temperature: float = 0.4,
    max_output_tokens: int = 1200,
) -> str:
    settings = get_settings()

    response = get_client().models.generate_content(
        model=settings["model"],
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=temperature,
            max_output_tokens=max_output_tokens,
        ),
    )

    text = (response.text or "").strip()
    if not text:
        raise RuntimeError("Gemini returned an empty response.")
    return text


def generate_json(
    prompt: str,
    response_schema,
    *,
    temperature: float = 0.3,
    max_output_tokens: int = 1800,
):
    settings = get_settings()

    response = get_client().models.generate_content(
        model=settings["model"],
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=temperature,
            max_output_tokens=max_output_tokens,
            response_mime_type="application/json",
            response_schema=response_schema,
        ),
    )

    if not response.text:
        raise RuntimeError("Gemini returned an empty JSON response.")

    return response_schema.model_validate_json(response.text)
