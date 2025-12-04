from fastapi import FastAPI
from src.Routes.index import router
from src.Middlewares.CORS import setup_cors
from src.Configs.OpenRouter.config import FREE_MODELS

app = FastAPI(
    title="Recrutement IA Service",
    description="Service IA pour la plateforme de recrutement utilisant OpenRouter",
    version="1.0.0"
)

# Configuration CORS
setup_cors(app)

# Inclusion des routes
app.include_router(router)


@app.get("/")
async def root():
    """
    Endpoint racine avec informations sur le service
    """
    return {
        "message": "Service IA pour Recrutement",
        "status": "running",
        "available_models": FREE_MODELS
    }


@app.get("/health")
async def health():
    """
    Endpoint de santé pour vérifier que le service est opérationnel
    """
    return {"status": "healthy"}


@app.get("/models")
async def get_models():
    """
    Retourne la liste des modèles disponibles
    """
    return {
        "free_models": FREE_MODELS,
        "default": FREE_MODELS[0]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
