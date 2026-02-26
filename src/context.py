"""Conversation context persistence for JAI Home.

Provides a tiny SQLite database (``context.db`` in the project root) that
stores the most recent user‑assistant exchanges. Helper functions ``add_entry``
and ``get_recent`` are used by ``src.llm`` to prepend recent context to each
prompt, giving the LLM a short memory window.
"""

import sqlite3
from pathlib import Path
from typing import List

# Database file lives at the repository root (two levels up from this file).
DB_PATH = Path(__file__).resolve().parents[2] / "context.db"

def _ensure_db() -> None:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS conversation (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT NOT NULL,
            assistant TEXT NOT NULL,
            ts DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()
    conn.close()

def add_entry(user: str, assistant: str) -> None:
    """Record a single exchange.

    ``user`` – what the person said.
    ``assistant`` – the LLM's response.
    """
    _ensure_db()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO conversation (user, assistant) VALUES (?, ?)", (user, assistant)
    )
    conn.commit()
    conn.close()

def get_recent(limit: int = 5) -> str:
    """Return the most recent ``limit`` exchanges formatted as a transcript.

    The result is a plain‑text block that can be prefixed to a new prompt.
    """
    _ensure_db()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "SELECT user, assistant FROM conversation ORDER BY id DESC LIMIT ?", (limit,)
    )
    rows = cur.fetchall()
    conn.close()
    # Reverse to chronological order.
    rows.reverse()
    lines: List[str] = []
    for user, assistant in rows:
        lines.append(f"User: {user}")
        lines.append(f"Assistant: {assistant}")
    return "\n".join(lines)
