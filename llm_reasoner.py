import cohere
import time
import os

COHERE_API_KEY = os.getenv("TFinrBNShrjda6awNw1KdfjWc7raoq42QGRu7mQe")
co = cohere.Client(COHERE_API_KEY)

def ask_cohere(question: str, context: str) -> str:
    trimmed_context = context[:4000]

    prompt = f"""You are an expert assistant answering strictly from insurance policy documents.

Only answer using information from the context. Do not guess or speculate.
Do not say “yes”, “no”, “the answer is”, or mention missing information.
Use one clear, complete sentence based only on the content below.

Context:
\"\"\"{trimmed_context}\"\"\"

Question: {question}
Answer:"""

    for attempt in range(3):
        try:
            response = co.generate(
                model="command-light",
                prompt=prompt,
                max_tokens=300,
                temperature=0.3,
                stop_sequences=["\n"]
            )
            return response.generations[0].text.strip()
        except Exception as e:
            print(f"[Attempt {attempt+1}] Cohere API error: {e}")
            time.sleep(1)

    return "❌ Cohere API error after 3 retries."
