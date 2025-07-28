import fitz
import numpy as np
from sklearn.cluster import KMeans
from .ocr_helper import ocr_extract_full_text

COMMON_FOOTER_KEYWORDS = ['Page', 'Confidential', '©', '–', '-']

def is_footer_header(text):
    return any(kw in text for kw in COMMON_FOOTER_KEYWORDS)

def extract_outline_from_pdf(pdf_path, lang_codes="eng+hin+pan+jpn"):
    doc = fitz.open(pdf_path)
    spans = []
    for pnum, page in enumerate(doc, start=1):
        for b in page.get_text("dict")["blocks"]:
            for line in b.get("lines", []):
                for span in line.get("spans", []):
                    t = span["text"].strip()
                    if t and not is_footer_header(t):
                        spans.append({"text": t, "size": span["size"], "page": pnum})

    headings = []
    title = ""
    if spans:
        sizes = np.array([[s["size"]] for s in spans])
        n = min(4, len(sizes))
        kmeans = KMeans(n_clusters=n, random_state=0).fit(sizes)
        labels = kmeans.labels_
        centroids = kmeans.cluster_centers_.flatten()
        order = np.argsort(centroids)[::-1]
        level_names = ["H1","H2","H3","H4"][:n]
        label2level = {lbl: level_names[i] for i, lbl in enumerate(order)}

        for s, lbl in zip(spans, labels):
            headings.append({"level": label2level[lbl], "text": s["text"], "page": s["page"]})

        p1 = [s for s in spans if s["page"] == 1]
        if p1:
            title = max(p1, key=lambda x: x["size"])["text"]
    else:
        content = ocr_extract_full_text(pdf_path, lang_codes)
        lines = [l.strip() for l in content.splitlines() if l.strip()]
        if lines:
            title = lines[0]
            for li in lines[1:]:
                if li.isupper() or len(li.split()) <=5:
                    headings.append({"level": "H1", "text": li, "page": 1})

    seen = set()
    filtered = []
    for h in headings:
        key = (h['level'], h['text'], h['page'])
        if key not in seen:
            seen.add(key)
            filtered.append(h)
    filtered.sort(key=lambda x: (x['page'], x['level']))
    return {"title": title, "headings": filtered}
