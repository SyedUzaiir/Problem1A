Here’s a **complete professional README.md** for your project – you can directly copy and paste:

---

# 📄 PDF Outline Extractor

This project extracts **headings and outlines** from PDF files and saves them as structured JSON files.
It uses **PyMuPDF (`fitz`)** and **KMeans clustering** to detect headings based on font size and numbering patterns.

The project is fully **Dockerized** for easy setup and runs in an isolated environment.

---

## 🚀 Features

✅ Extracts **title and headings (H1, H2, H3)** from PDFs
✅ Removes repeated/junk lines
✅ Generates **outline JSON** for each PDF
✅ Supports **batch processing of multiple PDFs**
✅ Works with **Docker** – no manual installation required

---

## 📂 Project Structure

```
Problem1A/
├── Dockerfile
├── docker-compose.yml
├── extractor.py
├── main.py
├── requirements.txt
├── README.md
├── input/           # Place all PDF files here
│   ├── file01.pdf
│   ├── file02.pdf
│   └── ...
└── output/          # JSON outputs will be saved here
    ├── file01_outline.json
    ├── file02_outline.json
    └── result.json
```

---

## 🛠️ Tech Stack

* **Python 3.10**
* **PyMuPDF (fitz)** – for PDF text extraction
* **scikit-learn** – for KMeans font-size clustering
* **Docker & Docker Compose**

---

## 📦 Setup & Installation

### 🔹 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/pdf-outline-extractor.git
cd Problem1A
```

### 🔹 2️⃣ Add Your PDFs

Place all your `.pdf` files inside the `input/` folder. Example:

```
Problem1A/input/file01.pdf
Problem1A/input/file02.pdf
```

---

## ▶️ Run with Docker

### 🔹 3️⃣ Build the Docker Image

```bash
docker-compose build
```

### 🔹 4️⃣ Run the Container

```bash
docker-compose up
```

✅ The script will process **all PDFs inside `input/`** and generate JSON files in `output/`.

---

## 📄 Output Files

* For each PDF → a JSON file like `file01_outline.json` will be created.
* A combined `result.json` will also be saved inside the `output/` folder.

Example JSON:

```json
{
    "title": "Sample PDF Document",
    "outline": [
        {"level": "H1", "text": "Introduction", "page": 1},
        {"level": "H2", "text": "Overview", "page": 2},
        {"level": "H3", "text": "Details", "page": 3}
    ]
}
```

---

## ⚡ Without Docker (Optional)

If you want to run locally without Docker:

```bash
# 1. Create Virtual Environment
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# 2. Install Dependencies
pip install -r requirements.txt

# 3. Run for a Single PDF
python main.py input/file01.pdf
```

---

## 📝 Folder Mounting in Docker

* `input/` → `/app/input` inside the container
* `output/` → `/app/output` inside the container

This is handled by **docker-compose.yml** automatically.

---

## 📌 Example Commands

### 🔹 Run & Stop

```bash
docker-compose up      # Start
docker-compose down    # Stop
```

### 🔹 Rebuild After Code Changes

```bash
docker-compose build --no-cache
docker-compose up
```

---

## 👨‍💻 Author

* **Syed Uzair Mohiuddin**
* **K. Sai Maruthi**
* Built for **Adobe Hackathon Project (Problem 1A)**


