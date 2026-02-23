# JAI Home Voice Assistant

A self‑hosted, always‑on voice‑assistant that combines:

- **LLM back‑ends** – Ollama and vLLM (choose whichever fits your hardware).
- **Speech‑to‑text** – Whisper.cpp (local, no API keys).
- **Text‑to‑speech** – Coqui TTS (local, offline).
- **Docker orchestration** – containers for the models; the Python controller runs on the host so it can access the microphone/speaker.
- **Deployment options** – OpenClaw cron job or native systemd service for persistence.

## Quick‑Start Guide

1. **Prerequisites**
   - Docker & Docker‑Compose installed.
   - Python 3.11+ and `pip`.
   - Microphone & speaker configured on the host.

2. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/jai-home.git
   cd jai-home
   ```

3. **Start model containers**
   ```bash
   docker compose up -d
   ```
   This brings up Ollama and vLLM containers.

4. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   *(If `requirements.txt` is missing, the project uses only the standard library and the bundled scripts.)*

5. **Run the voice loop**
   ```bash
   python -m src.voice_loop
   ```
   The assistant will listen, process, and respond.

## Usage Examples

- **Ask a question**: Speak "Hey JAI, what’s the weather today?" and hear a spoken answer.
- **Control home devices**: Integrate your own home‑automation commands inside `src/llm.py`.
- **Run a one‑off command**:
  ```bash
  python -c "from src import llm; print(llm.run('Tell me a joke'))"
  ```

## Systemd Service

To keep JAI Home running after reboots, create a systemd service:

```ini
[Unit]
Description=JAI Home Voice Assistant
After=network.target docker.service

[Service]
Type=simple
WorkingDirectory=/home/$(whoami)/jaihome
ExecStart=/usr/bin/python -m src.voice_loop
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

1. Save the file as `~/jaihome/systemd/jai-voice.service` (already provided).
2. Enable and start the service:
   ```bash
   sudo cp systemd/jai-voice.service /etc/systemd/system/
   sudo systemctl daemon-reload
   sudo systemctl enable jai-voice.service
   sudo systemctl start jai-voice.service
   ```
3. Check its status:
   ```bash
   sudo systemctl status jai-voice.service
   ```

## Development

- Run tests:
  ```bash
  pytest
  ```
- Lint and type‑check locally:
  ```bash
  ruff check src
  mypy src
  ```

For a full CI pipeline see `.github/workflows/ci.yml`.

---

The repository contains a complete, ready‑to‑run setup. Follow the steps above to get started.
