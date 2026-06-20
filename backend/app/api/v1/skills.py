from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.user import User
from app.models.skill import Skill
from app.api.deps import get_current_user
from app.schemas.skill import SkillCreate, SkillUpdate, SkillResponse, SkillExecuteRequest
from app.core.exceptions import NotFoundError
from app.services.skill_service import execute_skill

router = APIRouter()


@router.get("/", response_model=list[SkillResponse])
async def list_skills(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Skill).where((Skill.user_id == current_user.id) | (Skill.is_public == True)).order_by(Skill.created_at.desc())
    )
    return result.scalars().all()


@router.post("/", response_model=SkillResponse)
async def create_skill(body: SkillCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    skill = Skill(
        user_id=current_user.id, name=body.name, description=body.description,
        prompt_template=body.prompt_template, parameters=body.parameters, category=body.category,
    )
    db.add(skill)
    await db.commit()
    await db.refresh(skill)
    return skill


@router.get("/{skill_id}", response_model=SkillResponse)
async def get_skill(skill_id: str, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Skill).where(Skill.id == skill_id))
    skill = result.scalar_one_or_none()
    if not skill:
        raise NotFoundError("Skill not found")
    return skill


@router.put("/{skill_id}", response_model=SkillResponse)
async def update_skill(skill_id: str, body: SkillUpdate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Skill).where(Skill.id == skill_id, Skill.user_id == current_user.id))
    skill = result.scalar_one_or_none()
    if not skill:
        raise NotFoundError("Skill not found")
    if body.name is not None:
        skill.name = body.name
    if body.description is not None:
        skill.description = body.description
    if body.prompt_template is not None:
        skill.prompt_template = body.prompt_template
    if body.parameters is not None:
        skill.parameters = body.parameters
    if body.category is not None:
        skill.category = body.category
    await db.commit()
    await db.refresh(skill)
    return skill


@router.delete("/{skill_id}")
async def delete_skill(skill_id: str, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Skill).where(Skill.id == skill_id, Skill.user_id == current_user.id))
    skill = result.scalar_one_or_none()
    if not skill:
        raise NotFoundError("Skill not found")
    await db.delete(skill)
    await db.commit()
    return {"ok": True}


@router.post("/{skill_id}/execute")
async def run_skill(skill_id: str, body: SkillExecuteRequest, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await execute_skill(db, current_user, skill_id, body.datasource_id, body.parameter_values)
    return result
