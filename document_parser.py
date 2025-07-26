import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    """
    PDF file se pura text extract karta hai.
    """
    doc = fitz.open(pdf_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    return full_text

def chunk_text(text, max_words=100):
    """
    Text ko chunks me divide karta hai (100 words each).
    """
    words = text.split()
    return [" ".join(words[i:i + max_words]) for i in range(0, len(words), max_words)]
