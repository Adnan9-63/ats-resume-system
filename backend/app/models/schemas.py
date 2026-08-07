"""
Request/response schemas. Using Pydantic models instead of raw dicts
gives us automatic validation (bad requests get rejected with a clear
error before touching any of our logic) and automatic API docs
(FastAPI generates interactive docs from these at /docs for free).
"""
from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    resume_text: str = Field(..., min_length=10, description="Raw resume text")
    jd_text: str = Field(..., min_length=10, description="Raw job description text")


class AnalyzeResponse(BaseModel):
    keyword_match_score: float
    semantic_fit_score: float
    matched_skill_count: int
    predicted_shortlist_probability: float
    overall_score: float
    suggestions: list[str]
