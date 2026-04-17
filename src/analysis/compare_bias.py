from src.analysis.cluster_headlines import cluster_headlines


def compare_clusters():
    clusters, texts, sources, biases = cluster_headlines()

    print("\n=== CROSS-SOURCE BIAS ANALYSIS ===\n")

    for idx, cluster in enumerate(clusters):

        if len(cluster) < 2:
            continue

        # ----------------------------------------
        # Collect sources in cluster
        # ----------------------------------------
        cluster_sources = [sources[i] for i in cluster]
        unique_sources = set(cluster_sources)

        # ❌ Skip same-source clusters
        if len(unique_sources) < 2:
            continue

        # ----------------------------------------
        # Collect bias labels
        # ----------------------------------------
        cluster_biases = [biases[i].get("bias_label", "unknown") for i in cluster]

        # ❌ Skip if all same bias
        if len(set(cluster_biases)) == 1:
            continue

        print(f"\n--- STORY CLUSTER {idx+1} ---")

        for i in cluster:
            bias_label = biases[i].get("bias_label", "unknown")
            bias_score = biases[i].get("bias_score", 0)

            print(f"\nSource: {sources[i]}")
            print(f"Headline: {texts[i]}")
            print(f"Bias: {bias_label} ({bias_score})")