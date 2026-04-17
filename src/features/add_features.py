import sqlite3
import json

from src.features.feature_extractor import extract_features

from src.utils.db import DB_PATH


def add_features():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Updated to fetch NLP data for framing analysis
    cursor.execute("""
    SELECT headline_id, raw_text, sentiment, entity_sentiment, tokens, dependencies, named_entities 
    FROM headlines
    """)

    rows = cursor.fetchall()

    print(f"Extracting features for {len(rows)} headlines...")

    for row in rows:
        headline_id, text, sentiment_json, entity_sent_json, tokens_json, deps_json, ents_json = row

        try:
            sentiment = json.loads(sentiment_json) if sentiment_json else {}
            entity_sent = json.loads(entity_sent_json) if entity_sent_json else []
            tokens = json.loads(tokens_json) if tokens_json else []
            dependencies = json.loads(deps_json) if deps_json else []
            named_entities = json.loads(ents_json) if ents_json else []
        except:
            continue

        features = extract_features(text, sentiment, entity_sent, tokens, dependencies, named_entities)

        cursor.execute("""
        UPDATE headlines
        SET features = ?
        WHERE headline_id = ?
        """, (
            json.dumps(features),
            headline_id
        ))

    conn.commit()
    conn.close()

    print("Feature extraction complete.")