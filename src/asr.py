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
from typing import Optional

# Optional heavy dependencies – import lazily and handle failures.
try:
    import numpy as np  # type: ignore  # noqa: F401 (used by the real implementation)
    import sounddevice as sd  # type: ignore  # noqa: F401
    from whisper_cpp import Whisper  # type: ignore  # noqa: F401

    _HAS_WHISPER = True
except Exception:  # pragma: no cover – fallback path
    _HAS_WHISPER = False

# Load the Whisper model path (adjust via env if needed).
MODEL_PATH = os.getenv('WHISPER_MODEL', '/usr/share/whisper/models/ggml-base.en.bin')

# Shared objects – initialized according to availability.
whisper: Optional["Whisper"] = None
q: Optional[queue.Queue] = None

if _HAS_WHISPER:
    whisper = Whisper(MODEL_PATH)
    q = queue.Queue()


def _audio_callback(*args, **kwargs):
    """Callback for sounddevice input stream.

    When Whisper is available, the first positional argument is the audio data
    (``indata``); we forward a copy to the processing queue. When Whisper is
    unavailable this function is a no‑op.
    """
    if not _HAS_WHISPER:
        return
    # ``indata`` is expected as the first positional argument.
    indata = args[0] if args else None
    if indata is not None and q is not None:
        q.put(indata.copy())


def listen(stop_event: threading.Event, sample_rate: int = 16000) -> str:
    """Record from the default microphone until a phrase is detected.

    Returns the transcribed text, or an empty string if the Whisper library is
    unavailable or no speech is detected.
    """
    if not _HAS_WHISPER:
        # Fallback – no ASR capability.
        return ""
    assert q is not None, "Queue should be initialized when Whisper is available"
    with sd.InputStream(
        samplerate=sample_rate,
        channels=1,
        dtype='int16',
        callback=_audio_callback,
    ):
        while not stop_event.is_set():
            try:
                chunk = q.get(timeout=0.5)  # type: ignore[arg-type]
            except queue.Empty:
                continue
            result = whisper.transcribe(chunk.tobytes())  # type: ignore[union-attr]
            if result.text.strip():
                return result.text.strip()
    return ""


