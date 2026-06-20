import json
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.user import User
from app.models.datasource import Datasource
from app.api.deps import get_current_user
from app.schemas.datasource import DatasourceCreate, DatasourceUpdate, DatasourceResponse, TestConnectionRequest
from app.core.exceptions import NotFoundError, BadRequestError
from app.integrations.db_connectors import test_connection

router = APIRouter()


@router.get("/", response_model=list[DatasourceResponse])
async def list_datasources(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Datasource).where(Datasource.user_id == current_user.id).order_by(Datasource.created_at.desc()))
    return result.scalars().all()


@router.post("/", response_model=DatasourceResponse)
async def create_datasource(body: DatasourceCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    ds = Datasource(user_id=current_user.id, name=body.name, type=body.type, config=body.config, description=body.description)
    db.add(ds)
    await db.commit()
    await db.refresh(ds)
    return ds


@router.get("/{ds_id}", response_model=DatasourceResponse)
async def get_datasource(ds_id: str, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Datasource).where(Datasource.id == ds_id, Datasource.user_id == current_user.id))
    ds = result.scalar_one_or_none()
    if not ds:
        raise NotFoundError("Datasource not found")
    return ds


@router.put("/{ds_id}", response_model=DatasourceResponse)
async def update_datasource(ds_id: str, body: DatasourceUpdate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Datasource).where(Datasource.id == ds_id, Datasource.user_id == current_user.id))
    ds = result.scalar_one_or_none()
    if not ds:
        raise NotFoundError("Datasource not found")
    if body.name is not None:
        ds.name = body.name
    if body.config is not None:
        ds.config = body.config
    if body.description is not None:
        ds.description = body.description
    await db.commit()
    await db.refresh(ds)
    return ds


@router.delete("/{ds_id}")
async def delete_datasource(ds_id: str, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Datasource).where(Datasource.id == ds_id, Datasource.user_id == current_user.id))
    ds = result.scalar_one_or_none()
    if not ds:
        raise NotFoundError("Datasource not found")
    await db.delete(ds)
    await db.commit()
    return {"ok": True}


@router.post("/test-connection")
async def test_connection_endpoint(body: TestConnectionRequest):
    try:
        result = await test_connection(body.type, json.loads(body.config))
        return {"success": True, "message": result}
    except Exception as e:
        raise BadRequestError(str(e))
