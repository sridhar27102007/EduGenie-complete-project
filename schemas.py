from typing import List

from pydantic import BaseModel, Field, field_validator


class QARequest(BaseModel):
    question: str = Field(min_length=2, max_length=5000)


class ExplainRequest(BaseModel):
    topic: str = Field(min_length=2, max_length=3000)
    level: str = Field(default="beginner", max_length=50)


class SummaryRequest(BaseModel):
    text: str = Field(min_length=20, max_length=20000)


class QuizRequest(BaseModel):
    text: str = Field(min_length=10, max_length=12000)
    question_count: int = Field(default=3, ge=1, le=10)


class LearningPathRequest(BaseModel):
    topic: str = Field(min_length=2, max_length=1000)
    level: str = Field(default="beginner", max_length=50)
    goal: str = Field(default="understand the topic and build practical skills", max_length=1000)


class TextResponse(BaseModel):
    result: str


class QuizQuestion(BaseModel):
    question: str
    options: List[str] = Field(min_length=4, max_length=4)
    correct_answer: str
    explanation: str

    @field_validator("correct_answer")
    @classmethod
    def validate_answer(cls, value, info):
        options = info.data.get("options")
        if options and value not in options:
            raise ValueError("correct_answer must exactly match one of the options.")
        return value


class QuizResponse(BaseModel):
    title: str
    questions: List[QuizQuestion] = Field(min_length=1, max_length=10)


class LearningStep(BaseModel):
    stage: str
    topics: List[str]
    estimated_time: str
    resources: List[str]


class LearningPathResponse(BaseModel):
    topic: str
    level: str
    goal: str
    steps: List[LearningStep] = Field(min_length=1, max_length=10)
    study_tips: List[str] = Field(min_length=1, max_length=8)
