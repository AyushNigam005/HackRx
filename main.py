from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List

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

# --- Mock LLM Logic (until real GPT is plugged in) ---
def mock_gpt(question: str, content: str) -> str:
    return f"Mocked answer for: {question}"

# --- API Endpoint ---
@app.post("/api/v1/hackrx/run", response_model=QueryResponse, dependencies=[Depends(verify_token)])
def run_query(payload: QueryRequest):
    content = f"Fetched content from: {payload.documents}"  # Placeholder
    answers = [mock_gpt(q, content) for q in payload.questions]
    return {"answers": answers}
