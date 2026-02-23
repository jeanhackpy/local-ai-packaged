
import asyncio
import json
import sys
from unittest.mock import MagicMock, AsyncMock, patch
import httpx

import n8n_pipe

async def test_n8n_error_leakage():
    pipe = n8n_pipe.Pipe()
    pipe.valves.n8n_url = "http://mock-n8n/webhook"
    pipe.valves.n8n_bearer_token = "test-token"

    body = {"messages": [{"role": "user", "content": "hello"}]}

    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_response.text = "INTERNAL_DATABASE_ERROR: SecretKey=XYZ123"

    # We need to mock httpx.AsyncClient.post
    with patch('httpx.AsyncClient.post', return_value=mock_response):
        event_emitter = AsyncMock()
        event_emitter.__closure__ = []

        result = await pipe.pipe(body, __event_emitter__=event_emitter)
        print(f"Result: {result}")

        leaked = False
        if "SecretKey=XYZ123" in str(result):
            print("VULNERABILITY STILL PRESENT: Secret leaked in result!")
            leaked = True

        if not leaked and "An error occurred while communicating with the agent workflow" in str(result):
            print("SUCCESS: Vulnerability fixed. Generic error message returned.")

if __name__ == "__main__":
    asyncio.run(test_n8n_error_leakage())
