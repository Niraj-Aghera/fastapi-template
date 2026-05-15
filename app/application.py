from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse, Response

from app.api.health.router import health_check
from app.api.router import router as api_router
from app.config.settings import settings
from app.lifespan import lifespan
from app.middlewares.api_key import ApiKeyMiddleware
from app.utils.constants import API_PREFIX

def get_app() -> FastAPI:
    """Get and configure the FastAPI application."""
    app = FastAPI(
        title=settings.application_name,
        description=f"{settings.application_name} Backend Application",
        summary="",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/api/v1/openapi.json",
        debug=False,
        lifespan=lifespan,
    )

    # Configure GZip middleware
    app.add_middleware(GZipMiddleware, minimum_size=1024)

    # Configure CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=str(settings.cors_allow_origins).split(","),
        allow_credentials=True,
        allow_methods=str(settings.cors_allow_methods).split(","),
        allow_headers=str(settings.cors_allow_headers).split(","),
    )

    # Configure API Key middleware
    app.add_middleware(ApiKeyMiddleware)

    # Include API router with prefix
    app.include_router(api_router, prefix=API_PREFIX)

    @app.get("/", include_in_schema=False)
    async def root() -> JSONResponse:
        return await health_check()

    @app.get("/favicon.ico", include_in_schema=False)
    async def favicon() -> Response:
        return Response(status_code=204)

    return app