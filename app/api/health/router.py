"""Health check router for the application."""

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from sqlalchemy import text

from app.dependencies import DBSession
from app.schema.api_response import create_response
from app.schema.health import HealthCheckFailResponse, HealthCheckResponse
from libs.logger import get_logger

router = APIRouter(tags=["health"])

logger = get_logger(__name__)

@router.get(
    "/",
    summary="Health check endpoint",
    response_model=HealthCheckResponse,
    description="Basic health check endpoint. Returns a simple status indicating the service is up.",
    responses={
        status.HTTP_200_OK: {"model": HealthCheckResponse},
        status.HTTP_503_SERVICE_UNAVAILABLE: {"model": HealthCheckFailResponse},
    },
)
async def health_check() -> JSONResponse:
    try:
        return create_response(status_code=status.HTTP_200_OK, message="healthy")
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return create_response(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            message="unhealthy",
            errors=[{"code": "SERVICE_UNAVAILABLE", "message": "Service is unhealthy"}],
        )

@router.get(
    "/db",
    summary="Database health check",
    description="Returns the health status of the database connection",
)
async def db_health_check(db: DBSession) -> JSONResponse:
    try:
        result = await db.execute(text("SELECT 1"))
        if result.scalar_one() == 1:
            return create_response(
                status_code=status.HTTP_200_OK,
                message="Database connection is healthy",
            )
        return create_response(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            message="Database connection test failed",
        )
    except Exception as e:
        return create_response(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            message=f"Database connection is unhealthy. Error: {e}",
        )