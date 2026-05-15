"""API Key middleware and dependency for FastAPI application."""

import secrets
from typing import Any

from fastapi import Request, Security
from fastapi.security import APIKeyHeader
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.status import HTTP_403_FORBIDDEN

from app.config.settings import Settings
from app.exceptions import ApiForbiddenError
from app.schema.api_response import create_response
from app.utils.constants import API_KEY_HEADER


settings = Settings()

# --- 1. Reusable Validation Function ---


def validate_api_key(api_key: str | None) -> None:
    """
    A single, reusable function to perform the API key validation logic.
    Raises an ApiForbiddenError if validation fails.
    """
    if not api_key:
        raise ApiForbiddenError(error="MISSING_API_KEY", message=f"Missing {API_KEY_HEADER} header")

    # Use constant-time comparison to prevent timing attacks
    if not secrets.compare_digest(api_key, settings.api_key):
        raise ApiForbiddenError(error="INVALID_API_KEY", message="Invalid API Key")


# --- 2. Security Scheme and Dependency ---

api_key_header_scheme = APIKeyHeader(name=API_KEY_HEADER, auto_error=False)


async def get_api_key(api_key_header: str = Security(api_key_header_scheme)) -> str:
    """
    Dependency for routes that now calls our reusable validation function.
    """
    if not settings.enable_api_key_auth:
        return api_key_header

    try:
        # Call the reusable validation logic
        validate_api_key(api_key_header)
    except ApiForbiddenError as e:
        # Convert to HTTPException which FastAPI handles gracefully
         return create_response(
                status_code=HTTP_403_FORBIDDEN,
                message="Authentication failed",
                errors=[{"code": e.error_code, "message": e.message, "details": e.details}]
            )

    return api_key_header


# --- 3. The Middleware ---


class ApiKeyMiddleware(BaseHTTPMiddleware):
    """Middleware that now calls our reusable validation function."""

    async def dispatch(self, request: Request, call_next: Any) -> Any:
        """Process request and validate API key."""
        if not settings.enable_api_key_auth:
            return await call_next(request)

        current_path = request.url.path
        if any(current_path.startswith(excluded_path) for excluded_path in settings.api_key_exclude_paths_list):
            return await call_next(request)

        try:
            api_key = request.headers.get(API_KEY_HEADER)
            # Call the reusable validation logic
            validate_api_key(api_key)

        except ApiForbiddenError as e:
            # If our reusable function raises a known error, format it
            return create_response(
                status_code=HTTP_403_FORBIDDEN,
                message="Authentication failed",
                errors=[{"code": e.error_code, "message": e.message, "details": e.details}],
            )
        except Exception as e:
            # Catch any other unexpected errors
            return create_response(
                status_code=HTTP_403_FORBIDDEN,
                message="Authentication failed",
                errors=[
                    {
                        "code": "AUTH_ERROR",
                        "message": "An unexpected authentication error occurred",
                        "details": str(e),
                    }
                ],
            )

        return await call_next(request)
