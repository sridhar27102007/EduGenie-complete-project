from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from schemas import (
    QARequest,
    ExplainRequest,
    SummaryRequest,
    QuizRequest,
    LearningPathRequest,
    TextResponse,
    QuizResponse,
    LearningPathResponse,
)

from modules.qna import answer_question
from modules.explanation_module import explain_topic
from modules.summary_module import summarize_text
from modules.quiz_module import generate_quiz
from modules.learning_path import get_learning_recommendations


# ============================================================
# BASE DIRECTORY
# ============================================================

BASE_DIR = Path(__file__).resolve().parent


# ============================================================
# FASTAPI APP
# ============================================================

app = FastAPI(
    title="EduGenie - Gemini Powered Learning Assistant",
    version="1.0.0",
    description=(
        "AI-powered educational assistant with "
        "Q&A, explanations, summaries, quizzes, "
        "and personalized learning paths."
    ),
)


# ============================================================
# STATIC FILES
# ============================================================

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static",
)


# ============================================================
# JINJA2 TEMPLATES
# ============================================================

templates = Jinja2Templates(
    directory=BASE_DIR / "templates"
)


# ============================================================
# HOME PAGE
# ============================================================

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={},
    )


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "EduGenie",
    }


# ============================================================
# Q&A
# ============================================================

@app.post("/qa", response_model=TextResponse)
async def qa(payload: QARequest):
    try:
        result = answer_question(payload.question)

        return TextResponse(
            result=result
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc


# ============================================================
# EXPLANATION
# ============================================================

@app.post("/explain", response_model=TextResponse)
async def explain(payload: ExplainRequest):
    try:
        result = explain_topic(
            payload.topic,
            payload.level,
        )

        return TextResponse(
            result=result
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc


# ============================================================
# SUMMARIZATION
# ============================================================

@app.post("/summarize", response_model=TextResponse)
async def summarize(payload: SummaryRequest):
    try:
        result = summarize_text(
            payload.text
        )

        return TextResponse(
            result=result
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc


# ============================================================
# QUIZ GENERATION
# ============================================================

@app.post("/quiz", response_model=QuizResponse)
async def quiz(payload: QuizRequest):
    try:
        result = generate_quiz(
            payload.text,
            payload.question_count,
        )

        return result

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc


# ============================================================
# PERSONALIZED LEARNING PATH
# ============================================================

@app.post(
    "/learn/recommendations",
    response_model=LearningPathResponse,
)
async def learning_path(
    payload: LearningPathRequest,
):
    try:
        result = get_learning_recommendations(
            payload.topic,
            payload.level,
            payload.goal,
        )

        return result

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc