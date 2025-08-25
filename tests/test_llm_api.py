#!/usr/bin/env python3
"""
Test for LLM API client with mocked OpenAPI/Ollama server connectivity
"""

import json
import os
import sys
import unittest
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from plugins.certification.llm_api import LLMAPIClient, get_llm_client


class TestLLMAPIClient(unittest.TestCase):
    """Test cases for LLM API client functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.client = LLMAPIClient(
            server_url="http://test-server.com",
            api_token="test-token",
            model_name="test-model",
        )

    @patch("plugins.certification.llm_api.requests.post")
    def test_generate_completion_ollama_success(self, mock_post):
        """Test generate_completion with successful Ollama format"""
        # Mock successful Ollama response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"response": "Generated text response"}
        mock_post.return_value = mock_response

        result = self.client.generate_completion("Test prompt", max_tokens=100, temperature=0.7)

        self.assertEqual(result, "Generated text response")
        mock_post.assert_called()

    @patch("plugins.certification.llm_api.requests.post")
    def test_generate_completion_openai_success(self, mock_post):
        """Test generate_completion with OpenAI format when Ollama fails"""
        # First call (Ollama) fails, second call (OpenAI) succeeds
        ollama_response = MagicMock()
        ollama_response.status_code = 404
        
        openai_response = MagicMock()
        openai_response.status_code = 200
        openai_response.json.return_value = {"choices": [{"text": "OpenAI response"}]}
        
        mock_post.side_effect = [ollama_response, openai_response]

        result = self.client.generate_completion("Test prompt")

        self.assertEqual(result, "OpenAI response")
        self.assertEqual(mock_post.call_count, 2)

    @patch("plugins.certification.llm_api.requests.post")
    def test_generate_completion_both_formats_fail(self, mock_post):
        """Test generate_completion returns None when both formats fail"""
        # Both API calls fail
        fail_response = MagicMock()
        fail_response.status_code = 500
        fail_response.text = "Internal Server Error"
        mock_post.return_value = fail_response

        result = self.client.generate_completion("Test prompt")

        self.assertIsNone(result)

    @patch("plugins.certification.llm_api.requests.post")
    def test_generate_completion_network_error(self, mock_post):
        """Test generate_completion handles network errors gracefully"""
        import requests
        
        mock_post.side_effect = requests.exceptions.RequestException("Network error")

        result = self.client.generate_completion("Test prompt")

        self.assertIsNone(result)

    @patch("plugins.certification.llm_api.requests.post")
    def test_generate_completion_timeout(self, mock_post):
        """Test generate_completion handles timeout"""
        import requests
        
        mock_post.side_effect = requests.exceptions.Timeout("Request timed out")

        result = self.client.generate_completion("Test prompt")

        self.assertIsNone(result)

    @patch("plugins.certification.llm_api.requests.post")
    def test_generate_completion_json_decode_error(self, mock_post):
        """Test generate_completion handles invalid JSON responses"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)
        mock_post.return_value = mock_response

        result = self.client.generate_completion("Test prompt")

        self.assertIsNone(result)

    @patch.object(LLMAPIClient, "generate_completion")
    def test_test_connection_success(self, mock_generate):
        """Test connection test with successful response"""
        mock_generate.return_value = "Hello response"

        result = self.client.test_connection()

        self.assertTrue(result)
        mock_generate.assert_called_once_with("Hello", max_tokens=10)

    @patch.object(LLMAPIClient, "generate_completion")
    def test_test_connection_failure(self, mock_generate):
        """Test connection test with failed response"""
        mock_generate.return_value = None

        result = self.client.test_connection()

        self.assertFalse(result)

    @patch.object(LLMAPIClient, "generate_completion")
    def test_test_connection_empty_response(self, mock_generate):
        """Test connection test with empty response"""
        mock_generate.return_value = ""

        result = self.client.test_connection()

        self.assertFalse(result)

    @patch.object(LLMAPIClient, "generate_completion")
    def test_test_connection_exception(self, mock_generate):
        """Test connection test handles exceptions"""
        mock_generate.side_effect = Exception("Connection error")

        result = self.client.test_connection()

        self.assertFalse(result)


class TestGetLLMClient(unittest.TestCase):
    """Test cases for get_llm_client function"""

    @patch.dict(os.environ, {}, clear=True)
    def test_get_llm_client_defaults(self):
        """Test get_llm_client with default values"""
        client = get_llm_client()

        self.assertIsNotNone(client)
        self.assertEqual(client.server_url, "http://localhost:11434")
        self.assertIsNone(client.api_token)
        self.assertEqual(client.model_name, "deepseek-r1:70b")

    @patch.dict(
        os.environ,
        {
            "LLM_API_SERVER": "http://custom-server.com",
            "LLM_API_TOKEN": "custom-token",
            "LLM_MODEL_NAME": "custom-model",
        },
    )
    def test_get_llm_client_with_env_vars(self):
        """Test get_llm_client with environment variables"""
        client = get_llm_client()

        self.assertIsNotNone(client)
        self.assertEqual(client.server_url, "http://custom-server.com")
        self.assertEqual(client.api_token, "custom-token")
        self.assertEqual(client.model_name, "custom-model")


if __name__ == "__main__":
    unittest.main()