from typing import AsyncGenerator
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage


class GeminiProvider:
    def __init__(self, api_key: str, model: str = "gemini-2.0-flash"):
        self.llm = ChatGoogleGenerativeAI(model=model, google_api_key=api_key, temperature=0.1)

    async def generate(self, prompt: str) -> str:
        result = await self.llm.ainvoke([HumanMessage(content=prompt)])
        return result.content

    async def stream(self, prompt: str) -> AsyncGenerator[str, None]:
        async for chunk in self.llm.astream([HumanMessage(content=prompt)]):
            if chunk.content:
                yield chunk.content


class OllamaProvider:
    def __init__(self, base_url: str, model: str = "llama3.2"):
        self.llm = ChatOllama(base_url=base_url, model=model, temperature=0.1)

    async def generate(self, prompt: str) -> str:
        result = await self.llm.ainvoke([HumanMessage(content=prompt)])
        return result.content

    async def stream(self, prompt: str) -> AsyncGenerator[str, None]:
        async for chunk in self.llm.astream([HumanMessage(content=prompt)]):
            if chunk.content:
                yield chunk.content
