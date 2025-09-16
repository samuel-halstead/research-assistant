from typing import List

from openai import OpenAI

from app.core.config import settings
from app.schemas.correlation import Correlation
from app.schemas.doc_list import DocListResponse


class CorrelationFilterManager:
    def __init__(self):
        self.llm_client = OpenAI(api_key=settings.OPENAI_API_KEY)

    @staticmethod
    def build_correlation_prompt(query_str: str, retrieved_docs: List[DocListResponse]) -> str:
        doc_descriptions = "\n".join(
            f"Index {index+1}: Title: '{doc.title}'\nAbstract: {doc.abstract}"
            for index, doc in enumerate(retrieved_docs)
        )

        prompt = "User Query:\n" f'"{query_str}"\n\n' "Retrieved Documents:\n" f"{doc_descriptions}\n\n"
        return prompt

    def run_correlation_filter(self, query_str: str, retrieved_docs: List[DocListResponse]) -> List[DocListResponse]:
        # 1. Construir el prompt
        prompt_text = self.build_correlation_prompt(query_str, retrieved_docs)

        # 2. Definir un "Collection schema" en el mensaje del sistema, basado en la clase 'Correlation'
        #    Explicamos que el JSON devuelto debe contener solo un campo: "indexes": list[int].
        system_content = (
            "You are a specialized AI assistant focused on research analysis and comparison.\n"
            "You have received a user query and a list of documents (with indexes starting at 1). "
            "Your goal is to return a valid JSON object **strictly** following this schema:\n\n"
            "```\n"
            "{\n"
            '  "indexes": [int, int, ...]\n'
            "}\n"
            "```\n\n"
            "Guidelines:\n"
            "1. The 'indexes' field must be a list of integers (each integer corresponds to the 1-based index of a matching document).\n"
            '2. If all documents are relevant to the query, return "indexes" as an empty list, e.g., `{"indexes": []}`.\n'
            "3. Do NOT provide any additional fields or text. No explanation, no summary—just valid JSON.\n"
            "4. The user query and documents are below. Analyze them carefully, then produce your JSON answer.\n"
        )

        # 3. Definir instrucciones finales
        user_instructions = (
            "Instructions:\n"
            "1. Return only the JSON with the 'indexes' field.\n"
            "2. Do not output any extra text or keys outside this schema.\n"
            "3. Indicate documents irrelevant to the user_query by their 1-based index, if any.\n"
            '4. If all documents are relevant, return an empty list: {"indexes": []}.\n'
        )

        # 4. Llamar a la API, usando la función parse con el modelo pydantic 'Correlation'
        response = self.llm_client.beta.chat.completions.parse(
            model=settings.OPENAI_CORRELATION_MODEL,
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": prompt_text},
                {"role": "system", "content": user_instructions},
            ],
            response_format=Correlation,
        )

        filter_indexes = response.choices[0].message.parsed.indexes
        filter_indexes = [index - 1 for index in filter_indexes if index - 1 > 0]

        return [doc for index, doc in enumerate(retrieved_docs) if index not in filter_indexes]
