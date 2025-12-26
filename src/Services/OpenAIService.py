import os
from typing import List, Optional
from openai import AsyncOpenAI
from src.Utils.Interface.IModels import ChatMessage, ChatRequest
from src.Utils.BaseError import BaseError
from src.Configs.AI_config import PROTECTIVE_SYSTEM_PROMPT


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


class OpenAIService:
    @staticmethod
    def _get_client():
        if not OPENAI_API_KEY:
            raise BaseError("OPENAI_API_KEY manquant", 503)
        return AsyncOpenAI(api_key=OPENAI_API_KEY)

    @staticmethod
    async def chat(request: ChatRequest) -> dict:
        """
        Envoie une requête de chat à OpenAI avec protection du domaine.
        """
        # Injection du prompt de protection s'il n'est pas déjà présent
        has_system_prompt = any(msg.role == "system" for msg in request.messages)
        if not has_system_prompt:
            request.messages.insert(0, ChatMessage(role="system", content=PROTECTIVE_SYSTEM_PROMPT))
        else:
            # On renforce le prompt système existant
            for msg in request.messages:
                if msg.role == "system":
                    if PROTECTIVE_SYSTEM_PROMPT not in msg.content:
                        msg.content = f"{PROTECTIVE_SYSTEM_PROMPT}\n\nContexte additionnel : {msg.content}"

        client = OpenAIService._get_client()
        try:
            completion = await client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[{"role": m.role, "content": m.content} for m in request.messages],
                temperature=request.temperature or 0.7,
                max_tokens=request.max_tokens or 1000,
            )
            content = completion.choices[0].message.content
            return {
                "content": content,
                "model": OPENAI_MODEL,
                "usage": completion.usage.dict() if hasattr(completion, "usage") else None,
            }
        except Exception as e:
            raise BaseError(str(e), 503)

    @staticmethod
    async def simple_chat(messages: List[ChatMessage], temperature: float = 0.7, max_tokens: int = 1000) -> dict:
        req = ChatRequest(messages=messages, temperature=temperature, max_tokens=max_tokens)
        return await OpenAIService.chat(req)


