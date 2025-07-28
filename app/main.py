import os
import json
import fitz  # PyMuPDF
from extractor import extract_headings_from_text, GENERIC_HEADINGS
from utils import FIELD_LABEL_PATTERN
import re
from collections import Counter

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
    # Robust: Get the largest/topmost non-form, not-artifact line on page 1 as title
    page = doc.load_page(0)
    blocks = page.get_text("dict")["blocks"]
    candidates = []
    for b in blocks:
        if "lines" not in b:
            continue
        for l in b["lines"]:
            for s in l["spans"]:
                stxt = s["text"].strip()
                if len(stxt) > 3 and not FIELD_LABEL_PATTERN.search(stxt) and not stxt.islower():
                    candidates.append({
                        "text": stxt,
                        "size": s["size"],
                        "flags": s["flags"],
                        "y": s["bbox"][1]
                    })
    if candidates:
        sorted_candidates = sorted(candidates, key=lambda x: (x["y"], -x["size"]))
        return sorted_candidates[0]["text"]
    return "Untitled Document"

def is_numbered_heading(txt):
    return bool(re.match(r'^\d+(\.\d+)*[\.\)]?\s+\S', txt))

def should_drop_heading(txt, page_count, all_headings_counter):
    txt_clean = txt.strip().lower()
    if all_headings_counter[txt_clean] > 0.2 * page_count:
        return True
    if txt_clean in GENERIC_HEADINGS and (len(txt_clean.split()) < 3 and not is_numbered_heading(txt)):
        return True
    if re.match(r'^\d{1,2}\s+[A-Z]{3,}\s+\d{4}$', txt):  # 18 JUNE 2013
        return True
    if re.match(r'^[A-Z]{3,}\d?$', txt):  # AFM1
        return True
    if len(txt_clean.split()) == 1 and not is_numbered_heading(txt):
        return True
    return False

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

    # FORM SUPPRESSION
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
        # Dedup/clean up
        txts = [h['text'] for h in outline]
        counter = Counter([t.strip().lower() for t in txts])
        seen = set()
        clean_outline = []
        for h in outline:
            t = h['text'].strip()
            if should_drop_heading(t, num_pages, counter):
                continue
            tkey = (t.lower(), h['level'])
            if tkey in seen:
                continue
            seen.add(tkey)
            clean_outline.append(h)
        outline = clean_outline
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
