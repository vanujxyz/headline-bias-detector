import sqlite3
import json
from collections import Counter
from src.analysis.story_aggregator import aggregate_stories

from src.utils.db import DB_PATH

def generate_report():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT source_name, bias, features FROM headlines")
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print("No analysis data found in database.")
        return

    source_stats = {}

    for source, bias_json, features_json in rows:
        if source not in source_stats:
            source_stats[source] = {
                "total": 0,
                "biased_neg": 0,
                "biased_pos": 0,
                "neutral": 0,
                "scores": []
            }
        
        try:
            bias = json.loads(bias_json) if bias_json else {}
            features = json.loads(features_json) if features_json else {}
        except:
            continue

        label = bias.get("bias_label", "neutral")
        score = bias.get("bias_score", 0)

        source_stats[source]["total"] += 1
        source_stats[source]["scores"].append(score)

        if label == "biased_negative":
            source_stats[source]["biased_neg"] += 1
        elif label == "biased_positive":
            source_stats[source]["biased_pos"] += 1
        else:
            source_stats[source]["neutral"] += 1

    print("\n" + "="*70)
    print(" FINAL NEWS BIAS ANALYTICS REPORT")
    print("="*70)

    print(f"\n{'Source':<20} | {'Total':<6} | {'% Biased':<8} | {'Avg Score':<10}")
    print("-" * 70)

    for source, stats in sorted(source_stats.items()):
        biased_count = stats["biased_neg"] + stats["biased_pos"]
        biased_pct = (biased_count / stats["total"]) * 100 if stats["total"] > 0 else 0
        avg_score = sum(stats["scores"]) / len(stats["scores"]) if stats["scores"] else 0
        
        print(f"{source:<20} | {stats['total']:<6} | {biased_pct:>7.1f}% | {avg_score:>9.2f}")

    print("\n" + "="*70)
    print(" CLUSTER-LEVEL FRAMING INSIGHTS")
    print("="*70)
    
    comparisons = aggregate_stories()
    
    if not comparisons:
        print("\nNo significant cross-source framing differences detected.")
    else:
        for story in comparisons[:5]: # Show top 5 interesting clusters
            print(f"\n[STORY CLUSTER {story['cluster_id']}]")
            
            # Extract framing info if available
            for h in story["headlines"]:
                # We need to re-fetch features for framing details if aggregator doesn't have it
                # For brevity in CLI, we'll show high-level framing if possible or just the delta
                indicator = "!" if h["bias_label"] != "neutral" else " "
                print(f" {indicator} {h['source']:<15}: {h['bias_label']:<15} (Score: {h['bias_score']:>5.2f})")

    print("\n" + "="*70)

if __name__ == "__main__":
    generate_report()
