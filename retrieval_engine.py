# retrieval_engine.py

import fitz  # PyMuPDF
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss

# 🧠 Load sentence embedding model (can be changed if needed)
model = SentenceTransformer("all-MiniLM-L6-v2")

# ✅ Step 1: Extract paragraphs from PDF
def extract_paragraphs_from_pdf(file_path):
    doc = fitz.open(file_path)
    paragraphs = []

    for page in doc:
        text = page.get_text()
        for para in text.split("\n\n"):
            clean = para.strip().replace("\n", " ")
            if len(clean) > 40:
                paragraphs.append(clean)
    return paragraphs

# ✅ Step 2: Create embeddings and FAISS index
def create_faiss_index(paragraphs):
    embeddings = model.encode(paragraphs, convert_to_numpy=True)
    dim = embeddings.shape[1]

    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    return index, embeddings

# ✅ Step 3: Load and embed the PDF
def load_and_embed_pdf(file_path):
    paragraphs = extract_paragraphs_from_pdf(file_path)
    index, embeddings = create_faiss_index(paragraphs)
    return paragraphs, index

# ✅ Step 4: Retrieve relevant clause
def retrieve_relevant_clause(query, index, paragraphs, top_k=1):
    query_embedding = model.encode([query], convert_to_numpy=True)
    D, I = index.search(query_embedding, top_k)
    return paragraphs[I[0][0]]  # return most relevant match
