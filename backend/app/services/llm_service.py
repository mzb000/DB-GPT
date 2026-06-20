from typing import AsyncGenerator, Optional
from app.models.user import User
from app.config import settings


def get_llm(user: User, provider: str = "gemini"):
    api_key = user.gemini_api_key or settings.GEMINI_API_KEY
    if provider == "gemini" and api_key:
        from app.integrations.llm_providers import GeminiProvider
        return GeminiProvider(api_key=api_key)
    else:
        base_url = user.ollama_base_url or settings.OLLAMA_BASE_URL
        model = user.ollama_model or settings.OLLAMA_MODEL
        from app.integrations.llm_providers import OllamaProvider
        return OllamaProvider(base_url=base_url, model=model)


async def llm_generate(user: User, prompt: str, provider: str = "gemini") -> str:
    llm = get_llm(user, provider)
    return await llm.generate(prompt)


async def llm_stream(user: User, prompt: str, provider: str = "gemini") -> AsyncGenerator[str, None]:
    llm = get_llm(user, provider)
    async for chunk in llm.stream(prompt):
        yield chunk
