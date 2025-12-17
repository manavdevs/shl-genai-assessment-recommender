import requests
from bs4 import BeautifulSoup
import json
import time

BASE_URL = "https://www.shl.com"
CATALOG_URL = "https://www.shl.com/products/product-catalog/"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

PAGE_SIZE = 12

def parse_listing_page(start: int):
    params = {
        "start": start,
        "type": 1
    }

    response = requests.get(CATALOG_URL, headers=HEADERS, params=params)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    rows = soup.select("tr:has(a[href*='/products/product-catalog/view/'])")
    assessments = []

    for row in rows:
        link = row.select_one("a[href*='/products/product-catalog/view/']")
        if not link:
            continue

        name = link.text.strip()
        url = BASE_URL + link.get("href")

        test_type_el = row.select_one(".product-catalogue__key")
        test_type = test_type_el.text.strip() if test_type_el else None

        dots = row.select(".catalogue__circle.-yes")
        remote_support = len(dots) >= 1
        adaptive_support = len(dots) >= 2

        assessments.append({
            "name": name,
            "url": url,
            "test_type": test_type,
            "remote_support": remote_support,
            "adaptive_support": adaptive_support
        })

    return assessments



def scrape_all_listings():
    all_assessments = []
    seen_urls = set()
    empty_pages = 0
    MAX_START = 420  

    for start in range(0, MAX_START + PAGE_SIZE, PAGE_SIZE):
        print(f"Scraping start offset: {start}")
        page_data = parse_listing_page(start)

        new_items = 0
        for item in page_data:
            if item["url"] not in seen_urls:
                seen_urls.add(item["url"])
                all_assessments.append(item)
                new_items += 1

        if new_items == 0:
            empty_pages += 1
            if empty_pages >= 2:
                print("No new assessments found on consecutive pages. Stopping.")
                break
        else:
            empty_pages = 0

        if start >= 360 and empty_pages >= 3:
            print("Reached catalog end safely.")
            break
        time.sleep(0.7)

    return all_assessments

def remove_job_solutions(all_items):
    """
    SHL catalog invariant:
    First 12 entries (start=0) are pre-packaged job solutions.
    """
    print("Truncating first 12 pre-packaged job solutions")
    return all_items[12:]


if __name__ == "__main__":
    raw_data = scrape_all_listings()
    print(f"Total scraped (raw): {len(raw_data)}")

    final_data = remove_job_solutions(raw_data)
    print(f"Final individual assessments: {len(final_data)}")

    with open("data/raw/assessments_listing.json", "w") as f:
        json.dump(final_data, f, indent=2)
