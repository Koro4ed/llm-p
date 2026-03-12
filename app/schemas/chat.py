from pydantic import BaseModel
from typing import Optional


class ChatRequest(BaseModel):
    prompt: str
    system: Optional[str] = None
    max_history: int = 5
    temperature: float = 0.7


class ChatResponse(BaseModel):
    answer: str
