import re

PAGE_OF_PATTERN = re.compile(r"^\s*page\s+\d+\s+of\s+\d+\s*$", re.IGNORECASE)
JUNK_HEADING_PATTERNS = [
    re.compile(r"^table\s+of\s+contents$", re.IGNORECASE),
    re.compile(r"^contents$", re.IGNORECASE),
    re.compile(r"^figure\s+\d+$", re.IGNORECASE),
    re.compile(r"^table\s+\d+$", re.IGNORECASE),
    re.compile(r"^\d+\s+figures?$", re.IGNORECASE),
    re.compile(r"^\d+\s+tables?$", re.IGNORECASE),
]

def is_heading_artifact(text: str) -> bool:
    txt = text.strip()
    lower_txt = txt.lower()
    if len(txt) <= 2:
        return True
    if PAGE_OF_PATTERN.search(txt):
        return True
    for pat in JUNK_HEADING_PATTERNS:
        if pat.search(txt):
            return True
    if txt.endswith('.') and len(txt.split()) > 7:
        return True
    if txt.islower() and len(txt.split()) > 5:
        return True
    if txt.isdigit():
        return True
    if re.match(r'^\d+(\.\d+)+$', txt):
        return True
    if len(txt.split()) == 1 and lower_txt not in {"summary", "introduction", "conclusion"}:
        return True
    if txt.count(' ') > 10 or len(txt.split()) > 15:
        return True
    return False
