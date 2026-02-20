import unittest
from unittest.mock import patch, MagicMock, AsyncMock
import asyncio
import sys
import os
import httpx

# Add current directory to path so we can import router_pipe
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import router_pipe

class TestRouterPipe(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.pipe = router_pipe.Pipe()
        self.pipe.valves.openrouter_api_key = "test_key"

    async def asyncTearDown(self):
        await self.pipe.client.aclose()

    @patch('httpx.AsyncClient.post')
    async def test_evaluate_difficulty_easy(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"response": "This is Easy"}
        mock_post.return_value = mock_response

        difficulty = await self.pipe.evaluate_difficulty("Hello")
        self.assertEqual(difficulty, "Easy")
        mock_post.assert_called_once()

    @patch('httpx.AsyncClient.post')
    async def test_evaluate_difficulty_hard(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"response": "This is Hard"}
        mock_post.return_value = mock_response

        difficulty = await self.pipe.evaluate_difficulty("Explain quantum physics in great detail with examples")
        self.assertEqual(difficulty, "Hard")

    @patch('httpx.AsyncClient.post')
    async def test_pipe_heuristic_short_query(self, mock_post):
        body = {"messages": [{"role": "user", "content": "Hi"}]}

        # Mock for call_ollama which will be called
        mock_resp_ollama = MagicMock()
        mock_resp_ollama.status_code = 200
        mock_resp_ollama.json.return_value = {"message": {"content": "Hello!"}}
        mock_post.return_value = mock_resp_ollama

        response = await self.pipe.pipe(body)

        self.assertEqual(response, "Hello!")
        # Should only be called ONCE (for call_ollama), NOT for evaluate_difficulty
        self.assertEqual(mock_post.call_count, 1)

        # Verify it went to ollama and NOT evaluate_difficulty
        args, kwargs = mock_post.call_args
        self.assertIn("/api/chat", args[0])
        self.assertNotIn("/api/generate", args[0])

    @patch('httpx.AsyncClient.post')
    async def test_pipe_routing_hard_long_query(self, mock_post):
        # First call for difficulty (Hard), second for openrouter
        mock_resp_diff = MagicMock()
        mock_resp_diff.status_code = 200
        mock_resp_diff.json.return_value = {"response": "Hard"}

        mock_resp_cloud = MagicMock()
        mock_resp_cloud.status_code = 200
        mock_resp_cloud.json.return_value = {"choices": [{"message": {"content": "Cloud response"}}]}

        mock_post.side_effect = [mock_resp_diff, mock_resp_cloud]

        body = {"messages": [{"role": "user", "content": "Explain quantum physics in great detail please."}]}
        response = await self.pipe.pipe(body)

        self.assertEqual(response, "Cloud response")
        self.assertEqual(mock_post.call_count, 2)

        # Verify calls
        call1_args = mock_post.call_args_list[0][0][0]
        call2_args = mock_post.call_args_list[1][0][0]
        self.assertIn("/api/generate", call1_args)
        self.assertIn("openrouter.ai", call2_args)

if __name__ == '__main__':
    unittest.main()
