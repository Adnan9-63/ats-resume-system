"""
Module 5: API routes.

Responsibility: wire the already-built pipeline pieces (combined_score,
llm_feedback) into an actual HTTP endpoint. This file deliberately
contains almost no logic of its own -- it calls other modules and
shapes the response. Keeping routes "thin" (orchestration only, no
business logic) is a deliberate architecture choice: it means the
matching/scoring logic can be tested and reused independently of any
web framework, and the route itself is trivial to read.
"""
from fastapi import APIRouter, HTTPException
from app.models.schemas import AnalyzeRequest, AnalyzeResponse
from app.matching.combined_score import compute_match_report
from app.feedback.llm_feedback import get_llm_feedback

router = APIRouter()


@router.post("/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest):
    try:
        match_report = compute_match_report(request.resume_text, request.jd_text)
        suggestions = get_llm_feedback(match_report, request.resume_text, request.jd_text)
    except Exception as e:
        # Don't leak raw internal errors to API clients -- log-worthy
        # detail stays server-side, client gets a clean 500.
        raise HTTPException(status_code=500, detail=f"Analysis failed: {type(e).__name__}")

    return AnalyzeResponse(**match_report, suggestions=suggestions)
