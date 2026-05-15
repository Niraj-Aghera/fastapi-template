# Architecture & Tech Stack

## Tech Stack

- **Python 3.13+** with **UV** package manager
- **FastAPI** + **Uvicorn/Gunicorn** for high-performance APIs
- **PostgreSQL** with **SQLAlchemy** ORM and **Alembic** migrations
- **Docker** for containerization
- **Loguru** for structured logging

## Project Structure

```
fastapi-template/
├── app/                    # Main application
│   ├── api/                # API routes (health, v1)
│   ├── config/             # Settings & configuration
│   ├── exceptions/         # Custom exceptions
│   ├── middlewares/        # Authentication & middleware
│   ├── models/             # SQLAlchemy models
│   ├── repositories/       # Data access layer
│   ├── schema/             # Pydantic schemas
│   ├── services/           # Business logic
│   └── utils/              # Utilities & constants
├── infra/                  # Docker & deployment
├── libs/                   # Shared libraries (database, logger)
├── tests/                  # Test suite with factories
└── docs/                   # Documentation
```

## Layered Architecture

1. **API Layer** → Routes, validation, responses
2. **Service Layer** → Business logic, workflows
3. **Repository Layer** → Database operations
4. **Model Layer** → Data structures

## Dependencies

Core runtime dependencies are in `pyproject.toml`:

```toml
dependencies = [
    "fastapi>=0.116.1",
    "uvicorn>=0.35.0",
    "sqlalchemy[asyncio]>=2.0.43",
    "psycopg2-binary>=2.9.10",
    "loguru>=0.7.3",
    "pydantic-settings>=2.0.0"
]
```

Environment-specific groups:

- **local**: Full dev tools (testing, linting)
- **dev/prod**: Minimal runtime dependencies
