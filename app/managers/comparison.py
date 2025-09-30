from typing import List

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from app.core.config import settings
from app.schemas.comparison import Comparison
from app.schemas.research import ResearchResponseDocument


class ComparisonManager:
    def __init__(self):
        self.llm = ChatOpenAI(
            model=settings.OPENAI_CORRELATION_MODEL, api_key=settings.OPENAI_API_KEY, temperature=0
        ).with_structured_output(Comparison)

    @staticmethod
    def _build_summary_prompt(query_str: str, docs: List[ResearchResponseDocument]) -> str:
        """
        Build a prompt for document comparison analysis.

        Returns:
            A formatted prompt string for comparison analysis.
        """
        doc_descriptions = "\n".join(
            f"Index {index+1}: Title: '{doc.title}'\nAbstract: {doc.abstract}" for index, doc in enumerate(docs)
        )

        prompt = "User Query:\n" f'"{query_str}"\n\n' "Retrieved Documents:\n" f"{doc_descriptions}\n\n"
        return prompt

    def get_comparison(self, query_str: str, docs: List[ResearchResponseDocument], language: str) -> Comparison:
        """
        Get a comparison analysis between the query and retrieved documents.

        Returns:
            A Comparison instance with the analysis results.
        """
        # 1. Build the prompt
        prompt_text = self._build_summary_prompt(query_str, docs)

        # 2. Define the prompt template for LangChain
        system_content = (
            "You are a specialized AI assistant focused on research analysis and comparison.\n"
            "You have received a user query and a list of documents (with indexes starting at 1). "
            "Your goal is to compare the user query with the retrieved documents and provide a summary of the comparison.\n\n"
        )

        user_instructions = (
            "Instructions:\n"
            "1. You must provide similarities between the user query and the retrieved documents.\n"
            "2. You must provide differences between the user query and the retrieved documents.\n"
            "3. You must then provide a short summary with the similarities and differences.\n"
            "4. You must be concise and to the point.\n"
            f"5. You must respond in {language} language.\n"
        )

        # 3. Create the prompt template
        prompt_template = ChatPromptTemplate.from_messages(
            [("system", system_content), ("user", "{prompt_text}"), ("system", user_instructions)]
        )

        # 4. Execute the chain with structured output
        chain = prompt_template | self.llm
        response = chain.invoke({"prompt_text": prompt_text})

        return response.comparison
