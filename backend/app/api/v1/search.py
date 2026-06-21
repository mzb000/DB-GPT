from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_

from app.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.datasource import Datasource
from app.models.query import QueryRecord
from app.models.skill import Skill
from app.models.dashboard import Dashboard
from app.models.report import Report

router = APIRouter()


@router.get("/")
async def global_search(
    q: str = Query(..., min_length=1),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    term = f"%{q}%"
    results = []

    ds_query = await db.execute(
        select(Datasource)
        .where(Datasource.user_id == current_user.id)
        .where(or_(Datasource.name.ilike(term), Datasource.description.ilike(term)))
        .limit(5)
    )
    for ds in ds_query.scalars():
        results.append({"type": "datasource", "id": str(ds.id), "title": ds.name, "subtitle": ds.description or ""})

    q_query = await db.execute(
        select(QueryRecord)
        .where(QueryRecord.user_id == current_user.id)
        .where(QueryRecord.question.ilike(term))
        .limit(5)
    )
    for qr in q_query.scalars():
        results.append({"type": "query", "id": str(qr.id), "title": qr.question, "subtitle": qr.status})

    sk_query = await db.execute(
        select(Skill)
        .where(Skill.user_id == current_user.id)
        .where(or_(Skill.name.ilike(term), Skill.description.ilike(term)))
        .limit(5)
    )
    for sk in sk_query.scalars():
        results.append({"type": "skill", "id": str(sk.id), "title": sk.name, "subtitle": sk.description or ""})

    dash_query = await db.execute(
        select(Dashboard)
        .where(Dashboard.user_id == current_user.id)
        .where(or_(Dashboard.name.ilike(term), Dashboard.description.ilike(term)))
        .limit(5)
    )
    for d in dash_query.scalars():
        results.append({"type": "dashboard", "id": str(d.id), "title": d.name, "subtitle": d.description or ""})

    rp_query = await db.execute(
        select(Report)
        .where(Report.user_id == current_user.id)
        .where(or_(Report.title.ilike(term), Report.description.ilike(term)))
        .limit(5)
    )
    for r in rp_query.scalars():
        results.append({"type": "report", "id": str(r.id), "title": r.title, "subtitle": r.description or ""})

    return results
