```markdown
# 📄 PDF Outline Extractor

## 📌 Overview
This project extracts **Title and Headings (H1, H2, H3)** with page numbers from a PDF and outputs a structured JSON outline.

### ✅ Features
- Detects **numbered, roman, appendix-style, and title-like headings**
- Filters out **table of contents, footers, figure/table captions**
- Outputs JSON in the required format
- Runs **offline**, under **200MB**, and fast (**≤10s for 50 pages**)

---

## 📂 Project Structure
```

pdf-outline-extractor/
│── app/
│   ├── main.py          # Entry point
│   ├── extractor.py     # Heading extraction logic
│   ├── utils.py         # Helper functions
│   └── requirements.txt
│
├── Dockerfile
├── README.md

````

---

## 🚀 How to Run

### 1️⃣ Build Docker Image
```bash
docker build --platform linux/amd64 -t pdf-outline-extractor:latest .
````

### 2️⃣ Run the Container

```bash
docker run --rm \
-v $(pwd)/input:/app/input \
-v $(pwd)/output:/app/output \
--network none pdf-outline-extractor:latest
```

---

## 📄 Input / Output

* **Input:** Place PDFs inside `./input/`
* **Output:** Extracted JSON files will be saved in `./output/`

### 📌 Example Output

```json
{
  "title": "Understanding AI",
  "outline": [
    { "level": "H1", "text": "Introduction", "page": 1 },
    { "level": "H2", "text": "What is AI?", "page": 2 },
    { "level": "H3", "text": "History of AI", "page": 3 }
  ]
}
```

---

## ⚡ Performance

* **Runs completely offline**
* Uses **PyMuPDF** (fast PDF text extraction)
* Handles **multi-page PDFs up to 50 pages in ≤10s**

---

## 🏆 Hackathon Compliance

✅ **PDF Input → JSON Output**
✅ **Fast (≤10s)**
✅ **Lightweight (<200MB)**
✅ **Offline / No Internet Calls**

---