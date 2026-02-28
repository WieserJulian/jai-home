import pytest
import os
import sqlite3
from pathlib import Path

# Ensure the project root is on sys.path (already done via tests/__init__.py)

# Use a temporary DB for testing
TEST_DB_PATH = Path(__file__).resolve().parent.parent / "test_context.db"

# Patch the DB_PATH used in src.context to point to our temporary file
import src.context as ctx
ctx.DB_PATH = TEST_DB_PATH

def setup_function():
    # Ensure a clean DB before each test
    if TEST_DB_PATH.exists():
        TEST_DB_PATH.unlink()
    ctx._ensure_db()

def teardown_function():
    if TEST_DB_PATH.exists():
        TEST_DB_PATH.unlink()

def test_add_and_get_recent_single_entry():
    ctx.add_entry("Hello", "Hi there!")
    recent = ctx.get_recent(limit=1)
    assert "User: Hello" in recent
    assert "Assistant: Hi there!" in recent

def test_get_recent_limit_and_order():
    # Add multiple entries
    ctx.add_entry("First", "Response1")
    ctx.add_entry("Second", "Response2")
    ctx.add_entry("Third", "Response3")
    recent = ctx.get_recent(limit=2)
    # Should contain only the last two exchanges in chronological order
    lines = recent.splitlines()
    assert lines[0] == "User: Second"
    assert lines[1] == "Assistant: Response2"
    assert lines[2] == "User: Third"
    assert lines[3] == "Assistant: Response3"
    # Ensure older entry is not present
    assert "First" not in recent

def test_get_recent_empty_db_returns_empty_string():
    recent = ctx.get_recent(limit=5)
    assert recent == ""
