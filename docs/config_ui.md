# Configuration UI

The FastAPI server provides two endpoints:

- `GET /config` – returns the current `config.yaml` as JSON.
- `POST /config` – accepts `{ "backend": "vllm", "model": "meta-llama/..." }` and merges it into `config.yaml`.

Because the LLM wrapper (`src.llm.LLM`) reloads the configuration on every inference, changes take effect **immediately** without restarting the service.
