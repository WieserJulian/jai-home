# ASR & TTS Integration

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

`src.tts` uses the Coqui TTS CLI (`tts`). If the binary is missing, it simply prints `[TTS] <text>`.

```python
if not shutil.which('tts'):
    print(f"[TTS] {text}")
```

Both modules are designed to fail gracefully, enabling development on machines without the heavy dependencies.
