"""Health check schema."""

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Health check response model."""

    status: str = Field(default="ok", description="Service health status.")
    service: str = Field(default="docuextract", description="Service identifier.")
