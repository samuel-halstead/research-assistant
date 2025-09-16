from fastapi import APIRouter, Depends, status

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
    request: ResearchRequest,
    manager: ResearchManager = Depends(ManagerFactory.for_research),
) -> ResearchResponse:
    """
    Research should response status OK and 200 HTTP Response Code.

    Args:
        request(ResearchRequest): The request containing the query.
        manager(ResearchManager): The manager (domain) with the business logic.

    Returns:
        (json): message OK
    """

    return manager.research(request)
