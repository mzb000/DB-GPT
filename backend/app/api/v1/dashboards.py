from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.user import User
from app.models.dashboard import Dashboard, DashboardWidget
from app.api.deps import get_current_user
from app.schemas.dashboard import DashboardCreate, DashboardUpdate, DashboardResponse, WidgetCreate, WidgetResponse
from app.core.exceptions import NotFoundError

router = APIRouter()


@router.get("/", response_model=list[DashboardResponse])
async def list_dashboards(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Dashboard).where(Dashboard.user_id == current_user.id).order_by(Dashboard.created_at.desc()))
    return result.scalars().all()


@router.post("/", response_model=DashboardResponse)
async def create_dashboard(body: DashboardCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    db_dash = Dashboard(user_id=current_user.id, name=body.name, description=body.description, layout=body.layout)
    db.add(db_dash)
    await db.commit()
    await db.refresh(db_dash)
    return db_dash


@router.get("/{dash_id}", response_model=DashboardResponse)
async def get_dashboard(dash_id: str, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Dashboard).where(Dashboard.id == dash_id, Dashboard.user_id == current_user.id))
    dash = result.scalar_one_or_none()
    if not dash:
        raise NotFoundError("Dashboard not found")
    return dash


@router.put("/{dash_id}", response_model=DashboardResponse)
async def update_dashboard(dash_id: str, body: DashboardUpdate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Dashboard).where(Dashboard.id == dash_id, Dashboard.user_id == current_user.id))
    dash = result.scalar_one_or_none()
    if not dash:
        raise NotFoundError("Dashboard not found")
    if body.name is not None:
        dash.name = body.name
    if body.description is not None:
        dash.description = body.description
    if body.layout is not None:
        dash.layout = body.layout
    await db.commit()
    await db.refresh(dash)
    return dash


@router.delete("/{dash_id}")
async def delete_dashboard(dash_id: str, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Dashboard).where(Dashboard.id == dash_id, Dashboard.user_id == current_user.id))
    dash = result.scalar_one_or_none()
    if not dash:
        raise NotFoundError("Dashboard not found")
    await db.delete(dash)
    await db.commit()
    return {"ok": True}


@router.get("/{dash_id}/widgets", response_model=list[WidgetResponse])
async def list_widgets(dash_id: str, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(DashboardWidget).where(DashboardWidget.dashboard_id == dash_id))
    return result.scalars().all()


@router.post("/{dash_id}/widgets", response_model=WidgetResponse)
async def create_widget(dash_id: str, body: WidgetCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    widget = DashboardWidget(
        dashboard_id=dash_id, title=body.title, type=body.type, config=body.config,
        position_x=body.position_x, position_y=body.position_y, width=body.width, height=body.height,
    )
    db.add(widget)
    await db.commit()
    await db.refresh(widget)
    return widget


@router.delete("/{dash_id}/widgets/{widget_id}")
async def delete_widget(dash_id: str, widget_id: str, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(DashboardWidget).where(DashboardWidget.id == widget_id, DashboardWidget.dashboard_id == dash_id))
    widget = result.scalar_one_or_none()
    if not widget:
        raise NotFoundError("Widget not found")
    await db.delete(widget)
    await db.commit()
    return {"ok": True}
