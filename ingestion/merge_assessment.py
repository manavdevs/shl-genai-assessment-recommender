import json
import time
from scrape_details import scrape_assessment_detail

RAW_PATH = "data/raw/assessments_listing.json"
OUTPUT_PATH = "data/processed/assessments_full.json"

REQUEST_DELAY = 0.6 

def merge():
    with open(RAW_PATH, "r") as f:
        listings = json.load(f)

    enriched = []

    for idx, item in enumerate(listings, start=1):
        print(f"[{idx}/{len(listings)}] Enriching: {item['name']}")

        try:
            details = scrape_assessment_detail(item["url"])
        except Exception as e:
            print(f"⚠️ Failed to scrape {item['url']}: {e}")
            details = {}

        merged = {
            **item,
            **details
        }

        enriched.append(merged)
        time.sleep(REQUEST_DELAY)

    with open(OUTPUT_PATH, "w") as f:
        json.dump(enriched, f, indent=2)

    print(f"\n✅ Saved {len(enriched)} enriched assessments to {OUTPUT_PATH}")


if __name__ == "__main__":
    merge()
