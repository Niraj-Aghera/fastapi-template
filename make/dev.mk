# Setup and Operations Makefile
# This file contains setup, run, and utility related commands

.PHONY: setup python run run-dev run-prod clean-cache logs-files

# Setup environment
setup:
	@echo "Setting up environment for $(shell uname -s)..."
	@if [ "$(shell uname -s)" = "Darwin" ]; then \
		echo "Detected macOS - installing UV via Homebrew..."; \
		brew install uv; \
	elif [ "$(shell uname -s)" = "Linux" ]; then \
		echo "Detected Linux - installing UV..."; \
		pip3 install uv; \
	else \
		echo "Unsupported OS: $(shell uname -s)"; \
		echo "Please install UV manually: https://docs.astral.sh/uv/getting-started/installation/"; \
		exit 1; \
	fi
	uv sync
	@echo "Environment setup complete"
	@echo "Remember to run 'make install-pre-commit' to install pre-commit hooks"
	@echo "Remember to copy .env.sample to .env and configure it"
	@echo "Note: PostgreSQL is handled via Docker - no local installation required"

# Install Python
python:
	uv python install
	@echo "Latest Python version installed"

# Run the application with Uvicorn (local development)
run:
	APP_ENV=local uv run main.py

# Run the application with Gunicorn (development)
run-dev:
	APP_ENV=dev uv run main.py

# Run the application with Gunicorn (production)
run-prod:
	APP_ENV=prod uv run main.py

# Clean up cache files and logs
clean-cache:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .pytest_cache -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	@echo "Cleaned up cache files"

# Show recent logs
logs-files:
	@if [ -d "logs/application" ]; then \
		ls -lt logs/application | head -n 10; \
		echo "Recent application logs (last 10 lines):"; \
		tail -n 10 $$(find logs/application -type f -name "*.log" | sort -r | head -n 1); \
	else \
		echo "No application logs found"; \
	fi
	@if [ -d "logs/error" ]; then \
		echo "\nRecent error logs (last 10 lines):"; \
		tail -n 10 $$(find logs/error -type f -name "*.log" | sort -r | head -n 1) 2>/dev/null || echo "No error logs found"; \
	fi
