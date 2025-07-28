import re
from utils import is_heading_artifact

def extract_headings(lines):
    headings = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        is_numbered = re.match(r'^\d+(\.\d+)*[\.\)]?\s*[A-Za-z]', stripped)
        is_appendix = re.match(r'^[A-Z]\.\s+[A-Za-z]', stripped)
        is_roman = re.match(r'^[IVXLCDM]+\.\s+[A-Za-z]', stripped)
        is_title_like = re.match(r'^[A-Z][A-Za-z \-\(\)\&,:]{1,50}$', stripped)
        if any([is_numbered, is_appendix, is_roman, is_title_like]):
            if not is_heading_artifact(stripped):
                headings.append(stripped)
    return headings

def extract_headings_from_text(text):
    lines = text.splitlines()
    return extract_headings(lines)
