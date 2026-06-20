import asyncio
from sqlalchemy import select
from app.database import async_session
from app.models.user import User
from app.core.security import hash_password
from app.config import settings


async def seed_default_user():
    async with async_session() as session:
        result = await session.execute(select(User).where(User.email == "mzoraofficila@gmail.com"))
        if result.scalar_one_or_none() is None:
            user = User(
                email="mzoraofficila@gmail.com",
                hashed_password=hash_password("zabi12345"),
                full_name="Default Admin",
            )
            session.add(user)
            await session.commit()
