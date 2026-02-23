import os
import httpx

class LLM:
    def __init__(self):
        self.backend = os.getenv('LLM_BACKEND', 'ollama')  # ollama | vllm
        if self.backend == 'ollama':
            self.base = os.getenv('OLLAMA_URL', 'http://localhost:11434/api/generate')
        elif self.backend == 'vllm':
            self.base = os.getenv('VLLM_URL', 'http://localhost:8000/v1/chat/completions')
        else:
            raise ValueError(f'Unsupported LLM_BACKEND={self.backend}')

    async def infer(self, prompt: str) -> str:
        async with httpx.AsyncClient(timeout=30.0) as client:
            if self.backend == 'ollama':
                payload = {'model': 'phi3', 'prompt': prompt, 'stream': False}
                resp = await client.post(self.base, json=payload)
                resp.raise_for_status()
                return resp.json().get('response', '')
            else:  # vLLM – OpenAI compatible
                payload = {
                    'model': os.getenv('VLLM_MODEL', 'meta-llama/Meta-Llama-3-8B-Instruct'),
                    'messages': [{'role': 'user', 'content': prompt}],
                    'temperature': 0.7,
                }
                resp = await client.post(self.base, json=payload)
                resp.raise_for_status()
                return resp.json()['choices'][0]['message']['content']
