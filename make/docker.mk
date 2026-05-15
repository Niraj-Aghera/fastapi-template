# Docker commands Makefile
# Contains Docker-related variables and targets

# Variables
APP_ENV ?= local
DEVOPS_BASE_PATH = infra/devops
DOCKER_COMPOSE = docker compose -f $(DEVOPS_BASE_PATH)/docker-compose.yml --env-file .env
ENV_FILE = .env
SERVICE_NAME = fastapi-template
CONTAINER_NAME = fastapi-template-server-$(APP_ENV)
DB_CONTAINER = fastapi-template-postgres-$(APP_ENV)
POSTGRES_DATABASE_USERNAME = $(shell grep POSTGRES_DATABASE_USERNAME $(ENV_FILE) 2>/dev/null | cut -d '=' -f2)
POSTGRES_DATABASE_NAME = $(shell grep POSTGRES_DATABASE_NAME $(ENV_FILE) 2>/dev/null | cut -d '=' -f2)

# Build commands
.PHONY: build build-no-cache
build:
	$(DOCKER_COMPOSE) build

build-no-cache:
	$(DOCKER_COMPOSE) build --no-cache

# Docker commands (db + server)
.PHONY: up up-d up-d-build down restart stop start
up:
	$(DOCKER_COMPOSE) up

up-d:
	$(DOCKER_COMPOSE) up -d

up-d-build:
	$(DOCKER_COMPOSE) up -d --build

down:
	$(DOCKER_COMPOSE) down

restart: down up-d

stop:
	$(DOCKER_COMPOSE) stop

start:
	$(DOCKER_COMPOSE) start

# Logs
.PHONY: logs logs-app logs-db
logs:
	$(DOCKER_COMPOSE) logs -f

logs-app:
	$(DOCKER_COMPOSE) logs -f $(SERVICE_NAME)

logs-db:
	$(DOCKER_COMPOSE) logs -f postgres

# Cleanup Docker resources
.PHONY: clean clean-volumes clean-all
clean: down
	docker system prune -f

clean-volumes: down
	docker volume prune -f

clean-all: down
	docker system prune -af --volumes

# Status commands
.PHONY: ps status
ps:
	$(DOCKER_COMPOSE) ps

status:
	@echo "Container Status:"
	@docker ps --filter "name=$(CONTAINER_NAME)" --format "$(CONTAINER_NAME): {{.Status}}"
	@docker ps --filter "name=$(DB_CONTAINER)" --format "$(DB_CONTAINER): {{.Status}}"

# Database Migration Commands
.PHONY: db-shell db-revision db-upgrade db-downgrade db-history db-current

db-shell:
	$(DOCKER_COMPOSE) exec postgres psql -U $(POSTGRES_DATABASE_USERNAME) -d $(POSTGRES_DATABASE_NAME)

db-revision:
	@if [ -z "$(message)" ]; then \
		echo "Error: Please provide a migration message using 'message=your_message'"; \
		exit 1; \
	fi
	$(DOCKER_COMPOSE) exec $(SERVICE_NAME) python -m alembic -c libs/database/alembic.ini revision --autogenerate -m "$(message)"

db-upgrade:
	$(DOCKER_COMPOSE) exec $(SERVICE_NAME) python -m alembic -c libs/database/alembic.ini upgrade head

db-downgrade:
	$(DOCKER_COMPOSE) exec $(SERVICE_NAME) python -m alembic -c libs/database/alembic.ini downgrade -1

db-history:
	$(DOCKER_COMPOSE) exec $(SERVICE_NAME) python -m alembic -c libs/database/alembic.ini history

db-current:
	$(DOCKER_COMPOSE) exec $(SERVICE_NAME) python -m alembic -c libs/database/alembic.ini current

# Test Commands (run inside the container)
.PHONY: test test-app test-libs test-cov test-summary

test:
	docker exec $(CONTAINER_NAME) python -m pytest tests/ -v

test-app:
	docker exec $(CONTAINER_NAME) python -m pytest tests/app -v

test-libs:
	docker exec $(CONTAINER_NAME) python -m pytest tests/libs -v

test-cov:
	docker exec $(CONTAINER_NAME) python -m pytest tests/ --cov=app --cov=libs --cov-report=html --tb=short

# summary: failed test names + short tracebacks + counts, no noise
test-summary:
	docker exec $(CONTAINER_NAME) python -m pytest tests/ --tb=short -q --no-header 2>&1