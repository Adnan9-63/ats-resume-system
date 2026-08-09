"""
FastAPI entrypoint. Run with:
    uvicorn app.main:app --reload --port 8000
Then visit http://localhost:8000/docs for interactive API docs
(auto-generated from the Pydantic schemas in models/schemas.py).
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes_match import router as match_router
from app.api.routes_auth import router as auth_router
from app.api.routes_history import router as history_router
from app.api.routes_report import router as report_router

app = FastAPI(
    title="AI ATS Resume System",
    description="Scores a resume against a job description using a hybrid NLP/ML/LLM pipeline.",
    version="0.1.0",
)

# CORS: without this, a browser blocks the frontend (running on a different
# port, e.g. localhost:5173) from calling this API (localhost:8000), even
# on the same machine -- browsers treat different ports as different
# origins. Restricted to local dev origins here on purpose; a deployed
# version should list its real frontend domain instead of using "*".
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(match_router)
app.include_router(auth_router)
app.include_router(history_router)
app.include_router(report_router)


@app.get("/health")
def health():
    """Basic liveness check -- no dependencies, should always return instantly."""
    return {"status": "ok"}
