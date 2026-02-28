# Documentation for JAI Home Voice Assistant
[Home](/docs/index.md) | [Installation](/docs/installation.md) | [Configuration UI](/docs/config_ui.md) | [ASR & TTS](/docs/asr_tts.md) | [Developer](/docs/developer.md) | [Skills](/docs/skills.md)

Welcome to the **JAI Home** project! This site provides an overview of the
architecture, installation instructions, usage guide, and developer reference.

## 🚀 Quick start
```bash
# Clone the repo
git clone https://github.com/youruser/jaihome.git
cd jaihome
# Install dependencies (example)
python -m pip install -r requirements.txt
# Start the FastAPI UI
uvicorn src.config_api:app --reload
```

## 📚 Contents
- **Installation** – Docker, systemd, Home Assistant add‑on.
- **Configuration UI** – Using the `/config` endpoint.
- **ASR / TTS** – How the Whisper‑cpp and Coqui TTS integrations work.
- **Skill framework** – Defining new voice commands.
- **Developer guide** – Extending the codebase, testing & CI.

---
Generated with **MkDocs**.