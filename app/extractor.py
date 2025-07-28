import re
from .utils import is_heading_artifact, get_heading_level

def extract_headings_from_text(text: str, page_num: int):
    headings = []
    lines = text.splitlines()

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        # Patterns
        is_numbered = re.match(r'^\d+(\.\d+)*[\.\)]?\s*[A-Za-z]', stripped)
        is_appendix = re.match(r'^[A-Z]\.\s+[A-Za-z]', stripped)
        is_roman = re.match(r'^[IVXLCDM]+\.\s+[A-Za-z]', stripped)
        is_title_like = re.match(r'^[A-Z][A-Za-z \-\(\)\&,:]{1,50}$', stripped)

        if any([is_numbered, is_appendix, is_roman, is_title_like]):
            if not is_heading_artifact(stripped):
                level = get_heading_level(stripped)
                headings.append({"level": level, "text": stripped, "page": page_num})

    return headings
