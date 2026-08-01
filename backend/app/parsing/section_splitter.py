"""
Module 1b: section splitting.

Responsibility: take the raw extracted text and break it into
labeled sections (experience, education, skills, etc.) so downstream
modules can reason about "what's in the Skills section" instead of
treating the whole resume as one undifferentiated block of text.

Approach: rule-based (known header vocabulary + formatting heuristics),
not a trained model. Chosen deliberately -- resume section headers are
a small, low-variance vocabulary, so rules are fast, free, and fully
explainable. This is a decision to be able to justify, not a shortcut.
"""

# The known vocabulary of section header words. Lowercased, no punctuation.
# This list is deliberately small and extendable -- add to it as you
# encounter real resumes with headers you haven't seen yet.
KNOWN_HEADERS = {
    "experience", "work experience", "professional experience",
    "education", "skills", "technical skills", "projects",
    "certifications", "summary", "objective", "achievements",
    "publications", "awards", "extracurricular", "activities",
}


def is_header(line: str) -> bool:
    """
    A line is treated as a section header if it matches EITHER signal
    strongly, or is short + all-caps (a formatting-only signal that's
    reliable even for header words we haven't listed).
    """
    stripped = line.strip()
    if not stripped:
        return False

    normalized = stripped.lower().rstrip(":")
    if normalized in KNOWN_HEADERS:
        return True

    # Formatting heuristic: short line, ALL CAPS, no lowercase letters at all.
    # Real section headers are rarely more than a few words.
    word_count = len(stripped.split())
    is_all_caps = stripped == stripped.upper() and any(c.isalpha() for c in stripped)
    is_short = word_count <= 4

    return is_all_caps and is_short


def split_into_sections(text: str) -> dict[str, list[str]]:
    """
    Walks the text line by line. Every time it hits a header line, it
    starts a new section. Everything else gets appended to whichever
    section is currently 'open'. Content before the first header goes
    under 'header' (name, contact info, etc.) -- it isn't a section,
    but it still needs a home.
    """
    sections: dict[str, list[str]] = {"header": []}
    current_section = "header"

    for line in text.split("\n"):
        if is_header(line):
            current_section = line.strip().lower().rstrip(":")
            sections[current_section] = []
        else:
            if line.strip():
                sections[current_section].append(line.strip())

    return sections


if __name__ == "__main__":
    from extract_text import extract_text_from_pdf

    text = extract_text_from_pdf("../../test_resume.pdf")
    sections = split_into_sections(text)

    for name, lines in sections.items():
        print(f"\n--- {name.upper()} ---")
        for line in lines:
            print(" ", line)
