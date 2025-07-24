.PHONY: help install test lint format security migrate seed qa clean dev

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install dependencies
	poetry install

test: ## Run tests
	poetry run pytest -v --cov=app --cov-report=html --cov-report=term

test-fast: ## Run tests without coverage
	poetry run pytest -v

lint: ## Run linting
	poetry run ruff check app tests
	poetry run mypy app

format: ## Format code
	poetry run black app tests
	poetry run ruff check --fix app tests

security: ## Run security scans
	poetry run bandit -r app -f json -o bandit-report.json
	poetry run safety check --json --output safety-report.json

migrate: ## Run database migrations
	poetry run alembic upgrade head

migrate-create: ## Create new migration
	@read -p "Enter migration message: " msg; \
	poetry run alembic revision --autogenerate -m "$$msg"

seed: ## Seed database with test data
	poetry run python -m app.scripts.seed_data

qa: ## Run all quality assurance checks
	@echo "Running quality assurance checks..."
	@make format
	@make lint
	@make security
	@make test
	@echo "All QA checks passed!"

clean: ## Clean up generated files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .coverage htmlcov/ .pytest_cache/ .mypy_cache/
	rm -rf bandit-report.json safety-report.json

dev: ## Start development environment
	docker compose up -d

dev-logs: ## View development logs
	docker compose logs -f

dev-down: ## Stop development environment
	docker compose down

dev-rebuild: ## Rebuild and restart development environment
	docker compose down
	docker compose build --no-cache
	docker compose up -d

shell: ## Open shell in app container
	docker compose exec app bash

db-shell: ## Open database shell
	docker compose exec db psql -U postgres -d cargo_sms

reset-db: ## Reset database (WARNING: destroys all data)
	docker compose down -v
	docker compose up -d db
	sleep 5
	docker compose exec app alembic upgrade head

backup-db: ## Backup database
	docker compose exec db pg_dump -U postgres cargo_sms > backup_$(shell date +%Y%m%d_%H%M%S).sql

restore-db: ## Restore database from backup (usage: make restore-db BACKUP=backup_file.sql)
	@if [ -z "$(BACKUP)" ]; then echo "Usage: make restore-db BACKUP=backup_file.sql"; exit 1; fi
	docker compose exec -T db psql -U postgres cargo_sms < $(BACKUP)
