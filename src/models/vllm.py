"""vLLM client – OpenAI compatible endpoint.

The vLLM server exposes the standard OpenAI ChatCompletions API.  We use a
minimal payload that works for most instruction‑tuned models.
"""

import os
import httpx  # type: ignore
from . import BaseLLM

class VLLMClient(BaseLLM):
    def __init__(self, model: str = "meta-llama/Meta-Llama-3-8B-Instruct"):
        self.base = os.getenv("VLLM_URL", "http://localhost:8000/v1/chat/completions")
        self.model = model

    async def infer(self, prompt: str) -> str:
        async with httpx.AsyncClient(timeout=30.0) as client:
            payload = {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,
            }
            resp = await client.post(self.base, json=payload)
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"]
