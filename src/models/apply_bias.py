import sqlite3
import json

from src.models.bias_detector import compute_bias

from src.utils.db import DB_PATH


def apply_bias():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT headline_id, features FROM headlines")
    rows = cursor.fetchall()

    print(f"Computing bias for {len(rows)} headlines...")

    for headline_id, features_json in rows:

        try:
            features = json.loads(features_json) if features_json else {}
        except:
            continue

        result = compute_bias(features)

        cursor.execute("""
        UPDATE headlines
        SET bias = ?
        WHERE headline_id = ?
        """, (
            json.dumps(result),
            headline_id
        ))

    conn.commit()
    conn.close()

    print("Bias computation complete.")