import re
from utils import is_heading_artifact

GENERIC_HEADINGS = {
    "overview", "international", "version", "copyright notice",
    "foundation level extensions", "trademarks", "remarks", "may 31, 2014", "agile tester",
    "foundation level.", "foundation level working group.", "baseline: foundation",
    "extension: agile tester", "syllabus", "days", "acknowledgements", "identifier",
    "reference", "manifesto.", "introduction", "business outcomes", "content", "foundation level extension – agile tester", 
    "international software testing qualifications board", "qualifications board", "software testing"
}

def get_heading_level(text: str) -> str:
    if re.match(r'^\d+(\.\d+)*([\.\)]|\s)', text):
        level = text.split()[0].count('.') + 1
        return "H%d" % min(level, 3)
    elif text.isupper() and len(text.split()) >= 2:  # ALLCAPS 2+ words = H1
        return "H1"
    elif len(text.split()) <= 4:
        return "H2"
    else:
        return "H3"

def extract_headings(lines):
    headings = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        # Accept ALLCAPS 2+ word short headings as H1
        if stripped.isupper() and len(stripped.split()) >= 2 and not is_heading_artifact(stripped):
            headings.append({
                "text": stripped,
                "level": "H1"
            })
            continue
        # Patterns for numbered/appendix/roman/title-like
        is_numbered = re.match(r'^\d+(\.\d+)*[\.\)]?\s+[A-Za-z]', stripped)
        is_appendix = re.match(r'^[A-Z]\.\s+[A-Za-z]', stripped)
        is_roman = re.match(r'^[IVXLCDM]+\.\s+[A-Za-z]', stripped)
        is_title_like = (
            stripped.istitle() or stripped.isupper() or re.match(r'^[A-Z][A-Za-z0-9 \-\(\)\&,:]{2,80}$', stripped)
        )
        if any([is_numbered, is_appendix, is_roman, is_title_like]):
            if not is_heading_artifact(stripped):
                headings.append({
                    "text": stripped,
                    "level": get_heading_level(stripped)
                })
    return headings

def extract_headings_from_text(text):
    lines = text.splitlines()
    return extract_headings(lines)
