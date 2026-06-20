import json
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.datasource import Datasource
from app.core.exceptions import NotFoundError
from app.integrations.db_connectors import test_connection


async def get_datasource(db: AsyncSession, ds_id: str, user_id: str) -> Datasource:
    result = await db.execute(select(Datasource).where(Datasource.id == ds_id, Datasource.user_id == user_id))
    ds = result.scalar_one_or_none()
    if not ds:
        raise NotFoundError("Datasource not found")
    return ds


async def test_datasource_connection(ds_type: str, config: dict) -> str:
    return await test_connection(ds_type, config)
