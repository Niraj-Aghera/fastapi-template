# FastAPI Template Makefile
# Main Makefile that includes separated makefiles for better organization

# Include separated makefiles
include make/dev.mk
include make/quality.mk
include make/docker.mk

.PHONY: help

# Help command
help:
	@echo "FastAPI Template - Available commands:"
	@echo "\nLocal Development Commands:"
	@echo "  setup           - Install UV and set up the environment"
	@echo "  python          - Install latest Python version using UV"
	@echo "  run             - Run the application with Uvicorn (local development)"
	@echo "  run-dev         - Run the application with Gunicorn (development)"
	@echo "  run-prod        - Run the application with Gunicorn (production)"

	@echo "\nQuality & Linting:"
	@echo "  install-pre-commit - Install pre-commit hooks"
	@echo "  update-pre-commit  - Update pre-commit hooks"
	@echo "  lint               - Run pre-commit linting"
	@echo "  clean-cache     - Clean up Python cache files"
	@echo "  logs-files      - View local log files"

	@echo "\nDocker Commands:"
	@echo "  build           - Build the Docker container"
	@echo "  build-no-cache  - Build the Docker container without cache"
	@echo "  up              - Up the Docker container"
	@echo "  up-d            - Up the docker container in detached mode"
	@echo "  up-d-build      - Up the docker container in detached mode and build the container"
	@echo "  down            - Down the Docker container"
	@echo "  restart         - Restart the Docker container"
	@echo "  stop            - Stop the Docker container"
	@echo "  start           - Start the Docker container"
	@echo "  clean           - Clean the Docker container"
	@echo "  logs            - View the Docker container logs"
	@echo "  logs-app        - View the Docker container app logs"
	@echo "  logs-db         - View the Docker container db logs"
	@echo "  clean-volumes   - Clean the Docker container volumes"
	@echo "  clean-all       - Clean the Docker container all"
	@echo "  status          - View the Docker container status"

	@echo "\nTesting Commands:"
	@echo "  test            - Run all tests locally"
	@echo "  test-unit       - Run unit tests only (no database required)"
	@echo "  test-cov        - Run tests with coverage locally"

.DEFAULT_GOAL := help

# Test commands
.PHONY: test test-cov
test:
	uv run pytest tests/ -v --tb=short
test-cov:
	uv run pytest tests/ --cov=app --cov=libs --cov-report=html --tb=short
