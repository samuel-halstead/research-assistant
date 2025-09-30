from langchain_chroma import Chroma
from langchain_core.documents import Document as LangchainDocument
from langchain_openai import OpenAIEmbeddings

from app.core.config import settings
from app.schemas.documents import Document


class VectorStoreManager:
    def __init__(self, embeddings: OpenAIEmbeddings):
        self.vector_store = Chroma(
            collection_name=settings.COLLECTION_NAME,
            embedding_function=embeddings,
            persist_directory=settings.DATABASE_PATH,
        )

    def get_vector_store(self) -> Chroma:
        """
        Get the vector store instance.

        Returns:
            The Chroma vector store instance.
        """
        return self.vector_store

    def add_documents(self, documents: list[Document]):
        """
        Add documents to the vector store.

        Returns:
            None
        """
        langchain_documents = []
        for doc in documents:
            # Convert metadata to ChromaDB-compatible format
            metadata = doc.model_dump()
            langchain_documents.append(LangchainDocument(page_content=doc.abstract, metadata=metadata))

        uuids = [doc.uuid for doc in documents]
        self.vector_store.add_documents(langchain_documents, ids=uuids)

    def get_document_by_uuid(self, uuid: str) -> Document:
        """
        Get a document by its UUID.

        Returns:
            A Document instance with the specified UUID.
        """
        document = self.vector_store.get(ids=[uuid])
        metadata = document["metadatas"][0]
        return Document(**metadata)

    def get_documents(self, uuids: list[str] = None) -> list[Document]:
        """
        Get documents from the vector store.

        Returns:
            A list of Document instances.
        """
        if uuids is None:
            documents = self.vector_store.get()
            result = []
            for metadata in documents["metadatas"]:
                result.append(Document(**metadata))
            return result
        else:
            documents = self.vector_store.get(ids=uuids)
            result = []
            for metadata in documents["metadatas"]:
                result.append(Document(**metadata))
            return result

    def delete_documents(self, uuids: list[str]):
        """
        Delete documents from the vector store.

        Returns:
            None
        """
        self.vector_store.delete(ids=uuids)
