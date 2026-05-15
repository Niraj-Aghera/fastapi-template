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

	@echo "\nDocker Commands (all services: db + redis + valkey + server + worker):"
	@echo "  build           - Build Docker containers"
	@echo "  build-no-cache  - Build Docker containers without cache"
	@echo "  up              - Start all services (foreground)"
	@echo "  up-d            - Start all services (detached)"
	@echo "  up-d-build      - Start all services with build (detached)"
	@echo "  down            - Stop and remove all containers"
	@echo "  restart         - Restart all services (down + up-d)"
	@echo "  stop            - Stop all containers (keep containers)"
	@echo "  start           - Start stopped containers"

	@echo "\nDocker Logs:"
	@echo "  logs            - View all container logs"
	@echo "  logs-app        - View server logs"
	@echo "  logs-db         - View database logs"

	@echo "\nDocker Cleanup & Status:"
	@echo "  clean           - Stop containers and prune Docker system"
	@echo "  clean-volumes   - Stop containers and prune volumes"
	@echo "  clean-all       - Stop containers and prune everything"
	@echo "  ps              - List running containers"
	@echo "  status          - View container status"

	@echo "\nTesting Commands (run inside container, APP_ENV defaults to local):"
	@echo "  test            - Run all tests in container"
	@echo "  test-app        - Run tests/app in container"
	@echo "  test-libs       - Run tests/libs in container"
	@echo "  test-cov        - Run all tests with coverage in container"
	@echo "  test-summary    - Run all tests, AI-friendly short output"

.DEFAULT_GOAL := help