FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py extractor.py .  

RUN mkdir /app/input /app/output

ENTRYPOINT ["python", "main.py"]
