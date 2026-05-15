"""Main module for the application."""

import multiprocessing

import uvicorn

from app.appenv import AppEnv
from app.config.settings import Settings


# Attempt to import GunicornApplication from infra server package
try:
    from infra.server.gunicorn import GunicornApplication as GunicornApp
except ImportError as _e:  # pragma: no cover
    gunicorn_import_error = _e
    GunicornApp = None  # type: ignore

# Initialize variables for GunicornApplication import if try/except above didn't run yet
if "GunicornApp" not in globals():  # pragma: no cover
    GunicornApp = None  # type: ignore
if "gunicorn_import_error" not in globals():  # pragma: no cover
    gunicorn_import_error = None  # type: ignore

# Get settings
settings = Settings()


def main() -> None:
    """Run the application with the appropriate server based on the environment."""
    # Use Uvicorn for local development (hot reload)
    if settings.app_env == AppEnv.LOCAL:
        uvicorn.run(
            "app.application:get_app",
            host=settings.host,
            port=settings.port,
            reload=True,
            factory=True,
        )
    # Use Gunicorn for development and production
    else:
        if GunicornApp is None:
            error_msg = "GunicornApplication is not installed. Please install it with `pip install gunicorn`."
            raise ImportError(error_msg) from gunicorn_import_error

        # Determine worker count
        workers = settings.worker_count if settings.worker_count > 0 else multiprocessing.cpu_count() * 2 + 1

        # Set log level based on environment
        log_level = "info"
        if settings.app_env == AppEnv.DEV:
            log_level = "debug"

        # Additional configuration
        kwargs = {
            "loglevel": log_level,
            "reload": settings.app_env != AppEnv.PROD,  # Enable reload for non-prod environments
        }

        # Run with Gunicorn
        GunicornApp(
            app="app.application:get_app",
            host=settings.host,
            port=settings.port,
            workers=workers,
            **kwargs,
        ).run()


if __name__ == "__main__":
    main()
