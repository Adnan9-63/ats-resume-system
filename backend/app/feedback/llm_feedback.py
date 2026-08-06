"""
Module 3: LLM feedback generation.

Responsibility: take the numeric match report (from combined_score.py)
plus the raw resume/JD text, and turn it into specific, human-readable
advice -- "add these keywords," "rephrase this bullet," etc. This is
the layer that makes the system feel like a product, not a spreadsheet
of numbers.

Design choice worth defending in an interview: this module has an
explicit MOCK MODE, used automatically when no API key is configured.
This isn't a shortcut -- it means the rest of the app (frontend, tests,
demos) can run and be developed without needing a paid API key on
every machine, and without making a real network call on every single
test run during development. Real LLM calls are reserved for when
they're actually needed.
"""
import os
import json
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ANTHROPIC_API_KEY")


def build_prompt(match_report: dict, resume_text: str, jd_text: str) -> str:
    return f"""You are an expert resume reviewer. A candidate's resume was scored
against a job description with the following results:

- Keyword match score: {match_report['keyword_match_score']}
- Semantic fit score: {match_report['semantic_fit_score']}
- Matched skill count: {match_report['matched_skill_count']}
- Predicted shortlist probability: {match_report['predicted_shortlist_probability']}

Resume:
{resume_text}

Job description:
{jd_text}

Give exactly 3 specific, actionable suggestions to improve this resume's match
for this job. Each suggestion should be one sentence. Respond ONLY with a JSON
array of 3 strings, nothing else."""


def _mock_feedback(match_report: dict) -> list[str]:
    """
    Offline fallback -- used automatically when ANTHROPIC_API_KEY isn't set.
    Not a fake success message; clearly labeled as mock output so it's
    never mistaken for a real LLM response during development or demos.
    """
    return [
        "[MOCK MODE - add ANTHROPIC_API_KEY to .env for real suggestions]",
        f"Your keyword match score was {match_report['keyword_match_score']} — "
        f"consider adding more skills directly mentioned in the job description.",
        f"Predicted shortlist probability is {match_report['predicted_shortlist_probability']:.0%} — "
        f"strengthening quantified achievements usually helps this most.",
    ]


def get_llm_feedback(match_report: dict, resume_text: str, jd_text: str) -> list[str]:
    if not API_KEY:
        return _mock_feedback(match_report)

    import anthropic
    client = anthropic.Anthropic(api_key=API_KEY)
    prompt = build_prompt(match_report, resume_text, jd_text)

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}],
    )

    raw_text = response.content[0].text
    try:
        return json.loads(raw_text)
    except json.JSONDecodeError:
        # LLM occasionally wraps JSON in markdown fences despite instructions --
        # strip and retry once rather than crashing the whole pipeline over it.
        cleaned = raw_text.replace("```json", "").replace("```", "").strip()
        return json.loads(cleaned)


if __name__ == "__main__":
    fake_report = {
        "keyword_match_score": 0.42,
        "semantic_fit_score": 0.61,
        "matched_skill_count": 3,
        "predicted_shortlist_probability": 0.55,
    }
    feedback = get_llm_feedback(
        fake_report,
        resume_text="Sample resume text...",
        jd_text="Sample job description text...",
    )
    for i, tip in enumerate(feedback, 1):
        print(f"{i}. {tip}")
