import requests
from bs4 import BeautifulSoup
import json
import time

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def scrape_assessment_detail(url: str) -> dict:
    """
    Scrape detailed metadata from a single SHL assessment page.
    """
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    details = {
        "description": None,
        "duration_minutes": None,
        "job_levels": [],
        "languages": [],
        "skills": [],
        "test_format": None
    }

    # -------- Description --------
    description = None

    # Case 1: Explicit "Description" block (most reliable)
    desc_block = soup.find(
        "div",
        class_="product-catalogue-training-calendar__row"
    )
    if desc_block:
        header = desc_block.find("h4")
        if header and "description" in header.text.lower():
            p = desc_block.find("p")
            if p:
                description = p.get_text(strip=True)

    # Case 2: Common content containers
    if not description:
        description_selectors = [
            ".product-catalogue__description",
            ".product-catalogue__intro",
            ".rich-text"
        ]
        for selector in description_selectors:
            el = soup.select_one(selector)
            if el:
                text = el.get_text(strip=True)
                if len(text) > 50:
                    description = text
                    break

    # Case 3: Fallback — first paragraph after title
    if not description:
        title = soup.find("h1")
        if title:
            p = title.find_next("p")
            if p:
                description = p.get_text(strip=True)

    details["description"] = description

    # -------- Key-Value Metadata --------
    rows = soup.find_all(
        "div",
        class_="product-catalogue-training-calendar__row"
    )

    for row in rows:
        label_el = row.find("h4")
        value_el = row.find("p")

        if not label_el or not value_el:
            continue

        label = label_el.get_text(strip=True).lower()
        value = value_el.get_text(strip=True)
        
        
        # Duration
        if "assessment length" in label or "duration" in label:
            # Extract first number found (e.g., "60 minutes")
            digits = "".join(ch for ch in value if ch.isdigit())
            if digits:
                details["duration_minutes"] = int(digits)
        # Job levels
        elif "job level" in label:
            details["job_levels"] = [
    lvl.strip() for lvl in value.split(",") if lvl.strip()
            ]

        # Languages
        elif "language" in label:
            details["languages"] = [
                lang.strip() for lang in value.split(",") if lang.strip()
        ]

        # Test format / type
        test_type_el = soup.select_one(".product-catalogue__key")
        if test_type_el:
            details["test_format"] = test_type_el.get_text(strip=True)

    return details



if __name__ == "__main__":
    test_url = "https://www.shl.com/products/product-catalog/view/net-framework-4-5/"
    data = scrape_assessment_detail(test_url)
    print(json.dumps(data, indent=2))
