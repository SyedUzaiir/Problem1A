import fitz
import re
from collections import Counter
from statistics import median

FIELD_LABEL_PATTERN = re.compile(
    r"^(name|date|place|designation|signature|address|phone|email|department|age|sex|religion|caste|income|occupation)\b",
    re.I,
)

PAGE_OF_PATTERN = re.compile(r"\bPage\b\s*\d+\s*(of\s*\d+)?", re.I)
JUNK_HEADING_PATTERNS = [
    re.compile(r'copyright', re.I),
    re.compile(r'authors?:', re.I),
    re.compile(r'this document', re.I),
    re.compile(r'reviewers?:', re.I),
    re.compile(r'^page\b', re.I),
    re.compile(r'table of contents', re.I),
    re.compile(r'revision history', re.I),
    re.compile(r'confidential', re.I),
    re.compile(r'\b\b\d{4}\b', re.I),  # common for year lines
]

def is_heading_artifact(text):
    txt = text.strip()
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
    if (txt.count(' ') > 10) or (len(txt.split()) > 15):
        return True  # too long for heading
    return False

def find_heading_candidates(lines, avg_font):
    candidates = []
    for line in lines:
        text = line['text'].strip()
        if is_heading_artifact(text):
            continue
        bold = line.get('bold', False)
        large_font = line['font_size'] >= 1.2 * avg_font
        numbered = bool(re.match(r'^(\d+(\.\d+)*[\s\.])|^[IVXLCDM]+\.|^[A-Z]\.', text))
        if bold or large_font or numbered:
            candidates.append(line)
    return candidates

def filter_common_headers(candidates, num_pages):
    # Remove headings that appear on more than 25% of pages (running headers/footers)
    texts = [c['text'].strip().lower() for c in candidates]
    freq = Counter(texts)
    blacklist = {t for t, f in freq.items() if f > 0.25 * num_pages}
    return [c for c in candidates if c['text'].strip().lower() not in blacklist]

def remove_fragment_duplicates(candidates):
    # Remove substring-of-longer candidates within same page
    keep = []
    texts_kept = []
    for c in candidates:
        txt = c['text'].strip()
        is_fragment = False
        for t in texts_kept:
            if txt and t and txt != t and txt in t and len(txt) / len(t) < 0.7:
                is_fragment = True
                break
        if not is_fragment:
            keep.append(c)
            texts_kept.append(txt)
    return keep

def assign_heading_levels(candidates):
    # Use unique font size ranking to assign H1-H4, but also respect numbering
    unique_sizes = sorted({c['font_size'] for c in candidates}, reverse=True)
    size_to_level = {size: f"H{min(i + 1, 4)}" for i, size in enumerate(unique_sizes)}
    for c in candidates:
        text = c['text'].strip()
        # Numbered pattern rules (override font if explicit sectioning)
        if re.match(r'^\d+(\.\d+)*([\s\.]|$)', text):
            c['level'] = f"H{ text.count('.') + 1 }"
        elif re.match(r'^[IVXLCDM]+\.|^[A-Z]\.', text, re.I):
            c['level'] = "H2"
        else:
            c['level'] = size_to_level[c['font_size']]
    return candidates

def extract_title(lines):
    # Pick largest, bold, multi-word line on page 1 as title
    page1 = [l for l in lines if l['page'] == 1 and len(l['text'].split()) >= 3]
    if not page1:
        return ""
    max_size = max(l['font_size'] for l in page1)
    candidates = [l for l in page1 if l['font_size'] >= max_size * 0.9]
    bold_candidates = [l for l in candidates if l.get('bold', False)]
    title = (bold_candidates or candidates)[0]['text'].strip()
    return title

class PDFOutlineExtractor:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    def get_text_lines(self):
        doc = fitz.open(self.pdf_path)
        lines = []
        for page_idx, page in enumerate(doc, start=1):
            blocks = page.get_text("dict")["blocks"]
            for b in blocks:
                if "lines" not in b:
                    continue
                for l in b["lines"]:
                    line_text = " ".join(s["text"].strip() for s in l["spans"] if s["text"].strip())
                    if not line_text:
                        continue
                    # Use the max font size of the spans in each line
                    max_span = max(l["spans"], key=lambda s: s["size"])
                    # Determine bold: PyMuPDF sets the 2nd bit in flags for bold
                    bold = any(s.get("flags", 0) & 2 for s in l["spans"])
                    lines.append({
                        "text": line_text,
                        "font_size": max_span["size"],
                        "bold": bold,
                        "page": page_idx
                    })
        return lines

    def extract_outline(self):
        lines = self.get_text_lines()
        if not lines:
            return {"title": "", "outline": []}
        num_pages = max(l["page"] for l in lines)
        font_sizes = [l['font_size'] for l in lines if l['text'].strip()]
        avg_font = median(font_sizes) if font_sizes else 10

        # Detect form: if >20% of lines match form fields (across entire doc)
        form_count = sum(1 for l in lines if FIELD_LABEL_PATTERN.match(l['text'].strip()))
        if form_count / len(lines) > 0.2:
            title = extract_title(lines)
            if not title:
                # fallback to doc metadata
                with fitz.open(self.pdf_path) as doc:
                    title = doc.metadata.get("title", "")
            return {"title": title, "outline": []}

        title = extract_title(lines)
        if not title:
            with fitz.open(self.pdf_path) as doc:
                title = doc.metadata.get("title", "")

        # Heading extraction pipeline
        candidates = find_heading_candidates(lines, avg_font)
        candidates = filter_common_headers(candidates, num_pages)
        candidates = remove_fragment_duplicates(candidates)
        candidates = assign_heading_levels(candidates)

        # Build outline: dedupe per page, keep order
        outline = []
        seen_text = set()
        for c in candidates:
            text_key = (c['text'].strip().lower(), c['page'])
            if text_key in seen_text:
                continue
            seen_text.add(text_key)
            outline.append({
                "level": c["level"],
                "text": c["text"].strip(),
                "page": c["page"],
            })
        return {"title": title, "outline": outline}
