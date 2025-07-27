# app.py

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from document_parser import extract_text_from_pdf, chunk_text
from embed_store import create_faiss_index, search_faiss
# from llm_reasoner import ask_gpt  # Uncomment if GPT working

app = FastAPI()

# Request body schema
class QueryRequest(BaseModel):
    documents: str  # Not used yet
    questions: List[str]

@app.post("/api/v1/hackrx/run")
async def run_query(req: QueryRequest):
    # Load and process PDF
    pdf_path = "HDFHLIP23024V072223.pdf"
    text = extract_text_from_pdf(pdf_path)
    chunks = chunk_text(text)
    index, _ = create_faiss_index(chunks)

    answers = []
    for question in req.questions:
        top_chunks = search_faiss(question, chunks, index)
        evidence = "\n---\n".join(top_chunks) if top_chunks else "No matching clause found."

        # Mock answer (replace with GPT later)
        mock_answer = f"(Mock Answer): {question}\nClause: {evidence[:300]}..."
        answers.append(mock_answer)

    return {"answers": answers}
