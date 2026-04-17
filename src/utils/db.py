import sqlite3
import os
from datetime import datetime

# Consolidated path logic (handles running from project root or notebooks/ dir)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, "data", "headlines_db.sqlite")


def get_connection():
    return sqlite3.connect(DB_PATH)


def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS headlines (
        headline_id TEXT PRIMARY KEY,
        raw_text TEXT NOT NULL UNIQUE,
        source_name TEXT,
        source_url TEXT,
        source_known_lean TEXT,
        topic_category TEXT,
        published_at TEXT,
        fetched_at TEXT,
        tokens TEXT,
        pos_tags TEXT,
        dependencies TEXT,
        named_entities TEXT,
        sentiment TEXT,
        entity_sentiment TEXT,
        features TEXT,
        bias TEXT
    )
    """)

    conn.commit()
    conn.close()


def insert_headline(data: dict):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR IGNORE INTO headlines (
        headline_id,
        raw_text,
        source_name,
        source_url,
        source_known_lean,
        topic_category,
        published_at,
        fetched_at,
        tokens,
        pos_tags,
        dependencies,
        named_entities,
        sentiment,
        entity_sentiment
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["headline_id"],
        data["raw_text"],
        data.get("source_name"),
        data.get("source_url"),
        data.get("source_known_lean"),
        data.get("topic_category"),
        data.get("published_at"),
        data.get("fetched_at", datetime.utcnow().isoformat()),
        None,
        None,
        None,
        None,
        None,
        None
    ))

    conn.commit()
    conn.close()