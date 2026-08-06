"""
Module 2c: shortlist classifier training.

Trains multiple classifiers on the engineered features (lexical score,
semantic score, keyword overlap, experience gap) and compares them --
same pattern as CreditWise. Whichever performs best gets saved for use
in the live pipeline (classifier.py loads this saved model).
"""
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, classification_report

FEATURES = ["lexical_score", "semantic_score", "keyword_overlap_count", "years_experience_gap"]
TARGET = "shortlisted"


def train_and_compare():
    df = pd.read_csv("data/training_data.csv")
    X_train, X_test, y_train, y_test = train_test_split(
        df[FEATURES], df[TARGET], test_size=0.2, random_state=42, stratify=df[TARGET]
    )

    candidates = {
        "Logistic Regression": LogisticRegression(),
        "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
        "Gradient Boosting": GradientBoostingClassifier(random_state=42),
    }

    results = []
    best_model, best_name, best_f1 = None, None, -1

    for name, model in candidates.items():
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        acc = accuracy_score(y_test, preds)
        f1 = f1_score(y_test, preds)
        results.append({"model": name, "accuracy": round(acc, 3), "f1": round(f1, 3)})

        if f1 > best_f1:
            best_model, best_name, best_f1 = model, name, f1

    print(pd.DataFrame(results).to_string(index=False))
    print(f"\nBest model: {best_name} (F1={best_f1:.3f})")
    print("\nClassification report for best model:")
    print(classification_report(y_test, best_model.predict(X_test)))

    joblib.dump(best_model, "saved_models/shortlist_classifier.pkl")
    print(f"Saved {best_name} to saved_models/shortlist_classifier.pkl")


if __name__ == "__main__":
    train_and_compare()
