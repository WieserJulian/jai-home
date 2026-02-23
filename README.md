# JAI Home Voice Assistant

A self‑hosted, always‑on voice‑assistant that combines:

- **LLM back‑ends** – Ollama and vLLM (choose whichever fits your hardware).
- **Speech‑to‑text** – Whisper.cpp (local, no API keys).
- **Text‑to‑speech** – Coqui TTS (local, offline).
- **Docker orchestration** – containers for the models; the Python controller runs on the host so it can access the microphone/speaker.
- **Deployment options** – OpenClaw cron job or native systemd service for persistence.

The repository contains a complete, ready‑to‑run setup. See `README.md` for quick start instructions.
