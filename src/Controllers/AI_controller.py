from fastapi import HTTPException, UploadFile
from src.Services.OpenRouterService import OpenRouterService
from src.Services.FileExtractionService import FileExtractionService
from src.Utils.Interface.IModels import (
    ChatRequest,
    ChatResponse,
    AnalyzeCVRequest,
    GenerateJobDescriptionRequest,
    ExtractTextResponse
)
from src.Utils.BaseError import BaseError
import os


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
    
    @staticmethod
    async def extract_text(file: UploadFile) -> ExtractTextResponse:
        """
        Extrait le texte d'un fichier (PDF, DOCX, TXT)
        """
        try:
            # Vérifier le type de fichier
            file_extension = os.path.splitext(file.filename)[1] if file.filename else ''
            if not file_extension:
                raise BaseError("Impossible de déterminer le type de fichier", 400)
            
            # Lire le contenu du fichier
            file_content = await file.read()
            
            # Vérifier la taille (max 10MB)
            max_size = 10 * 1024 * 1024  # 10MB
            if len(file_content) > max_size:
                raise BaseError("Le fichier est trop volumineux (max 10MB)", 400)
            
            # Extraire le texte
            text = FileExtractionService.extract_text_from_file(file_content, file_extension)
            
            return ExtractTextResponse(
                text=text,
                file_name=file.filename or "unknown",
                file_type=file_extension.lstrip('.'),
                character_count=len(text)
            )
        except BaseError as e:
            raise HTTPException(status_code=e.status_code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erreur lors de l'extraction: {str(e)}")

