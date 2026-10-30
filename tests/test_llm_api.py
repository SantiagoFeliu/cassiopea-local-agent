from unittest.mock import Mock, patch
from fastapi.testclient import TestClient
from llm_api import app

client = TestClient(app)

def test_health_ok():
    with patch("llm_api.requests.get") as get:
        get.return_value = Mock(status_code=200)
        assert client.get("/health").json()["ollama"] == "reachable"

def test_health_unavailable():
    import requests
    with patch("llm_api.requests.get", side_effect=requests.ConnectionError):
        assert client.get("/health").status_code == 503

def test_generate_success():
    with patch("llm_api.requests.post") as post:
        post.return_value.json.return_value = {"response": "  hello  "}
        response = client.post("/generate", json={"prompt": "test"})
        assert response.status_code == 200
        assert response.json()["response"] == "hello"

def test_generate_invalid_upstream_json():
    with patch("llm_api.requests.post") as post:
        post.return_value.json.side_effect = ValueError()
        assert client.post("/generate", json={"prompt": "test"}).status_code == 502

def test_generate_unavailable():
    import requests
    with patch("llm_api.requests.post", side_effect=requests.ConnectionError):
        assert client.post("/generate", json={"prompt": "test"}).status_code == 503
