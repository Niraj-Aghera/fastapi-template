# FastAPI Template

**FastAPI Template** is a modern, production-ready template for building high-performance Python web APIs. Built with Python 3.13+ and FastAPI, it provides a clean layered architecture with comprehensive quality tooling and Docker containerization.

## Features

- **Modern Architecture**: Clean layered design with clear separation of concerns
- **Performance First**: FastAPI + async/await for maximum throughput
- **Developer Experience**: Comprehensive tooling, quality checks, and documentation
- **Production Ready**: Docker containerization with environment-specific configurations
- **Quality Focused**: Strict quality standards with automated tooling
- **AI-Optimized**: Built to handle AI workloads and vector operations efficiently

## Prerequisites

- **Python 3.13+**
- **UV** package manager
- **Docker** & **Docker Compose**
- **Git**

## Tech Stack

- **Python 3.13+** with **UV** package manager
- **FastAPI** + **Uvicorn/Gunicorn** for APIs
- **PostgreSQL** with **SQLAlchemy** ORM
- **Docker** for containerization
- **Comprehensive quality tools** (Ruff, Pylint, MyPy)

## Core Dependencies

```toml
# Runtime dependencies
dependencies = [
    "fastapi>=0.116.1",           # Web framework
    "uvicorn>=0.35.0",            # ASGI server
    "pydantic-settings>=2.0.0",   # Settings management
    "sqlalchemy[asyncio]>=2.0.43", # Async ORM
    "psycopg2-binary>=2.9.10",    # PostgreSQL adapter
    "asyncpg>=0.29.0",            # Async PostgreSQL driver
    "alembic>=1.13.0",            # Database migrations
    "loguru>=0.7.3",              # Structured logging
    "python-dotenv>=1.1.1",       # Environment variables
    "yarl>=1.9.0",                # URL handling
]
```

## Quick Start

```bash
# 1. Clone and setup
git clone git@github.com:JeavioLLC/fastapi-template.git
cd fastapi-template
cp .env.sample .env

# 2. Start with Docker (recommended)
make up-d-build

# 3. Verify setup
curl http://localhost:5000/api/health/
```

**API Documentation**: http://localhost:5000/docs

## Development

```bash
make help                    # Show all commands
make run                     # Local development server
make test                    # Run tests + quality checks
make logs-app               # View application logs
make shell                  # Enter container shell
```

## Testing

```bash
# Run tests
make test                     # Run all tests
make test-unit                # Run unit tests only (no database required)
make test-cov                 # Run tests with coverage report
```

**Test Configuration:**

- Tests use isolated environments with `patch.dict()` for clean state
- No external configuration files required - tests are self-contained
- Comprehensive unit tests for database models and session management
- Fast execution with minimal dependencies

## Environment Types

| Environment | Server   | Use Case                     |
| ----------- | -------- | ---------------------------- |
| **Local**   | Uvicorn  | Hot reload development       |
| **Dev**     | Gunicorn | Development deployment       |
| **Test**    | N/A      | Automated testing (isolated) |
| **Prod**    | Gunicorn | Optimized production         |

## Documentation

- **[Architecture](docs/architecture.md)** - Tech stack, project structure, layered architecture
- **[Code Quality](docs/code_quality.md)** - Quality tools, pre-commit hooks, configurations
- **[Setup](docs/setup.md)** - Environment setup, troubleshooting, common issues

## Project Structure

```
fastapi-template/
├── app/                    # Main application
│   ├── api/                # API routes & endpoints
│   ├── services/           # Business logic
│   ├── repositories/       # Data access layer
│   └── models/             # Database models
├── libs/                   # Shared libraries
├── tests/                  # Test suite
└── docs/                   # Documentation
```

## Quality Assurance

All code changes are validated through:

- **Pre-commit hooks** with Ruff, Pylint, MyPy
- **Automated testing** with pytest
- **Architecture enforcement** with import-linter
- **Dead code detection** with vulture
