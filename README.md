# PDF Outline Extractor (Multilingual)

## Overview
Extracts Title, H1, H2, H3 from PDFs, supports multilingual text via OCR.

## Requirements
- Docker
- Tesseract inside container
- Works offline

## Build
```bash
docker build --platform linux/amd64 -t doc_outline_multilang .
