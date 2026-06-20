"""Seed default data into DB-GPT."""
import asyncio
from app.database import async_session, init_db
from app.models.user import User
from app.core.security import hash_password
from app.models.skill import Skill
from sqlalchemy import select


async def seed():
    await init_db()
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
            await session.refresh(user)
            print("Default user created: mzoraofficila@gmail.com / zabi12345")
        else:
            user = result.scalar_one()
            print("Default user already exists")

        skills = [
            Skill(
                user_id=user.id,
                name="Monthly Sales Report",
                description="Generate a monthly sales summary by region",
                category="sales",
                prompt_template="Show me total sales by region for {month}. Include the number of orders and average order value.",
                parameters='[{"name": "month", "type": "string", "description": "Month to analyze (e.g., January 2024)"}]',
                is_public=True,
            ),
            Skill(
                user_id=user.id,
                name="Customer Segmentation",
                description="Segment customers by total spending",
                category="marketing",
                prompt_template="Segment customers into tiers (High, Medium, Low) based on total spending. Show count and average spending per tier.",
                parameters='[]',
                is_public=True,
            ),
            Skill(
                user_id=user.id,
                name="Inventory Status",
                description="Check inventory levels and identify low stock items",
                category="operations",
                prompt_template="Show all products with stock levels below {threshold}. Include product name, current stock, and reorder level.",
                parameters='[{"name": "threshold", "type": "number", "description": "Stock threshold"}]',
                is_public=True,
            ),
            Skill(
                user_id=user.id,
                name="Year-over-Year Comparison",
                description="Compare metrics across years",
                category="finance",
                prompt_template="Compare {metric} by {dimension} for {year_1} vs {year_2}. Show the absolute change and percentage change.",
                parameters='[{"name": "metric", "type": "string"}, {"name": "dimension", "type": "string"}, {"name": "year_1", "type": "string"}, {"name": "year_2", "type": "string"}]',
                is_public=True,
            ),
        ]

        for skill in skills:
            existing = await session.execute(
                select(Skill).where(Skill.name == skill.name, Skill.user_id == user.id)
            )
            if existing.scalar_one_or_none() is None:
                session.add(skill)

        await session.commit()
        print("Seed skills created")


if __name__ == "__main__":
    asyncio.run(seed())
    print("Seeding complete!")
