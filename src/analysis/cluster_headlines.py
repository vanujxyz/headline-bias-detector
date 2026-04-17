import sqlite3
import json

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

from src.utils.db import DB_PATH


def cluster_headlines(threshold=0.7):
    """
    Groups headlines into stories based on semantic similarity using Sentence Embeddings.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT headline_id, raw_text, source_name, sentiment, bias 
    FROM headlines
    """)

    rows = cursor.fetchall()
    if not rows:
        print("No headlines found to cluster.")
        return [], [], [], []

    ids = []
    texts = []
    sources = []
    biases = []
    sentiments = []

    for row in rows:
        ids.append(row[0])
        texts.append(row[1])
        sources.append(row[2])

        try:
            sent = json.loads(row[3]) if row[3] else {}
        except:
            sent = {}
        
        try:
            b = json.loads(row[4]) if row[4] else {}
        except:
            b = {}

        sentiments.append(sent)
        biases.append(b)

    # ----------------------------------------
    # Sentence Embedding Vectorization
    # ----------------------------------------
    print(f"Generating embeddings for {len(texts)} headlines...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(texts)

    # ----------------------------------------
    # Similarity matrix
    # ----------------------------------------
    sim_matrix = cosine_similarity(embeddings)

    # ----------------------------------------
    # Clustering (Greedy Threshold Clustering)
    # ----------------------------------------
    clusters = []
    visited = set()

    for i in range(len(texts)):
        if i in visited:
            continue

        cluster = [i]
        visited.add(i)

        for j in range(len(texts)):
            if j != i and j not in visited and sim_matrix[i][j] >= threshold:
                cluster.append(j)
                visited.add(j)

        clusters.append(cluster)

    conn.close()

    return clusters, texts, sources, biases