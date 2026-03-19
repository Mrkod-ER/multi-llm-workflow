# ================================================
# Multi-LLM Workflow Builder — Makefile
# ================================================

.PHONY: up down build logs ps clean pull-model list-models \
        dev dev-backend dev-frontend install test lint

# ---------------------------------------------------
# Docker — Production
# ---------------------------------------------------

## Start all services in detached mode
up:
	docker compose -f docker-compose.yml up -d

## Stop all services
down:
	docker compose down

## Rebuild all images (no cache)
build:
	docker compose build --no-cache

## View live logs for all services
logs:
	docker compose logs -f

## View logs for a single service: make logs-service SVC=backend
logs-service:
	docker compose logs -f $(SVC)

## Show running containers
ps:
	docker compose ps

## Remove containers, networks, and volumes
clean:
	docker compose down -v --remove-orphans

# ---------------------------------------------------
# Docker — Development (hot-reload)
# ---------------------------------------------------

## Start all services with dev overrides (hot-reload)
dev:
	docker compose -f docker-compose.yml -f docker-compose.override.yml up

## Start only backend with hot-reload
dev-backend:
	docker compose -f docker-compose.yml -f docker-compose.override.yml up backend

## Start only frontend with hot-reload
dev-frontend:
	docker compose -f docker-compose.yml -f docker-compose.override.yml up frontend

# ---------------------------------------------------
# Ollama Model Management
# ---------------------------------------------------

## Pull a model: make pull-model MODEL=llama3
pull-model:
	docker exec mlw_ollama ollama pull $(MODEL)

## List all downloaded Ollama models
list-models:
	docker exec mlw_ollama ollama list

# ---------------------------------------------------
# Local Dev (without Docker)
# ---------------------------------------------------

## Install all dependencies
install:
	cd backend && pip install -r requirements-dev.txt
	cd frontend && npm install

## Run all backend tests
test:
	cd backend && pytest tests/ -v --tb=short

## Run backend linter
lint:
	cd backend && ruff check .
	cd frontend && npm run lint
