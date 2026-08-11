"""
Tests for Module 1 (parsing) and Module 2a (lexical scoring) --
these had zero test coverage until now, despite being the earliest,
most foundational modules. All run fully offline, no network needed.
"""
import re
from app.parsing.extract_text import extract_email, extract_phone
from app.parsing.section_splitter import is_header, split_into_sections
from app.matching.lexical_score import lexical_score


def test_extract_email_finds_valid_email():
    text = "Contact me at rohan.sharma@example.com for more info."
    assert extract_email(text) == "rohan.sharma@example.com"


def test_extract_email_returns_none_when_absent():
    assert extract_email("No email in this text at all.") is None


def test_extract_phone_handles_multiple_formats():
    formats = [
        "987-654-3210",
        "(987) 654-3210",
        "987 654 3210",
        "987.654.3210",
    ]
    for phone in formats:
        assert extract_phone(phone) == phone


def test_is_header_recognizes_known_vocabulary():
    assert is_header("EXPERIENCE") is True
    assert is_header("Skills:") is True
    assert is_header("education") is True


def test_is_header_rejects_regular_content():
    assert is_header("Built REST APIs using Python and FastAPI") is False
    assert is_header("") is False


def test_split_into_sections_groups_content_correctly():
    text = "John Doe\nEmail: john@example.com\nEXPERIENCE\nDid some work\nSKILLS\nPython, SQL"
    sections = split_into_sections(text)
    assert "experience" in sections
    assert "skills" in sections
    assert "Did some work" in sections["experience"]
    assert "Python, SQL" in sections["skills"]


def test_lexical_score_relevant_vs_unrelated():
    resume = "Python developer with FastAPI and Docker experience."
    relevant_jd = "Looking for a Python developer with FastAPI experience."
    unrelated_jd = "Hiring a marketing coordinator for social media campaigns."

    relevant_score = lexical_score(resume, relevant_jd)
    unrelated_score = lexical_score(resume, unrelated_jd)

    # The core property that matters: relevant should score meaningfully
    # higher than unrelated, not an exact number (TF-IDF output shifts
    # slightly with vocabulary changes, so pinning an exact float here
    # would make this test brittle for no real benefit).
    assert relevant_score > unrelated_score
