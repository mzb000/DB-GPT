from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.database import get_db
from app.models.user import User
from app.models.datasource import Datasource
from app.models.query import Query
from app.models.skill import Skill
from app.models.dashboard import Dashboard
from app.models.report import Report
from app.api.deps import get_current_user

router = APIRouter()


@router.get("/stats")
async def get_stats(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    ds_count = (await db.execute(select(func.count()).select_from(Datasource).where(Datasource.user_id == current_user.id))).scalar() or 0
    q_count = (await db.execute(select(func.count()).select_from(Query).where(Query.user_id == current_user.id))).scalar() or 0
    sk_count = (await db.execute(select(func.count()).select_from(Skill).where(Skill.user_id == current_user.id))).scalar() or 0
    dash_count = (await db.execute(select(func.count()).select_from(Dashboard).where(Dashboard.user_id == current_user.id))).scalar() or 0
    rp_count = (await db.execute(select(func.count()).select_from(Report).where(Report.user_id == current_user.id))).scalar() or 0

    recent_queries = (await db.execute(
        select(Query)
        .where(Query.user_id == current_user.id)
        .order_by(Query.created_at.desc())
        .limit(5)
    )).scalars().all()

    activity = []
    for q in recent_queries:
        activity.append({
            "type": "query",
            "title": q.question[:60],
            "status": q.status,
            "created_at": q.created_at.isoformat() if q.created_at else "",
        })

    return {
        "datasources": ds_count,
        "queries": q_count,
        "skills": sk_count,
        "dashboards": dash_count,
        "reports": rp_count,
        "recent_activity": activity,
    }
