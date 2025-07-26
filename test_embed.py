from document_parser import extract_text_from_pdf, chunk_text
from embed_store import create_faiss_index, search_faiss

# Load and chunk document
text = extract_text_from_pdf("HDFHLIP23024V072223.pdf")
chunks = chunk_text(text)

# Index banayein
index, _ = create_faiss_index(chunks)

# Sample query
query = "Kya maternity expenses covered hai?"
results = search_faiss(query, chunks, index)

# Results print
print("🔍 Query results:\n")
for i, r in enumerate(results):
    print(f"Chunk {i+1}:\n{r}\n")
