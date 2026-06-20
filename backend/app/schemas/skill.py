from pydantic import BaseModel
from typing import Any, Optional


class SkillCreate(BaseModel):
    name: str
    description: str = ""
    prompt_template: str
    parameters: str = "[]"
    category: str = "general"


class SkillUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    prompt_template: Optional[str] = None
    parameters: Optional[str] = None
    category: Optional[str] = None


class SkillResponse(BaseModel):
    id: str
    user_id: str
    name: str
    description: str
    prompt_template: str
    parameters: str
    is_public: bool
    category: str
    created_at: Any
    updated_at: Any

    model_config = {"from_attributes": True}


class SkillExecuteRequest(BaseModel):
    datasource_id: str
    parameter_values: str = "{}"
