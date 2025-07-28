import re
from utils import is_heading_artifact

GENERIC_UNINFORMATIVE = {
    "overview", "international", "version", "copyright notice",
    "may 31, 2014", "foundation level extensions", 
    "introduction", "table of contents", "references",
    "learning objectives", "entry requirements", "conclusion", "summary",
    "days", "remarks", "acknowledgements", "syllabus", "content", "business outcomes",
    "foundation level extension – agile tester", 
    "international software testing qualifications board",
    "qualifications board", "software testing"
}

def get_heading_level(text: str) -> str:
    if re.match(r'^\d+(\.\d+)*([\.\)]|\s)', text):
        level = text.split()[0].count('.') + 1
        return "H%d" % min(level, 3)
    elif text.isupper() and len(text.split()) <= 6:
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
