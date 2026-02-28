"""OpenAI client – uses the official ChatCompletion endpoint.

The implementation is deliberately lightweight and only requires the
``OPENAI_API_KEY`` environment variable.  If the key is missing, a clear
RuntimeError is raised.
"""

import os
import httpx  # type: ignore
from . import BaseLLM

class OpenAIClient(BaseLLM):
    def __init__(self, model: str = "gpt-3.5-turbo"):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY environment variable not set")
        self.base = "https://api.openai.com/v1/chat/completions"
        self.model = model

    async def infer(self, prompt: str) -> str:
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
        }
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(self.base, json=payload, headers=headers)
            resp.raise_for_status()
            return resp.json()["choices"][0]["message"]["content"]
