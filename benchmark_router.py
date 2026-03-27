import asyncio
import time
import unittest.mock as mock
from router_pipe import Pipe

def mocked_post(url, **kwargs):
    response = mock.Mock()
    response.status_code = 200
    if "/api/generate" in url:
        time.sleep(0.2) # 200ms delay for evaluation
        response.json.return_value = {"response": "Easy"}
    elif "/api/chat" in url or "openrouter.ai" in url:
        time.sleep(0.5) # 500ms delay for model response
        if "openrouter" in url:
             response.json.return_value = {"choices": [{"message": {"content": "OpenRouter response"}}]}
        else:
             response.json.return_value = {"message": {"content": "Ollama response"}}
    return response

async def run_benchmark():
    pipe = Pipe()
    pipe.valves.openrouter_api_key = "test_key"

    print("--- Benchmark ---")

    # Short query
    body_short = {"messages": [{"role": "user", "content": "Hi"}]}
    start = time.perf_counter()
    await pipe.pipe(body_short)
    end = time.perf_counter()
    print(f"Short query (< 15 chars) time: {end - start:.3f}s")

    # Long query
    body_long = {"messages": [{"role": "user", "content": "Tell me a long story about a robot who wanted to become a professional chef."}]}
    start = time.perf_counter()
    await pipe.pipe(body_long)
    end = time.perf_counter()
    print(f"Long query (> 15 chars) time: {end - start:.3f}s")

    # Concurrent queries (simulating 5 users)
    print("\nConcurrent queries (5 users):")
    bodies = [{"messages": [{"role": "user", "content": f"Query {i} that is long enough to trigger evaluation"}]} for i in range(5)]
    start = time.perf_counter()
    await asyncio.gather(*(pipe.pipe(body) for body in bodies))
    end = time.perf_counter()
    print(f"Total time for 5 concurrent queries: {end - start:.3f}s")

if __name__ == "__main__":
    with mock.patch("requests.post", side_effect=mocked_post):
        asyncio.run(run_benchmark())
