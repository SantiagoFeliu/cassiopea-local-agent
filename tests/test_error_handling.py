import unittest
from unittest.mock import Mock, patch

import requests
from fastapi import HTTPException

import llm_api


class ErrorHandlingTests(unittest.TestCase):
    def test_health_success(self):
        response = Mock()
        with patch.object(llm_api.requests, "get", return_value=response) as get:
            self.assertEqual(llm_api.health()["status"], "ok")
        get.assert_called_once_with(llm_api.OLLAMA_TAGS_URL, timeout=5)

    def test_health_upstream_failure_is_sanitized_503(self):
        with patch.object(llm_api.requests, "get", side_effect=requests.Timeout("secret detail")):
            with self.assertRaises(HTTPException) as ctx:
                llm_api.health()
        self.assertEqual(ctx.exception.status_code, 503)
        self.assertNotIn("secret", ctx.exception.detail)

    def test_generate_success(self):
        response = Mock()
        response.json.return_value = {"response": " hello "}
        with patch.object(llm_api.requests, "post", return_value=response):
            result = llm_api.generate(llm_api.PromptRequest(prompt="hi"))
        self.assertEqual(result["response"], "hello")

    def test_generate_upstream_failure_is_sanitized_503(self):
        with patch.object(llm_api.requests, "post", side_effect=requests.HTTPError("secret detail")):
            with self.assertRaises(HTTPException) as ctx:
                llm_api.generate(llm_api.PromptRequest(prompt="hi"))
        self.assertEqual(ctx.exception.status_code, 503)
        self.assertNotIn("secret", ctx.exception.detail)

    def test_invalid_json_and_incomplete_payload_are_502(self):
        for payload in (ValueError("secret detail"), [], {"response": 12}):
            response = Mock()
            if isinstance(payload, Exception):
                response.json.side_effect = payload
            else:
                response.json.return_value = payload
            with self.subTest(payload=type(payload).__name__), patch.object(llm_api.requests, "post", return_value=response):
                with self.assertRaises(HTTPException) as ctx:
                    llm_api.generate(llm_api.PromptRequest(prompt="hi"))
            self.assertEqual(ctx.exception.status_code, 502)
            self.assertNotIn("secret", ctx.exception.detail)


if __name__ == "__main__":
    unittest.main()
