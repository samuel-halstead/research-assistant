from langchain_openai import OpenAIEmbeddings

from app.core.config import settings


class EmbeddingManager:
    def __init__(self):
        self.embedding_model = OpenAIEmbeddings(api_key=settings.OPENAI_API_KEY, model=settings.EMBED_MODEL_NAME)

    def get_embedding_model(self) -> list[float]:
        """
        Get the embedding model instance.

        Returns:
            The OpenAIEmbeddings model instance.
        """
        return self.embedding_model
