import importlib
import pytest
import sys
import os
from unittest import mock

# Ensure the project root is on sys.path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src import tts as tts_module

def test_import_tts():
    try:
        tts = importlib.import_module('src.tts')
    except Exception as e:
        assert False, f"Failed to import src.tts: {e}"
    assert hasattr(tts, '__doc__')

def test_speak_fallback_when_binary_missing(monkeypatch, capsys):
    # Simulate missing `tts` binary
    monkeypatch.setattr(tts_module.shutil, "which", lambda _: None)
    tts_module.speak("Hello world")
    captured = capsys.readouterr()
    assert "[TTS] Hello world" in captured.out

def test_speak_validates_input(monkeypatch, capsys):
    # Simulate binary present
    monkeypatch.setattr(tts_module.shutil, "which", lambda _: "/usr/bin/tts")
    # Mock the internal TTS call to avoid heavy dependencies
    monkeypatch.setattr(tts_module, "_run_coqui_tts", lambda text: "/tmp/fake.wav")
    # Mock subprocess.run (playback)
    mock_run = mock.MagicMock()
    monkeypatch.setattr(tts_module.subprocess, "run", mock_run)
    # Provide non‑printable characters – should trigger validation error
    tts_module.speak("Bad\x00Text")
    captured = capsys.readouterr()
    assert "Validation error" in captured.out
    mock_run.assert_not_called()

def test_speak_calls_coqui_when_available(monkeypatch):
    # Simulate binary present
    monkeypatch.setattr(tts_module.shutil, "which", lambda _: "/usr/bin/tts")
    # Mock validation to pass
    monkeypatch.setattr(tts_module, "_validate_text", lambda text: text)
    mock_tts = mock.MagicMock(return_value="/tmp/fake.wav")
    mock_play = mock.MagicMock()
    monkeypatch.setattr(tts_module, "_run_coqui_tts", mock_tts)
    monkeypatch.setattr(tts_module.subprocess, "run", mock_play)
    tts_module.speak("Test")
    mock_tts.assert_called_once_with("Test")
    mock_play.assert_called_once()
