import asyncio
from fastapi import HTTPException
from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser

from core.config import settings
from core.schemas.llm import GenAltRequest


class LLMService:
    def __init__(self):
        self.llm = OllamaLLM(
            model=settings.llm.model,
            model_url=settings.llm.base_url,
            temperature=settings.llm.temperature,
        )
        self.output_parser = StrOutputParser()

    def create_prompt_template(self, target: str) -> PromptTemplate:
        if target == "title":
            template = """
            You are a creative content writer specializing in podcast titles.
            
            Original podcast information:
            - Title: {original_title}
            - Description: {description}
            - Host: {host}

            Task: {user_prompt}

            Create a new title that is:
            - Engaging and catchy
            - Relevant to the content
            - Appropriate for the requested style/audience
            - Short and concise (less than 20 words)
            - Clear and informative
            """
        else:  # description
            template = """
            You are a content writer specializing in podcast descriptions.

            Original podcast information:
            - Title: {title}
            - Description: {original_description}
            - Host: {host}

            Task: {user_prompt}

            Create a new description that is:
            - Clear and informative
            - Engaging for the target audience
            - Relevant to the podcast content
            - Appropriate for the requested style/audience
            - Short and concise (less than 50 words)
            - Clear and informative
            """

        prompt_template = PromptTemplate(
            template=template,
            input_variables=[
                "title",
                "description",
                "host",
                "user_prompt",
                "original_title",
                "original_description",
            ],
        )
        return prompt_template

    async def generate_alternatives(
        self,
        podcast: GenAltRequest,
        target: str,
        user_prompt: str,
    ) -> str:
        try:
            prompt_template = self.create_prompt_template(target)
            prompt_data = {
                "title": podcast.title,
                "description": podcast.description,
                "host": podcast.host,
                "user_prompt": user_prompt,
                "original_title": podcast.title,
                "original_description": podcast.description,
            }
            chain = prompt_template | self.llm | self.output_parser
            result = await asyncio.to_thread(chain.invoke, prompt_data)

            return result.strip().strip("'").strip('"')
        except Exception as e:
            raise HTTPException(
                status_code=400, detail=f"LLM generation failed: {str(e)}"
            )

    async def connect_check(self) -> bool:
        try:
            test_prompt = "Say 'OK' if you can hear me."
            result = await asyncio.to_thread(self.llm.invoke, test_prompt)
            return "OK" in result or "ok" in result.lower()
        except Exception:
            return False


llm_services = LLMService()
