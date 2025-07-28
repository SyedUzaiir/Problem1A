import re

def is_heading_artifact(line: str) -> bool:
    text = line.strip().lower()

    # Junk patterns
    if len(text) <= 2:
        return True
    if text.isdigit():
        return True
    if re.match(r'^\d+(\.\d+)*$', text):  # Section number alone
        return True
    if any(keyword in text for keyword in ["table of contents", "figure", "fig.", "page", "index"]):
        return True
    if len(text.split()) > 12:
        return True
    if len(text) > 80:
        return True
    if text.islower() and len(text.split()) > 3:
        return True
    return False

def get_heading_level(text: str) -> str:
    """Determine heading level based on numbering depth."""
    if re.match(r'^\d+\.', text):  # 1. or 1.2 etc.
        depth = text.split()[0].count('.')
        return "H1" if depth == 0 else "H2" if depth == 1 else "H3"
    return "H1"  # Default fallback
