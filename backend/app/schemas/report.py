from pydantic import BaseModel
from typing import Any, Optional


class ReportCreate(BaseModel):
    title: str
    description: str = ""
    query_ids: str = "[]"


class ReportResponse(BaseModel):
    id: str
    user_id: str
    title: str
    description: str
    html_content: str
    query_ids: str
    share_token: str
    created_at: Any
    updated_at: Any

    model_config = {"from_attributes": True}
