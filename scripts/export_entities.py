import sqlite3
import json
import re

conn = sqlite3.connect("data/headlines_db.sqlite")
cursor = conn.cursor()

cursor.execute("SELECT named_entities FROM headlines")
rows = cursor.fetchall()

entity_set = set()

def is_valid_entity(text):
    text = text.strip()

    # Remove numbers / money / units
    if re.search(r'\d', text):
        return False

    # Remove very short tokens
    if len(text) < 3:
        return False

    # Remove lowercase-only words
    if text.islower():
        return False

    # Remove phrases with too many words (likely broken headlines)
    if len(text.split()) > 4:
        return False

    # Remove unwanted generic words
    blacklist = {
        "Explainer", "Explained", "Articles", "Next",
        "First", "Second", "Third", "Today",
        "Breaking", "Update"
    }

    if text in blacklist:
        return False

    return True


for row in rows:
    if not row[0]:
        continue

    try:
        entities = json.loads(row[0])

        for ent in entities:
            if isinstance(ent, list):
                text = ent[0]
            elif isinstance(ent, dict):
                text = ent.get("entity")
            else:
                continue

            if text and is_valid_entity(text):
                entity_set.add(text)

    except:
        continue

# Print cleaned entities
for e in sorted(entity_set):
    print(e)

conn.close()