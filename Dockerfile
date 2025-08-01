FROM --platform=linux/amd64 python:3.9-slim

RUN apt-get update && apt-get install -y \
    tesseract-ocr libtesseract-dev \
    tesseract-ocr-eng tesseract-ocr-hin tesseract-ocr-pan tesseract-ocr-jpn && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "main.py"]
