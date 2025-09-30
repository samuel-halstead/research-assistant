from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from app.core.config import settings
from app.schemas.research import ResearchResponseDocument
from app.schemas.translation import Translation


class TranslatorManager:
    def __init__(self):
        self.llm = ChatOpenAI(
            model=settings.OPENAI_CORRELATION_MODEL, api_key=settings.OPENAI_API_KEY, temperature=0
        ).with_structured_output(Translation)

    @staticmethod
    def _build_translation_prompt(doc: ResearchResponseDocument) -> str:
        prompt = f"Title: '{doc.title}'\nAbstract: {doc.abstract}\n\n"
        return prompt

    def translate_document(self, doc: ResearchResponseDocument, target_language: str) -> ResearchResponseDocument:
        # 1. Construir el prompt
        prompt_text = self._build_translation_prompt(doc)

        # 2. Definir el prompt template para LangChain
        system_content = (
            "You are a specialized AI assistant focused on document translation.\n"
            "You have received a document with a title and abstract. "
            "Your goal is to translate both the title and abstract to the specified target language.\n\n"
        )

        user_instructions = (
            "Instructions:\n"
            "1. Translate the title to the target language while preserving its meaning and academic tone.\n"
            "2. Translate the abstract to the target language while maintaining scientific accuracy and clarity.\n"
            "3. Keep the same structure and formatting as the original.\n"
            "4. Ensure the translation is natural and fluent in the target language.\n"
            f"5. Translate to {target_language} language.\n"
        )

        # 3. Crear el prompt template
        prompt_template = ChatPromptTemplate.from_messages(
            [("system", system_content), ("user", "{prompt_text}"), ("system", user_instructions)]
        )

        # 4. Ejecutar la cadena con structured output
        chain = prompt_template | self.llm
        response = chain.invoke({"prompt_text": prompt_text})

        # 5. Crear un nuevo documento con las traducciones
        translated_doc = ResearchResponseDocument(
            uuid=doc.uuid,
            title=response.translated_title,
            abstract=response.translated_abstract,
            authors=doc.authors,
            similarity=doc.similarity,
            language=doc.language,
        )

        return translated_doc
