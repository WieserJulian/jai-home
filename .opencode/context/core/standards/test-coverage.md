# Test Coverage Standards

- Write tests using **pytest**.
- Mock external services (HTTP, DB, hardware) with `responses`, `httpx‑mock`, or `unittest.mock`.
- Aim for **≥ 80 %** line coverage (run `pytest --cov=src`).
- Include both **unit** and **integration** tests where feasible.
- Name test files `test_*.py` and place them under the `tests/` directory.
