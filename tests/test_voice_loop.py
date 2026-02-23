import importlib

def test_import_voice_loop():
    try:
        vl = importlib.import_module('src.voice_loop')
    except Exception as e:
        assert False, f"Failed to import src.voice_loop: {e}"
    assert hasattr(vl, '__doc__')
