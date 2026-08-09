"""
Module 6c: history routes.

Design note: only a short snippet (not the full resume/JD text) is
stored per history row, deliberately. Storing full text for every
analysis a user runs would grow the table fast and raises a privacy
question -- a snippet is enough to let a user recognize "oh, this was
my Google application" in a history list, without hoarding full
resume text indefinitely.
"""
from fastapi import APIRouter, HTTPException
from app.models.schemas import HistoryItem
from app.auth.supabase_client import get_client, is_configured

router = APIRouter(prefix="/history", tags=["history"])


def _snippet(text: str, length: int = 80) -> str:
    text = text.strip().replace("\n", " ")
    return text[:length] + ("..." if len(text) > length else "")


@router.post("/save")
def save_analysis(user_id: str, resume_text: str, jd_text: str, overall_score: float):
    if not is_configured():
        raise HTTPException(
            status_code=501,
            detail="History storage not configured yet -- add SUPABASE_URL and SUPABASE_KEY to .env",
        )
    client = get_client()
    row = {
        "user_id": user_id,
        "resume_snippet": _snippet(resume_text),
        "jd_snippet": _snippet(jd_text),
        "overall_score": overall_score,
    }
    result = client.table("analyses").insert(row).execute()
    return {"saved": True, "id": result.data[0]["id"]}


@router.get("/{user_id}", response_model=list[HistoryItem])
def get_history(user_id: str):
    if not is_configured():
        raise HTTPException(
            status_code=501,
            detail="History storage not configured yet -- add SUPABASE_URL and SUPABASE_KEY to .env",
        )
    client = get_client()
    result = (
        client.table("analyses")
        .select("*")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .execute()
    )
    return result.data
