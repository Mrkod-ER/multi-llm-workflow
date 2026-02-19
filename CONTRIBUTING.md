# Contributing to Multi-LLM Workflow Builder

Thank you for considering contributing! This guide covers everything you need to know.

---

## Branch Strategy

```
main
 └── develop
      ├── feat/<feature-name>
      ├── fix/<bug-name>
      └── docs/<topic>
```

- **`main`** — always stable, only merged from `develop` via PR
- **`develop`** — integration branch
- **`feat/*`** — new features
- **`fix/*`** — bug fixes

**Never push directly to `main`.**

---

## Commit Convention

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <short description>
```

### Types

| Type | Usage |
|---|---|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `test` | Adding or updating tests |
| `refactor` | Code restructure, no behavior change |
| `chore` | Build, config, tooling |
| `ci` | CI/CD pipeline changes |
| `perf` | Performance improvement |

### Scopes

`backend`, `frontend`, `engine`, `llm`, `api`, `memory`, `schema`, `docker`, `nodes`, `canvas`, `store`, `ui`, `docs`

### Examples

```
feat(llm): implement OllamaProvider for local model inference
fix(engine): resolve cycle detection bug in topological sort
docs: add workflow export guide to README
test(api): add integration tests for workflow run endpoint
chore(docker): pin service versions for reproducible builds
```

---

## Pull Request Process

1. Fork the repo and create a branch from `develop`
2. Write your code following the existing patterns
3. Add tests for any new functionality
4. Ensure CI passes
5. Open a PR against `develop` with a clear description
6. Reference the related issue: `Closes #N`

---

## Local Development Setup

```bash
git clone https://github.com/Mrkod-ER/multi-llm-workflow.git
cd multi-llm-workflow
cp .env.example .env
# Fill in your API keys in .env
docker compose up
```

Frontend: http://localhost:3000  
Backend API: http://localhost:8000  
API Docs: http://localhost:8000/docs
