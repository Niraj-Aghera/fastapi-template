"""Application lifespan manager.

This module defines the lifespan events for the FastAPI application,
handling the initialization and cleanup of essential services like the
database connection pool.
"""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.config.settings import settings
from libs.logger import get_logger

logger = get_logger("lifespan")

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    """
    Context manager to handle application startup and shutdown events.

    On startup, it creates the database engine and a session factory,
    storing the factory in the application's state.

    On shutdown, it disposes of the database engine's connection pool.
    """
    startup_start_time = datetime.now()
    logger.info("Starting application initialization...")

    # Database Setup
    try:
        # Create the SQLAlchemy async engine with connection pooling
        async_engine = create_async_engine(
            settings.postgres_database_url,
            pool_size=20,
            max_overflow=10,
            pool_recycle=3600,
            echo=settings.postgres_database_echo,
        )

        # Create a session maker factory
        session_factory = async_sessionmaker(
            bind=async_engine,
            autoflush=False,
            expire_on_commit=False,
        )

        # Store the session factory in the application state for access in dependencies
        app.state.db_session_factory = session_factory
        logger.info("Database connection pool and session factory created successfully.")

    except Exception as e:
        logger.error(f"Failed to initialize database connection: {e}")
        raise
    startup_elapsed_time = (datetime.now() - startup_start_time).total_seconds()
    logger.info(f"Application initialization completed in {startup_elapsed_time:.2f}s")

    yield

    # Shutdown
    shutdown_start_time = datetime.now()
    logger.info("Starting application shutdown...")

    try:
        await async_engine.dispose()
        logger.info("Database engine disposed successfully.")
    except Exception as e:
        logger.error(f"Error disposing database engine: {e}")

    shutdown_elapsed_time = (datetime.now() - shutdown_start_time).total_seconds()
    logger.info(f"Application shutdown completed in {shutdown_elapsed_time:.2f}s")