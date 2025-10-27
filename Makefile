.PHONY: help install test lint format type-check clean build publish dev-install

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	poetry install

dev-install: ## Install with development dependencies
	poetry install --extras dev

test: ## Run tests
	poetry run pytest

test-cov: ## Run tests with coverage
	poetry run pytest --cov=phagetrix --cov-report=html --cov-report=term

lint: ## Run linting tools
	poetry run black --check .
	poetry run isort --check-only .
	poetry run flake8 src tests

format: ## Format code
	poetry run black .
	poetry run isort .

type-check: ## Run type checking
	poetry run mypy src

pre-commit: ## Run pre-commit hooks
	poetry run pre-commit run --all-files

clean: ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .mypy_cache/
	rm -rf .tox/

build: clean ## Build package
	poetry build

publish: build ## Publish to PyPI
	poetry publish

check: lint test ## Run all checks

ci: check ## Run CI pipeline locally

tox: ## Run tox tests
	tox

example: ## Run example
	poetry run phagetrix examples/sample.phagetrix

bump-version: ## Bump version (usage: make bump-version VERSION=0.2.4)
	@if [ -z "$(VERSION)" ]; then echo "Usage: make bump-version VERSION=0.2.4"; exit 1; fi
	python scripts/bump_version.py $(VERSION)
