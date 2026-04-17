import sqlite3
import json

conn = sqlite3.connect("data/headlines_db.sqlite")
cursor = conn.cursor()

cursor.execute("""
SELECT raw_text, features 
FROM headlines 
LIMIT 5
""")

for row in cursor.fetchall():
    print("\nHEADLINE:", row[0])
    print("FEATURES:", json.loads(row[1]))

conn.close()