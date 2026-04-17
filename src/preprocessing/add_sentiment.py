import sqlite3
import json

from src.preprocessing.sentiment import (
    get_headline_sentiment,
    get_entity_sentiment
)

from src.utils.db import DB_PATH


def add_sentiment():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT headline_id, raw_text, named_entities FROM headlines")
    rows = cursor.fetchall()

    print(f"Processing sentiment for {len(rows)} headlines...")

    for headline_id, text, entities_json in rows:
        if not text:
            continue

        try:
            entities = json.loads(entities_json) if entities_json else []
        except:
            entities = []

        headline_sent = get_headline_sentiment(text)
        entity_sent = get_entity_sentiment(text, entities)

        cursor.execute("""
        UPDATE headlines
        SET sentiment = ?, entity_sentiment = ?
        WHERE headline_id = ?
        """, (
            json.dumps(headline_sent),
            json.dumps(entity_sent),
            headline_id
        ))

    conn.commit()
    conn.close()

    print("Sentiment enrichment complete.")