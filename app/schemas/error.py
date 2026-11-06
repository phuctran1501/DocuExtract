"""Standard error schemas conforming to API Contract."""

from pydantic import BaseModel, Field


class ErrorDetail(BaseModel):
    """Structured error payload."""

    code: str = Field(..., description="Machine-readable stable error code.")
    message: str = Field(..., description="Human-readable error explanation.")
    correlation_id: str | None = Field(
        default=None, description="Correlation ID for log tracing."
    )


class ErrorResponse(BaseModel):
    """Standard error response envelope."""

    error: ErrorDetail

