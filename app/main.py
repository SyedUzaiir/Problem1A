import os
import json
import fitz  # PyMuPDF
from extractor import extract_headings_from_text, GENERIC_UNINFORMATIVE
from utils import FIELD_LABEL_PATTERN
import re

def get_base_dirs():
    if os.path.exists("/app/input"):
        input_dir = "/app/input"
        output_dir = "/app/output"
    else:
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        input_dir = os.path.join(base_dir, 'input')
        output_dir = os.path.join(base_dir, 'output')
    return input_dir, output_dir

INPUT_DIR, OUTPUT_DIR = get_base_dirs()

def get_title(doc):
    for page in doc:
        text_lines = page.get_text("text").splitlines()
        for line in text_lines[:10]:
            s = line.strip()
            if len(s) > 3 and not s.islower():
                return s
    return "Untitled Document"

from collections import Counter

def filter_common_headings(headings, num_pages):
    # Remove boilerplate repeated on >20% of pages or global generic words
    count = Counter(h["text"].strip().lower() for h in headings)
    blacklist = {t for t, f in count.items() if f > 0.2 * num_pages or t in GENERIC_UNINFORMATIVE}
    seen = set()
    result = []
    for h in headings:
        t = h["text"].strip().lower()
        # Exclude generic one/two-word headings even if not frequent, unless numbered
        if t in blacklist:
            continue
        nwords = len(t.split())
        is_numbered = h["level"] in {"H1", "H2", "H3"} and re.match(r'^\d+(\.\d+)*', h["text"])
        if nwords < 3 and t in GENERIC_UNINFORMATIVE and not is_numbered:
            continue
        if t in seen:
            continue
        seen.add(t)
        result.append(h)
    return result

def process_pdf(file_path, output_path):
    doc = fitz.open(file_path)
    title = get_title(doc)
    all_headings = []
    pagewise_headings = []
    num_pages = doc.page_count
    for page_num, page in enumerate(doc, start=1):
        text = page.get_text("text")
        headings = extract_headings_from_text(text)
        pagewise_headings.append((page_num, headings))
        all_headings += headings

    # FORM SUPPRESSION: Like before
    num_field_like = sum(1 for h in all_headings if FIELD_LABEL_PATTERN.search(h["text"]))
    if all_headings and num_field_like / len(all_headings) > 0.2:
        outline = []
    else:
        outline = []
        for page_num, headings in pagewise_headings:
            outline.extend([
                { "level": h["level"], "text": h["text"], "page": page_num }
                for h in headings
            ])
        outline = filter_common_headings(outline, num_pages)
    output = {"title": title, "outline": outline}
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    pdf_files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(".pdf")]
    if not pdf_files:
        print("⚠️  No PDF files found in input folder.")
    for file in pdf_files:
        input_file = os.path.join(INPUT_DIR, file)
        output_file = os.path.join(OUTPUT_DIR, file.replace(".pdf", ".json"))
        try:
            process_pdf(input_file, output_file)
            print(f"✅ Processed {file} -> {output_file}")
        except Exception as e:
            print(f"⚠️ Error processing {file}: {e}")

if __name__ == "__main__":
    main()
