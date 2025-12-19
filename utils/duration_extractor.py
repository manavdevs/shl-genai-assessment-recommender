import re
from typing import Optional


def extract_max_duration_minutes(query: str) -> Optional[int]:
    """
    Extracts maximum allowed duration in minutes from query.
    Returns None if no duration constraint found.
    """
    q = query.lower()

    # Explicit minutes
    mins_match = re.search(r'(\d+)\s*(minute|min|mins)', q)
    if mins_match:
        return int(mins_match.group(1))

    # Explicit hours
    hours_match = re.search(r'(\d+)\s*(hour|hr|hrs)', q)
    if hours_match:
        return int(hours_match.group(1)) * 60

    # Ranges like "1-2 hour"
    range_match = re.search(r'(\d+)\s*-\s*(\d+)\s*(hour|hr)', q)
    if range_match:
        return int(range_match.group(2)) * 60

    # Soft phrases
    if "about an hour" in q or "around an hour" in q:
        return 60

    if "at most" in q:
        num = re.search(r'at most\s*(\d+)', q)
        if num:
            return int(num.group(1))

    return None
