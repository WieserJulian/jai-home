# Configuration UI

The FastAPI server exposes two endpoints that allow you to view and edit the runtime configuration without restarting the service.

## Endpoints

- **GET `/config`** – Returns the current `config.yaml` as JSON. Useful for confirming the current settings.
- **POST `/config`** – Accepts a JSON payload, e.g. `{ "backend": "vllm", "model": "meta-llama/…" }`, and merges it into `config.yaml`.

> **Note**: The LLM wrapper (`src.llm.LLM`) reloads the configuration on every inference, so changes take effect **immediately**.

## Example Usage
```bash
# Retrieve current configuration
curl http://localhost:8000/config

# Update model and backend
curl -X POST http://localhost:8000/config \
  -H "Content-Type: application/json" \
  -d '{"backend": "vllm", "model": "meta-llm/7b"}'
```

## Troubleshooting
- **404 on `/config`** – Ensure the FastAPI server is running on the correct host/port.
- **No change after POST** – Verify the JSON payload syntax and that the `config.yaml` file is writable by the service user.

---
*Formatted to the project’s documentation standards.*

The FastAPI server provides two endpoints:

- `GET /config` – returns the current `config.yaml` as JSON.
- `POST /config` – accepts `{ "backend": "vllm", "model": "meta-llama/..." }` and merges it into `config.yaml`.

Because the LLM wrapper (`src.llm.LLM`) reloads the configuration on every inference, changes take effect **immediately** without restarting the service.
