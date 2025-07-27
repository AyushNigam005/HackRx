from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List
from retrieval import get_context_for_questions  # ← Importing function from retrieval.py

app = FastAPI()

# --- Token Security ---
security = HTTPBearer()

def verify_token(auth: HTTPAuthorizationCredentials = Depends(security)):
    expected_token = "ee780205a54c3c1504fd981ed73efa751d8b9a453087a3f5a9b9d03c8e93ed83"
    if auth.credentials != expected_token:
        raise HTTPException(status_code=401, detail="Unauthorized")

# --- Request and Response Models ---
class QueryRequest(BaseModel):
    documents: str
    questions: List[str]

class QueryResponse(BaseModel):
    answers: List[str]

# --- API Endpoint ---
@app.post("/api/v1/hackrx/run", response_model=QueryResponse, dependencies=[Depends(verify_token)])
def run_query(payload: QueryRequest):
    print("Running query for:", payload.questions)
    answers = get_context_for_questions(payload.documents, payload.questions)
    print("Answers generated:", answers)
    return {"answers": answers}

