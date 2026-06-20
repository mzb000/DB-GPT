from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.database import get_db
from app.models.user import User
from app.api.deps import get_current_user

router = APIRouter()


class SettingsUpdate(BaseModel):
    gemini_api_key: str = ""
    ollama_base_url: str = ""
    ollama_model: str = ""


class SettingsResponse(BaseModel):
    gemini_api_key: str
    ollama_base_url: str
    ollama_model: str


@router.get("/", response_model=SettingsResponse)
async def get_settings(current_user: User = Depends(get_current_user)):
    return SettingsResponse(
        gemini_api_key="••••" + current_user.gemini_api_key[-4:] if current_user.gemini_api_key else "",
        ollama_base_url=current_user.ollama_base_url,
        ollama_model=current_user.ollama_model,
    )


@router.put("/", response_model=SettingsResponse)
async def update_settings(body: SettingsUpdate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if body.gemini_api_key:
        current_user.gemini_api_key = body.gemini_api_key
    if body.ollama_base_url:
        current_user.ollama_base_url = body.ollama_base_url
    if body.ollama_model:
        current_user.ollama_model = body.ollama_model
    await db.commit()
    await db.refresh(current_user)
    return SettingsResponse(
        gemini_api_key="••••" + current_user.gemini_api_key[-4:] if current_user.gemini_api_key else "",
        ollama_base_url=current_user.ollama_base_url,
        ollama_model=current_user.ollama_model,
    )
