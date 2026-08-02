"""
Module 2a: lexical matching.

Responsibility: score how much a resume and a job description overlap
in the ACTUAL WORDS they use, weighted so rare/distinctive words (skills,
tools) matter more than common filler words.

This deliberately does NOT understand meaning or synonyms -- "ML" and
"Machine Learning" will NOT match each other here. That limitation is
intentional and is exactly what the semantic (embedding) layer, built
next, exists to fix. Keeping this layer 'dumb on purpose' is the right
engineering choice, and being able to explain that limitation clearly
is itself a good interview answer.
"""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def lexical_score(resume_text: str, jd_text: str) -> float:
    """
    Returns a 0-1 score: how much the resume's word usage overlaps
    with the job description's, weighted by TF-IDF.
    """
    # TfidfVectorizer needs a LIST of documents -- it computes IDF
    # (how rare each word is) across all documents given to it at once.
    # With only 2 documents, IDF is fairly crude, but the mechanism is
    # identical to how it'd work across thousands of resumes.
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform([resume_text, jd_text])

    # tfidf_matrix has 2 rows: row 0 = resume vector, row 1 = jd vector.
    # cosine_similarity returns a 2x2 matrix of every pair's similarity;
    # we only want the resume-vs-jd cell, at position [0, 1].
    similarity_matrix = cosine_similarity(tfidf_matrix)
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

    good_jd = """
    We are looking for a Software Engineering Intern with experience
    in Python and FastAPI. Familiarity with REST APIs and databases
    is required. Bonus: exposure to machine learning with scikit-learn.
    """

    unrelated_jd = """
    We are hiring a Marketing Coordinator to manage social media
    campaigns, write email newsletters, and coordinate with the
    design team on brand assets.
    """

    print("Score vs a genuinely relevant JD:", round(lexical_score(resume_text, good_jd), 3))
    print("Score vs an unrelated JD:        ", round(lexical_score(resume_text, unrelated_jd), 3))
