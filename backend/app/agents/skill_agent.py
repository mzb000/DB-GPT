from app.services.llm_service import llm_generate


async def execute_skill_prompt(user, skill_name: str, prompt_template: str, params: dict, provider: str = "gemini") -> str:
    filled = prompt_template
    for k, v in params.items():
        filled = filled.replace(f"{{{k}}}", str(v))
    return await llm_generate(user, filled, provider)
