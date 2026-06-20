from pydantic import BaseModel
from typing import Any, Optional


class DashboardCreate(BaseModel):
    name: str
    description: str = ""
    layout: str = "[]"


class DashboardUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    layout: Optional[str] = None


class DashboardResponse(BaseModel):
    id: str
    user_id: str
    name: str
    description: str
    layout: str
    created_at: Any
    updated_at: Any

    model_config = {"from_attributes": True}


class WidgetCreate(BaseModel):
    title: str
    type: str
    config: str = "{}"
    position_x: int = 0
    position_y: int = 0
    width: int = 4
    height: int = 3


class WidgetResponse(BaseModel):
    id: str
    dashboard_id: str
    title: str
    type: str
    config: str
    position_x: int
    position_y: int
    width: int
    height: int

    model_config = {"from_attributes": True}
