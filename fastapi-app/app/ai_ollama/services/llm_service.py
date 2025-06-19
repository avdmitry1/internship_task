import asyncio
from fastapi import HTTPException
from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser

from core.config import settings
from core.schemas.llmSchema import Episode, GenAltRequest


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
                "user_prompt",
            ],
        )
        return prompt_template

    async def generate_alternatives(
        self,
        podcast: GenAltRequest,
        target: str,
        user_prompt: str,
        episode_data: Episode,
    ) -> str:
        try:
            prompt_template = self.create_prompt_template(target)
            prompt_data = {}

            # Prepare prompt data based on target type
            if target == "title":
                prompt_data = {
                    "original_title": episode_data.title,
                    "description": episode_data.description,
                    "user_prompt": user_prompt,
                }
            elif target == "description":
                prompt_data = {
                    "title": episode_data.title,
                    "original_description": episode_data.description,
                    "user_prompt": user_prompt,
                }
            else:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid target. Use 'title' or 'description'.",
                )

            # Execute prompt generation using the template and LLM
            chain = prompt_template | self.llm | self.output_parser
            result = await asyncio.to_thread(chain.invoke, prompt_data)

            # Return the stripped result
            return result.strip().strip("'").strip('"')

        except Exception as e:
            raise HTTPException(
                status_code=400, detail=f"LLM generation failed: {str(e)}"
            )

    async def connect_check(self) -> bool:
        print("Checking LLM connection...")
        try:
            test_prompt = "Can you generate a podcast title or description?"
            result = await asyncio.to_thread(self.llm.invoke, test_prompt)
            return result
        except Exception as e:
            print(f"LLM connect check failed: {e}")
            return False


llm_services = LLMService()
