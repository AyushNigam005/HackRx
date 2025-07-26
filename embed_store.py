# embed_store.py
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Load model (once)
model = SentenceTransformer("all-MiniLM-L6-v2")

def create_faiss_index(chunks):
    """
    Chunks ka embedding banao aur FAISS index create karo.
    """
    embeddings = model.encode(chunks)
    dim = embeddings[0].shape[0]  # typically 384
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings))
    return index, embeddings

def search_faiss(query, chunks, index, top_k=3):
    """
    User query se top_k matching chunks laao.
    """
    q_embed = model.encode([query])
    D, I = index.search(np.array(q_embed), top_k)
    return [chunks[i] for i in I[0]]
