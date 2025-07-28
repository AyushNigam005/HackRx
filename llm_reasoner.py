import cohere

co = cohere.Client("TFinrBNShrjda6awNw1KdfjWc7raoq42QGRu7mQe")

def ask_cohere(question, context):
    prompt = f"""You are a smart insurance assistant.
Use the following clause to answer the user query clearly.

Clause:
\"\"\"{context}\"\"\"

Query: {question}
Give a YES or NO answer, and short explanation."""

    response = co.generate(
        model="command",  # ✅ Use "command" instead of "command-r"
        prompt=prompt,
        max_tokens=150,
        temperature=0.3
    )
    return response.generations[0].text.strip()
