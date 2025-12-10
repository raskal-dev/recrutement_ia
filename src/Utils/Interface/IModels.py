from pydantic import BaseModel, Field
from typing import Optional, List


class ChatMessage(BaseModel):
    """Message dans une conversation avec l'IA"""
    role: str = Field(..., description="Rôle du message", example="user", enum=["user", "assistant", "system"])
    content: str = Field(..., description="Contenu du message", example="Bonjour, peux-tu m'aider ?")

    class Config:
        json_schema_extra = {
            "example": {
                "role": "user",
                "content": "Bonjour, peux-tu m'aider ?"
            }
        }


class ChatRequest(BaseModel):
    """Requête pour une conversation avec l'IA"""
    messages: List[ChatMessage] = Field(..., description="Liste des messages de la conversation")
    model: Optional[str] = Field(None, description="Modèle IA à utiliser (optionnel, utilise le modèle par défaut si non spécifié)", example="google/gemini-flash-1.5-8b:free")
    temperature: Optional[float] = Field(0.7, description="Température pour la génération (0.0 à 2.0)", ge=0.0, le=2.0)
    max_tokens: Optional[int] = Field(1000, description="Nombre maximum de tokens à générer", ge=1, le=4000)

    class Config:
        json_schema_extra = {
            "example": {
                "messages": [
                    {"role": "user", "content": "Bonjour, peux-tu m'aider ?"}
                ],
                "model": "google/gemini-flash-1.5-8b:free",
                "temperature": 0.7,
                "max_tokens": 1000
            }
        }


class ChatResponse(BaseModel):
    """Réponse de l'IA"""
    content: str = Field(..., description="Contenu de la réponse générée", example="Bonjour ! Je serais ravi de vous aider.")
    model: str = Field(..., description="Modèle utilisé pour générer la réponse", example="google/gemini-flash-1.5-8b:free")
    usage: Optional[dict] = Field(None, description="Informations sur l'utilisation des tokens")

    class Config:
        json_schema_extra = {
            "example": {
                "content": "Bonjour ! Je serais ravi de vous aider.",
                "model": "google/gemini-flash-1.5-8b:free",
                "usage": {
                    "prompt_tokens": 10,
                    "completion_tokens": 15,
                    "total_tokens": 25
                }
            }
        }


class AnalyzeCVRequest(BaseModel):
    """Requête pour l'analyse d'un CV"""
    cv_text: str = Field(..., description="Texte du CV à analyser", example="John Doe\nDéveloppeur Full Stack\n5 ans d'expérience en développement web...")
    job_description: Optional[str] = Field(None, description="Description de poste pour une analyse ciblée (optionnel)", example="Nous recherchons un développeur React expérimenté...")

    class Config:
        json_schema_extra = {
            "example": {
                "cv_text": "John Doe\nDéveloppeur Full Stack\n5 ans d'expérience...",
                "job_description": "Nous recherchons un développeur React expérimenté..."
            }
        }


class GenerateJobDescriptionRequest(BaseModel):
    """Requête pour générer une description de poste"""
    title: str = Field(..., description="Titre du poste", example="Développeur Full Stack")
    company: str = Field(..., description="Nom de l'entreprise", example="TechCorp")
    requirements: List[str] = Field(default_factory=list, description="Liste des exigences", example=["Bac+5", "3 ans d'expérience", "Anglais courant"])
    skills: List[str] = Field(default_factory=list, description="Liste des compétences requises", example=["React", "Node.js", "TypeScript", "Docker"])

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Développeur Full Stack",
                "company": "TechCorp",
                "requirements": ["Bac+5", "3 ans d'expérience", "Anglais courant"],
                "skills": ["React", "Node.js", "TypeScript", "Docker"]
            }
        }


class ExtractTextResponse(BaseModel):
    """Réponse pour l'extraction de texte depuis un fichier"""
    text: str = Field(..., description="Texte extrait du fichier", example="John Doe\nDéveloppeur Full Stack\n...")
    file_name: str = Field(..., description="Nom du fichier", example="cv.pdf")
    file_type: str = Field(..., description="Type de fichier", example="pdf")
    character_count: int = Field(..., description="Nombre de caractères extraits", example=1234)

    class Config:
        json_schema_extra = {
            "example": {
                "text": "John Doe\nDéveloppeur Full Stack\n5 ans d'expérience...",
                "file_name": "cv.pdf",
                "file_type": "pdf",
                "character_count": 1234
            }
        }

