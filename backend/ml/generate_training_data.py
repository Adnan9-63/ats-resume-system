"""
Generates synthetic training data for the shortlist classifier.

Why synthetic: real labeled "was this resume shortlisted for this JD"
data isn't publicly available (companies don't release it). Synthetic
data lets us build and validate the ML pipeline end-to-end now; it can
be swapped for real labeled data later without changing any code here,
only the data source. This distinction (synthetic-for-now vs
production-data-later) is worth stating explicitly in an interview --
it shows you understand the difference between "the pipeline works" and
"the pipeline is trained on representative real-world data."

Features used, and why each is a reasonable proxy signal:
- lexical_score: TF-IDF/cosine overlap (0-1)
- semantic_score: embedding similarity (0-1)
- keyword_overlap_count: how many required skills literally appear
- years_experience_gap: candidate years minus required years (can be negative)

Label: shortlisted (1) or not (0), generated with realistic noise so
the classifier has to genuinely learn a decision boundary rather than
memorize a perfect rule.
"""
import numpy as np
import pandas as pd

np.random.seed(42)


def generate_dataset(n=400) -> pd.DataFrame:
    lexical_score = np.random.beta(2, 2, n)          # spread across 0-1
    semantic_score = np.clip(lexical_score + np.random.normal(0, 0.15, n), 0, 1)
    keyword_overlap_count = np.random.poisson(4, n)
    years_experience_gap = np.random.normal(0, 2, n)

    # Underlying "true" score combining signals -- this is the pattern
    # the classifier will have to discover from data, not be told directly.
    true_signal = (
        0.4 * lexical_score
        + 0.4 * semantic_score
        + 0.1 * np.clip(keyword_overlap_count / 8, 0, 1)
        + 0.1 * np.clip((years_experience_gap + 3) / 6, 0, 1)
    )
    noise = np.random.normal(0, 0.08, n)
    probability = np.clip(true_signal + noise, 0, 1)
    label = (probability > 0.55).astype(int)

    return pd.DataFrame({
        "lexical_score": lexical_score.round(3),
        "semantic_score": semantic_score.round(3),
        "keyword_overlap_count": keyword_overlap_count,
        "years_experience_gap": years_experience_gap.round(2),
        "shortlisted": label,
    })


if __name__ == "__main__":
    df = generate_dataset()
    df.to_csv("data/training_data.csv", index=False)
    print(df.head(10))
    print(f"\n{len(df)} rows, {df['shortlisted'].mean():.1%} positive class")
