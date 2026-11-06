"""Correlation ID tracking across request-response cycles."""

import uuid
from contextvars import ContextVar

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

CORRELATION_ID_HEADER = "X-Correlation-ID"

_correlation_id_ctx: ContextVar[str | None] = ContextVar("correlation_id", default=None)


def get_correlation_id() -> str | None:
    """Get the current request correlation ID from context."""
    return _correlation_id_ctx.get()


def set_correlation_id(correlation_id: str) -> None:
    """Set the current request correlation ID in context."""
    _correlation_id_ctx.set(correlation_id)


def generate_correlation_id() -> str:
    """Generate a unique correlation ID."""
    return uuid.uuid4().hex


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    """Middleware ensuring each request has a correlation ID for observability."""

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        header_correlation_id = request.headers.get(CORRELATION_ID_HEADER)
        correlation_id = header_correlation_id or generate_correlation_id()

        set_correlation_id(correlation_id)

        response = await call_next(request)
        response.headers[CORRELATION_ID_HEADER] = correlation_id
        return response
