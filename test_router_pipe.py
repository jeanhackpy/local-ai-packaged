import asyncio
import unittest
from unittest.mock import MagicMock, patch
from router_pipe import Pipe

async def test_fast_path():
    print("Testing fast-path...")
    pipe = Pipe()
    # Mock the session to avoid actual network calls
    pipe.session = MagicMock()

    body = {
        "messages": [{"role": "user", "content": "Hi"}]
    }

    # This should NOT call evaluate_difficulty
    with patch.object(Pipe, 'evaluate_difficulty') as mock_eval:
        # Mock call_ollama
        pipe.call_ollama = MagicMock(return_value="Mocked response")

        response = await pipe.pipe(body)

        assert response == "Mocked response"
        mock_eval.assert_not_called()
        print("Fast-path test passed!")

async def test_difficulty_evaluation():
    print("Testing difficulty evaluation...")
    pipe = Pipe()
    pipe.session = MagicMock()

    # Mock response for difficulty evaluation
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"response": "Hard"}
    pipe.session.post.return_value = mock_response

    body = {
        "messages": [{"role": "user", "content": "This is a very long query that should be evaluated."}]
    }

    # Mock call_openrouter since "Hard" routes there by default
    pipe.call_openrouter = MagicMock(return_value="Cloud response")

    response = await pipe.pipe(body)

    assert response == "Cloud response"
    # Check if session.post was called for evaluation
    pipe.session.post.assert_called()
    call_args = pipe.session.post.call_args_list[0]
    assert "num_predict" in call_args.kwargs["json"]["options"]
    assert call_args.kwargs["json"]["options"]["num_predict"] == 5
    print("Difficulty evaluation test passed!")

async def main():
    try:
        await test_fast_path()
        await test_difficulty_evaluation()
        print("\nAll tests passed successfully!")
    except Exception as e:
        print(f"\nTest failed: {e}")
        import traceback
        traceback.print_exc()
        exit(1)

if __name__ == "__main__":
    asyncio.run(main())
