# PC Local Agent

**Local LLM integration proof of concept — Python, FastAPI, Ollama and Qwen2.5-Coder.**

PC demonstrates a small, inspectable HTTP interface to a locally running language model. The focus is straightforward API integration, explicit upstream timeouts and a localhost-first deployment boundary.

> **Status:** Functional proof of concept (POC). Not production-ready.

## What is implemented

- `GET /health` checks reachability of the local Ollama tags API (5-second timeout).
- `POST /generate` accepts a JSON prompt and forwards it to `qwen2.5-coder:7b` through Ollama (120-second timeout).
- The generation endpoint returns a JSON object containing `ok`, `model` and `response`.
- A shell script provides a manual smoke test of the generation endpoint.

A successful health check **does not** verify that the model is installed or can generate a response.

## Architecture

```mermaid
flowchart LR
    A[Local HTTP client] --> B[FastAPI service]
    B --> C[Ollama on localhost:11434]
    C --> D[Qwen2.5-Coder 7B]
```

## Requirements

- Python 3.10+
- Ollama running locally at `http://localhost:11434`
- The `qwen2.5-coder:7b` model downloaded into Ollama

## Quick start

```bash
git clone https://github.com/SantiagoFeliu/cassiopea-local-agent.git
cd cassiopea-local-agent
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

ollama pull qwen2.5-coder:7b
python -m uvicorn llm_api:app --host 127.0.0.1 --port 8002
```

Run Ollama separately before starting the API.

## API examples

**Health check**

```bash
curl http://127.0.0.1:8002/health
```

When Ollama is reachable, the service reports `status: "ok"`, `ollama: "reachable"` and the configured model name.

**Generate text**

```bash
curl -X POST http://127.0.0.1:8002/generate \
  -H 'Content-Type: application/json' \
  -d '{"prompt":"Explain the purpose of a health check in one sentence."}'
```

The response includes the generated text under `response`. Output varies by model and prompt.

**Manual smoke test**

```bash
bash tests/test_api.sh
```

This script is a manual API request, not an automated test suite.

## Engineering boundaries

- Keep the service bound to `127.0.0.1`. The code does not implement authentication or rate limiting.
- Exceptions can include upstream error details; do not expose this API to untrusted clients.
- No automated unit tests, CI, production monitoring or deployment hardening are demonstrated.
- Ollama and the model must be installed and running separately; the repository does not provision them.
- The model and upstream endpoints are fixed in `llm_api.py`.

## Evidence and next steps

Read [Engineering Notes](docs/ENGINEERING_NOTES.md) for source-grounded behavior, architecture and limitations.

Potential future work includes mocked upstream tests, sanitized error responses, request limits and CI. These are **not** claimed as implemented features.

## Verification checklist

Run the service locally and record the HTTP status and response body for each check:

1. With Ollama running, request `GET /health`; this establishes upstream reachability only.
2. Send a valid JSON prompt to `POST /generate` and confirm the response contains `ok`, `model`, and `response`.
3. Stop Ollama and repeat the health check; confirm the API reports failure rather than silently succeeding.
4. Restart Ollama and repeat generation; confirm recovery.

The repository includes a manual smoke test (`bash tests/test_api.sh`), **not** an automated CI test suite. These steps are a reproducible acceptance checklist, not a claim that they were executed in this review.

## Security and deployment decision

**Local-only POC.** Bind Uvicorn to `127.0.0.1`. Do not publish port 8002 or put the API behind a public reverse proxy without authentication, request limits, sanitized errors, and dependency review. No performance, uptime, or production-security guarantee is asserted.
