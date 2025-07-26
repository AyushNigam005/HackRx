# llm_reasoner.py
import openai

# ✅ Tumhara OpenAI API key yaha daalo
openai.api_key = "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"  # ← Replace this!

def mock_gpt(question, context):
    return f"Mocked answer for: {question}"
# ⚠️ Mock function for testing purposes, replace with actual GPT call in production
def ask_gpt(question, evidence):
    """
    GPT-4 se intelligent answer lena with retrieved clause context.
    """
    prompt = f"""
You are an expert insurance assistant.
Use the below extracted clause from the policy document to answer the user's query.

Clause:
\"\"\"{evidence}\"\"\"

Query: {question}
Give a clear YES/NO followed by explanation.
Answer:"""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # use gpt-3.5-turbo if GPT-4 not available
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    
    return response["choices"][0]["message"]["content"]
