import importlib

def test_import_tts():
    try:
        tts = importlib.import_module('src.tts')
    except Exception as e:
        assert False, f"Failed to import src.tts: {e}"
    assert hasattr(tts, '__doc__')
