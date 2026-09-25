from config import get_settings
from gemini_client import generate_text


def _gemini_explanation(topic: str, level: str) -> str:
    prompt = f"""
You are EduGenie, a patient teacher.

Explain the following topic for a {level} learner:
TOPIC: {topic}

Requirements:
1. Start with a one-sentence definition.
2. Explain the idea in small steps.
3. Give one simple real-world example.
4. Mention 3 key points to remember.
5. Avoid unnecessary jargon; define any technical term you must use.
6. Keep the explanation concise enough for a student to revise.
"""
    return generate_text(prompt, temperature=0.35, max_output_tokens=1400)


def _local_explanation(topic: str, level: str) -> str:
    # Optional path matching the original project document's local-model idea.
    # It is intentionally optional because Transformers/PyTorch are much heavier
    # than the default cloud-only installation.
    try:
        from transformers import pipeline
    except ImportError as exc:
        raise RuntimeError(
            "Local explanation mode is enabled, but transformers is not installed. "
            "Install requirements-local.txt or set USE_LOCAL_EXPLANATION=false."
        ) from exc

    settings = get_settings()
    generator = pipeline(
        "text2text-generation",
        model=settings["local_model"],
    )
    prompt = (
        f"Explain {topic} to a {level} student. "
        "Use simple language, steps, one example, and three key points."
    )
    result = generator(prompt, max_new_tokens=300)
    return result[0]["generated_text"].strip()


def explain_topic(topic: str, level: str = "beginner") -> str:
    settings = get_settings()
    if settings["use_local_explanation"]:
        return _local_explanation(topic, level)
    return _gemini_explanation(topic, level)
