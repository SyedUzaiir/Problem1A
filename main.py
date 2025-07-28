import os
import json
from extractor import PDFOutlineExtractor

INPUT_DIR = "input"  # Use "/app/input" if mounting in Docker
OUTPUT_DIR = "output"  # Use "/app/output" if mounting in Docker

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    pdf_files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(".pdf")]
    if not pdf_files:
        print("❌ No PDF files found in input folder.")
        return

    for pdf_file in pdf_files:
        input_path = os.path.join(INPUT_DIR, pdf_file)
        output_file = os.path.splitext(pdf_file)[0] + ".json"
        output_path = os.path.join(OUTPUT_DIR, output_file)
        try:
            print(f"📄 Processing: {pdf_file}")
            extractor = PDFOutlineExtractor(input_path)
            result = extractor.extract_outline()
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            print(f"✅ Outline saved to {output_path}")
        except Exception as e:
            print(f"⚠️ Error processing {pdf_file}: {e}")

if __name__ == "__main__":
    main()
