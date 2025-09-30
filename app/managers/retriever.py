from typing import List

from langchain_core.documents import Document as LangchainDocument
from langchain_core.retrievers import BaseRetriever
from langchain_core.vectorstores import VectorStore
from pydantic import Field

from app.schemas.research import ResearchResponseDocument


class VectorDBRetriever(BaseRetriever):
    vector_store: VectorStore = Field(description="Vector store instance")
    k: int = Field(default=5, description="Number of documents to retrieve")

    def __init__(self, vector_store: VectorStore, k: int = 5, **kwargs) -> None:
        super().__init__(vector_store=vector_store, k=k, **kwargs)

    def _get_relevant_documents(self, query: str) -> List[LangchainDocument]:
        """
        Retrieve relevant documents from the vector store.

        Returns:
            A list of LangchainDocument instances matching the query.
        """
        return self.vector_store.similarity_search(query, k=self.k)

    def _get_relevant_documents_with_score(self, query: str) -> List[tuple[LangchainDocument, float]]:
        """
        Retrieve relevant documents with similarity scores from the vector store.

        Returns:
            A list of tuples containing LangchainDocument instances and their similarity scores.
        """
        return self.vector_store.similarity_search_with_score(query, k=self.k)

    def retrieve_nodes(self, query: str) -> List[ResearchResponseDocument]:
        """
        Retrieve relevant documents and convert them to ResearchResponseDocument format.

        Returns:
            A list of ResearchResponseDocument instances with similarity scores.
        """
        # Get documents with scores
        docs_with_scores = self._get_relevant_documents_with_score(query)

        # Convert to NodeWithScore format for compatibility
        nodes_with_scores = []
        for doc, score in docs_with_scores:
            # Convert similarity score to distance score (lower is better)
            # LangChain returns similarity scores, we need to convert to distance
            distance_score = 1.0 - score if score <= 1.0 else 1.0 / (1.0 + score)
            nodes_with_scores.append(ResearchResponseDocument(**doc.metadata, similarity=distance_score))

        return nodes_with_scores
