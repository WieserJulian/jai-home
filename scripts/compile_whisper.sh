#!/usr/bin/env bash
set -euo pipefail

# Build Whisper.cpp for the host platform.
# Assumes you have cmake and a C++ compiler installed.

SRC_DIR="$(dirname "$0")/../src"
WHISPER_DIR="$SRC_DIR/whisper_cpp"
BUILD_DIR="$WHISPER_DIR/build"

if [ ! -d "$WHISPER_DIR" ]; then
  echo "Error: Whisper source not found at $WHISPER_DIR"
  exit 1
fi

mkdir -p "$BUILD_DIR"
cd "$BUILD_DIR"
cmake ..
make -j$(nproc)

echo "Whisper compiled successfully. Binary at $BUILD_DIR/whisper"
