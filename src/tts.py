import os
import subprocess
import tempfile


def speak(text: str):
    """Render *text* with Coqui TTS and play it via aplay (ALSA)."""
    model_id = os.getenv('TTS_MODEL', 'tts_models/en/ljspeech/tacotron2-DDC')
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as wav:
        subprocess.run(
            ['tts', '--text', text, '--model_name', model_id, '--out_path', wav.name],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        subprocess.run(['aplay', wav.name], check=True)
        os.unlink(wav.name)
