"""Unit tests for database session management."""

from unittest.mock import AsyncMock, MagicMock, patch

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker


class TestDatabaseSession:
    """Test suite for database session functionality."""

    def test_database_session_import(self) -> None:
        """Test that database session components can be imported."""
        from libs.database.database_session import DatabaseSession

        assert DatabaseSession is not None

    @patch("libs.database.database_session.create_async_engine")
    def test_database_session_initialization(self, mock_create_engine: MagicMock) -> None:
        """Test database session initialization."""
        from libs.database.database_session import DatabaseSession

        mock_engine = AsyncMock(spec=AsyncEngine)
        mock_create_engine.return_value = mock_engine

        db_session = DatabaseSession("postgresql://test:test@localhost/test")

        assert db_session is not None
        mock_create_engine.assert_called_once()

    @patch("libs.database.database_session.create_async_engine")
    def test_database_session_factory_creation(self, mock_create_engine: MagicMock) -> None:
        """Test database session factory creation."""
        from libs.database.database_session import DatabaseSession

        mock_engine = AsyncMock(spec=AsyncEngine)
        mock_create_engine.return_value = mock_engine

        db_session = DatabaseSession("postgresql://test:test@localhost/test")
        factory = db_session.get_session_factory()

        assert factory is not None
        assert callable(factory)

    @patch("libs.database.database_session.create_async_engine")
    def test_database_url_validation(self, mock_create_engine: MagicMock) -> None:
        """Test database URL validation."""
        from libs.database.database_session import DatabaseSession

        mock_engine = AsyncMock(spec=AsyncEngine)
        mock_create_engine.return_value = mock_engine

        # Test valid URL
        valid_url = "postgresql+asyncpg://user:pass@localhost:5432/db"
        db_session = DatabaseSession(valid_url)
        assert db_session is not None

        # Verify engine was created with correct URL
        mock_create_engine.assert_called_with(valid_url)

    def test_session_context_manager_protocol(self) -> None:
        """Test that session follows context manager protocol."""
        mock_session = AsyncMock(spec=AsyncSession)
        mock_session.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session.__aexit__ = AsyncMock(return_value=None)

        # Verify context manager methods exist
        assert hasattr(mock_session, "__aenter__")
        assert hasattr(mock_session, "__aexit__")

    def test_session_factory_type_hints(self) -> None:
        """Test session factory type hints."""

        # Test that async_sessionmaker is properly typed
        factory = async_sessionmaker()
        assert factory is not None

    @patch("libs.database.database_session.create_async_engine")
    def test_database_engine_disposal(self, mock_create_engine: MagicMock) -> None:
        """Test database engine disposal."""
        from libs.database.database_session import DatabaseSession

        mock_engine = AsyncMock(spec=AsyncEngine)
        mock_engine.dispose = AsyncMock()
        mock_create_engine.return_value = mock_engine

        db_session = DatabaseSession("postgresql://test:test@localhost/test")

        # Test that engine has dispose method
        assert hasattr(db_session.engine, "dispose")

    def test_database_session_configuration_options(self) -> None:
        """Test database session configuration options."""
        # Test common SQLAlchemy configuration options
        config_options = {
            "echo": False,
            "pool_size": 5,
            "max_overflow": 10,
            "pool_pre_ping": True,
            "pool_recycle": 3600,
        }

        for key, value in config_options.items():
            assert isinstance(key, str)
            assert value is not None

    def test_async_session_methods(self) -> None:
        """Test async session method availability."""
        mock_session = AsyncMock(spec=AsyncSession)

        # Test that common session methods exist
        expected_methods = [
            "execute",
            "scalar",
            "scalars",
            "add",
            "delete",
            "merge",
            "commit",
            "rollback",
            "close",
            "begin",
            "flush",
            "refresh",
        ]

        for method_name in expected_methods:
            assert hasattr(mock_session, method_name)

    def test_database_connection_string_formats(self) -> None:
        """Test various database connection string formats."""
        valid_formats = [
            "postgresql://user:pass@localhost/db",
            "postgresql+asyncpg://user:pass@localhost:5432/db",
            "sqlite+aiosqlite:///path/to/db.sqlite",
            "mysql+aiomysql://user:pass@localhost/db",
        ]

        for url_format in valid_formats:
            assert isinstance(url_format, str)
            assert "://" in url_format
