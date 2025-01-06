from langchain_ollama import OllamaLLM
from config.settings import OLLAMA_HOST


def create_llm(model, temperature, max_tokens):
    return OllamaLLM(
        base_url=OLLAMA_HOST,
        model=model,
        temperature=temperature,
        num_ctx=max_tokens,
        keep_alive=-1
    )