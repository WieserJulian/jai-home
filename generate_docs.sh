#!/usr/bin/env bash
set -e
# Move to the directory where the script resides (project root)
cd "$(dirname "${BASH_SOURCE[0]}")"

# Ensure the docs folder exists
mkdir -p docs

# Generate documentation with Codex (full‑auto mode, runs inside a git repo)
codex exec --full-auto "Create comprehensive documentation in markdown for this project, including README.md, CONTRIBUTING.md, ARCHITECTURE.md, and usage examples. Place them in the docs/ folder, add them to the repo, commit with message \"Add project documentation\", and push to origin."

echo "Documentation generation finished."
