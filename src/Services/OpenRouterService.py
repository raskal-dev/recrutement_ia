import httpx
import os
import logging
from typing import List, Optional
from src.Configs.OpenRouter_config import OPENROUTER_API_KEY, OPENROUTER_API_URL, FREE_MODELS, APP_URL
from src.Configs.AI_config import PROTECTIVE_SYSTEM_PROMPT
from src.Utils.BaseError import BaseError
from src.Utils.Interface.IModels import ChatRequest, ChatMessage
from src.Services.OpenAIService import OpenAIService


class OpenRouterService:
    @staticmethod
    async def chat(request: ChatRequest) -> dict:
        """
        Tente OpenAI (si clé dispo), sinon fallback OpenRouter
        """
        openai_key = os.getenv("OPENAI_API_KEY")

        # Injection du prompt de protection s'il n'est pas déjà présent
        has_system_prompt = any(msg.role == "system" for msg in request.messages)
        if not has_system_prompt:
            request.messages.insert(0, ChatMessage(role="system", content=PROTECTIVE_SYSTEM_PROMPT))
        else:
            # On renforce le prompt système existant
            for msg in request.messages:
                if msg.role == "system":
                    msg.content = f"{PROTECTIVE_SYSTEM_PROMPT}\n\nContexte additionnel : {msg.content}"

        # 1) Tentative OpenAI si clé présente
        if openai_key:
            try:
                return await OpenAIService.chat(request)
            except BaseError as e:
                logging.warning(f"OpenAI indisponible ({e.message}), fallback OpenRouter")
            except Exception as e:
                logging.warning(f"OpenAI erreur inattendue ({e}), fallback OpenRouter")

        # 2) Fallback OpenRouter
        if not OPENROUTER_API_KEY:
            raise BaseError("OPENROUTER_API_KEY n'est pas configurée", 500)

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
        system_content = (
            f"{PROTECTIVE_SYSTEM_PROMPT}\n\n"
            "Tu es un expert en recrutement. Analyse les CVs de manière professionnelle et objective."
        )
        
        messages = [
            ChatMessage(role="system", content=system_content),
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
        system_content = (
            f"{PROTECTIVE_SYSTEM_PROMPT}\n\n"
            "Tu es un expert en rédaction de descriptions de poste. Crée des descriptions claires et attractives."
        )
        
        messages = [
            ChatMessage(role="system", content=system_content),
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

