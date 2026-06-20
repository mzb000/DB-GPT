import json
import time
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.query import Query
from app.models.datasource import Datasource
from app.services.datasource_service import get_datasource
from app.integrations.db_connectors import execute_sql


async def execute_sql_query(db: AsyncSession, user_id: str, datasource_id: str, sql: str, question: str = "") -> Query:
    ds = await get_datasource(db, datasource_id, user_id)
    config = json.loads(ds.config)

    start = time.time()
    result_df, columns, rows = await execute_sql(ds.type, config, sql)
    elapsed = time.time() - start

    query = Query(
        user_id=user_id,
        datasource_id=datasource_id,
        question=question,
        sql_generated=sql,
        result_json=json.dumps({"columns": columns, "rows": rows}),
        execution_time=round(elapsed, 3),
        status="completed",
    )
    db.add(query)
    await db.commit()
    await db.refresh(query)
    return query
