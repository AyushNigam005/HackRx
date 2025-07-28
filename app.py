# app.py

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from document_parser import extract_text_from_pdf, chunk_text
from embed_store import create_faiss_index, search_faiss
from llm_reasoner import ask_cohere  # 🧠 Mock or Real GPT answer

app = FastAPI()

# Request format (now multiple PDFs allowed)
class QueryRequest(BaseModel):
    documents: List[str]
    questions: List[str]

# Response format
class Answer(BaseModel):
    document: str
    question: str
    answer: str

class QueryResponse(BaseModel):
    answers: List[Answer]

@app.post("/api/v1/hackrx/run", response_model=QueryResponse)
async def run_query(req: QueryRequest):
    final_answers = []

    for doc_path in req.documents:
        try:
            text = extract_text_from_pdf(doc_path)
            chunks = chunk_text(text)
            index, _ = create_faiss_index(chunks)

            for question in req.questions:
                top_chunks = search_faiss(question, chunks, index)
                evidence = "\n---\n".join(top_chunks) if top_chunks else "No matching clause found."

                # 🧠 Ask Gemini
                gpt_answer = ask_cohere(question, evidence)

                final_answers.append({
                    "document": doc_path,
                    "question": question,
                    "answer": gpt_answer
                })

        except Exception as e:
            for question in req.questions:
                final_answers.append({
                    "document": doc_path,
                    "question": question,
                    "answer": f"❌ Error while processing '{doc_path}': {str(e)}"
                })

    return {"answers": final_answers}
