from gemini_client import generate_text


def summarize_text(text: str) -> str:
    prompt = f"""
You are EduGenie, an educational summarization assistant.

Summarize the following study material for quick revision.

Requirements:
- Preserve the central meaning and important facts.
- Remove repetition and filler.
- Use a short overview followed by bullet points.
- Do not add facts that are not supported by the supplied text.
- Use simple student-friendly language.

TEXT:
{text}
"""
    return generate_text(prompt, temperature=0.25, max_output_tokens=1200)
