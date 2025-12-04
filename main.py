from fastapi import FastAPI
from src.Routes.index import router
from src.Middlewares.CORS import setup_cors
from src.Configs.OpenRouter.config import FREE_MODELS

app = FastAPI(
    title="Recrutement IA Service",
    description="""
    Service IA pour la plateforme de recrutement utilisant OpenRouter.
    
    ## Fonctionnalités
    
    * **Chat avec l'IA** : Conversations avec des modèles IA via OpenRouter
    * **Analyse de CV** : Analyse intelligente de CVs avec recommandations
    * **Génération de descriptions** : Création automatique de descriptions de poste optimisées
    
    ## Modèles disponibles
    
    Les modèles gratuits suivants sont disponibles :
    * google/gemini-flash-1.5-8b:free
    * meta-llama/llama-3.2-3b-instruct:free
    * mistralai/mistral-7b-instruct:free
    * qwen/qwen-2.5-7b-instruct:free
    """,
    version="1.0.0",
    contact={
        "name": "Support IA",
        "email": "support-ia@recrutement.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    servers=[
        {
            "url": "http://localhost:8000",
            "description": "Serveur de développement",
        },
        {
            "url": "https://ai.recrutement.com",
            "description": "Serveur de production",
        },
    ],
)

# Configuration CORS
setup_cors(app)

# Inclusion des routes
app.include_router(router)


@app.get(
    "/",
    summary="Informations du service",
    description="Retourne les informations générales sur le service IA",
    tags=["Service"]
)
async def root():
    """
    Endpoint racine avec informations sur le service
    """
    return {
        "message": "Service IA pour Recrutement",
        "status": "running",
        "available_models": FREE_MODELS,
        "version": "1.0.0"
    }


@app.get(
    "/health",
    summary="Santé du service",
    description="Vérifie que le service est opérationnel",
    tags=["Service"],
    responses={
        200: {
            "description": "Service opérationnel",
            "content": {
                "application/json": {
                    "example": {"status": "healthy"}
                }
            }
        }
    }
)
async def health():
    """
    Endpoint de santé pour vérifier que le service est opérationnel
    """
    return {"status": "healthy"}


@app.get(
    "/models",
    summary="Liste des modèles disponibles",
    description="Retourne la liste de tous les modèles IA disponibles via OpenRouter",
    tags=["Service"],
    responses={
        200: {
            "description": "Liste des modèles",
            "content": {
                "application/json": {
                    "example": {
                        "free_models": [
                            "google/gemini-flash-1.5-8b:free",
                            "meta-llama/llama-3.2-3b-instruct:free"
                        ],
                        "default": "google/gemini-flash-1.5-8b:free"
                    }
                }
            }
        }
    }
)
async def get_models():
    """
    Retourne la liste des modèles disponibles
    """
    return {
        "free_models": FREE_MODELS,
        "default": FREE_MODELS[0] if FREE_MODELS else None
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
