# Developer Guide

## Testing & CI

- Unit tests live in the `tests/` directory.
- GitHub Actions workflow runs `pytest`, `ruff` lint, and `mypy` type checking.

## Extending the Project

- Add new modules under `src/`.
- Update `mkdocs.yml` to include new pages.
- Remember to add entries to `skills.yaml` for new voice commands.

## Hot‑reload

The `src.llm.LLM` class reloads `config.yaml` on every inference, so any changes made via the `/config` endpoint are applied instantly.
