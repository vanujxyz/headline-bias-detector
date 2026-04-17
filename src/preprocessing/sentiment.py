from nltk.sentiment import SentimentIntensityAnalyzer

# Initialize once
sia = SentimentIntensityAnalyzer()


# ----------------------------------------
# Headline Sentiment
# ----------------------------------------
def get_headline_sentiment(text):
    scores = sia.polarity_scores(text)

    return {
        "neg": scores["neg"],
        "neu": scores["neu"],
        "pos": scores["pos"],
        "compound": scores["compound"]
    }


# ----------------------------------------
# Entity-level sentiment (simple heuristic)
# ----------------------------------------
def get_entity_sentiment(text, entities, window_size=5):
    """
    Computes sentiment for each entity based on a local window of words.
    """
    results = []
    text_lower = text.lower()

    for ent in entities:
        entity_text = ent["entity"]
        entity_lower = entity_text.lower()
        
        sentiment_scores = []
        
        if entity_lower in text_lower:
            start_idx = text_lower.find(entity_lower)
            
            # Extract local context
            prefix = text[:start_idx].split()
            suffix = text[start_idx + len(entity_text):].split()
            
            local_context = " ".join(prefix[-window_size:] + [entity_text] + suffix[:window_size])
            scores = sia.polarity_scores(local_context)
            sentiment_scores.append(scores["compound"])
        
        if not sentiment_scores:
            compound = sia.polarity_scores(text)["compound"]
        else:
            compound = sum(sentiment_scores) / len(sentiment_scores)

        results.append({
            "entity": entity_text,
            "side": ent["side"],
            "sentiment": round(compound, 3)
        })

    return results