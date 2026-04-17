from src.utils.db import create_table
from src.ingestion.fetch_headlines import run_ingestion
from src.preprocessing.enrich_headlines import enrich_headlines
from src.preprocessing.add_sentiment import add_sentiment
from src.features.add_features import add_features
from src.models.apply_bias import apply_bias
from src.analysis.story_aggregator import aggregate_stories, display_comparisons
from src.analysis.reporting import generate_report


def main():
    print("\n" + "="*50)
    print(" NEWS BIAS DETECTION PIPELINE")
    print("="*50)

    print("\n[STEP 1] Creating database...")
    create_table()

    print("\n[STEP 2] Running ingestion...")
    run_ingestion()

    print("\n[STEP 3] Running NLP enrichment...")
    enrich_headlines()

    print("\n[STEP 4] Adding sentiment...")
    add_sentiment()

    print("\n[STEP 5] Extracting features...")
    add_features()

    print("\n[STEP 6] Computing bias...")
    apply_bias()

    print("\n[STEP 7] Running Cross-Source Comparison...")
    comparisons = aggregate_stories()
    display_comparisons(comparisons)

    print("\n[STEP 8] Generating Final Analytics Report...")
    generate_report()

    print("\n[DONE] Pipeline complete.")


if __name__ == "__main__":
    main()