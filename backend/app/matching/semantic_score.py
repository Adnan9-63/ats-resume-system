"""
Module 2b: semantic matching.

Responsibility: score resume-vs-JD similarity based on MEANING, not
exact word overlap. This directly fixes the demonstrated weakness of
lexical_score.py -- "ML" vs "Machine Learning" scoring lower purely
due to wording, despite being the same skill.

Model: all-MiniLM-L6-v2 -- a small, fast sentence-transformer model.
Chosen deliberately over a larger model: it's ~80MB, runs fast even on
CPU, and is accurate enough for this use case. A bigger model would be
marginally more accurate but much slower and heavier to deploy -- not
worth the tradeoff here. Being able to justify a "smaller model on
purpose" choice is itself a good interview answer about production
tradeoffs, not just chasing max accuracy.
"""
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Loaded once at import time, not per-call -- loading the model is slow,
# scoring with an already-loaded model is fast. This matters a lot once
# this runs inside an API that handles many requests.
_model = SentenceTransformer("all-MiniLM-L6-v2")


def semantic_score(resume_text: str, jd_text: str) -> float:
    """
    Returns a 0-1 score: how similar the resume and JD are in MEANING,
    computed by embedding both into vectors and measuring cosine
    similarity between them -- same math as lexical_score, completely
    different vectors (learned meaning vs raw word-weights).
    """
    embeddings = _model.encode([resume_text, jd_text])
    similarity_matrix = cosine_similarity(embeddings)
    return float(similarity_matrix[0, 1])


if __name__ == "__main__":
    resume_text = """
    Rohan Sharma. Software Engineering Intern, Acme Corp.
    Built REST APIs using Python and FastAPI. Improved database
    query performance by 30 percent. Machine Learning Intern,
    DataWorks. Trained classification models using scikit-learn.
    Worked with Pandas and NumPy for data cleaning.
    Skills: Python, SQL, Machine Learning, FastAPI, Docker, Git.
    """

    jd_full_phrase = """
    We are looking for a Software Engineering Intern with experience
    in Python and FastAPI. Familiarity with REST APIs and databases
    is required. Bonus: exposure to machine learning with scikit-learn.
    """

    jd_ml_abbrev = """
    We are looking for a Software Engineering Intern with experience
    in Python and FastAPI. Familiarity with REST APIs and databases
    is required. Bonus: exposure to ML with scikit-learn.
    """

    print("Semantic score with 'machine learning':", round(semantic_score(resume_text, jd_full_phrase), 3))
    print("Semantic score with 'ML' instead:      ", round(semantic_score(resume_text, jd_ml_abbrev), 3))
