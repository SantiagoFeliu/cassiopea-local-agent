from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_TAGS_URL = "http://localhost:11434/api/tags"
MODEL = "qwen2.5-coder:7b"

app = FastAPI(title="PC Local Agent")

class PromptRequest(BaseModel):
    prompt: str

@app.get("/health")
def health():
    try:
        r = requests.get(OLLAMA_TAGS_URL, timeout=5)
        r.raise_for_status()
        return {"status": "ok", "ollama": "reachable", "model": MODEL}
    except requests.RequestException:
        raise HTTPException(status_code=503, detail="Ollama no disponible")

@app.post("/generate")
def generate(req: PromptRequest):
    try:
        r = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": req.prompt,
                "stream": False
            },
            timeout=120
        )
        r.raise_for_status()
        data = r.json()
        return {
            "ok": True,
            "model": MODEL,
            "response": data.get("response", "").strip()
        }
    except requests.RequestException:
        raise HTTPException(status_code=503, detail="Servicio de generación no disponible")
    except ValueError:
        raise HTTPException(status_code=502, detail="Respuesta inválida del servicio de generación")
