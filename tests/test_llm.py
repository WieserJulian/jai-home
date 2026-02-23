import importlib

def test_import_llm():
    try:
        llm = importlib.import_module('src.llm')
    except Exception as e:
        assert False, f"Failed to import src.llm: {e}"
    assert hasattr(llm, '__doc__')
