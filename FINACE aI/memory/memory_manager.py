"""
Memory Manager
Stores conversation history in SQLite (local, no setup needed)
Can be swapped for MySQL in production
"""

import sqlite3
import json
import os
from datetime import datetime


class MemoryManager:
    def __init__(self, db_path: str = "finance_ai_memory.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with self._connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    timestamp TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_session ON messages(session_id)
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS user_profiles (
                    session_id TEXT PRIMARY KEY,
                    profile_data TEXT,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def save_message(self, session_id: str, role: str, content: str):
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO messages (session_id, role, content) VALUES (?, ?, ?)",
                (session_id, role, content)
            )

    def get_history(self, session_id: str, limit: int = 10) -> list:
        with self._connect() as conn:
            cursor = conn.execute(
                """SELECT role, content FROM messages
                   WHERE session_id = ?
                   ORDER BY id DESC LIMIT ?""",
                (session_id, limit)
            )
            rows = cursor.fetchall()
        # Return in chronological order
        return [{"role": r[0], "content": r[1]} for r in reversed(rows)]

    def save_profile(self, session_id: str, profile: dict):
        with self._connect() as conn:
            conn.execute(
                """INSERT OR REPLACE INTO user_profiles (session_id, profile_data, updated_at)
                   VALUES (?, ?, ?)""",
                (session_id, json.dumps(profile), datetime.now().isoformat())
            )

    def get_profile(self, session_id: str) -> dict:
        with self._connect() as conn:
            cursor = conn.execute(
                "SELECT profile_data FROM user_profiles WHERE session_id = ?",
                (session_id,)
            )
            row = cursor.fetchone()
        return json.loads(row[0]) if row else {}

    def clear_session(self, session_id: str):
        with self._connect() as conn:
            conn.execute("DELETE FROM messages WHERE session_id = ?", (session_id,))
            conn.execute("DELETE FROM user_profiles WHERE session_id = ?", (session_id,))

    def get_all_sessions(self) -> list:
        with self._connect() as conn:
            cursor = conn.execute(
                "SELECT DISTINCT session_id FROM messages"
            )
            return [r[0] for r in cursor.fetchall()]
