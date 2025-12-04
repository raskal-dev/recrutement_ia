from pydantic import BaseModel
from typing import Optional, List


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    model: Optional[str] = None
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 1000


class ChatResponse(BaseModel):
    content: str
    model: str
    usage: Optional[dict] = None


class AnalyzeCVRequest(BaseModel):
    cv_text: str
    job_description: Optional[str] = None


class GenerateJobDescriptionRequest(BaseModel):
    title: str
    company: str
    requirements: List[str] = []
    skills: List[str] = []

