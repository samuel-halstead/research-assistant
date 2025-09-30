from fastapi import APIRouter, Depends, Request, status

from app.api.dependencies import ManagerFactory
from app.business.research import ResearchManager
from app.schemas.research import ResearchRequest, ResearchResponse

router = APIRouter(prefix="/research", tags=["Research"])


@router.post(
    "",
    response_model=ResearchResponse,
    status_code=status.HTTP_200_OK,
)
async def research(
    payload: ResearchRequest,
    request: Request,
    manager: ResearchManager = Depends(ManagerFactory.for_research),
) -> ResearchResponse:
    """
    Research the query and return relevant documents and summary.

    Returns:
        A ResearchResponse instance with relevant documents and summary.
    """

    return manager.research(payload, request)
