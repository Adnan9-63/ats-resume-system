"""
FastAPI entrypoint. Run with:
    uvicorn app.main:app --reload --port 8000
Then visit http://localhost:8000/docs for interactive API docs
(auto-generated from the Pydantic schemas in models/schemas.py).
"""
from fastapi import FastAPI
from app.api.routes_match import router as match_router

app = FastAPI(
    title="AI ATS Resume System",
    description="Scores a resume against a job description using a hybrid NLP/ML/LLM pipeline.",
    version="0.1.0",
)

app.include_router(match_router)


@app.get("/health")
def health():
    """Basic liveness check -- no dependencies, should always return instantly."""
    return {"status": "ok"}
