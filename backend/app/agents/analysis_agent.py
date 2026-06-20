from app.services.llm_service import llm_generate


ANALYSIS_PROMPT = """You are a data analyst. Given the question, SQL, and results, write a clear summary.

Question: {question}
SQL: {sql}

Results (first 10 rows):
{results}

Write a concise 2-3 sentence analysis highlighting key findings, trends, and insights."""


async def analyze_results(user, question: str, sql: str, result_data: dict, provider: str = "gemini") -> str:
    rows = result_data.get("rows", [])
    cols = result_data.get("columns", [])
    import json
    result_preview = json.dumps({"columns": cols, "rows": rows[:10]}, indent=2)
    prompt = ANALYSIS_PROMPT.format(question=question, sql=sql, results=result_preview)
    return await llm_generate(user, prompt, provider)
