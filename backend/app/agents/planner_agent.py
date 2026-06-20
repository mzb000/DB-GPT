from app.services.llm_service import llm_generate


PLANNER_PROMPT = """You are a data analysis planner. Given a user's question, break it down into clear steps.
List the tables/columns needed, the analysis steps, and the output format.

User question: {question}

Return a concise step-by-step plan."""


async def plan_query(user, question: str, provider: str = "gemini") -> str:
    prompt = PLANNER_PROMPT.format(question=question)
    return await llm_generate(user, prompt, provider)
