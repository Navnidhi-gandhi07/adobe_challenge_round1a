#!/bin/bash
set -e
cp sample_dataset/pdfs/sample_multi.pdf input/
docker build --platform linux/amd64 -t doc_outline_multilang .
docker run --rm -v "$(pwd)/input":/app/input:ro -v "$(pwd)/output":/app/output --network none doc_outline_multilang
echo "=== OUTPUT JSON ==="
cat output/sample_multi.json
