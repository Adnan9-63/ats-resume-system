"""
Module 2 orchestration: combines the three matching signals built so
far (lexical, semantic, classifier) into one match report.

Honest scope note: keyword_overlap_count and years_experience_gap are
currently naive placeholders (simple set-intersection on a hardcoded
skill list; experience gap defaulted to 0). Building a real skill
taxonomy extractor and a "years required" parser from JD text are
real, separate pieces of future work -- not solved here, and flagged
rather than faked. Silently returning a plausible-looking number for
an unbuilt feature would be worse than admitting the gap.
"""
from app.matching.lexical_score import lexical_score
from app.matching.semantic_score import semantic_score
from app.matching.classifier import predict_shortlist_probability

# Placeholder skill vocabulary for naive keyword overlap counting.
# TODO: replace with a real extracted skill list from the parser module.
COMMON_SKILLS = [
    "python", "sql", "java", "javascript", "react", "fastapi", "django",
    "docker", "kubernetes", "aws", "machine learning", "deep learning",
    "nlp", "pandas", "numpy", "scikit-learn", "git", "linux",
]


def _naive_keyword_overlap(resume_text: str, jd_text: str) -> int:
    resume_lower = resume_text.lower()
    jd_lower = jd_text.lower()
    return sum(1 for skill in COMMON_SKILLS if skill in resume_lower and skill in jd_lower)


def compute_match_report(resume_text: str, jd_text: str) -> dict:
    lex = lexical_score(resume_text, jd_text)
    sem = semantic_score(resume_text, jd_text)
    keyword_overlap = _naive_keyword_overlap(resume_text, jd_text)
    years_gap = 0.0  # TODO: real extraction not built yet

    shortlist_probability = predict_shortlist_probability(
        lexical_score=lex,
        semantic_score=sem,
        keyword_overlap_count=keyword_overlap,
        years_experience_gap=years_gap,
    )

    return {
        "keyword_match_score": round(lex, 3),
        "semantic_fit_score": round(sem, 3),
        "matched_skill_count": keyword_overlap,
        "predicted_shortlist_probability": round(shortlist_probability, 3),
        "overall_score": round((lex + sem + shortlist_probability) / 3, 3),
    }


if __name__ == "__main__":
    resume_text = """
    Rohan Sharma. Software Engineering Intern, Acme Corp.
    Built REST APIs using Python and FastAPI. Machine Learning Intern,
    DataWorks. Trained classification models using scikit-learn.
    Skills: Python, SQL, Machine Learning, FastAPI, Docker, Git.
    """
    jd_text = """
    Looking for a Software Engineering Intern with experience in
    Python and FastAPI, familiarity with REST APIs and Docker.
    Bonus: exposure to machine learning with scikit-learn.
    """

    report = compute_match_report(resume_text, jd_text)
    for k, v in report.items():
        print(f"{k}: {v}")
