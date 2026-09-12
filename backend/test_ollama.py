from ollama import chat


response = chat(
    model="qwen3:0.6b",
    messages=[
        {
            "role": "user",
            "content": (
                "Say hello and confirm that the Python to Ollama "
                "connection is working."
            )
        }
    ]
)

print(response.message.content)