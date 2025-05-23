import requests
from bs4 import BeautifulSoup
import csv
import time
import random
import logging
from urllib.parse import urljoin
from scripts.utils import delay, clean_text, extract_price


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0 Safari/537.36"
}

BASE_URL = "https://dir.indiamart.com/"
CATEGORIES = [
    "impcat/industrial-machinery.html",
    "impcat/electronic-products-devices.html",
    "impcat/textile-fabrics.html"
]

def get_product_links(category_url):
    product_links = []
    try:
        for page in range(1, 4):  # Scrape 3 pages/category
            url = f"{category_url}?page={page}"
            response = requests.get(url, headers=HEADERS)
            soup = BeautifulSoup(response.text, "html.parser")
            cards = soup.select(".prd-list li a")
            for card in cards:
                href = card.get("href")
                if href:
                    product_links.append(urljoin(BASE_URL, href))
            time.sleep(random.uniform(2, 5))
    except Exception as e:
        logging.error(f"Error fetching product links: {e}")
    return list(set(product_links))

def parse_product_page(url):
    data = {"name": None, "price": None, "location": None, "url": url}
    try:
        res = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(res.text, "html.parser")
        data["name"] = soup.select_one(".bcls h1").get_text(strip=True) if soup.select_one(".bcls h1") else None
        data["price"] = soup.select_one(".price`).get_text(strip=True) if soup.select_one(".price") else None
        data["location"] = soup.select_one(".location").get_text(strip=True) if soup.select_one(".location") else None
        time.sleep(random.uniform(1, 3))
    except Exception as e:
        logging.warning(f"Failed to parse {url}: {e}")
    return data

def scrape_all():
    all_products = []
    for category in CATEGORIES:
        category_url = urljoin(BASE_URL, category)
        logging.info(f"Scraping category: {category_url}")
        links = get_product_links(category_url)
        for link in links:
            product = parse_product_page(link)
            all_products.append(product)
    return all_products

def save_to_csv(data, filename="../data/raw/b2b_products.csv"):
    keys = data[0].keys() if data else []
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)

def main():
    data = scrape_all()
    save_to_csv(data)
    logging.info("Data scraping complete.")

if __name__ == "__main__":
    main(