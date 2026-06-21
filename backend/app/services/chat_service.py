import json
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.models.query import Query
from app.schemas.chat import ChatRequest
from app.services.llm_service import llm_generate, llm_stream
from app.agents.planner_agent import plan_query
from app.agents.sql_agent import generate_sql
from app.agents.python_agent import generate_python
from app.agents.analysis_agent import analyze_results
from app.integrations.db_connectors import execute_sql
from app.services.datasource_service import get_datasource


async def process_chat_stream(db: AsyncSession, user: User, req: ChatRequest) -> AsyncGenerator[dict, None]:
    try:
        yield {"type": "status", "content": "Planning analysis..."}

        plan = await plan_query(user, req.message, req.model_provider)
        yield {"type": "plan", "content": plan}

        if req.datasource_id:
            ds = await get_datasource(db, req.datasource_id, user.id)
            config = json.loads(ds.config)

            yield {"type": "status", "content": "Generating SQL..."}
            sql = await generate_sql(user, req.message, ds.type, config, req.model_provider)
            yield {"type": "sql", "content": sql}

            yield {"type": "status", "content": "Executing query..."}
            df, columns, rows = await execute_sql(ds.type, config, sql)
            result_data = {"columns": columns, "rows": rows}
            yield {"type": "result", "content": json.dumps(result_data)}

            yield {"type": "status", "content": "Analyzing results..."}
            analysis = await analyze_results(user, req.message, sql, result_data, req.model_provider)
            yield {"type": "analysis", "content": analysis}

            query = Query(
                user_id=user.id,
                datasource_id=req.datasource_id,
                question=req.message,
                sql_generated=sql,
                result_json=json.dumps(result_data),
                summary=analysis,
                status="completed",
            )
            db.add(query)
            await db.commit()
        else:
            yield {"type": "status", "content": "Answering with AI..."}
            response = await llm_generate(user, req.message, req.model_provider)
            yield {"type": "analysis", "content": response}
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
            yield {"type": "error", "content": "Gemini API quota exceeded. Please wait a moment and try again, or check your API key billing."}
        elif "401" in error_msg or "UNAUTHENTICATED" in error_msg:
            yield {"type": "error", "content": "Invalid API key. Please check your Gemini API key in Settings."}
        else:
            yield {"type": "error", "content": f"Error: {error_msg}"}
