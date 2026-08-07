"""
Tests for the API layer.

test_health runs anywhere, no external dependencies -- this is the
kind of test that should run in CI on every push.

test_analyze_endpoint is marked skip-by-default in constrained network
environments (like a CI runner without internet, or this project's
build sandbox) because it depends on downloading the sentence-transformer
model on first run. On a real machine with normal internet access, unset
SKIP_NETWORK_TESTS to run it for real.
"""
import os
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.skipif(
    os.getenv("SKIP_NETWORK_TESTS", "1") == "1",
    reason="Requires downloading the sentence-transformer model (needs real internet access)",
)
def test_analyze_endpoint():
    response = client.post("/analyze", json={
        "resume_text": "Python developer with FastAPI and Docker experience. "
                        "Built REST APIs and worked with machine learning models.",
        "jd_text": "Looking for a Software Engineer with Python, FastAPI, "
                   "and Docker experience.",
    })
    assert response.status_code == 200
    data = response.json()
    assert 0 <= data["overall_score"] <= 1
    assert len(data["suggestions"]) > 0


def test_analyze_rejects_short_input():
    response = client.post("/analyze", json={"resume_text": "hi", "jd_text": "hi"})
    assert response.status_code == 422  # Pydantic validation error, not a 500
