import os, glob, json
from utils.extractor import extract_outline_from_pdf

def main():
    os.makedirs("/app/output", exist_ok=True)
    for pdf in glob.glob("/app/input/*.pdf"):
        result = extract_outline_from_pdf(pdf)
        name = os.path.splitext(os.path.basename(pdf))[0]
        out = {"title": result["title"], "outline": result["headings"]}
        with open(f"/app/output/{name}.json", "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=2)
        print(f"Processed {name}")

if __name__ == "__main__":
    main()
