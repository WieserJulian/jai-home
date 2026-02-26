"""FastAPI endpoints for reading and updating the JAI Home configuration.

GET  /config   -> returns current config as JSON
POST /config   -> accepts JSON with optional keys 'backend' and 'model', writes config.yaml
"""

from fastapi import FastAPI, HTTPException, Body
import yaml
from pathlib import Path

from fastapi.staticfiles import StaticFiles


from .skill_manager import SkillManager

skill_manager = SkillManager()


app = FastAPI(title="JAI Home Config API")
app.mount("/", StaticFiles(directory=Path(__file__).resolve().parent / "static", html=True))

# Determine the repository root (two levels up from this file)
REPO_ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = REPO_ROOT / "config.yaml"

def load_current() -> dict:
    if CONFIG_PATH.is_file():
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            try:
                return yaml.safe_load(f) or {}
            except yaml.YAMLError as exc:
                raise HTTPException(status_code=500, detail=f"Invalid YAML: {exc}")
    return {}

def write_config(data: dict):
    # Merge with existing to keep unknown keys untouched
    current = load_current()
    current.update(data)
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        yaml.safe_dump(current, f)

@app.get("/config")
def get_config():
    return load_current()

@app.post("/config")
def update_config(payload: dict):
    allowed = {"backend", "model"}
    unknown = set(payload) - allowed
    if unknown:
        raise HTTPException(status_code=400, detail=f"Unknown keys: {', '.join(unknown)}")
    write_config(payload)
    return {"status": "ok", "config": load_current()}



@app.post("/ha/command")
def ha_command(payload: dict = Body(...)):
    """Receive a plain‑text command from Home Assistant and dispatch via the skill manager.
    Expects JSON like {"command": "turn on the kitchen light"}.
    Returns the skill's response string (or empty if no skill matches)."""
    command = payload.get("command", "")
    response = skill_manager.dispatch(command)
    return {"response": response}
