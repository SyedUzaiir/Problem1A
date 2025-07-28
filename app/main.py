import os
import json
import fitz  # PyMuPDF
from extractor import extract_headings_from_text
import re

def get_base_dirs():
    """
    Returns (input_dir, output_dir) that work for both Docker and local:
    - If /app/input exists, use it (Docker)
    - Otherwise use ../input/ and ../output/ relative to this script (local)
    """
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
    """Return the first likely title line from the PDF."""
    for page in doc:
        text_lines = page.get_text("text").splitlines()
        for line in text_lines[:10]:
            s = line.strip()
            if len(s) > 3 and not s.islower():
                return s
    return "Untitled Document"

def determine_heading_level(heading):
    """Assign outline level based on numbering or fallback to H1."""
    if re.match(r'^\d+(\.\d+)*', heading):
        depth = heading.split(".")
        return f"H{min(len(depth), 3)}"
    return "H1"

def process_pdf(file_path, output_path):
    doc = fitz.open(file_path)
    title = get_title(doc)
    outline = []
    for page_num, page in enumerate(doc, start=1):
        text = page.get_text("text")
        headings = extract_headings_from_text(text)
        seen = set()
        for heading in headings:
            heading_key = (heading.strip().lower(), page_num)
            if heading_key in seen:
                continue  # dedupe per page
            seen.add(heading_key)
            level = determine_heading_level(heading)
            outline.append({
                "level": level,
                "text": heading,
                "page": page_num
            })
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
