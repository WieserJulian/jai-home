# Installation Guide

## Docker
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
