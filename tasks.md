# Project Tasks for JAI Home Voice Assistant

## 1️⃣ Configuration UI
- [x] Build a minimal FastAPI endpoint to read and write `config.yaml` (completed).
- [x] Add a simple HTML/JS config page (served by FastAPI).
- [ ] Implement hot‑reload: when config changes, the running LLM instance should pick up new values (e.g., signal via file watch or restart controller).

## 2️⃣ Real ASR/TTS Integration
- [ ] Compile Whisper.cpp for the host platform and wrap it in `src/asr.py` with a `listen(stop_event)` function.
- [ ] Install Coqui TTS models; implement `src/tts.py` with a `speak(text)` function that streams audio to the default speaker.
- [ ] Add fallback stubs if binaries are missing.
- [x] Added placeholder `asr.py` and `tts.py` files (basic implementations).
- [ ] Compile Whisper.cpp for the host platform and wrap it in `src/asr.py` with a `listen(stop_event)` function.
- [ ] Install Coqui TTS models; implement `src/tts.py` with a `speak(text)` function that streams audio to the default speaker.
- [ ] Add fallback stubs if binaries are missing.


## 3️⃣ Complete Backend Clients
- [ ] Implement `src/models/vllm.py` (async HTTP to vLLM server).
- [x] Added placeholder `vllm.py` (basic implementation).
- [ ] Implement `src/models/openai.py` (calls OpenAI API, using `OPENAI_API_KEY`).
- [x] Added placeholder `openai.py` (basic implementation).
- [ ] Implement `src/models/anthropic.py` (calls Anthropic API, using `ANTHROPIC_API_KEY`).
- [x] Added placeholder `anthropic.py` (basic implementation).
- [ ] Add unit tests with mocked HTTP responses.

## 4️⃣ Command / Skill Framework
- [x] Designed a `skills.yaml` format mapping voice phrases/regex to Python callables.
- [x] Added a dispatcher in `src/skill_manager.py` that loads the file and routes LLM responses or detected intents.
- [x] Provided example skill: "turn on the living‑room light" → HTTP POST to Home Assistant (placeholder functions in `src/skills/lighting.py`).

## 5️⃣ Conversation Context Persistence
- [x] Created `src/context.py` with SQLite persistence for recent conversation exchanges.
- [x] Modified `src/llm.py` to prepend recent context (up to 3 turns) to each LLM prompt.
- [ ] Create unit tests for context storage and retrieval.

## 6️⃣ Home Assistant Webhook
- [x] Added Home Assistant webhook endpoint (`/ha/command`) to `src/config_api.py` that forwards commands to the skill manager.
- [ ] Document HA integration steps in README.

## 7️⃣ Testing & CI
- [ ] Expand `tests/` with real inference tests using `responses` or `httpx-mock`.
- [ ] Add linting (`ruff check src`) and type‑checking (`mypy src`) steps to `.github/workflows/ci.yml`.
- [ ] Ensure CI runs on every push and PR.

## 8️⃣ Docker Refinement
- [ ] Convert the Python controller into a multi‑stage Docker build (builder → runtime image).
- [ ] Add healthcheck to the controller service.
- [ ] Set resource limits (CPU/Memory) and restart policy.

## 9️⃣ Documentation Improvements
- [ ] Auto‑generate API docs from FastAPI (Swagger UI) and link from README.
- [ ] Add quick‑start screenshots/gifs for the new UI.
- [ ] Write a CONTRIBUTING guide.

## 🔟 Optional Packaging
- [ ] Create a `setup.cfg`/`pyproject.toml` to build a pip wheel for the controller.
- [ ] Provide an entry‑point script (`jai-home`) that runs the voice loop without Docker.
- [ ] Document installation via `pip install jai-home`.
