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

def _run_coqui_tts(text: str) -> str:
    """Run the Coqui ``tts`` CLI and return the path to the generated WAV file.

    Raises ``subprocess.CalledProcessError`` if the command fails.
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
    wav_path = _run_coqui_tts(text)
    try:
        subprocess.run(['aplay', wav_path], check=False)
    finally:
        # Clean up temporary file.
        try:
            os.unlink(wav_path)
        except OSError:
            pass

