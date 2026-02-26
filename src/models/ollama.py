"""Ollama LLM client.

The Ollama API is simple – a POST to ``/api/generate`` with ``model`` and
``prompt`` fields.  This client mirrors the original implementation but lives
in the unified model layer.
"""

import os
import httpx
from . import BaseLLM

class OllamaLLM(BaseLLM):
    def __init__(self, model: str = "phi3"):
        self.base = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
        self.model = model

    async def infer(self, prompt: str) -> str:
        async with httpx.AsyncClient(timeout=30.0) as client:
            payload = {"model": self.model, "prompt": prompt, "stream": False}
            resp = await client.post(self.base, json=payload)
            resp.raise_for_status()
            return resp.json().get("response", "")
