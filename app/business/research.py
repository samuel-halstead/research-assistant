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

        # Create a summary that includes the detected language
        summary = f"Query: '{payload.query}'\nDetected Language: {detected_language}"

        # Get the relevant documents
        relevant_documents = request.app.state.retriever.retrieve_nodes(payload.query)

        return ResearchResponse(
            are_relevant_documents=True,
            documents=relevant_documents,
            summary=summary,
        )
