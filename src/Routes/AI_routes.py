from fastapi import APIRouter, HTTPException
from src.Controllers.AI_controller import AIController
from src.Utils.Interface.IModels import (
    ChatRequest,
    ChatResponse,
    AnalyzeCVRequest,
    GenerateJobDescriptionRequest
)

ai_router = APIRouter(prefix="", tags=["AI"])


@ai_router.post(
    "/chat",
    response_model=ChatResponse,
    summary="Chat avec l'IA",
    description="""
    Permet d'avoir une conversation avec l'IA via OpenRouter.
    
    Vous pouvez spécifier le modèle à utiliser ou laisser le système choisir un modèle gratuit par défaut.
    
    **Exemple de requête :**
    ```json
    {
        "messages": [
            {"role": "user", "content": "Bonjour, peux-tu m'aider ?"}
        ],
        "model": "google/gemini-flash-1.5-8b:free",
        "temperature": 0.7,
        "max_tokens": 1000
    }
    ```
    """,
    responses={
        200: {
            "description": "Réponse générée avec succès",
            "content": {
                "application/json": {
                    "example": {
                        "content": "Bonjour ! Je serais ravi de vous aider. Comment puis-je vous assister aujourd'hui ?",
                        "model": "google/gemini-flash-1.5-8b:free",
                        "usage": {"prompt_tokens": 10, "completion_tokens": 15}
                    }
                }
            }
        },
        400: {"description": "Requête invalide"},
        500: {"description": "Erreur serveur"},
        503: {"description": "Service IA indisponible"},
    }
)
async def chat(request: ChatRequest):
    """
    Endpoint pour les conversations avec l'IA via OpenRouter
    """
    return await AIController.chat(request)


@ai_router.post(
    "/analyze-cv",
    response_model=ChatResponse,
    summary="Analyser un CV",
    description="""
    Analyse un CV et fournit des recommandations personnalisées.
    
    Si une description de poste est fournie, l'analyse comparera le CV avec les exigences du poste.
    
    **Exemple de requête :**
    ```json
    {
        "cv_text": "John Doe\\nDéveloppeur Full Stack\\n5 ans d'expérience...",
        "job_description": "Nous recherchons un développeur React expérimenté..."
    }
    ```
    """,
    responses={
        200: {
            "description": "Analyse terminée avec succès",
            "content": {
                "application/json": {
                    "example": {
                        "content": "Votre CV présente de solides compétences en développement web...",
                        "model": "google/gemini-flash-1.5-8b:free"
                    }
                }
            }
        },
        400: {"description": "CV texte requis"},
        500: {"description": "Erreur lors de l'analyse"},
    }
)
async def analyze_cv(request: AnalyzeCVRequest):
    """
    Analyse un CV et le compare avec une description de poste (optionnelle)
    """
    return await AIController.analyze_cv(request)


@ai_router.post(
    "/generate-job-description",
    response_model=ChatResponse,
    summary="Générer une description de poste",
    description="""
    Génère une description de poste optimisée et professionnelle basée sur les informations fournies.
    
    **Exemple de requête :**
    ```json
    {
        "title": "Développeur Full Stack",
        "company": "TechCorp",
        "requirements": ["Bac+5", "3 ans d'expérience", "Anglais courant"],
        "skills": ["React", "Node.js", "TypeScript", "Docker"]
    }
    ```
    """,
    responses={
        200: {
            "description": "Description générée avec succès",
            "content": {
                "application/json": {
                    "example": {
                        "content": "TechCorp recherche un Développeur Full Stack expérimenté...",
                        "model": "google/gemini-flash-1.5-8b:free"
                    }
                }
            }
        },
        400: {"description": "Données invalides"},
        500: {"description": "Erreur lors de la génération"},
    }
)
async def generate_job_description(request: GenerateJobDescriptionRequest):
    """
    Génère une description de poste optimisée et professionnelle
    """
    return await AIController.generate_job_description(request)

