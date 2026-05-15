# Setup & Troubleshooting

## Quick Start

```bash
# 1. Setup environment
cp .env.sample .env                    # Copy environment file
make up-d-build                        # Build and start containers

# 2. Verify setup
curl http://localhost:5000/api/health/ # Test health endpoint
make logs-app                          # Check application logs
```

## Environment Types

| Environment | Server   | Dependencies   | Use Case                |
| ----------- | -------- | -------------- | ----------------------- |
| **Local**   | Uvicorn  | Full dev tools | Hot reload development  |
| **Dev**     | Gunicorn | Runtime + DB   | Production-like testing |
| **Prod**    | Gunicorn | Minimal        | Optimized production    |

## Common Issues & Solutions

### Docker Issues

```bash
# Container won't start
make down && make up-d-build           # Clean rebuild
docker system prune -f                # Clean Docker cache

# Permission errors
sudo chown -R $USER:$USER logs/        # Fix log permissions
```

### Database Issues

```bash
# Connection refused
make logs-db                           # Check PostgreSQL logs
docker exec -it fastapi-template-db-1 psql -U postgres  # Direct DB access

# Migration errors
make shell                             # Enter app container
uv run alembic upgrade head            # Run migrations manually
```

### Development Issues

```bash
# Pre-commit hooks fail
uv sync --group local                  # Install dev dependencies
uv run pre-commit install --overwrite # Reinstall hooks

# Import errors
uv sync                                # Sync dependencies
make shell                             # Check container environment
```

### Production Security

```bash
# Required changes for production
API_KEY=your-secure-api-key            # Change default API key
POSTGRES_DATABASE_PASSWORD=secure-pwd  # Change DB password
API_KEY_ENABLED=true                   # Enable authentication
CORS_ALLOW_ORIGINS=https://yourdomain.com  # Restrict CORS
```

## Useful Commands

```bash
# Container management
make up-d-build                        # Build and start detached
make down                              # Stop containers
make restart                           # Restart containers
make shell                             # Enter app container

# Monitoring
make logs                              # All logs
make logs-app                          # Application only
make logs-db                           # Database only

# Testing & Coverage
uv run pytest                         # Run all tests
uv run pytest -v                      # Verbose test output
uv run pytest --cov=app               # Run tests with coverage
uv run pytest --cov=app --cov-report=html  # Generate HTML coverage report
uv run pytest tests/specific_test.py  # Run specific test file
make test                              # Run tests + quality checks

# Quality checks
uv run pre-commit run --all-files      # Run all quality tools
make lint                              # Same as above
```
