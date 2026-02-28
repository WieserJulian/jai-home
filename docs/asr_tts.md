# ASR & TTS Integration

## Overview

The project ships with optional **Automatic Speech Recognition (ASR)** and **Text‑to‑Speech (TTS)** capabilities. Both are designed to degrade gracefully when dependencies are missing, ensuring the core assistant remains functional.

## ASR (Speech‑to‑Text)

The `src.asr` module attempts to import the `whisper_cpp` library. If unavailable, the `listen` function returns an empty string, allowing the system to continue operating.

```python
try:
    from whisper_cpp import Whisper
except Exception:
    _HAS_WHISPER = False
```

When present, audio is captured with `sounddevice` and passed to Whisper for transcription.

## TTS (Text‑to‑Speech)

`src.tts` provides a `speak(text: str)` function that uses **Coqui TTS** when installed. The implementation follows a safe‑fallback strategy:

1. **Binary check** – If the `tts` CLI binary is missing, the function prints `[TTS] <text>`.
2. **Python‑API path** – If the optional `TTS` Python package is installed, the model loads lazily, is cached, and audio is written to a temporary WAV file.
3. **CLI fallback** – If the Python package is unavailable, the CLI is invoked.
4. **Input validation** – Text is validated before synthesis to mitigate injection or resource‑exhaustion attacks (non‑printable characters are rejected and the length is limited to 500 characters by default – configurable via `TTS_MAX_LENGTH`).

```python
if not shutil.which('tts'):
    print(f"[TTS] {text}")
    return

# Validate input
try:
    safe_text = _validate_text(text)
except ValueError as e:
    print(f"[TTS] Validation error: {e}")
    return
```

## Installation

### Python package (recommended)
```bash
pip install "TTS"          # Installs the Coqui TTS library and its dependencies
```

Set the model via the `TTS_MODEL` environment variable, e.g.:
```bash
export TTS_MODEL="tts_models/en/ljspeech/tacotron2-DDC"
```

### CLI fallback (optional)
If you prefer the original CLI approach, install the binary:
```bash
# On Ubuntu/Debian
sudo apt-get install tts
```
Or build from source following the Coqui TTS repository instructions.

## Usage example
```python
from src.tts import speak

speak("Hello, welcome to JAI Home!")
```

## Security considerations
- **Input sanitisation** – `_validate_text` ensures the text contains only printable characters and does not exceed the configured length (default 500 chars).
- **Subprocess safety** – The only external command executed is the `tts` binary (or `aplay` for playback). Arguments are never constructed from user‑provided data.
- **Dependency handling** – The Python library is optional; the system continues to work with a simple print fallback if dependencies are missing.

## Troubleshooting
- If you see `[TTS]` messages only, verify that the `tts` binary is on your `PATH` or that the `TTS` Python package is installed.
- Ensure the `TTS_MODEL` environment variable points to a valid model name.
- Check that `aplay` is installed for audio playback on Linux systems.

---
*Formatted according to the project’s documentation standards.*

## ASR (Speech‑to‑Text)

The `src.asr` module tries to import the `whisper_cpp` library. If it is not available, the `listen` function returns an empty string, allowing the system to continue operating.

```python
try:
    from whisper_cpp import Whisper
except Exception:
    _HAS_WHISPER = False
```

When the library is present, audio is captured with `sounddevice` and passed to Whisper for transcription.

## TTS (Text‑to‑Speech)

`src.tts` provides a `speak(text: str)` function that renders *text* using **Coqui TTS**. The implementation follows a safe‑fallback strategy:

1. **Binary check** – If the `tts` CLI binary is not found, the function simply prints `[TTS] <text>`.
2. **Python‑API path** – When the optional `TTS` Python package is installed, the model is loaded lazily, cached, and audio is written to a temporary WAV file.
3. **CLI fallback** – If the Python package is unavailable, the CLI is invoked.
4. **Input validation** – Text is validated before synthesis to mitigate injection or resource‑exhaustion attacks (non‑printable characters are rejected and the length is limited to 500 characters by default – configurable via `TTS_MAX_LENGTH`).

```python
if not shutil.which('tts'):
    print(f"[TTS] {text}")
    return

# Validate input
try:
    safe_text = _validate_text(text)
except ValueError as e:
    print(f"[TTS] Validation error: {e}")
    return
```

### Installation

#### Python package (recommended)
```bash
pip install "TTS"          # Installs the Coqui TTS library and its dependencies
```
*The library will download the required model on first use. Set the model via the `TTS_MODEL` environment variable, e.g.:
```bash
export TTS_MODEL="tts_models/en/ljspeech/tacotron2-DDC"
```

#### CLI fallback (optional)
If you prefer the original CLI approach, install the binary:
```bash
# On Ubuntu/Debian
sudo apt-get install tts
```
Or build from source following the Coqui TTS repository instructions.

### Usage example
```python
from src.tts import speak

speak("Hello, welcome to JAI Home!")
```

### Security considerations
- **Input sanitisation** – `_validate_text` ensures the text contains only printable characters and does not exceed the configured length (default 500 chars).
- **Subprocess safety** – The only external command executed is the `tts` binary (or `aplay` for playback). Arguments are never constructed from user‑provided data.
- **Dependency handling** – The Python library is optional; the system continues to work with a simple print fallback if dependencies are missing.

### Troubleshooting
- If you see `[TTS]` messages only, verify that the `tts` binary is on your `PATH` or that the `TTS` Python package is installed.
- Ensure the `TTS_MODEL` environment variable points to a valid model name.
- Check that `aplay` is installed for audio playback on Linux systems.
