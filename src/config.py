"""Configuration handling for JAI Home.

The configuration is read from a ``config.yaml`` file located at the project root
(or any path pointed to by the ``JAI_CONFIG`` environment variable).  The file
has a very small schema – currently only the LLM backend and an optional model
name are needed:

```yaml
backend: ollama   # one of: ollama, vllm, openai, anthropic, copilot
model: phi3       # provider‑specific model identifier (optional)
```

If the file does not exist, sensible defaults are used (``ollama`` backend and
the ``phi3`` model).  Environment variables ``LLM_BACKEND`` and ``LLM_MODEL``
override the YAML values, making it easy to switch backends at runtime.
"""

import os
import yaml  # type: ignore

from pathlib import Path

DEFAULT_CONFIG = {
    "backend": "ollama",
    "model": "phi3",
}

def load_config() -> dict:
    """Load configuration from YAML file or fall back to defaults.

    The lookup order is:
    1. ``JAI_CONFIG`` environment variable – path to a YAML file.
    2. ``config.yaml`` in the repository root.
    3. Built‑in defaults.
    """
    config_path_env = os.getenv("JAI_CONFIG")
    if config_path_env:
        config_path = Path(config_path_env)
    else:
        # repository root is two levels up from this file (src/ -> project root)
        config_path = Path(__file__).resolve().parents[2] / "config.yaml"

    if config_path.is_file():
        with open(config_path, "r", encoding="utf-8") as f:
            try:
                user_cfg = yaml.safe_load(f) or {}
            except yaml.YAMLError as exc:
                raise RuntimeError(f"Invalid YAML in {config_path}: {exc}")
        cfg = {**DEFAULT_CONFIG, **user_cfg}
    else:
        cfg = DEFAULT_CONFIG.copy()

    # Environment overrides – they have highest priority
    cfg["backend"] = os.getenv("LLM_BACKEND", cfg.get("backend", "ollama"))
    cfg["model"] = os.getenv("LLM_MODEL", cfg.get("model", "phi3"))
    return cfg
