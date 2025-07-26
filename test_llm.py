from document_parser import extract_text_from_pdf, chunk_text
from embed_store import create_faiss_index, search_faiss
from llm_reasoner import ask_gpt

# 1. Load and Chunk the PDF
text = extract_text_from_pdf("HDFHLIP23024V072223.pdf")
chunks = chunk_text(text)
index, _ = create_faiss_index(chunks)

# 2. User Query
question = "Kya maternity expenses covered hai?"

# 3. FAISS se Relevant Chunks
top_chunks = search_faiss(question, chunks, index)
evidence = "\n---\n".join(top_chunks)

# 4. Ask GPT
answer = ask_gpt(question, evidence)

# 5. Print Output
print("🧠 GPT Answer:\n")
print(answer)
