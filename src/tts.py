"""TTS module for JAI Home.

Uses the Coqui TTS command‑line interface (``tts``) to synthesize speech and
plays the resulting WAV file with ``aplay``. If the ``tts`` binary cannot be
found, the function falls back to printing ``[TTS] <text>`` so the rest of the
pipeline continues to work without external dependencies.
"""

import os
import shutil
import subprocess
import tempfile

# Optional heavy dependency – Coqui TTS Python library
try:
    from TTS.api import TTS as CoquiTTS  # type: ignore
    _HAS_COQUI_TTS = True
except Exception:
    _HAS_COQUI_TTS = False

# Cache the TTS instance to avoid reloading model on every call
_TTS_INSTANCE = None


def _run_coqui_tts(text: str) -> str:
    """Generate speech using Coqui TTS Python API (if available).

    Returns the path to a temporary WAV file containing the synthesized audio.
    """
    global _TTS_INSTANCE
    model_id = os.getenv('TTS_MODEL', 'tts_models/en/ljspeech/tacotron2-DDC')
    # Initialize TTS instance lazily
    if _TTS_INSTANCE is None:
        if _HAS_COQUI_TTS:
            # Load model; CoquiTTS will download if not cached
            _TTS_INSTANCE = CoquiTTS(model_name=model_id, progress_bar=False, gpu=False)
        else:
            # Fallback to CLI implementation below
            return _run_coqui_cli_tts(text)
    # Use the instance to generate audio to a temporary file
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as wav:
        _TTS_INSTANCE.tts_to_file(text=text, file_path=wav.name)
        return wav.name

def _validate_text(text: str) -> str:
    """Validate input text before sending to TTS.

    * Reject non‑printable characters.
    * Limit length to 500 characters (adjustable via env var).
    Returns a sanitized string or raises ``ValueError``.
    """
    max_len = int(os.getenv('TTS_MAX_LENGTH', '500'))
    if len(text) > max_len:
        raise ValueError(f"Text exceeds maximum length of {max_len} characters")
    # Ensure all characters are printable (excluding control chars)
    if not all(c.isprintable() for c in text):
        raise ValueError("Text contains non‑printable characters")
    return text

def _run_coqui_cli_tts(text: str) -> str:
    """Run the Coqui ``tts`` CLI and return the path to the generated WAV file.

    This is used when the Python library is not installed.
    """
    model_id = os.getenv('TTS_MODEL', 'tts_models/en/ljspeech/tacotron2-DDC')
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as wav:
        subprocess.run(
            ['tts', '--text', text, '--model_name', model_id, '--out_path', wav.name],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return wav.name


def speak(text: str) -> None:
    """Render *text* with Coqui TTS and play it.

    If the ``tts`` binary is missing, falls back to a simple ``print``
    with a ``[TTS]`` prefix.
    """
    if not shutil.which('tts'):
        print(f"[TTS] {text}")
        return
    # Validate text before synthesis to mitigate injection / resource‑exhaustion risks
    try:
        safe_text = _validate_text(text)
    except ValueError as e:
        # Log the validation error and fall back to simple print
        print(f"[TTS] Validation error: {e}")
        return
    wav_path = _run_coqui_tts(safe_text)

    try:
        subprocess.run(['aplay', wav_path], check=False)
    finally:
        # Clean up temporary file.
        try:
            os.unlink(wav_path)
        except OSError:
            pass

