from llama_index.core import QueryBundle

from app.core.config import settings
from app.managers.doc_list import doc_list_manager


class ConfidenceFilterManager:
    def __init__(self, retriever):
        self.retriever = retriever

    def query_with_confidence(self, query_str: str) -> str:
        """
        Realiza una query utilizando un umbral de confianza.

        Este método recibe una query como texto y utiliza un "retriever" para
        recuperar los documentos más relevantes. Evalúa la similitud de los resultados
        recuperados y sólo devuelve aquellos cuya similitud sea mayor o igual al umbral
        de confianza especificado (`confidence_threshold`).

        Parámetros:
        -----------
        query_str : str
            El texto de la query a realizar.

        Devuelve:
        --------
        list
            Una lista de documentos cuya similitud con la consulta supera el umbral de confianza.
            Si no se encuentra ningún documento que cumpla el criterio, retorna una lista vacía.
        """

        # Retrieve the nodes (directly from the retriever)
        query_bundle = QueryBundle(query_str)
        retrieved_nodes_with_scores = self.retriever.retrieve_nodes(query_bundle)

        # Get documents for the top k nodes
        retrieved_docs = doc_list_manager.build_doc_list_response(retrieved_nodes_with_scores)
        if not retrieved_docs:
            # No documents retrieved => zero confidence
            return []

        # Filter documents based on confidence threshold
        retrieved_docs = [doc for doc in retrieved_docs if doc.similarity >= settings.RETRIEVER_CONFIDENCE_THRESHOLD]

        return retrieved_docs
