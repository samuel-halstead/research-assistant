from typing import List

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from app.core.config import settings
from app.schemas.correlation import Correlation
from app.schemas.research import ResearchResponseDocument


class CorrelationFilterManager:
    def __init__(self):
        self.llm = ChatOpenAI(
            model=settings.OPENAI_CORRELATION_MODEL, api_key=settings.OPENAI_API_KEY, temperature=0
        ).with_structured_output(Correlation)

    @staticmethod
    def _build_correlation_prompt(query_str: str, retrieved_docs: List[ResearchResponseDocument]) -> str:
        doc_descriptions = "\n".join(
            f"Index {index+1}: Title: '{doc.title}'\nAbstract: {doc.abstract}"
            for index, doc in enumerate(retrieved_docs)
        )

        prompt = "User Query:\n" f'"{query_str}"\n\n' "Retrieved Documents:\n" f"{doc_descriptions}\n\n"
        return prompt

    def check_correlation(
        self, query_str: str, retrieved_docs: List[ResearchResponseDocument]
    ) -> List[ResearchResponseDocument]:
        # 1. Construir el prompt
        prompt_text = self._build_correlation_prompt(query_str, retrieved_docs)

        # 2. Definir el prompt template para LangChain
        system_content = (
            "You are a specialized AI assistant focused on research analysis and comparison.\n"
            "You have received a user query and a list of documents (with indexes starting at 1). "
            "Your goal is to identify documents that are irrelevant to the user query.\n\n"
            "Guidelines:\n"
            "1. The 'indexes' field must be a list of integers (each integer corresponds to the 1-based index of an irrelevant document).\n"
            '2. If all documents are relevant to the query, return "indexes" as an empty list.\n'
            "3. Only include documents that are clearly irrelevant or off-topic.\n"
            "4. Analyze the user query and documents carefully, then produce your response.\n"
        )

        user_instructions = (
            "Instructions:\n"
            "1. Return only the indexes of documents that are irrelevant to the user query.\n"
            "2. Use 1-based indexing (first document is index 1, second is index 2, etc.).\n"
            "3. If all documents are relevant, return an empty list.\n"
            "4. Be conservative - only mark documents as irrelevant if they are clearly off-topic.\n"
        )

        # 3. Crear el prompt template
        prompt_template = ChatPromptTemplate.from_messages(
            [("system", system_content), ("user", "{prompt_text}"), ("system", user_instructions)]
        )

        # 4. Ejecutar la cadena con structured output
        chain = prompt_template | self.llm
        response = chain.invoke({"prompt_text": prompt_text})

        # 5. Procesar la respuesta
        filter_indexes = response.indexes
        # Convertir de 1-based a 0-based indexing y filtrar índices válidos
        filter_indexes = [index - 1 for index in filter_indexes if 1 <= index <= len(retrieved_docs)]

        # 6. Retornar documentos que no están en la lista de filtros
        return [doc for index, doc in enumerate(retrieved_docs) if index not in filter_indexes]
