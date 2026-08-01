"""
Module 1: text extraction.

Responsibility: take a resume file (PDF or DOCX) and return clean,
readable text. This is the FIRST step of the whole pipeline -- every
other module (parsing sections, scoring, feedback) depends on this
working correctly.
"""
import re
import pdfplumber
from docx import Document


def extract_text_from_pdf(path: str) -> str:
    """
    pdfplumber reads the raw character-position data inside the PDF
    and reconstructs lines/words for us. Without a library like this,
    we'd be looking at a soup of (character, x, y) triples with no
    idea what order they go in.
    """
    full_text = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                full_text.append(page_text)
    return "\n".join(full_text)


def extract_text_from_docx(path: str) -> str:
    """
    DOCX is much easier: it's XML with actual paragraph structure,
    so python-docx just hands us paragraphs directly. No coordinate
    reconstruction needed -- this is why DOCX parsing is the 'easy
    mode' compared to PDF.
    """
    doc = Document(path)
    return "\n".join(p.text for p in doc.paragraphs if p.text.strip())


def show_raw_words(path: str, limit: int = 15):
    """
    TEACHING FUNCTION -- not used in the real pipeline.
    Shows the raw (word, x0, y0) data pdfplumber works with internally,
    so you can SEE the coordinate-soup problem before the library
    solves it for you.
    """
    with pdfplumber.open(path) as pdf:
        page = pdf.pages[0]
        words = page.extract_words()
        for w in words[:limit]:
            print(f"'{w['text']}'  at x={w['x0']:.0f}, y={w['top']:.0f}")


# --- Regex extraction: pulling structured fields out of raw text ---

EMAIL_PATTERN = r"[\w.+-]+@[\w-]+\.[\w.-]+"
# Handles: 987-654-3210 | (987) 654-3210 | 987 654 3210 | 987.654.3210
PHONE_PATTERN = r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}"


def extract_email(text: str) -> str | None:
    match = re.search(EMAIL_PATTERN, text)
    return match.group(0) if match else None


def extract_phone(text: str) -> str | None:
    match = re.search(PHONE_PATTERN, text)
    return match.group(0) if match else None


if __name__ == "__main__":
    print("=== Raw word-level data (coordinate soup) ===")
    show_raw_words("test_resume.pdf")

    print("\n=== Reconstructed text (what pdfplumber gives us) ===")
    text = extract_text_from_pdf("test_resume.pdf")
    print(text)

    print("\n=== Regex-extracted fields ===")
    print("Email:", extract_email(text))
    print("Phone:", extract_phone(text))
