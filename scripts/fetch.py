import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

URL = "https://www.setel.com/latest-fuel-prices-malaysia"

response = requests.get(URL)
soup = BeautifulSoup(response.text, "html.parser")

def extract_price(label):
    tag = soup.find(string=lambda text: text and label in text)
    if not tag:
        return None

    parent = tag.parent
    price_tag = parent.find_next(string=lambda t: "RM" in t)
    if not price_tag:
        return None

    price = float(price_tag.replace("RM", "").strip())
    return price

data = {
    "last_updated": datetime.now().strftime("%Y-%m-%d"),
    "RON95": {
        "Price": extract_price("RON95"),
        "Unit": "RM/litre"
    },
    "RON97": {
        "Price": extract_price("RON97"),
        "Unit": "RM/litre"
    },
    "Diesel": {
        "Price": extract_price("Diesel B10/B20"),
        "Unit": "RM/litre"
    }
}

with open("price.json", "w") as f:
    json.dump(data, f, indent=4)

print("Updated price.json")
