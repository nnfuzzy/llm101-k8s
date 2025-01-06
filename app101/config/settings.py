import os
from dotenv import load_dotenv

load_dotenv()

# Global settings
ollama_models = []
current_model = None
temperature = 0.7
max_tokens = 256

OLLAMA_HOST = os.getenv("OLLAMA_BASE_URL")