"""
Módulo: retriever.py

Módulo que implementa una clase para la recuperación de documentos relevantes a partir de
un almacén vectorial, utilizando un modelo de incrustaciones para consultas.
Proporciona funcionalidad para integrar recuperación basada en similitud con LangChain.
"""

from typing import List

from langchain_core.documents import Document as LangchainDocument
from langchain_core.retrievers import BaseRetriever
from langchain_core.vectorstores import VectorStore
from pydantic import Field

from app.schemas.research import ResearchResponseDocument


class VectorDBRetriever(BaseRetriever):
    """
    Recuperador de documentos basado en un almacén vectorial usando LangChain.

    Esta clase utiliza un almacén vectorial de LangChain para realizar búsquedas
    de similitud y devuelve documentos relevantes con sus puntuaciones.

    Parámetros:
    -----------
    vector_store : VectorStore
        Instancia del almacén vectorial de LangChain donde se encuentran los datos.
    k : int, opcional
        Número máximo de documentos devueltos por la consulta (por defecto, 5).
    """

    vector_store: VectorStore = Field(description="Vector store instance")
    k: int = Field(default=5, description="Number of documents to retrieve")

    def __init__(self, vector_store: VectorStore, k: int = 5, **kwargs) -> None:
        super().__init__(vector_store=vector_store, k=k, **kwargs)

    def _get_relevant_documents(self, query: str) -> List[LangchainDocument]:
        """
        Recupera documentos relevantes basados en una consulta.

        Parámetros:
        -----------
        query : str
            La cadena de consulta.

        Devuelve:
        --------
        List[LangchainDocument]
            Una lista de documentos relevantes.
        """
        return self.vector_store.similarity_search(query, k=self.k)

    def _get_relevant_documents_with_score(self, query: str) -> List[tuple[LangchainDocument, float]]:
        """
        Recupera documentos relevantes con sus puntuaciones de similitud.

        Parámetros:
        -----------
        query : str
            La cadena de consulta.

        Devuelve:
        --------
        List[tuple[LangchainDocument, float]]
            Una lista de tuplas (documento, puntuación).
        """
        return self.vector_store.similarity_search_with_score(query, k=self.k)

    def retrieve_nodes(self, query: str) -> List[ResearchResponseDocument]:
        """
        Recupera nodos relevantes basados en una consulta (compatibilidad con LlamaIndex).

        Este método mantiene la compatibilidad con la interfaz de LlamaIndex
        esperada por ConfidenceFilterManager.

        Parámetros:
        -----------
        query : str
            La cadena de consulta.

        Devuelve:
        --------
        List[ResearchResponseDocument]
            Una lista de nodos con sus respectivas puntuaciones de similitud.
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
