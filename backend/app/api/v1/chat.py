import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import StreamingResponse

from app.database import get_db
from app.models.user import User
from app.api.deps import get_current_user
from app.schemas.chat import ChatRequest
from app.services.chat_service import process_chat_stream

router = APIRouter()


@router.post("/stream")
async def chat_stream(body: ChatRequest, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    async def event_generator():
        async for chunk in process_chat_stream(db, current_user, body):
            yield f"data: {json.dumps(chunk)}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
