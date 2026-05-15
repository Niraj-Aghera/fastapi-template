"""API Key middleware for FastAPI application."""

import secrets
from typing import Any

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.status import HTTP_403_FORBIDDEN

from app.config.settings import settings
from app.exceptions import ApiForbiddenError
from app.schema.api_response import create_response
from app.utils.constants import API_KEY_HEADER

def validate_api_key(api_key: str | None) -> None:
    if not api_key:
        raise ApiForbiddenError(error="MISSING_API_KEY", message=f"Missing {API_KEY_HEADER} header")

    # Use constant-time comparison to prevent timing attacks
    if not secrets.compare_digest(api_key, settings.api_key):
        raise ApiForbiddenError(error="INVALID_API_KEY", message="Invalid API Key")

class ApiKeyMiddleware(BaseHTTPMiddleware):
    """Middleware that now calls our reusable validation function."""

    async def dispatch(self, request: Request, call_next: Any) -> Any:
        """Process request and validate API key."""
        if not settings.enable_api_key:
            return await call_next(request)

        current_path = request.url.path
        if any(current_path.startswith(excluded_path) for excluded_path in settings.api_key_exclude_paths_list):
            return await call_next(request)

        try:
            api_key = request.headers.get(API_KEY_HEADER)
            # Call the reusable validation logic
            validate_api_key(api_key)

        except ApiForbiddenError as e:
            return create_response(
                status_code=HTTP_403_FORBIDDEN,
                message="API key validation failed",
                errors=[{"code": e.error_code, "message": e.message, "details": e.details}],
            )
        except Exception as e:
            return create_response(
                status_code=HTTP_403_FORBIDDEN,
                message="API key validation failed",
                errors=[
                    {
                        "code": "API_KEY_ERROR",
                        "message": "An unexpected error occurred while validating the API key",
                        "details": str(e),
                    }
                ],
            )

        return await call_next(request)