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
    Research should response status OK and 200 HTTP Response Code.

    Args:
        payload(ResearchRequest): The payload containing the query.
        request(Request): The request object.
        manager(ResearchManager): The manager (domain) with the business logic.

    Returns:
        (json): message OK
    """

    return manager.research(payload, request)
