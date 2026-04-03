# Cassiopea Local Agent

API local funcional sobre Ollama + Qwen2.5-Coder.

## Qué hace
Expone una API FastAPI en localhost con dos endpoints:
- /health
- /generate

## Requisitos
- Ollama corriendo en localhost
- Modelo qwen2.5-coder:7b descargado
- Python 3.10+

## Instalación
pip install -r requirements.txt

## Ejecutar
python -m uvicorn llm_api:app --host 127.0.0.1 --port 8002

## Test rápido
./tests/test_api.sh

## Healthcheck
curl http://localhost:8002/health
