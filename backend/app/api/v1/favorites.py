from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.database import get_db
from app.models.user import User
from app.models.favorite import Favorite
from app.api.deps import get_current_user

router = APIRouter()


@router.get("/")
async def list_favorites(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Favorite).where(Favorite.user_id == current_user.id))
    favs = result.scalars().all()
    return [{"id": f.id, "entity_type": f.entity_type, "entity_id": f.entity_id} for f in favs]


@router.post("/")
async def toggle_favorite(
    body: dict,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    entity_type = body.get("entity_type", "")
    entity_id = body.get("entity_id", "")

    result = await db.execute(
        select(Favorite).where(
            and_(
                Favorite.user_id == current_user.id,
                Favorite.entity_type == entity_type,
                Favorite.entity_id == entity_id,
            )
        )
    )
    existing = result.scalar_one_or_none()

    if existing:
        await db.delete(existing)
        await db.commit()
        return {"favorited": False}
    else:
        fav = Favorite(user_id=current_user.id, entity_type=entity_type, entity_id=entity_id)
        db.add(fav)
        await db.commit()
        return {"favorited": True}
