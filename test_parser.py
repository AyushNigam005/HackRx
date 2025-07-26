from document_parser import extract_text_from_pdf, chunk_text

# Tumhara test PDF file
pdf_path = "HDFHLIP23024V072223.pdf"  # Ensure same folder me ho

# Text extract karo
text = extract_text_from_pdf(pdf_path)
print("✅ PDF se text extract ho gaya")

# Chunk bana lo
chunks = chunk_text(text)
print(f"🔹 {len(chunks)} chunks ban gaye\n")

# Pehle 3 chunks print karo
for i, chunk in enumerate(chunks[:3]):
    print(f"--- Chunk {i+1} ---\n{chunk}\n")
