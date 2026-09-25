from gemini_client import generate_json
from schemas import QuizResponse


def generate_quiz(text: str, question_count: int = 3) -> QuizResponse:
    prompt = f"""
You are EduGenie, an educational quiz generator.

Create exactly {question_count} multiple-choice questions from the supplied study material.

Rules:
- Every question must be answerable from the supplied material.
- Each question must have exactly four distinct options.
- correct_answer must be the exact text of one option.
- Add a short explanation for why the correct answer is correct.
- Avoid trick questions and duplicate questions.
- Return only the requested JSON structure.

Study material:
{text}
"""
    quiz = generate_json(
        prompt,
        QuizResponse,
        temperature=0.25,
        max_output_tokens=2200,
    )

    if len(quiz.questions) != question_count:
        raise RuntimeError(
            f"Gemini returned {len(quiz.questions)} questions instead of {question_count}."
        )
    return quiz
