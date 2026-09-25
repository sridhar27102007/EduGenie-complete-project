from gemini_client import generate_json
from schemas import LearningPathResponse


def get_learning_recommendations(
    topic: str,
    level: str = "beginner",
    goal: str = "understand the topic and build practical skills",
) -> LearningPathResponse:
    prompt = f"""
You are EduGenie, a personalized learning-path designer.

Create a structured learning path for:
Topic: {topic}
Learner level: {level}
Goal: {goal}

Requirements:
- Move from foundational concepts toward advanced concepts.
- Use practical, realistic stages.
- Include an estimated time for each stage.
- Include useful resource TYPES or well-known resource names when appropriate,
  but do not invent URLs.
- Include study tips.
- Adapt the path to the stated learner level.
- Return only the requested JSON structure.
"""
    return generate_json(
        prompt,
        LearningPathResponse,
        temperature=0.35,
        max_output_tokens=2200,
    )
