import os, json, fitz
from .extractor import extract_headings_from_text

INPUT_DIR = "/app/input"
OUTPUT_DIR = "/app/output"

def process_pdf(pdf_path, output_path):
    doc = fitz.open(pdf_path)

    all_headings = []
    title = doc[0].get_text("text").strip().split("\n")[0]  # First line as title

    for page_num, page in enumerate(doc, start=1):
        text = page.get_text("text")
        page_headings = extract_headings_from_text(text, page_num)
        all_headings.extend(page_headings)

    result = {"title": title, "outline": all_headings}

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for file in os.listdir(INPUT_DIR):
        if file.endswith(".pdf"):
            pdf_path = os.path.join(INPUT_DIR, file)
            output_path = os.path.join(OUTPUT_DIR, file.replace(".pdf", ".json"))
            process_pdf(pdf_path, output_path)

if __name__ == "__main__":
    main()
