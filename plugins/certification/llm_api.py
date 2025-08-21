import json
import logging
import os
from typing import Dict, Optional

import requests
from requests.exceptions import RequestException, Timeout

logger = logging.getLogger(__name__)


class LLMAPIClient:
    """Client for interacting with OpenAPI compatible language model endpoints (like Ollama)"""

    def __init__(
        self,
        server_url: str,
        api_token: Optional[str] = None,
        model_name: str = "deepseek-r1:70b",
    ):
        self.server_url = server_url.rstrip("/")
        self.api_token = api_token
        self.model_name = model_name

    def _get_headers(self) -> Dict[str, str]:
        """Get request headers with optional authorization"""
        headers = {"Content-Type": "application/json"}

        if self.api_token:
            headers["Authorization"] = f"Bearer {self.api_token}"

        return headers

    def generate_completion(
        self, prompt: str, max_tokens: int = 1000, temperature: float = 0.3
    ) -> Optional[str]:
        """
        Generate a completion using the configured LLM

        Args:
            prompt: The prompt to send to the model
            max_tokens: Maximum number of tokens to generate
            temperature: Sampling temperature (0.0 = deterministic, 1.0 = very random)

        Returns:
            Generated text response or None if failed
        """
        try:
            # Try Ollama format first
            response = self._try_ollama_format(prompt, max_tokens, temperature)
            if response:
                return response

            # Fallback to OpenAI-compatible format
            return self._try_openai_format(prompt, max_tokens, temperature)

        except Exception as e:
            logger.error(f"Error generating completion: {e}")
            return None

    def _try_ollama_format(
        self, prompt: str, max_tokens: int, temperature: float
    ) -> Optional[str]:
        """Try Ollama API format"""
        try:
            url = f"{self.server_url}/api/generate"
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": False,
                "options": {"num_predict": max_tokens, "temperature": temperature},
            }

            response = requests.post(
                url,
                headers=self._get_headers(),
                json=payload,
                timeout=120,  # 2 minute timeout for LLM generation
            )

            if response.status_code == 200:
                result = response.json()
                return result.get("response", "").strip()
            else:
                return None

        except (RequestException, Timeout, json.JSONDecodeError):
            return None

    def _try_openai_format(
        self, prompt: str, max_tokens: int, temperature: float
    ) -> Optional[str]:
        """Try OpenAI-compatible API format"""
        try:
            url = f"{self.server_url}/v1/completions"
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "stream": False,
            }

            response = requests.post(
                url, headers=self._get_headers(), json=payload, timeout=120
            )

            if response.status_code == 200:
                result = response.json()
                choices = result.get("choices", [])
                if choices:
                    return choices[0].get("text", "").strip()
            else:
                pass

        except (RequestException, Timeout, json.JSONDecodeError):
            pass

        return None

    def test_connection(self) -> bool:
        """Test if the LLM API is available and responding"""
        try:
            # Test with a simple prompt
            response = self.generate_completion("Hello", max_tokens=10)
            return response is not None and len(response) > 0
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False


def get_llm_client() -> Optional[LLMAPIClient]:
    """Get configured LLM client instance"""
    server = os.environ.get("LLM_API_SERVER", "http://localhost:11434")
    token = os.environ.get("LLM_API_TOKEN")
    model = os.environ.get("LLM_MODEL_NAME", "deepseek-r1:70b")

    return LLMAPIClient(server, token, model)
