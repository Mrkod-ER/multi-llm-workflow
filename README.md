# Multi-LLM Workflow Builder

[![CI](https://github.com/Mrkod-ER/multi-llm-workflow/actions/workflows/ci.yml/badge.svg)](https://github.com/Mrkod-ER/multi-llm-workflow/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)

> A visual, open-source, self-hostable platform for orchestrating multi-LLM workflows using a drag-and-drop node canvas.

---

## Overview

Multi-LLM Workflow Builder lets you chain multiple AI language models together in a visual graph — routing prompts through different models, merging outputs, and building sophisticated AI pipelines without code.

## Features

- 🔀 **Visual DAG Builder** — Drag-and-drop canvas powered by React Flow
- 🤖 **Multi-Provider Support** — OpenAI (GPT-4o), Ollama (local), and a Mock provider for testing
- ⚡ **Real-time Execution** — Run workflows and watch results stream node-by-node
- 🐳 **Self-Hostable** — One-command Docker Compose setup with Ollama, Redis, and the full stack
- 🔒 **Secure by Default** — API keys stored in environment variables, never in code
- 📡 **REST API** — Full OpenAPI spec available at `/api/v1/docs/swagger`

## Architecture

```
┌─────────────────────────────────────────────────────┐
│   Browser (Next.js 14 + React Flow)                 │
│   Visual DAG Builder + Properties Panel             │
└───────────────────┬─────────────────────────────────┘
                    │ REST / WebSocket
┌───────────────────▼─────────────────────────────────┐
│   FastAPI Backend                                   │
│   ┌──────────┐  ┌──────────┐  ┌──────────────────┐  │
│   │ Workflow  │  │  Engine  │  │  Provider Layer  │  │
│   │  Router  │→ │ DAG Sort │→ │ OpenAI / Ollama  │  │
│   └──────────┘  └──────────┘  └──────────────────┘  │
└───────────────────┬─────────────────────────────────┘
        ┌───────────┼───────────┐
┌───────▼──┐  ┌─────▼────┐  ┌──▼──────────┐
│  Redis   │  │  Ollama  │  │  OpenAI API │
│ (Memory) │  │ (Local)  │  │  (Cloud)    │
└──────────┘  └──────────┘  └─────────────┘
```

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js 14, TypeScript, React Flow, Zustand, Tailwind CSS |
| Backend | FastAPI, Python 3.11, Pydantic v2, Uvicorn |
| LLM Providers | Ollama (local), OpenAI via LiteLLM |
| Memory | Redis |
| Infrastructure | Docker, Docker Compose, GitHub Actions |

## Getting Started

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/) and Docker Compose
- (Optional) An OpenAI API key for cloud models
- (Optional) A GPU for running large local models via Ollama

### Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/Mrkod-ER/multi-llm-workflow.git
cd multi-llm-workflow

# 2. Configure environment
cp .env.example .env
# Edit .env with your API keys

# 3. Start the full stack
make up

# 4. Open the app
open http://localhost:3000
```

### Development (Hot Reload)

```bash
make dev
```

### Pull a Local Model (Ollama)

```bash
make pull-model MODEL=llama3
make pull-model MODEL=mistral
```

### Useful Commands

```bash
make logs          # View all logs
make ps            # Show container status
make test          # Run backend tests
make clean         # Remove all containers + volumes
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for branch strategy, commit conventions, and PR guidelines.

## License

MIT — see [LICENSE](LICENSE) for details.
