import requests
import pandas as pd

# Your BscScan API Key (Get one for free at https://bscscan.com/myapikey)
API_KEY = "JUKGWVKHF17F5HR74KUXKDUJHQHVBC26ZV"

# Contract address to track (Gnosis Proxy Contract)
CONTRACT_ADDRESS = "0x0efcf893b6097bc221504d0d6df2d36879b8fe84"

# Base API URL for BEP-20 token transactions
BASE_URL = "https://api.bscscan.com/api?module=account&action=tokentx&address={}&page={}&offset=100&sort=asc&apikey={}".format(CONTRACT_ADDRESS, "{}", API_KEY)

TOTAL_PAGES = 30  # Adjust if necessary

# List to store transaction data
data = []

def fetch_transactions(page):
    url = BASE_URL.format(page)
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch page {page}")
        return []
    
    result = response.json()
    if result["status"] != "1":
        print(f"No transactions found on page {page}")
        return []
    
    return result["result"]

# Fetch all pages
for page in range(1, TOTAL_PAGES + 1):
    print(f"Fetching page {page}...")
    transactions = fetch_transactions(page)
    data.extend(transactions)

# Convert to DataFrame and save to CSV
if data:
    df = pd.DataFrame(data)
    df.to_csv("bscscan_bep20_transactions.csv", index=False)
    print("✅ CSV saved: bscscan_bep20_transactions.csv")
else:
    print("❌ No data scraped.")
