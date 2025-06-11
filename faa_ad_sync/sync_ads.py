import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

XANO_API_URL = "https://x8ki-letl-twmt.n7.xano.io/api:Luv2nZcj/ad"
XANO_TOKEN = os.getenv("XANO_TOKEN")
FAA_DRS_URL = "https://drs.faa.gov/browse"

def fetch_latest_ads():
    today = datetime.now().strftime('%Y-%m-%d')
    seven_days_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')

    response = requests.get(FAA_DRS_URL)
    soup = BeautifulSoup(response.text, 'lxml')

    ads = []
    for row in soup.select(".search-result-row"):
        ad = {
            "ad_number": row.select_one(".ad-number").text.strip() if row.select_one(".ad-number") else "",
            "title": row.select_one(".ad-title").text.strip() if row.select_one(".ad-title") else "",
            "issue_date": row.select_one(".ad-date").text.strip() if row.select_one(".ad-date") else "",
            "link": "https://drs.faa.gov" + row.select_one("a")["href"] if row.select_one("a") else ""
        }
        ads.append(ad)
    return ads

def post_to_xano(ad_list):
    headers = {
        "Authorization": f"Bearer {XANO_TOKEN}",
        "Content-Type": "application/json",
    }
    for ad in ad_list:
        response = requests.post(XANO_API_URL, headers=headers, json=ad)
        print(f"Posted {ad['ad_number']}: {response.status_code}")

def main():
    print("Fetching latest FAA ADs...")
    ads = fetch_latest_ads()
    print(f"Found {len(ads)} ADs.")
    if ads:
        post_to_xano(ads)

if __name__ == "__main__":
    main()
