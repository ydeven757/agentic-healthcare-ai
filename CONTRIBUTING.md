# Contributing to Agentic Healthcare AI

## Prerequisites

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose

## Setup

```bash
# Clone the repository
git clone https://github.com/ydeven757/agentic-healthcare-ai.git
cd agentic-healthcare-ai

# Copy environment template
cp env.template .env
# Edit .env with your configuration (at minimum set OPENAI_API_KEY)

# Install Python dependencies (per service)
pip install -r crewai_fhir_agent/requirements.txt
pip install -r autogen_fhir_agent/requirements.txt
pip install -r agent_backend/requirements.txt

# Install frontend dependencies
cd ui && npm install && cd ..

# Or use Docker Compose for the full stack
cd docker && docker compose up --build
```

## Running Tests

```bash
# Python tests
pip install pytest pytest-cov
pytest tests/ -v

# Frontend tests
cd ui && npm test
```

## Code Style

- **Python**: Follow PEP 8. Use `black` for formatting, `flake8` for linting.
- **TypeScript**: ESLint with the project's config. Run `npm run lint` in `ui/`.

## Environment Variables

All configuration is via environment variables. See `env.template` for the full list.

Key variables:
- `OPENAI_API_KEY` — Required for LLM calls
- `FHIR_BASE_URL` — FHIR server endpoint (default: `http://localhost:8080/fhir/`)
- `ALLOWED_ORIGINS` — Comma-separated list of allowed CORS origins
- `JWT_SECRET_KEY` — Secret for JWT token validation (if unset, auth runs in dev mode)

## Architecture

| Service | Port | Description |
|---------|------|-------------|
| CrewAI Agent | 8000 | Sequential task execution framework |
| Autogen Agent | 8001 | Conversational multi-agent framework |
| Agent Backend | 8002 | Unified backend wrapping both frameworks |
| FHIR Proxy | 8003 | CORS proxy for FHIR server requests |
| FHIR MCP Server | 8004 | MCP protocol server for FHIR operations |
| UI | 3030 | React frontend |

## Pull Requests

1. Create a feature branch from `main`
2. Make your changes
3. Ensure tests pass locally
4. Open a PR with a clear description of changes
