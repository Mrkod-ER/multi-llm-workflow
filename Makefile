# ================================================
# Multi-LLM Workflow Builder — Makefile
# ================================================

.PHONY: up down build logs ps clean pull-model

## Start all services
up:
	docker compose up -d

## Stop all services
down:
	docker compose down

## Rebuild all images
build:
	docker compose build

## View live logs
logs:
	docker compose logs -f

## Show running containers
ps:
	docker compose ps

## Remove containers, networks, and volumes
clean:
	docker compose down -v --remove-orphans

## Pull a local LLM model via Ollama
## Usage: make pull-model MODEL=llama3
pull-model:
	docker exec mlw_ollama ollama pull $(MODEL)

## List downloaded Ollama models
list-models:
	docker exec mlw_ollama ollama list
