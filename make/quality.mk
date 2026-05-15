# Quality and Linting Makefile
# This file contains all quality assurance and linting related commands

# Helper function for venv check
define check_venv
	@if [ -z "$$VIRTUAL_ENV" ]; then \
		echo "Error: Virtual environment is not activated!"; \
		echo "Please activate it first:"; \
		echo "source .venv/bin/activate  # For Unix/Linux/MacOS"; \
		echo "# OR"; \
		echo ".venv\\\Scripts\\\activate  # For Windows"; \
		exit 1; \
	fi
endef

.PHONY: install-pre-commit update-pre-commit lint

# Pre-commit commands
install-pre-commit:
	$(call check_venv)
	uv add --dev pre-commit
	pre-commit install

update-pre-commit:
	$(call check_venv)
	pre-commit autoupdate

lint:
	$(call check_venv)
	pre-commit run --all-files
