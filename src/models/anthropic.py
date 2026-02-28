"""Anthropic client – calls the Claude API.

Requires ``ANTHROPIC_API_KEY``.  The request format follows the official
Anthropic HTTP API (v1/complete).  For simplicity we use the ``messages``
style similar to OpenAI.
"""

import os
import httpx  # type: ignore
from . import BaseLLM

class AnthropicClient(BaseLLM):
    def __init__(self, model: str = "claude-2.1"):
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise RuntimeError("ANTHROPIC_API_KEY environment variable not set")
        self.base = "https://api.anthropic.com/v1/messages"
        self.model = model

    async def infer(self, prompt: str) -> str:
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "max_tokens": 1024,
            "messages": [{"role": "user", "content": prompt}],
        }
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(self.base, json=payload, headers=headers)  # type: ignore

            resp.raise_for_status()
            data = resp.json()
            return data["content"][0]["text"]
