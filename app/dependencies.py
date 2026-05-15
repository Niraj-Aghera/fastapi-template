"""Application dependencies for dependency injection."""

from collections.abc import AsyncGenerator

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession


async def get_db(request: Request) -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency that provides a database session.
    
    Yields an AsyncSession from the session factory stored in app state.
    The session is automatically closed after the request is complete.
    """
    session_factory = request.app.state.db_session_factory
    async with session_factory() as session:
        yield session
