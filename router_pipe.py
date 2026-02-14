"""
title: LLM Router Pipe
version: 1.0.0
description: Routes queries between local and cloud models based on difficulty evaluation and privacy settings.
"""

import httpx
import json
from typing import Optional, Callable, Awaitable
from pydantic import BaseModel, Field

class Pipe:
    class Valves(BaseModel):
        ollama_url: str = Field(
            default="http://ollama:11434",
            description="URL for the local Ollama instance"
        )
        eval_model: str = Field(
            default="granite4:350m",
            description="Local model used to evaluate query difficulty"
        )
        easy_model: str = Field(
            default="qwen2.5:7b-instruct-q4_K_M",
            description="Model to use for Easy queries (usually local)"
        )
        hard_model: str = Field(
            default="openrouter/anthropic/claude-3-haiku",
            description="Model to use for Hard queries (routed through OpenClaw)"
        )
        privacy_mode: bool = Field(
            default=False,
            description="If True, all queries are routed to the local Easy model regardless of difficulty"
        )
        openrouter_api_key: str = Field(
            default="",
            description="API Key for OpenRouter (if calling direct)"
        )


    def __init__(self):
        self.type = "pipe"
        self.id = "llm_router"
        self.name = "LLM Router"
        self.valves = self.Valves()
        # Bolt: Initialize AsyncClient for connection pooling across the pipe's lifetime
        self.client = httpx.AsyncClient()

    async def pipe(
        self,
        body: dict,
        __user__: Optional[dict] = None,
        __event_emitter__: Callable[[dict], Awaitable[None]] = None,
        __event_call__: Callable[[dict], Awaitable[dict]] = None,
    ) -> Optional[dict]:
        messages = body.get("messages", [])
        if not messages:
            return "No messages found."

        user_query = messages[-1]["content"]

        if self.valves.privacy_mode:
            selected_model = self.valves.easy_model
            route_reason = "Privacy Mode Enabled"
        elif len(user_query.strip()) < 15:
            # Bolt: Fast path for very short queries (greetings, simple confirmations)
            # Saves a network call and LLM inference for trivial inputs
            selected_model = self.valves.easy_model
            route_reason = "Short Query -> Routing to Local (Fast Path)"
        else:
            # Evaluate difficulty
            difficulty = await self.evaluate_difficulty(user_query)
            if difficulty == "Hard":
                selected_model = self.valves.hard_model
                route_reason = "Evaluated as Hard -> Routing to Cloud"
            else:
                selected_model = self.valves.easy_model
                route_reason = "Evaluated as Easy -> Routing to Local"

        if __event_emitter__:
            await __event_emitter__({
                "type": "status",
                "data": {
                    "description": f"Routing: {route_reason} ({selected_model})",
                    "done": False
                }
            })

        # Bolt: Use await for asynchronous model calls
        if selected_model.startswith("openrouter/"):
            response = await self.call_openrouter(selected_model, body)
        else:
            response = await self.call_ollama(selected_model, body)

        if __event_emitter__:
            await __event_emitter__({
                "type": "status",
                "data": {
                    "description": "Response received",
                    "done": True
                }
            })

        return response

    async def evaluate_difficulty(self, query: str) -> str:
        prompt = f"Evaluate the difficulty of the following user query. Respond with only one word: 'Easy' or 'Hard'.\n\nQuery: {query}\n\nDifficulty:"
        try:
            payload = {
                "model": self.valves.eval_model,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0}
            }
            # Bolt: Use async client and explicit timeout
            response = await self.client.post(
                f"{self.valves.ollama_url}/api/generate",
                json=payload,
                timeout=10.0
            )
            if response.status_code == 200:
                result = response.json().get("response", "").strip()
                return "Hard" if "Hard" in result else "Easy"
        except Exception as e:
            print(f"Error evaluating difficulty: {e}")
        return "Easy" # Default to Easy/Local on error

    async def call_ollama(self, model: str, body: dict) -> str:
        # Strip the provider prefix if present
        model_id = model.split("/")[-1] if "/" in model else model
        payload = {
            "model": model_id,
            "messages": body.get("messages", []),
            "stream": False
        }
        try:
            # Bolt: Use async client and explicit timeout for inference
            response = await self.client.post(
                f"{self.valves.ollama_url}/api/chat",
                json=payload,
                timeout=60.0
            )
            if response.status_code == 200:
                return response.json()["message"]["content"]
            else:
                return f"Error from Ollama: {response.status_code} - {response.text}"
        except Exception as e:
            return f"Error calling Ollama: {str(e)}"

    async def call_openrouter(self, model: str, body: dict) -> str:
        # Clean model name for OpenRouter
        model_id = model.replace("openrouter/", "")
        headers = {
            "Authorization": f"Bearer {self.valves.openrouter_api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": model_id,
            "messages": body.get("messages", []),
        }
        try:
            # Bolt: Use async client and explicit timeout for cloud inference
            response = await self.client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=60.0
            )
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            else:
                return f"Error from OpenRouter: {response.status_code} - {response.text}"
        except Exception as e:
            return f"Error calling OpenRouter: {str(e)}"
