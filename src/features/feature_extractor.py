import json
import re


# ----------------------------------------
# Load lexicon
# ----------------------------------------
def load_lexicon():
    with open("config/loaded_lexicon.json", "r", encoding="utf-8") as f:
        return json.load(f)


lexicon = load_lexicon()


# ----------------------------------------
# Basic preprocessing
# ----------------------------------------
def tokenize(text):
    return re.findall(r'\b\w+\b', text.lower())


# ----------------------------------------
# Feature extraction
# ----------------------------------------
def extract_features(text, sentiment, entity_sentiment, tokens=None, dependencies=None, named_entities=None):
    """
    Extracts linguistic and framing features from a headline.
    """
    # Use provided tokens if available (from spaCy), otherwise fallback to simple regex
    words = [t.lower() for t in tokens] if tokens else tokenize(text)

    # ----------------------------------------
    # Loaded word counts
    # ----------------------------------------
    neg_count = sum(1 for t in words if t in lexicon["negative"])
    pos_count = sum(1 for t in words if t in lexicon["positive"])
    intensifier_count = sum(1 for t in words if t in lexicon["intensifiers"])

    # ----------------------------------------
    # Sentiment
    # ----------------------------------------
    compound = sentiment.get("compound", 0)

    # ----------------------------------------
    # Entity sentiment aggregation
    # ----------------------------------------
    side_scores = {}
    entity_to_sentiment = {}

    for ent in entity_sentiment:
        side = ent.get("side", "unknown")
        score = ent.get("sentiment", 0)
        entity_text = ent.get("entity", "")
        
        if side not in side_scores:
            side_scores[side] = []
        side_scores[side].append(score)
        
        if entity_text:
            entity_to_sentiment[entity_text.lower()] = score

    avg_side_sentiment = {side: sum(sc)/len(sc) for side, sc in side_scores.items() if sc}

    # ----------------------------------------
    # Framing Analysis (Role: Subject/Object)
    # ----------------------------------------
    framing = []
    if dependencies:
        # Create a mapping of token to its dependency role
        # dependencies list: (token_text, dep, head_text)
        for ent in entity_sentiment:
            ent_name = ent.get("entity", "")
            ent_name_lower = ent_name.lower()
            
            role = "other"
            # Look for the entity in the dependency list
            for dep_token, dep_label, _ in dependencies:
                if dep_token.lower() == ent_name_lower:
                    if "subj" in dep_label:
                        role = "subject"
                    elif "obj" in dep_label:
                        role = "object"
                    break
            
            framing.append({
                "entity": ent_name,
                "role": role,
                "sentiment": ent.get("sentiment", 0),
                "side": ent.get("side", "unknown")
            })

    # ----------------------------------------
    # Final feature object
    # ----------------------------------------
    return {
        "neg_word_count": neg_count,
        "pos_word_count": pos_count,
        "intensifier_count": intensifier_count,
        "headline_sentiment": compound,
        "side_sentiment": avg_side_sentiment,
        "framing": framing
    }