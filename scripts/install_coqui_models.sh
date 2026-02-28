#!/usr/bin/env bash
set -euo pipefail

# Download Coqui TTS model and place it under the project.
# Default model: LJSpeech Tacotron2‑DDC.

MODEL_URL="https://huggingface.co/coqui/tts_models_en_ljspeech_tacotron2-DDC/resolve/main/tacotron2-DDC.tar.gz"
TARGET_DIR="$(dirname "$0")/../models/coqui"

mkdir -p "$TARGET_DIR"

echo "Downloading Coqui TTS model..."
curl -L "$MODEL_URL" -o /tmp/coqui_model.tar.gz

tar -xzf /tmp/coqui_model.tar.gz -C "$TARGET_DIR" --strip-components=1

echo "Model installed to $TARGET_DIR"
