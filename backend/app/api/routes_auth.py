"""
Module 6b: auth routes. Thin wrappers around Supabase's own auth API --
no password handling, no token generation happens in this codebase,
which is exactly the point of using a managed provider.
"""
from fastapi import APIRouter, HTTPException
from app.models.schemas import SignupRequest, LoginRequest
from app.auth.supabase_client import get_client, is_configured

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup")
def signup(request: SignupRequest):
    if not is_configured():
        raise HTTPException(
            status_code=501,
            detail="Auth not configured yet -- add SUPABASE_URL and SUPABASE_KEY to .env",
        )
    client = get_client()
    try:
        result = client.auth.sign_up({"email": request.email, "password": request.password})
        return {"user_id": result.user.id, "email": result.user.email}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
def login(request: LoginRequest):
    if not is_configured():
        raise HTTPException(
            status_code=501,
            detail="Auth not configured yet -- add SUPABASE_URL and SUPABASE_KEY to .env",
        )
    client = get_client()
    try:
        result = client.auth.sign_in_with_password(
            {"email": request.email, "password": request.password}
        )
        return {"access_token": result.session.access_token, "user_id": result.user.id}
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid credentials")
