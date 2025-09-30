from fastapi import APIRouter, Depends, status

from app.api.dependencies import ManagerFactory
from app.business.healthcheck import HealthcheckManager
from app.schemas.healthcheck import HealthcheckStatus

router = APIRouter(prefix="/healthcheck", tags=["Healthcheck"])


@router.get(
    "",
    response_model=HealthcheckStatus,
    status_code=status.HTTP_200_OK,
)
async def healthcheck(
    manager: HealthcheckManager = Depends(ManagerFactory.for_healthchecks),
) -> HealthcheckStatus:
    """
    Check if the backend is up and running properly.

    Returns:
        A HealthcheckStatus instance with the service status.
    """

    return manager.status()
