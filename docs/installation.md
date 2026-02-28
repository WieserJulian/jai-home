# Installation Guide

## Prerequisites
- Docker (for container deployment) **or** Systemd (for native service)
- Git (to clone the repository)
- Python 3.12+ (if installing from source)
- Optional: Home Assistant instance (for the add‑on)

## Installation Options

### Docker Compose
```bash
docker compose -f docker/compose.yml up -d
```
> Starts all required containers in the background.

### Systemd Service (native)
```bash
sudo cp systemd/jai-voice.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now jai-voice.service
```
> The service will restart automatically on system boot.

## Home Assistant Add‑on
Follow the official Home Assistant add‑on tutorial in the repository **README** and add the add‑on via the Supervisor UI.

## Verification
```bash
curl http://localhost:8000/health
```
If you receive a JSON response with `status: "ok"`, the assistant is running.

## Troubleshooting
- **Docker not starting** – ensure the Docker daemon is running and you have permission to use it.
- **Systemd fails** – check `journalctl -u jai-voice.service` for error logs.
- **Port conflict** – confirm that port 8000 (default) is free or adjust `config.yaml`.

---
*Documentation generated according to the project’s documentation standards.*

## Prerequisites
- Docker installed (if using Docker deployment)
- Systemd (for service installation)
- Home Assistant (optional, for add‑on)

## Docker
```bash
docker compose -f docker/compose.yml up -d
```

## Systemd Service
```bash
sudo cp systemd/jai-voice.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now jai-voice.service
```
```bash
docker compose -f docker/compose.yml up -d
```

## Systemd Service
Copy the service file and enable:
```bash
sudo cp systemd/jai-voice.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now jai-voice.service
```

## Home Assistant Add‑on
Follow the steps in the repository README to add the add‑on via Supervisor.

Follow the steps in the repository README to add the add‑on via Supervisor.
