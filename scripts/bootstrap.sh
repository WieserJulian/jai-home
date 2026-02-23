#!/usr/bin/env bash
set -euo pipefail

# 1️⃣ Install Python deps (Poetry)
if ! command -v poetry >/dev/null; then
  echo "Installing Poetry…"
  curl -sSL https://install.python-poetry.org | python3 -
  export PATH="$HOME/.local/bin:$PATH"
fi
poetry install

# 2️⃣ Build & start the LLM containers
docker compose up -d --build

# 3️⃣ Pull a decent Ollama model (if you plan to use Ollama)
# Adjust the model name as you wish
if docker ps --filter "name=ollama" --format "{{.Names}}" | grep -q ollama; then
  docker exec -it ollama ollama pull phi3 || true
fi

echo "✅ All services are up."
echo "   - Ollama API   : http://localhost:11434"
echo "   - vLLM API    : http://localhost:8000"
echo "Run the voice loop with:"
echo "   poetry run python -m src.voice_loop"
