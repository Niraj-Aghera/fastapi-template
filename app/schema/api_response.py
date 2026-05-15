"""API schema for standardized responses."""

from typing import Any

from fastapi.responses import JSONResponse

def create_response(
    status_code: int,
    message: str,
    data: Any | None = None,
    errors: list[dict[str, Any]] | None = None,
    meta: dict[str, Any] | None = None,
) -> JSONResponse:
    """
    Create a standardized JSON API response.

    Args:
        status_code: HTTP status code
        message: Human-readable message
        data: Response data
        errors: List of error objects
        meta: Metadata about the response

    Returns:
        JSONResponse with standardized format
    """
    response_body: dict[str, Any] = {
        "message": message,
    }

    if data is not None:
        response_body["data"] = data

    if errors is not None:
        response_body["errors"] = errors

    if meta is not None:
        response_body["meta"] = meta

    return JSONResponse(
        status_code=status_code,
        content=response_body,
    )