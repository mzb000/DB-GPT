from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi.responses import HTMLResponse

from app.database import get_db
from app.models.user import User
from app.models.report import Report
from app.api.deps import get_current_user
from app.schemas.report import ReportCreate, ReportResponse
from app.core.exceptions import NotFoundError
from app.services.report_service import generate_html_report

router = APIRouter()


@router.get("/", response_model=list[ReportResponse])
async def list_reports(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Report).where(Report.user_id == current_user.id).order_by(Report.created_at.desc()))
    return result.scalars().all()


@router.post("/", response_model=ReportResponse)
async def create_report(body: ReportCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    report = await generate_html_report(db, current_user, body.title, body.description, body.query_ids)
    return report


@router.get("/{report_id}", response_model=ReportResponse)
async def get_report(report_id: str, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Report).where(Report.id == report_id, Report.user_id == current_user.id))
    report = result.scalar_one_or_none()
    if not report:
        raise NotFoundError("Report not found")
    return report


@router.get("/{report_id}/html")
async def view_report_html(report_id: str, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Report).where(Report.id == report_id, Report.user_id == current_user.id))
    report = result.scalar_one_or_none()
    if not report:
        raise NotFoundError("Report not found")
    return HTMLResponse(content=report.html_content)


@router.delete("/{report_id}")
async def delete_report(report_id: str, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Report).where(Report.id == report_id, Report.user_id == current_user.id))
    report = result.scalar_one_or_none()
    if not report:
        raise NotFoundError("Report not found")
    await db.delete(report)
    await db.commit()
    return {"ok": True}
