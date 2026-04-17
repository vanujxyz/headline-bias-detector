import math


# ----------------------------------------
# Bias scoring function
# ----------------------------------------
def compute_bias(features):
    """
    Computes a weighted bias score based on linguistic features, sentiment, and framing.
    Positive Score -> biased_negative (Negative bias / Biased Against)
    Negative Score -> biased_positive (Positive bias / Biased For)
    """
    neg_words = features.get("neg_word_count", 0)
    pos_words = features.get("pos_word_count", 0)
    intensity = features.get("intensifier_count", 0)
    sentiment = features.get("headline_sentiment", 0)
    framing = features.get("framing", [])

    # Weighted Scoring Components
    score = 0.0
    explanation = []

    # 1. Loaded Language (Weight: 1.5)
    # Negative loaded words increase the bias score (positive score)
    if neg_words != pos_words:
        diff = neg_words - pos_words
        impact = diff * 1.5
        score += impact
        explanation.append(f"Loaded language imbalance impact: {impact:.2f}")

    # 2. Emotional Intensity (Weight: 0.75)
    if intensity > 0:
        # Intensity amplifies the direction of sentiment
        impact = intensity * 0.75
        direction = 1 if sentiment < 0 else -1 if sentiment > 0 else 0
        score += impact * direction
        if direction != 0:
            explanation.append(f"Intensifiers amplifying tone: {impact:.2f}")

    # 3. Overall Headline Sentiment (Weight: 3.0)
    # We want Negative Sentiment to produce a Positive Score
    if abs(sentiment) > 0.2:
        impact = -sentiment * 3.0
        score += impact
        explanation.append(f"Overall sentiment impact: {impact:.2f}")

    # 4. Framing Analysis (Weight: 2.0)
    # Focus on subjects of negative actions
    subject_sentiments = [f["sentiment"] for f in framing if f["role"] == "subject"]
    if subject_sentiments:
        avg_subj_sent = sum(subject_sentiments) / len(subject_sentiments)
        if abs(avg_subj_sent) > 0.1:
            impact = -avg_subj_sent * 2.0
            score += impact
            explanation.append(f"Subject framing impact: {impact:.2f}")

    # Final label based on thresholds
    bias_label = "neutral"
    if score >= 1.5:
        bias_label = "biased_negative"
    elif score <= -1.5:
        bias_label = "biased_positive"

    return {
        "bias_score": round(score, 2),
        "bias_label": bias_label,
        "explanation": explanation
    }