"""High‑level LLM interface for JAI Home.

Loads configuration on **each inference call** so that updates made via the
FastAPI ``/config`` endpoint take effect immediately (hot‑reload). The class
still caches the concrete backend client for efficiency, but will recreate it
if the backend or model settings have changed since the last call.
"""

import importlib
from .config import load_config
from .context import add_entry

# Mapping from backend name to module / class
_BACKEND_MAP = {
    "ollama": ("src.models.ollama", "OllamaLLM"),
    "vllm": ("src.models.vllm", "VLLMClient"),
    "openai": ("src.models.openai", "OpenAIClient"),
    "anthropic": ("src.models.anthropic", "AnthropicClient"),
    "copilot": ("src.models.copilot", "CopilotClient"),
}

class LLM:
    def __init__(self):
        # Hold the last loaded config to detect changes.
        self._last_cfg = None
        self.client = None
        self._load_client()

    def _load_client(self):
        cfg = load_config()
        backend = cfg.get("backend", "ollama").lower()
        model = cfg.get("model", "phi3")
        if backend not in _BACKEND_MAP:
            raise ValueError(f"Unsupported LLM backend: {backend}")
        module_name, class_name = _BACKEND_MAP[backend]
        module = importlib.import_module(module_name)
        client_cls = getattr(module, class_name)
        self.client = client_cls(model=model)
        self._last_cfg = {"backend": backend, "model": model}

    async def infer(self, prompt: str) -> str:
        """Run the LLM on *prompt* and store the exchange in the context DB.

        The configuration is reloaded on each call; if the backend or model has
        changed, a new client instance is created automatically.
        """
        # Reload config if it changed since the last inference.
        cfg = load_config()
        if cfg.get("backend", "ollama").lower() != self._last_cfg.get("backend") or \
           cfg.get("model", "phi3") != self._last_cfg.get("model"):
            self._load_client()
        # Prepend recent context (if any).
        try:
            from .context import get_recent
            context = get_recent(limit=3)
            if context:
                full_prompt = f"Context:\n{context}\n\nUser: {prompt}\nAssistant:"
            else:
                full_prompt = prompt
        except Exception:
            full_prompt = prompt
        response = await self.client.infer(full_prompt)
        # Store the exchange for future context.
        add_entry(prompt, response)
        return response

