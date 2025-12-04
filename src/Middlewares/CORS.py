from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import os

def setup_cors(app: FastAPI):
    """
    Configure le middleware CORS
    """
    allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

