"""Database session management."""

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

# Type alias for database session
DbSession = AsyncSession


class DatabaseSession:
    """Database session manager."""

    def __init__(self, database_url: str) -> None:
        """Initialize database session with URL."""
        self.database_url = database_url
        self.engine: AsyncEngine = create_async_engine(database_url)
        self._session_factory = async_sessionmaker(self.engine)

    def get_session_factory(self) -> async_sessionmaker[AsyncSession]:
        """Get the session factory."""
        return self._session_factory

    async def close(self) -> None:
        """Close the database engine."""
        await self.engine.dispose()
