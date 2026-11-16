
# storage/chat_store.py

import sqlite3
import uuid

from pathlib import Path
from datetime import datetime, timezone

DB_PATH = Path(__file__).resolve().parent.parent / "chat_history.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def initialize_database():

    with get_connection() as conn:

        conn.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                conversation_id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                message_id TEXT PRIMARY KEY,
                conversation_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL,

                FOREIGN KEY (conversation_id)
                REFERENCES conversations(conversation_id)
                ON DELETE CASCADE
            )
        """)

        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_messages_conversation
            ON messages(conversation_id, created_at)
        """)


def create_conversation(title="New Chat"):

    conversation_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()

    with get_connection() as conn:

        conn.execute("""
            INSERT INTO conversations
            (conversation_id, title, created_at, updated_at)
            VALUES (?, ?, ?, ?)
        """, (conversation_id, title, now, now))

    return conversation_id


def get_all_conversations():

    with get_connection() as conn:

        rows = conn.execute("""
            SELECT * FROM conversations
            ORDER BY updated_at DESC
        """).fetchall()

    return [dict(row) for row in rows]


def save_message(conversation_id, role, content):

    now = datetime.now(timezone.utc).isoformat()

    with get_connection() as conn:

        conn.execute("""
            INSERT INTO messages
            (message_id, conversation_id, role, content, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (
            str(uuid.uuid4()),
            conversation_id,
            role,
            content,
            now
        ))

        conn.execute("""
            UPDATE conversations
            SET updated_at = ?
            WHERE conversation_id = ?
        """, (now, conversation_id))


def get_messages(conversation_id):

    with get_connection() as conn:

        rows = conn.execute("""
            SELECT role, content, created_at
            FROM messages
            WHERE conversation_id = ?
            ORDER BY created_at ASC, rowid ASC
        """, (conversation_id,)).fetchall()

    return [dict(row) for row in rows]


def get_recent_messages(conversation_id, limit=8):

    with get_connection() as conn:

        rows = conn.execute("""
            SELECT role, content
            FROM messages
            WHERE conversation_id = ?
            ORDER BY created_at DESC, rowid DESC
            LIMIT ?
        """, (conversation_id, limit)).fetchall()

    return list(reversed([dict(row) for row in rows]))


def update_conversation_title(conversation_id, title):

    with get_connection() as conn:

        conn.execute("""
            UPDATE conversations
            SET title = ?
            WHERE conversation_id = ?
        """, (title, conversation_id))


def delete_conversation(conversation_id):

    with get_connection() as conn:

        conn.execute("""
            DELETE FROM conversations
            WHERE conversation_id = ?
        """, (conversation_id,))
