from fastapi import HTTPException
from src.Services.OpenRouterService import OpenRouterService
from src.Utils.Interface.IModels import (
    ChatRequest,
    ChatResponse,
    AnalyzeCVRequest,
    GenerateJobDescriptionRequest
)
from src.Utils.BaseError import BaseError


class AIController:
    @staticmethod
    async def chat(request: ChatRequest) -> ChatResponse:
        """
        Endpoint pour les conversations avec l'IA via OpenRouter
        """
        try:
            result = await OpenRouterService.chat(request)
            return ChatResponse(**result)
        except BaseError as e:
            raise HTTPException(status_code=e.status_code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    async def analyze_cv(request: AnalyzeCVRequest) -> ChatResponse:
        """
        Analyse un CV et le compare avec une description de poste
        """
        try:
            result = await OpenRouterService.analyze_cv(
                request.cv_text,
                request.job_description
            )
            return ChatResponse(**result)
        except BaseError as e:
            raise HTTPException(status_code=e.status_code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    async def generate_job_description(request: GenerateJobDescriptionRequest) -> ChatResponse:
        """
        Génère une description de poste optimisée
        """
        try:
            result = await OpenRouterService.generate_job_description(
                request.title,
                request.company,
                request.requirements,
                request.skills
            )
            return ChatResponse(**result)
        except BaseError as e:
            raise HTTPException(status_code=e.status_code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

