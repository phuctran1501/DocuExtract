"""Health check endpoint."""

from fastapi import APIRouter, status

from app.schemas.health import HealthResponse

router = APIRouter(tags=["Health"])


@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Service health check",
    description=(
        "Returns HTTP 200 when the process is active and ready to serve requests."
    ),
)
async def check_health() -> HealthResponse:
    """Return service health status."""
    return HealthResponse(status="ok", service="docuextract")
