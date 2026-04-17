import json
from src.analysis.cluster_headlines import cluster_headlines

def aggregate_stories():
    """
    Aggregates bias findings per story cluster to highlight cross-source differences.
    """
    clusters, texts, sources, biases = cluster_headlines()
    
    comparisons = []

    for idx, cluster in enumerate(clusters):
        if len(cluster) < 2:
            continue
            
        cluster_data = []
        unique_sources = set()
        
        for i in cluster:
            unique_sources.add(sources[i])
            cluster_data.append({
                "source": sources[i],
                "headline": texts[i],
                "bias_label": biases[i].get("bias_label", "neutral"),
                "bias_score": biases[i].get("bias_score", 0),
                "explanation": biases[i].get("explanation", [])
            })
            
        # Only include stories covered by multiple sources
        if len(unique_sources) >= 2:
            # Check if there's any bias difference
            bias_labels = set(d["bias_label"] for d in cluster_data)
            
            # We want to highlight stories where at least one source is biased
            is_interesting = any(d["bias_label"] != "neutral" for d in cluster_data)
            
            if is_interesting:
                comparisons.append({
                    "cluster_id": idx,
                    "headlines": cluster_data
                })
                
    return comparisons

def display_comparisons(comparisons):
    print("\n" + "="*60)
    print(" CROSS-SOURCE STORY BIAS REPORT")
    print("="*60)
    
    if not comparisons:
        print("\nNo significant cross-source bias detected in current stories.")
        return

    for story in comparisons:
        print(f"\n[STORY CLUSTER {story['cluster_id']}]")
        print("-" * 30)
        
        for h in story["headlines"]:
            indicator = "[BIASED]" if h["bias_label"] != "neutral" else "[NEUTRAL]"
            print(f"{indicator} SOURCE: {h['source']}")
            print(f"   Headline: {h['headline']}")
            print(f"   Label:    {h['bias_label']} (Score: {h['bias_score']})")
            if h["explanation"]:
                print(f"   Reason:   {', '.join(h['explanation'][:2])}...")
            print()

if __name__ == "__main__":
    results = aggregate_stories()
    display_comparisons(results)
