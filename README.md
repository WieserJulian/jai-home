# JAI Home Voice Assistant

A self‑hosted, always‑on voice‑assistant that combines:

- **LLM back‑ends** – Ollama and vLLM (choose whichever fits your hardware).
- **Speech‑to‑text** – Whisper.cpp (local, no API keys).
- **Text‑to‑speech** – Coqui TTS (local, offline).
- **Docker orchestration** – containers for the models; the Python controller runs on the host so it can access the microphone/speaker.
- **Deployment options** – Home Assistant add‑on, systemd service, or plain Docker.

---

## Installation

### 1️⃣ As a Home Assistant Add‑on (recommended)

1. Open **Supervisor → Add‑on Store** in Home Assistant.
2. Click the **⋮** menu → **Repositories**.
3. Add the URL `https://github.com/WieserJulian/jai-home` and press **Add**.
4. The **JAI Home Voice Assistant** add‑on appears – click **Install**.
5. After the build finishes, enable **Start on boot** and press **Start**.

*If you prefer a manual one‑liner, run the helper script from the Home Assistant host terminal:*

```bash
bash <(curl -sSL https://raw.githubusercontent.com/WieserJulian/jai-home/main/scripts/install_addon.sh)
```

---

### 2️⃣ Stand‑alone systemd service (any Linux box)

1. Ensure Docker & Docker‑Compose are installed.
2. Copy the provided service file and enable it:

```bash
sudo cp systemd/jai-voice.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now jai-voice.service
```

The service runs the Docker compose stack defined in `docker/compose.yml`.

---

### 3️⃣ Manual Docker run (quick test)

```bash
cd /path/to/jai-home/docker
docker compose up -d   # starts Ollama, vLLM and the voice‑loop container
```

---

## Quick‑Start (after installation)

1. **Prerequisites** – Docker, Python 3.11+, microphone & speaker.
2. **Clone (if you used the manual method)**
   ```bash
   git clone https://github.com/WieserJulian/jai-home.git
   cd jai-home
   ```
3. **Start the containers** (already done by the add‑on or systemd service).
4. **Run the voice loop manually** (optional, for debugging):
   ```bash
   python -m src.voice_loop
   ```

---

## Usage Examples

- **Ask a question** – speak "Hey JAI, what’s the weather today?".
- **Control devices** – add your own commands inside `src/llm.py`.
- **One‑off Python call**:
  ```python
  from src import llm
  print(llm.run('Tell me a joke'))
  ```

---

## Development

- Run tests:
  ```bash
  pytest
  ```
- Lint & type‑check:
  ```bash
  ruff check src
  mypy src
  ```
- CI pipeline (GitHub Actions) is defined in `.github/workflows/ci.yml`.

---

The repository contains a complete, ready‑to‑run setup. Choose the installation method that fits your environment and enjoy a local, privacy‑first voice assistant.

