from fastapi import Request

from app.schemas.research import ResearchRequest, ResearchResponse


class ResearchManager:

    """
    A manager to handle the business logic related with research.
    """

    @staticmethod
    def research(payload: ResearchRequest, request: Request) -> ResearchResponse:
        """
        Research the query and return the relevant documents and summary.

        Returns:
            A valid ResearchResponse instance with the relevant documents and summary.
        """

        # Detect the language of the query
        detected_language = request.app.state.language_manager.detect_language(payload.query)

        # Get the relevant documents
        relevant_documents = request.app.state.retriever.retrieve_nodes(payload.query)

        # Check if the documents are relevant
        relevant_documents = request.app.state.correlation_filter_manager.check_correlation(
            payload.query, relevant_documents
        )

        # Check if there are relevant documents
        are_relevant_documents = len(relevant_documents) > 0
        if not are_relevant_documents:
            return ResearchResponse(are_relevant_documents=are_relevant_documents)

        # Get the comparison
        comparison = request.app.state.comparison_manager.get_comparison(
            payload.query, relevant_documents, detected_language
        )

        # Translate the documents
        translated_documents = []
        for doc in relevant_documents:
            doc.language = request.app.state.language_manager.detect_language(doc.title)
            translated_doc = request.app.state.translator_manager.translate_document(doc, detected_language)
            translated_documents.append(translated_doc)

        return ResearchResponse(
            are_relevant_documents=are_relevant_documents,
            documents=translated_documents,
            comparison=comparison,
        )
