from langchain_ollama.llms import OllamaLLM


def create_model():
    model = OllamaLLM(
        model="llama3.1:8b",
        temperature=0.7,
        frequency_penalty=0.5,
        presence_penalty=0.3,
        max_tokens=1000
    )
    return model
