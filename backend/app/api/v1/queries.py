from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.user import User
from app.models.query import Query
from app.api.deps import get_current_user
from app.schemas.query import QueryRequest, QueryResponse
from app.core.exceptions import NotFoundError

router = APIRouter()


@router.get("/", response_model=list[QueryResponse])
async def list_queries(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Query).where(Query.user_id == current_user.id).order_by(Query.created_at.desc()).limit(50))
    return result.scalars().all()


@router.get("/{query_id}", response_model=QueryResponse)
async def get_query(query_id: str, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Query).where(Query.id == query_id, Query.user_id == current_user.id))
    q = result.scalar_one_or_none()
    if not q:
        raise NotFoundError("Query not found")
    return q


@router.post("/", response_model=QueryResponse)
async def execute_query(body: QueryRequest, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    from app.services.query_service import execute_sql_query
    query = await execute_sql_query(db, current_user.id, body.datasource_id, body.sql, body.question)
    return query
