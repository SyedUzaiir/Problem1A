import re

FIELD_LABEL_PATTERN = re.compile(
    r"(name|date|signature|address|phone|email|dept|department|class|roll|dob|designation|amount|advance|block|section|subject|purpose|relation|type of leave|office|post|reason|permanent|temporary|service book|concession|availed|required|government servant|home town|whether|single|s\.no|service|age|relationship|rs\.?|pay)",
    re.I
)

PAGE_OF_PATTERN = re.compile(r"^\s*page\s+\d+(\s+of\s+\d+)?\s*$", re.I)
JUNK_HEADING_PATTERNS = [
    re.compile(r"^table\s+of\s+contents$", re.I),
    re.compile(r"^contents$", re.I),
    re.compile(r"^figure\s+\d+$", re.I),
    re.compile(r"^table\s+\d+$", re.I),
    re.compile(r"^\d+\s+figures?$", re.I),
    re.compile(r"^\d+\s+tables?$", re.I),
]

def is_heading_artifact(text: str) -> bool:
    txt = text.strip()
    if not txt:
        return True
    if FIELD_LABEL_PATTERN.search(txt):
        return True
    if len(txt) <= 2:
        return True
    if PAGE_OF_PATTERN.search(txt):
        return True
    for pat in JUNK_HEADING_PATTERNS:
        if pat.search(txt):
            return True
    if txt.endswith('.') and len(txt.split()) > 7:
        return True
    if len(txt.split()) > 10:
        return True
    if txt.isdigit() or re.match(r'^\d+(\.\d+)+$', txt):
        return True
    if txt.islower() and len(txt.split()) > 3:
        return True
    return False
