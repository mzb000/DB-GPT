import json
from app.services.llm_service import llm_generate


SQL_PROMPT = """You are an expert SQL analyst. Given a question, datasource type, and schema, generate a safe SQL query.

Rules:
- Use only SELECT statements (read-only)
- Use standard SQL syntax compatible with {ds_type}
- Include column names, aggregations, GROUP BY, ORDER BY as needed
- Return ONLY the SQL query, no markdown, no explanation

Question: {question}

Datasource type: {ds_type}

Schema info:
{schema_info}

SQL:"""


async def generate_sql(user, question: str, ds_type: str, config: dict, provider: str = "gemini") -> str:
    from app.integrations.db_connectors import get_schema_info
    schema_info = await get_schema_info(ds_type, config)
    prompt = SQL_PROMPT.format(question=question, ds_type=ds_type, schema_info=schema_info)
    sql = await llm_generate(user, prompt, provider)
    sql = sql.strip().removeprefix("```sql").removeprefix("```").removesuffix("```").strip()
    return sql
