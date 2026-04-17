import feedparser
import uuid
from datetime import datetime
import yaml

from src.utils.db import insert_headline


def load_sources():
    with open("config/sources.yaml", "r") as f:
        return yaml.safe_load(f)["sources"]


def fetch_from_rss(source):
    feed = feedparser.parse(source["url"])
    headlines = []

    for entry in feed.entries:
        headline = {
            "headline_id": str(uuid.uuid4()),
            "raw_text": entry.title,
            "source_name": source["name"],
            "source_url": entry.link,
            "source_known_lean": source["lean"],
            "topic_category": "general",
            "published_at": getattr(entry, "published", None),
            "fetched_at": datetime.utcnow().isoformat(),
            "named_entities": ""
        }

        headlines.append(headline)

    return headlines


def run_ingestion():
    sources = load_sources()

    total = 0

    for source in sources:
        print(f"Fetching from {source['name']}...")

        try:
            headlines = fetch_from_rss(source)

            for h in headlines:
                insert_headline(h)

            print(f"Inserted {len(headlines)} headlines.")
            total += len(headlines)

        except Exception as e:
            print(f"Error with {source['name']}: {e}")

    print(f"\nTotal headlines inserted: {total}")