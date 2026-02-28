# Code Review Workflow

1. Run **ruff** lint and **mypy** type check.
2. Run the full **pytest** suite.
3. Verify security considerations (no secrets in code, safe subprocess usage).
4. Ensure documentation updates are present if code changes affect user‑facing behavior.
5. Approve or request changes before merging.
