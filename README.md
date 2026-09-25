# EduGenie — Google Gemini Powered Learning Assistant

EduGenie is a FastAPI + HTML/CSS/JavaScript educational assistant based on the supplied college project document.

## Features

- Q&A
- Simplified concept explanation
- Text summarization
- MCQ quiz generation with exactly four options per question
- Personalized beginner-to-advanced learning paths
- Responsive browser interface
- JSON validation with Pydantic
- `/health` endpoint for testing

## Project structure

```text
EduGenie/
├── main.py
├── config.py
├── gemini_client.py
├── schemas.py
├── requirements.txt
├── requirements-local.txt
├── .env.example
├── .gitignore
├── README.md
├── modules/
│   ├── __init__.py
│   ├── qna.py
│   ├── explanation_module.py
│   ├── quiz_module.py
│   ├── summary_module.py
│   └── learning_path.py
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   └── app.js
└── tests/
    └── test_health.py
```

## Important update from the original document

The supplied document specifies Gemini 1.5 Pro for cloud tasks and LaMini-Flan-T5-783M for local explanations. Those are preserved as the project's intended architecture, but the default implementation uses Google's current `google-genai` SDK and `gemini-2.5-flash` so the project is practical to run today.

The LaMini model remains available as an optional explanation path. Enable it only after installing `requirements-local.txt`.

## 1. Install Python

Python 3.10+ is required. Python 3.11 or 3.12 is a convenient choice for broad package compatibility.

Check:

```powershell
python --version
```

## 2. Open the project in VS Code

Open the `EduGenie` folder.

## 3. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can run the project without activating the environment by using `.venv\Scripts\python.exe`, or adjust your PowerShell execution policy according to your machine's normal developer setup.

## 4. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 5. Configure the Gemini API key

Create `.env` from `.env.example`:

```powershell
Copy-Item .env.example .env
```

Open `.env` and replace:

```text
GEMINI_API_KEY=PASTE_YOUR_GEMINI_API_KEY_HERE
```

with your own Gemini API key.

Do not commit `.env` to Git.

## 6. Start EduGenie

```powershell
uvicorn main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

## 7. Test the backend

Health check:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
```

Expected:

```json
{
  "status": "ok",
  "service": "EduGenie"
}
```

Test Q&A:

```powershell
$body = @{ question = "What is an operating system?" } | ConvertTo-Json
Invoke-RestMethod -Uri http://127.0.0.1:8000/qa -Method Post -ContentType "application/json" -Body $body
```

## 8. Test every feature in the browser

### Q&A
Ask:
`What is an operating system?`

### Explain
Topic:
`Pythagoras theorem`

Level:
`Beginner`

### Summary
Paste a paragraph from your study material.

### Quiz
Paste a passage and select 3, 5, or 10 questions.

### Learning Path
Topic:
`SQL`

Level:
`Beginner`

Goal:
`Learn SQL for college projects`

## 9. API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Web application |
| GET | `/health` | Health check |
| POST | `/qa` | Question answering |
| POST | `/explain` | Concept explanation |
| POST | `/summarize` | Summarization |
| POST | `/quiz` | MCQ generation |
| POST | `/learn/recommendations` | Learning path |

FastAPI also provides automatic API documentation at:

```text
http://127.0.0.1:8000/docs
```

## Optional local explanation model

The original document describes LaMini-Flan-T5-783M for concept explanations.

To try that path:

```powershell
pip install -r requirements-local.txt
```

Then change `.env`:

```text
USE_LOCAL_EXPLANATION=true
LOCAL_EXPLANATION_MODEL=MBZUAI/LaMini-Flan-T5-783M
```

The first local-model run can download model files and may use significant disk/RAM. The default Gemini path does not require this.

## Troubleshooting

### `GEMINI_API_KEY is not configured`
Make sure `.env` exists in the project root and contains a valid key.

### `ModuleNotFoundError`
Activate the virtual environment and run:

```powershell
pip install -r requirements.txt
```

### Gemini API error
Check that:
- the API key is correct;
- the selected model is available to your API account;
- your internet connection works;
- any account/project limits have not been reached.

### Quiz JSON error
The application uses Gemini structured JSON output plus Pydantic validation. If the model/API returns an error, the FastAPI response will expose the error so it can be diagnosed.

## Academic presentation flow

For a college demo, show this sequence:

1. Open EduGenie.
2. Ask a normal academic question.
3. Explain a difficult concept at beginner level.
4. Paste study material and generate a summary.
5. Generate a 3-question MCQ quiz.
6. Build a beginner-to-advanced SQL learning path.
7. Open `/docs` to demonstrate the FastAPI REST endpoints.

## Future extensions from the supplied document

Possible next versions include voice interaction, multilingual support, mobile UI, progress tracking, gamification, adaptive learning, PDF/image input, and LMS integration.
