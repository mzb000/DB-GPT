from pydantic import BaseModel
from typing import Any, Optional


class DatasourceCreate(BaseModel):
    name: str
    type: str
    config: str = "{}"
    description: str = ""


class DatasourceUpdate(BaseModel):
    name: Optional[str] = None
    config: Optional[str] = None
    description: Optional[str] = None


class DatasourceResponse(BaseModel):
    id: str
    user_id: str
    name: str
    type: str
    config: str
    description: str
    created_at: Any

    model_config = {"from_attributes": True}


class TestConnectionRequest(BaseModel):
    type: str
    config: str
