import os
from dotenv import load_dotenv

load_dotenv()

# Configuration OpenRouter
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Modèles gratuits disponibles sur OpenRouter
FREE_MODELS = [
    "google/gemini-flash-1.5-8b:free",
    "meta-llama/llama-3.2-3b-instruct:free",
    "mistralai/mistral-7b-instruct:free",
    "qwen/qwen-2.5-7b-instruct:free",
]

APP_URL = os.getenv("APP_URL", "http://localhost:8000")

