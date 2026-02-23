#!/usr/bin/env bash
set -euo pipefail

# Verify we are running inside Home Assistant (ha CLI available)
if ! command -v ha &>/dev/null; then
  echo "Error: This script must be run from a Home Assistant host with the 'ha' CLI."
  exit 1
fi

# Temporary directory for cloning the repo
TMPDIR=$(mktemp -d)

git clone https://github.com/WieserJulian/jai-home.git "$TMPDIR"

# Destination for the local add‑on repository
ADDON_DIR="/addons/jai_home"
mkdir -p "$ADDON_DIR"

# Copy Docker‑related files and descriptor
cp -r "$TMPDIR/docker/." "$ADDON_DIR/"
cp "$TMPDIR/docker/config.json" "$ADDON_DIR/config.json"

# Register the local repository with Home Assistant
ha addons repository add --name "JAI Home" "file:///addons"

# Build and start the add‑on (re‑install forces a rebuild)
ha addons reinstall jai_home

echo "✅ JAI Home add‑on installed and running."
