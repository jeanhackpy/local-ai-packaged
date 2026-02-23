
import asyncio
import json
import sys
from unittest.mock import MagicMock, AsyncMock, patch
import httpx

import router_pipe

async def test_router_error_leakage():
    pipe = router_pipe.Pipe()
    pipe.valves.ollama_url = "http://mock-ollama"

    body = {"messages": [{"role": "user", "content": "hello"}]}

    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_response.text = "OLLAMA_CRASH_DUMP: Secret=ABC456"

    # Mocking difficulty evaluation to return Easy
    mock_eval_response = MagicMock()
    mock_eval_response.status_code = 200
    mock_eval_response.json.return_value = {"response": "Easy"}

    with patch('httpx.AsyncClient.post', side_effect=[mock_eval_response, mock_response]):
        event_emitter = AsyncMock()

        result = await pipe.pipe(body, __event_emitter__=event_emitter)
        print(f"Result: {result}")

        if "Secret=ABC456" in str(result):
            print("VULNERABILITY STILL PRESENT: Secret leaked in result!")
        elif "An error occurred while communicating with the local model" in str(result):
            print("SUCCESS: Vulnerability fixed. Generic error message returned.")
        else:
            print(f"Unexpected result: {result}")

if __name__ == "__main__":
    asyncio.run(test_router_error_leakage())
