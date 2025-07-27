import fitz  # PyMuPDF
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import requests
import tempfile

# Load sentence transformer model once
model = SentenceTransformer("all-MiniLM-L6-v2")

def extract_clauses_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    # Split by full stops for rough clause segmentation
    clauses = [clause.strip() for clause in text.split('.') if clause.strip()]
    return clauses

def build_faiss_index(clauses):
    embeddings = model.encode(clauses)
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings))
    return index, embeddings

def retrieve_relevant_clauses(query, clauses, index, embeddings, top_k=3):
    query_embedding = model.encode([query])
    D, I = index.search(np.array(query_embedding), top_k)
    results = [clauses[i] for i in I[0]]
    return results

def get_context_for_questions(document_url: str, questions: list) -> list:
    # Step 1: Download the PDF from URL
    response = requests.get(document_url)
    if response.status_code != 200:
        return [f"Failed to download PDF: {response.status_code}"]

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(response.content)
        tmp_path = tmp.name

    # Step 2: Extract clauses from PDF
    clauses = extract_clauses_from_pdf(tmp_path)

    # Step 3: Build FAISS index
    index, embeddings = build_faiss_index(clauses)

    # Step 4: Retrieve top answers for each question
    results = []
    for question in questions:
        top_clauses = retrieve_relevant_clauses(question, clauses, index, embeddings)
        answer = f"Question: {question}\nAnswer:\n" + "\n".join(top_clauses)
        results.append(answer)

    return results
