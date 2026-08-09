"""
Module 7: PDF report export.

Uses reportlab (already a dependency from Day 1's test-resume generator)
rather than adding WeasyPrint. WeasyPrint (HTML/CSS -> PDF) produces
nicer-looking output but needs system-level libraries (Cairo, Pango) that
complicate deployment. reportlab draws directly, no system dependencies,
which matters more at this stage than visual polish -- this can be
swapped later without changing the API contract (generate_pdf_report
still takes the same inputs, returns the same bytes) if the tradeoff
ever flips.
"""
import io
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas


def generate_pdf_report(match_report: dict, suggestions: list[str], candidate_name: str = "Candidate") -> bytes:
    """
    Renders a match report + suggestions into a PDF, returned as raw
    bytes so the API layer can stream it directly to the client without
    ever writing a temp file to disk.
    """
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    y = height - 2 * cm

    c.setFont("Helvetica-Bold", 18)
    c.drawString(2 * cm, y, "ATS Match Report")
    y -= 0.8 * cm
    c.setFont("Helvetica", 11)
    c.drawString(2 * cm, y, f"Candidate: {candidate_name}")
    y -= 1.2 * cm

    c.setFont("Helvetica-Bold", 13)
    c.drawString(2 * cm, y, "Score breakdown")
    y -= 0.7 * cm
    c.setFont("Helvetica", 11)

    rows = [
        ("Overall score", match_report["overall_score"]),
        ("Keyword match", match_report["keyword_match_score"]),
        ("Semantic fit", match_report["semantic_fit_score"]),
        ("Shortlist probability", match_report["predicted_shortlist_probability"]),
        ("Matched skills", match_report["matched_skill_count"]),
    ]
    for label, value in rows:
        display = f"{value:.0%}" if isinstance(value, float) else str(value)
        c.drawString(2.3 * cm, y, f"{label}: {display}")
        y -= 0.6 * cm

    y -= 0.6 * cm
    c.setFont("Helvetica-Bold", 13)
    c.drawString(2 * cm, y, "Suggestions")
    y -= 0.7 * cm
    c.setFont("Helvetica", 11)

    for i, tip in enumerate(suggestions, 1):
        # Naive word-wrap -- reportlab doesn't wrap text automatically.
        # Fine for short suggestion sentences; a long-form report would
        # need a proper text-wrapping approach (e.g. Platypus/Paragraph).
        words = tip.split()
        line = f"{i}. "
        for word in words:
            if len(line) + len(word) > 90:
                c.drawString(2.3 * cm, y, line)
                y -= 0.55 * cm
                line = "   "
            line += word + " "
        c.drawString(2.3 * cm, y, line)
        y -= 0.8 * cm

    c.save()
    buffer.seek(0)
    return buffer.read()


if __name__ == "__main__":
    fake_report = {
        "overall_score": 0.68,
        "keyword_match_score": 0.42,
        "semantic_fit_score": 0.71,
        "predicted_shortlist_probability": 0.55,
        "matched_skill_count": 4,
    }
    fake_suggestions = [
        "Add more specific keywords from the job description, such as Docker and Kubernetes.",
        "Quantify your achievements with numbers where possible.",
        "Move your most relevant experience closer to the top of the resume.",
    ]
    pdf_bytes = generate_pdf_report(fake_report, fake_suggestions, candidate_name="Rohan Sharma")
    with open("test_report.pdf", "wb") as f:
        f.write(pdf_bytes)
    print(f"Wrote test_report.pdf ({len(pdf_bytes)} bytes)")
