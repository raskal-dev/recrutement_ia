import httpx
from typing import List, Optional
from src.Configs.OpenRouter.config import OPENROUTER_API_KEY, OPENROUTER_API_URL, FREE_MODELS, APP_URL
from src.Utils.BaseError import BaseError
from src.Utils.Interface.IModels import ChatRequest, ChatMessage


class OpenRouterService:
    @staticmethod
    async def chat(request: ChatRequest) -> dict:
        """
        Envoie une requête de chat à OpenRouter
        """
        if not OPENROUTER_API_KEY:
            raise BaseError("OPENROUTER_API_KEY n'est pas configurée", 500)

        # Utiliser le modèle spécifié ou le premier modèle gratuit par défaut
        model = request.model or FREE_MODELS[0]

        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": APP_URL,
            "X-Title": "Recrutement Platform"
        }

        payload = {
            "model": model,
            "messages": [{"role": msg.role, "content": msg.content} for msg in request.messages],
            "temperature": request.temperature,
            "max_tokens": request.max_tokens
        }

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    OPENROUTER_API_URL,
                    headers=headers,
                    json=payload
                )
                response.raise_for_status()
                data = response.json()

                return {
                    "content": data["choices"][0]["message"]["content"],
                    "model": data["model"],
                    "usage": data.get("usage")
                }
        except httpx.HTTPStatusError as e:
            raise BaseError(
                f"Erreur OpenRouter: {e.response.text}",
                e.response.status_code
            )
        except Exception as e:
            raise BaseError(
                f"Erreur lors de la communication avec l'IA: {str(e)}",
                500
            )

    @staticmethod
    async def analyze_cv(cv_text: str, job_description: Optional[str] = None) -> dict:
        """
        Analyse un CV et le compare avec une description de poste
        """
        messages = [
            ChatMessage(
                role="system",
                content="Tu es un expert en recrutement. Analyse les CVs et fournis des insights pertinents."
            ),
            ChatMessage(
                role="user",
                content=f"Analyse ce CV:\n\n{cv_text}\n\n"
            )
        ]

        if job_description:
            messages[1].content += f"\n\nCompare-le avec cette description de poste:\n\n{job_description}"

        request = ChatRequest(messages=messages)
        return await OpenRouterService.chat(request)

    @staticmethod
    async def generate_job_description(
        title: str,
        company: str,
        requirements: List[str],
        skills: List[str]
    ) -> dict:
        """
        Génère une description de poste optimisée
        """
        messages = [
            ChatMessage(
                role="system",
                content="Tu es un expert en rédaction de descriptions de poste. Crée des descriptions claires et attractives."
            ),
            ChatMessage(
                role="user",
                content=f"Génère une description de poste pour:\n"
                       f"Titre: {title}\n"
                       f"Entreprise: {company}\n"
                       f"Exigences: {', '.join(requirements) if requirements else 'Aucune'}\n"
                       f"Compétences: {', '.join(skills) if skills else 'Aucune'}"
            )
        ]

        request = ChatRequest(messages=messages)
        return await OpenRouterService.chat(request)

