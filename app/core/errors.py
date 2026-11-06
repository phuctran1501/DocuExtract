"""Global exception handling and error response formatting."""

import logging
from typing import Any

from fastapi import FastAPI, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.requests import Request

from app.core.correlation import get_correlation_id
from app.schemas.error import ErrorDetail, ErrorResponse

logger = logging.getLogger(__name__)


class AppException(Exception):
    """Base application exception for DocuExtract errors."""

    def __init__(
        self,
        code: str,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.status_code = status_code


def _build_error_response(status_code: int, code: str, message: str) -> JSONResponse:
    """Build a standardized JSONResponse with the API error envelope."""
    payload = ErrorResponse(
        error=ErrorDetail(
            code=code,
            message=message,
            correlation_id=get_correlation_id(),
        )
    )
    return JSONResponse(
        status_code=status_code,
        content=payload.model_dump(),
    )


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """Handle custom application exceptions."""
    return _build_error_response(
        status_code=exc.status_code,
        code=exc.code,
        message=exc.message,
    )


async def http_exception_handler(
    request: Request, exc: StarletteHTTPException
) -> JSONResponse:
    """Handle Starlette/FastAPI HTTPExceptions."""
    code_map = {
        400: "INVALID_REQUEST",
        404: "NOT_FOUND",
        413: "FILE_TOO_LARGE",
        415: "UNSUPPORTED_FILE_TYPE",
        422: "INVALID_DOCUMENT",
        500: "EXTRACTION_FAILED",
        503: "SERVICE_UNAVAILABLE",
    }
    code = code_map.get(exc.status_code, f"HTTP_{exc.status_code}")
    message = str(exc.detail) if exc.detail else "An HTTP error occurred."
    return _build_error_response(
        status_code=exc.status_code,
        code=code,
        message=message,
    )


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Handle request validation errors without exposing internal traces."""
    # Simplify validation error messages for callers
    errors: list[Any] = exc.errors()
    if errors:
        first_error = errors[0]
        field_loc = " -> ".join(str(loc) for loc in first_error.get("loc", []))
        detail_msg = first_error.get("msg", "invalid input")
        msg = f"Validation failed at '{field_loc}': {detail_msg}"
    else:
        msg = "Request validation failed."

    return _build_error_response(
        status_code=status.HTTP_400_BAD_REQUEST,
        code="INVALID_REQUEST",
        message=msg,
    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle unexpected server errors without leaking internals."""
    correlation_id = get_correlation_id()
    logger.error(
        "Unhandled exception during request [correlation_id=%s]: %s",
        correlation_id,
        exc,
        exc_info=True,
    )
    return _build_error_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        code="EXTRACTION_FAILED",
        message="An unexpected error occurred while processing the request.",
    )


def register_exception_handlers(app: FastAPI) -> None:
    """Register all standard exception handlers on the FastAPI application."""
    app.add_exception_handler(AppException, app_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(RequestValidationError, validation_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(Exception, unhandled_exception_handler)
