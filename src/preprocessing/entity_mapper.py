import json


def load_kb():
    try:
        with open("config/entity_side_kb.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[ERROR] Failed to load KB: {e}")
        return {}


def normalize_entity(text):
    if not text:
        return ""

    text = text.strip()

    if text.endswith("'s"):
        text = text[:-2]

    return text


def map_entities(entities):
    """
    Maps named entities to political sides using a knowledge base.
    Uses fuzzy/substring matching for improved coverage.
    """
    kb = load_kb()
    mapped = []

    for ent in entities:
        try:
            if isinstance(ent, (list, tuple)):
                if len(ent) >= 2:
                    text, label = ent[0], ent[1]
                else: continue
            elif isinstance(ent, dict):
                text = ent.get("entity")
                label = ent.get("label")
            else: continue

            text = normalize_entity(text)
            if not text:
                continue

            # Improved Matching Logic
            side = "unknown"
            
            # 1. Exact match first
            if text in kb:
                side = kb[text]
            else:
                # 2. Substring/Fuzzy match
                # Check if text is in KB keys (e.g., "Narendra Modi" matches "Modi")
                # Or if any KB key is in text
                text_lower = text.lower()
                for kb_key, kb_side in kb.items():
                    key_lower = kb_key.lower()
                    if key_lower in text_lower or text_lower in key_lower:
                        side = kb_side
                        break

            mapped.append({
                "entity": text,
                "label": label,
                "side": side
            })

        except Exception as e:
            print(f"[WARN] Failed to map entity: {ent}, error: {e}")
            continue

    return mapped