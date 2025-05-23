
import time
import random
import logging

def delay(min_sec=1, max_sec=3):
    """Sleep for a random duration to mimic human behavior and avoid blocking."""
    sleep_time = random.uniform(min_sec, max_sec)
    logging.info(f"Sleeping for {sleep_time:.2f} seconds")
    time.sleep(sleep_time)

def clean_text(text):
    """Clean and normalize text."""
    if text:
        return ' '.join(text.strip().split())
    return None

def extract_price(price_str):
    """Extract numeric price value from string."""
    import re
    try:
        price = re.findall(r"\\d+(?:\\.\\d+)?", price_str.replace(",", ""))
        return float(price[0]) if price else None
    except:
        return None
