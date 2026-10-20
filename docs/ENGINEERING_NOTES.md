# PC Local Agent — Engineering Notes

Local Python FastAPI integration with Ollama and Qwen2.5-Coder. This is a small proof of concept, not a production-ready service.

## Verified from source

- `GET /health` calls Ollama's local tags endpoint with a 5-second timeout.
- `POST /generate` forwards a prompt to a fixed local model with a 120-second timeout.
- The repository includes `requirements.txt` and a manual shell smoke test.

## Run

```bash
pip install -r requirements.txt
python -m uvicorn llm_api:app --host 127.0.0.1 --port 8002
curl http://127.0.0.1:8002/health
```

## Architecture

```mermaid
flowchart LR
  A[Local client] --> B[FastAPI]
  B --> C[Local Ollama]
  C --> D[Qwen2.5-Coder]
```

## Limitations and safety

No authentication, rate limiting, automated unit tests, or production monitoring is demonstrated. Exception messages may reveal upstream details. Keep the API bound to localhost. Do not publish prompts containing sensitive information. A successful health check confirms upstream reachability, not successful model inference.

## Planned improvements

Mocked upstream tests, sanitized error handling, request limits, and CI. These are plans, not completed features.
