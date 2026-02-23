import os
import queue
import threading
import numpy as np
import sounddevice as sd
from whisper_cpp import Whisper

# Load the Whisper.cpp model (adjust path in .env if needed)
MODEL_PATH = os.getenv('WHISPER_MODEL', '/usr/share/whisper/models/ggml-base.en.bin')
whisper = Whisper(MODEL_PATH)

q: queue.Queue = queue.Queue()

def _audio_callback(indata, frames, time, status):
    if status:
        print(f"[ASR] {status}", flush=True)
    q.put(indata.copy())

def listen(stop_event: threading.Event, sample_rate: int = 16000) -> str:
    """Record from the default mic until a phrase is detected.
    Returns the transcribed text (empty string on timeout)."""
    with sd.InputStream(samplerate=sample_rate,
                        channels=1,
                        dtype='int16',
                        callback=_audio_callback):
        while not stop_event.is_set():
            try:
                chunk = q.get(timeout=0.1)
            except queue.Empty:
                continue
            result = whisper.transcribe(chunk.tobytes())
            if result.text.strip():
                return result.text.strip()
    return ''
