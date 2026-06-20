from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.dashboard import Dashboard, DashboardWidget
from app.core.exceptions import NotFoundError


async def get_dashboard_with_widgets(db: AsyncSession, dash_id: str, user_id: str) -> dict:
    result = await db.execute(select(Dashboard).where(Dashboard.id == dash_id, Dashboard.user_id == user_id))
    dash = result.scalar_one_or_none()
    if not dash:
        raise NotFoundError("Dashboard not found")

    widget_result = await db.execute(select(DashboardWidget).where(DashboardWidget.dashboard_id == dash_id))
    widgets = widget_result.scalars().all()

    return {
        "id": dash.id,
        "name": dash.name,
        "description": dash.description,
        "layout": dash.layout,
        "widgets": [
            {
                "id": w.id,
                "title": w.title,
                "type": w.type,
                "config": w.config,
                "position_x": w.position_x,
                "position_y": w.position_y,
                "width": w.width,
                "height": w.height,
            }
            for w in widgets
        ],
    }
