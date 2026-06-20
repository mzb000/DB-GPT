import json
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.models.skill import Skill
from app.models.query import Query
from app.core.exceptions import NotFoundError
from app.services.llm_service import llm_generate
from app.integrations.db_connectors import execute_sql
from app.services.datasource_service import get_datasource


async def execute_skill(db: AsyncSession, user: User, skill_id: str, datasource_id: str, parameter_values: str) -> dict:
    result = await db.execute(select(Skill).where(Skill.id == skill_id))
    skill = result.scalar_one_or_none()
    if not skill:
        raise NotFoundError("Skill not found")

    ds = await get_datasource(db, datasource_id, user.id)
    config = json.loads(ds.config)
    params = json.loads(parameter_values)

    prompt = skill.prompt_template
    for k, v in params.items():
        prompt = prompt.replace(f"{{{k}}}", str(v))

    sql = await llm_generate(user, prompt, "gemini")
    sql_clean = sql.strip().removeprefix("```sql").removesuffix("```").strip()

    df, columns, rows = await execute_sql(ds.type, config, sql_clean)

    query = Query(
        user_id=user.id,
        datasource_id=datasource_id,
        question=f"Skill: {skill.name}",
        sql_generated=sql_clean,
        result_json=json.dumps({"columns": columns, "rows": rows}),
        status="completed",
    )
    db.add(query)
    await db.commit()
    await db.refresh(query)

    return {"query_id": query.id, "columns": columns, "rows": rows, "sql": sql_clean}
