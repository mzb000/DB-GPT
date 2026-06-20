from app.services.llm_service import llm_generate


PYTHON_PROMPT = """You are a Python data analyst. Given a task and dataframe info, write Python code using pandas.

Rules:
- Use pandas (imported as pd)
- The dataframe is available as variable `df`
- Print/output the result
- Do NOT use any external files
- Return ONLY the Python code, no markdown

Task: {question}

DataFrame info:
{df_info}

Python code:"""


async def generate_python(user, question: str, df_info: str, provider: str = "gemini") -> str:
    prompt = PYTHON_PROMPT.format(question=question, df_info=df_info)
    code = await llm_generate(user, prompt, provider)
    code = code.strip().removeprefix("```python").removeprefix("```").removesuffix("```").strip()
    return code
