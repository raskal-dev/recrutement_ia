import os
from dotenv import load_dotenv

load_dotenv()

# Configuration OpenRouter
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Modèles gratuits disponibles sur OpenRouter (priorité en tête de liste)
FREE_MODELS = [
    "qwen/qwen3-coder:free",
    "qwen/qwen3-235b-a22b:free",
    "nousresearch/hermes-3-llama-3.1-405b:free",
    "openai/gpt-oss-120b:free",
]

APP_URL = os.getenv("APP_URL", "http://localhost:8000")

