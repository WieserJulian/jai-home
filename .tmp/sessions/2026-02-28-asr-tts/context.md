# Task Context : ASR/TTS Integration & Security

## Session ID : 2026‑02‑28‑asr‑tts

## Created at : 2026‑02‑28T12:34:56Z

## Current Request
- Finish **Coqui TTS** Python‑API integration in `src/tts.py` (lazy‑load, caching, fallback to CLI).
- Add **input validation** to guard against unsafe text (non‑printable characters, length > 500 chars).
- Run a **Bandit** security scan on the modified files.
- Update **documentation** (`docs/asr_tts.md`) with install steps, usage examples, and security notes.
- Extend the **CI workflow** (`.github/workflows/ci.yml`) to include a Bandit step.
- Add **unit & integration tests** for the new TTS functionality.
- Ensure all code passes **ruff**, **mypy**, and **pytest** with ≥ 80 % coverage.

## Context Files (Standards to Follow)
- `.opencode/context/core/standards/code-quality.md`
- `.opencode/context/core/standards/test-coverage.md`
- `.opencode/context/core/standards/documentation.md`
- `.opencode/context/core/workflows/code-review.md`

## Reference Files (Source files to modify)
- `src/tts.py`
- `docs/asr_tts.md`
- `.github/workflows/ci.yml`
- `tests/test_tts.py` (new file)

## External Docs
- Coqui TTS Python API documentation (model loading, `tts_to_file`).

## Components
- **TTS Engine** – Coqui TTS Python library or CLI wrapper.
- **Security** – Bandit scan, input sanitisation.
- **Docs** – Installation & usage guide.
- **CI** – Lint, type‑check, tests, security.

## Constraints
- Must keep the fallback behaviour (`[TTS] <text>`) when the binary is missing.
- Avoid heavy‑weight dependencies on CI machines – download models lazily.

## Exit Criteria
- [ ] `src/tts.py` implements lazy‑loaded Coqui TTS with validation.
- [ ] Bandit reports **no high‑severity findings**.
- [ ] `docs/asr_tts.md` reflects the new implementation.
- [ ] CI runs successfully with the additional Bandit step.
- [ ] Tests pass and coverage ≥ 80 %.
