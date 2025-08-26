.PHONY: help install install-dev test lint format clean run

help:  ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install:  ## Install the package
	pip install -e .

install-dev:  ## Install with development dependencies
	pip install -e ".[dev]"

test:  ## Run tests
	pytest

test-coverage:  ## Run tests with coverage report
	pytest --cov=src --cov-report=html --cov-report=term

lint:  ## Run linting tools
	ruff check src tests

format:  ## Format code
	ruff format src tests

format-check:  ## Check code formatting
	ruff check src tests
	ruff format --check src tests

clean:  ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

run:  ## Run the dashboard
	python -m src.system_monitor.main

run-script:  ## Run using the shell script
	./scripts/run_dashboard.sh

build:  ## Build the package
	python -m build

dev-setup:  ## Set up development environment
	python -m venv venv
	source venv/bin/activate && pip install -e ".[dev]"
	@echo "Development environment set up. Activate with: source venv/bin/activate"
