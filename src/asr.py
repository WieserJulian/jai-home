"""ASR module for JAI Home.

Attempts to use the ``whisper_cpp`` library (which wraps a compiled Whisper
binary). If the library cannot be imported – for example on a system without
the compiled extension – the function gracefully falls back to a **stub** that
returns an empty string. This keeps the rest of the pipeline operational
without requiring heavy dependencies.
"""

import os
import queue
import threading

# Optional heavy dependencies – import lazily and handle failures.
try:
    import numpy as np  # noqa: F401 (used by the real implementation)
    import sounddevice as sd  # noqa: F401
    from whisper_cpp import Whisper  # noqa: F401
    _HAS_WHISPER = True
except Exception:  # pragma: no cover – fallback path
    _HAS_WHISPER = False

# Load the Whisper model path (adjust via env if needed).
MODEL_PATH = os.getenv('WHISPER_MODEL', '/usr/share/whisper/models/ggml-base.en.bin')
if _HAS_WHISPER:
    whisper = Whisper(MODEL_PATH)
    q: queue.Queue = queue.Queue()
    def _audio_callback(indata, frames, time, status):
        if status:
            print(f"[ASR] {status}", flush=True)
        q.put(indata.copy())
else:
    # Stub placeholders – they will never be used.
    whisper = None
    q = None
    def _audio_callback(*args, **kwargs):
        pass

def listen(stop_event: threading.Event, sample_rate: int = 16000) -> str:
    """Record from the default microphone until a phrase is detected.

    Returns the transcribed text, or an empty string if the Whisper library is
    unavailable or no speech is detected.
    """
    if not _HAS_WHISPER:
        # Fallback – no ASR capability.
        return ""
    with sd.InputStream(
        samplerate=sample_rate,
        channels=1,
        dtype='int16',
        callback=_audio_callback,
    ):
        while not stop_event.is_set():
            try:
                chunk = q.get(timeout=0.1)
            except queue.Empty:
                continue
            result = whisper.transcribe(chunk.tobytes())
            if result.text.strip():
                return result.text.strip()
    return ""

