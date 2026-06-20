from pydantic import BaseModel
from typing import Optional


class ChatRequest(BaseModel):
    message: str
    datasource_id: Optional[str] = None
    model_provider: str = "ollama"
    stream: bool = True


class ChatResponse(BaseModel):
    type: str
    content: str
    metadata: str = "{}"
