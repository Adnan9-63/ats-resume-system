"""
Tests for reports and auth/history.

test_generate_pdf_report runs fully offline -- no network, no external
service -- so it should always run, including in CI.

test_auth_and_history_unconfigured confirm the app fails GRACEFULLY
(a clean 501 with a helpful message) rather than crashing when Supabase
credentials aren't set -- which is the expected state until real
credentials are added to .env.
"""
from fastapi.testclient import TestClient
from app.main import app
from app.reports.generate_report import generate_pdf_report

client = TestClient(app)


def test_generate_pdf_report():
    report = {
        "overall_score": 0.7,
        "keyword_match_score": 0.5,
        "semantic_fit_score": 0.8,
        "predicted_shortlist_probability": 0.6,
        "matched_skill_count": 3,
    }
    pdf_bytes = generate_pdf_report(report, ["Add more keywords.", "Quantify achievements."])
    assert pdf_bytes[:4] == b"%PDF"  # valid PDF file signature
    assert len(pdf_bytes) > 500


def test_signup_unconfigured_returns_501():
    response = client.post("/auth/signup", json={"email": "test@example.com", "password": "password123"})
    assert response.status_code == 501
    assert "not configured" in response.json()["detail"]


def test_history_unconfigured_returns_501():
    response = client.get("/history/some-user-id")
    assert response.status_code == 501
