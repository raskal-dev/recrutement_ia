from fastapi import APIRouter
from src.Controllers.AI.controller import AIController
from src.Utils.Interface.IModels import (
    ChatRequest,
    ChatResponse,
    AnalyzeCVRequest,
    GenerateJobDescriptionRequest
)

ai_router = APIRouter(prefix="", tags=["AI"])


@ai_router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Endpoint pour les conversations avec l'IA via OpenRouter
    """
    return await AIController.chat(request)


@ai_router.post("/analyze-cv", response_model=ChatResponse)
async def analyze_cv(request: AnalyzeCVRequest):
    """
    Analyse un CV et le compare avec une description de poste
    """
    return await AIController.analyze_cv(request)


@ai_router.post("/generate-job-description", response_model=ChatResponse)
async def generate_job_description(request: GenerateJobDescriptionRequest):
    """
    Génère une description de poste optimisée
    """
    return await AIController.generate_job_description(request)

