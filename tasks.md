# Project Tasks for JAI Home Voice Assistant

## 1️⃣ Configuration UI
- [x] Implement hot‑reload so changes to `config.yaml` are automatically applied to the running LLM instance (via file‑watch or controller restart).
- [x] Provide a minimal FastAPI endpoint for reading and writing `config.yaml`.
- [x] Build a simple HTML/JavaScript configuration page served through FastAPI.

## 2️⃣ Real ASR/TTS Integration
- [x] Compile **Whisper.cpp** for the host platform and expose `listen(stop_event)` in `src/asr.py`.
- [x] Install Coqui TTS models and implement `speak(text)` in `src/tts.py` to stream audio to the default speaker.
- [x] Add graceful fallback stubs for missing binaries.
- [x] Write documentation for installation steps in `docs/asr_tts.md` (following the referenced style).

## 3️⃣ Backend Model Clients
- [x] Implement an asynchronous HTTP client for **vLLM** in `src/models/vllm.py`.
- [x] Implement an OpenAI API client in `src/models/openai.py` using `OPENAI_API_KEY`.
- [x] Implement an Anthropic API client in `src/models/anthropic.py` using `ANTHROPIC_API_KEY`.
- [x] Add unit tests for all model clients with mocked HTTP responses.

## 4️⃣ Command / Skill Framework
- [x] Define `skills.yaml` schema mapping voice phrases / regex to Python callables.
- [x] Build a dispatcher (`src/skill_manager.py`) that loads `skills.yaml` and routes intents to skill functions.
- [x] Provide example skill (e.g., "turn on the living‑room light" → HTTP POST to Home Assistant).

## 5️⃣ Conversation Context Persistence
- [x] Create SQLite‑backed context store (`src/context.py`) for recent conversation exchanges.
- [x] Modify LLM wrapper (`src/llm.py`) to prepend up to three previous turns to each prompt.
- [x] Write unit tests covering context storage, retrieval, and integration with the LLM pipeline.

## 6️⃣ Home Assistant Integration
- [x] Add FastAPI webhook (`/ha/command`) in `src/config_api.py` that forwards commands to the skill manager.
- [x] Document Home Assistant setup steps in the project README.

## 7️⃣ Testing & Continuous Integration
- [x] Expand test suite with real inference tests using `responses` or `httpx-mock`.
- [x] Integrate linting (`ruff`) and type‑checking (`mypy`) into CI workflow (`.github/workflows/ci.yml`).
- [x] Ensure CI runs on every push and pull request.

## 8️⃣ Docker Refinement
- [x] Convert the Python controller into a multi‑stage Docker build (builder → runtime image).
- [x] Add a health‑check endpoint for the controller container.
- [x] Configure resource limits (CPU / memory) and a restart policy for the Docker service.

## 9️⃣ Documentation Improvements
- [x] Auto‑generate FastAPI OpenAPI/Swagger documentation and link it from the README.
- [x] Add quick‑start screenshots or GIFs showing the new configuration UI.
- [x] Write a CONTRIBUTING guide outlining contribution workflow, code style, and testing expectations.

## 🔟 Optional Packaging
- [x] Create packaging metadata (`setup.cfg` / `pyproject.toml`) to build a pip‑installable wheel for the controller.
- [x] Provide an entry‑point script (`jai-home`) that starts the voice loop without Docker.
- [x] Document the pip‑installation process in the README.
