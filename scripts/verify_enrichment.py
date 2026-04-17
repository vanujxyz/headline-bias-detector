import sqlite3
import json

conn = sqlite3.connect("data/headlines_db.sqlite")
cursor = conn.cursor()

cursor.execute("""
SELECT raw_text, sentiment, entity_sentiment 
FROM headlines 
LIMIT 5
""")

rows = cursor.fetchall()

for row in rows:
    print("\nHEADLINE:", row[0])
    print("SENTIMENT:", json.loads(row[1]))
    print("ENTITY SENTIMENT:", json.loads(row[2]))

conn.close()