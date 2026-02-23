import importlib
import sys

def test_import_asr():
    try:
        asr = importlib.import_module('src.asr')
    except Exception as e:
        assert False, f"Failed to import src.asr: {e}"
    # basic sanity: module should have a __doc__ attribute (even if None)
    assert hasattr(asr, '__doc__')
