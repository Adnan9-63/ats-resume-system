"""
Module 7 (API side): serves the generated PDF as a downloadable file.
Runs the full match pipeline first (same as /analyze), then converts
the result into a PDF instead of JSON.
"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from app.models.schemas import AnalyzeRequest
from app.matching.combined_score import compute_match_report
from app.feedback.llm_feedback import get_llm_feedback
from app.reports.generate_report import generate_pdf_report

router = APIRouter()


@router.post("/report/pdf")
def download_report(request: AnalyzeRequest):
    try:
        match_report = compute_match_report(request.resume_text, request.jd_text)
        suggestions = get_llm_feedback(match_report, request.resume_text, request.jd_text)
        pdf_bytes = generate_pdf_report(match_report, suggestions)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Report generation failed: {type(e).__name__}")

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=ats_match_report.pdf"},
    )
