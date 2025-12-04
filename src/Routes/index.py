from fastapi import APIRouter
from src.Routes.AI.routes import ai_router

router = APIRouter(prefix="/ai", tags=["AI"])

router.include_router(ai_router)

