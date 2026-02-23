#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

# Ensure containers are up (idempotent)
./scripts/bootstrap.sh

# Launch the voice loop; if it crashes the script exits with non‑zero status
poetry run python -m src.voice_loop
