# Use Python base image for AMD64 architecture
FROM --platform=linux/amd64 python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . /app

# The container should process PDFs from /app/input and output JSON to /app/output
CMD ["python", "main.py", "/app/input", "/app/output"]
