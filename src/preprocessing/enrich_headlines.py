import sqlite3
import json

from src.preprocessing.nlp_pipeline import process_text
from src.preprocessing.entity_mapper import map_entities

from src.utils.db import DB_PATH


def enrich_headlines():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT headline_id, raw_text FROM headlines")
    rows = cursor.fetchall()

    print(f"Processing {len(rows)} headlines...")

    for headline_id, text in rows:
        result = process_text(text)

        mapped_entities = map_entities(result["entities"])

        cursor.execute("""
        UPDATE headlines
        SET tokens = ?, pos_tags = ?, dependencies = ?, named_entities = ?
        WHERE headline_id = ?
        """, (
            json.dumps(result["tokens"]),
            json.dumps(result["pos_tags"]),
            json.dumps(result["dependencies"]),
            json.dumps(mapped_entities),
            headline_id
        ))

    conn.commit()
    conn.close()

    print("Enrichment complete.")