from app.schemas.research import ResearchRequest, ResearchResponse


class ResearchManager:

    """
    A manager to handle the business logic related with research.
    """

    @staticmethod
    def research(request: ResearchRequest) -> ResearchResponse:
        """
        Research the query and return the relevant documents and summary.

        Returns:
            A valid ResearchResponse instance with a -forced- healthy status.
        """
        return ResearchResponse(
            are_relevant_documents=True,
            documents=[],
            summary=request.query,
        )
