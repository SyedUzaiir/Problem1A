# 📄 PDF Outline Extractor

## 📌 Overview

This project extracts **Title and Headings (H1, H2, H3)** with page numbers from PDF files and outputs a structured JSON outline.

### ✅ Features

* Detects **numbered, roman numeral, appendix-style, and title-like headings**
* Filters out **table of contents, footers, figure/table captions, and artifacts**
* Outputs JSON in the required format
* Runs **offline**, **fast (≤10s for 50 pages)**, and **lightweight (<200MB)**

---

## 📂 Project Structure

```
pdf-outline-extractor/
│── app/
│   ├── main.py          # Entry point script
│   ├── extractor.py     # Core heading extraction logic
│   ├── utils.py         # Helper functions
│   └── requirements.txt # Python dependencies
│
├── Dockerfile
├── README.md
```

---

## 🚀 How to Build & Run

### 1️⃣ Build Docker Image

```
docker build --platform linux/amd64 -t pdf-outline-extractor:latest .
```

### 2️⃣ Run the Container

```
docker run --rm \
-v $(pwd)/input:/app/input \
-v $(pwd)/output:/app/output \
--network none pdf-outline-extractor:latest
```

---

## 📄 Input & Output

* **Input:** Place PDFs in the `./input/` folder
* **Output:** Extracted JSON files will be saved in the `./output/` folder

### 📌 Example Output

```
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

* Extracts headings **without internet access**
* Uses **PyMuPDF** for fast text extraction
* Processes **≤50-page PDFs in under 10 seconds**

---

## 🏆 Hackathon Compliance

✅ Accepts PDFs from `/app/input` and writes JSON to `/app/output`
✅ Works fully **offline**
✅ Compatible with **AMD64 CPUs**
✅ Meets execution time and size requirements

---

## 📜 License

MIT License
