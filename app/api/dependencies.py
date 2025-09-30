from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader

from app.business.documents import DocumentsManager
from app.business.healthcheck import HealthcheckManager
from app.business.research import ResearchManager
from app.core.config import settings


class ManagerFactory:

    """
    A factory class to handle the business managers instantiation.
    """

    @staticmethod
    def for_healthchecks() -> HealthcheckManager:
        """
        Build an instance of HealthcheckManager to inject as a dependency in the endpoints.

        Returns:
            An instance of HealthcheckManager.
        """

        return HealthcheckManager()

    @staticmethod
    def for_research(
        token: str = Depends(APIKeyHeader(name=settings.AUTH_HEADER_KEY)),
    ) -> ResearchManager:
        """
        Build an instance of ResearchManager to inject as a dependency in the endpoints.

        Returns:
            An instance of ResearchManager.
        """

        if token != settings.AUTH_SECRET_KEY:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

        return ResearchManager()

    @staticmethod
    def for_documents(
        token: str = Depends(APIKeyHeader(name=settings.AUTH_HEADER_KEY)),
    ) -> DocumentsManager:
        """
        Build an instance of DocumentsManager to inject as a dependency in the endpoints.

        Returns:
            An instance of DocumentsManager.
        """

        if token != settings.AUTH_SECRET_KEY:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

        return DocumentsManager()
