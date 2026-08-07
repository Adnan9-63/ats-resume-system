"""
Module 2c (inference side): loads the trained classifier and exposes a
simple predict function. This is what the live API calls -- training
(train_classifier.py) and inference are kept as separate concerns on
purpose: training is a slow, occasional offline process; inference
needs to be fast and run on every request.
"""
import joblib
import pandas as pd
from pathlib import Path

MODEL_PATH = Path(__file__).parent.parent.parent / "ml" / "saved_models" / "shortlist_classifier.pkl"
_model_cache = {}


def _get_model():
    if "model" not in _model_cache:
        _model_cache["model"] = joblib.load(MODEL_PATH)
    return _model_cache["model"]

FEATURES = ["lexical_score", "semantic_score", "keyword_overlap_count", "years_experience_gap"]


def predict_shortlist_probability(
    lexical_score: float,
    semantic_score: float,
    keyword_overlap_count: int,
    years_experience_gap: float,
) -> float:
    """
    Returns the model's predicted probability (0-1) that this resume
    would be shortlisted for this job description, given the four
    engineered features computed by the earlier pipeline stages.
    """
    row = pd.DataFrame([{
        "lexical_score": lexical_score,
        "semantic_score": semantic_score,
        "keyword_overlap_count": keyword_overlap_count,
        "years_experience_gap": years_experience_gap,
    }])
    model = _get_model()
    # predict_proba returns [P(class=0), P(class=1)] -- we want P(shortlisted=1)
    return float(model.predict_proba(row[FEATURES])[0][1])


if __name__ == "__main__":
    strong_candidate = predict_shortlist_probability(
        lexical_score=0.75, semantic_score=0.8, keyword_overlap_count=6, years_experience_gap=1.0
    )
    weak_candidate = predict_shortlist_probability(
        lexical_score=0.2, semantic_score=0.25, keyword_overlap_count=1, years_experience_gap=-2.5
    )
    print(f"Strong match candidate: {strong_candidate:.1%} shortlist probability")
    print(f"Weak match candidate:   {weak_candidate:.1%} shortlist probability")
