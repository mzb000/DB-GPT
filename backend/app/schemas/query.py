from pydantic import BaseModel
from typing import Any, Optional


class QueryRequest(BaseModel):
    datasource_id: str
    sql: str
    question: str = ""


class QueryResponse(BaseModel):
    id: str
    user_id: str
    datasource_id: Optional[str]
    question: str
    sql_generated: str
    python_generated: str
    result_json: str
    chart_config: str
    summary: str
    execution_time: float
    status: str
    created_at: Any

    model_config = {"from_attributes": True}
