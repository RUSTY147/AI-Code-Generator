import ollama

def ask_llm(context, question):

    prompt = f"""
You are a senior software engineer.

Context:
{context}

Question:
{question}

Explain clearly.
"""

    response = ollama.chat(
        model="llama3",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]