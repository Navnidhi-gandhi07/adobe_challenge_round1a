from multilingual_pdf2text.pdf2text import PDF2Text
from multilingual_pdf2text.models.document_model.document import Document

def ocr_extract_full_text(pdf_path, lang_codes="eng+hin+pan+jpn"):
    doc = Document(document_path=pdf_path, language=lang_codes)
    pdf2text = PDF2Text(document=doc)
    return pdf2text.extract()
