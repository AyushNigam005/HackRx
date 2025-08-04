from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List
import requests, os, tempfile

from document_parser import extract_text_from_pdf, chunk_text
from embed_store import create_faiss_index, search_faiss
from llm_reasoner import ask_cohere  # if using Cohere

app = FastAPI()

API_KEY = os.getenv("ee780205a54c3c1504fd981ed73efa751d8b9a453087a3f5a9b9d03c8e93ed83")
security = HTTPBearer()

def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    if credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid auth scheme")
    if credentials.credentials != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return True  # can return user/context if needed

class QueryRequest(BaseModel):
    documents: str
    questions: List[str]

class QueryResponse(BaseModel):
    answers: List[str]

@app.post("/hackrx/run", response_model=QueryResponse, dependencies=[Depends(verify_token)])
async def run_query(req: QueryRequest):
    # Download PDF from URL
    try:
        response = requests.get(req.documents, verify=False)
        response.raise_for_status()
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(response.content)
            pdf_path = tmp.name
    except Exception as e:
        return {"answers": [f"❌ Failed to download PDF: {e}"]}

    # Extract / chunk / embed
    try:
        text = extract_text_from_pdf(pdf_path)
        chunks = chunk_text(text)
        index, _ = create_faiss_index(chunks)
    except Exception as e:
        return {"answers": [f"❌ Failed to process PDF: {e}"]}

    # Answer via Cohere (or mock)
    final_answers = []
    for question in req.questions:
        try:
            top_chunks = search_faiss(question, chunks, index)
            evidence = "\n".join(top_chunks)[:4000]  # ensures context stays tight and focused
            answer = ask_cohere(question, evidence)  # or fallback mock
            final_answers.append(answer)
        except Exception as e:
            final_answers.append(f"❌ Error answering: {question} → {e}")

    return {"answers": final_answers}
