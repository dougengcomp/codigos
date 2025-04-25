import requests
import time
from datetime import datetime
from datetime import timezone
from pymongo import MongoClient

# MongoDB connection details
MONGO_CONNECTION_STRING = "mongodb+srv://douglasnascimento:Clg9xDHgAE7XmDyB@cluster0.rda0w.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DATABASE_NAME = "crypto_monitor_v1"
COLLECTION_NAME = "crypto_prices"

# Define the list of cryptocurrencies to monitor with their codes
CRYPTO_CODES = {
    "bitcoin": "BTC",
    "ethereum": "ETH",
    "solana": "SOL",
    "avalanche": "AVAX",
    "cardano": "ADA",
    "dogecoin": "DOGE",
    "shiba-inu": "SHIB",
    "sui": "SUI",
    "ripple": "XRP",
    "hyperliquid": "HYPE",
    "polkadot": "DOT"
}

# Define the currency to get prices in (e.g., USD)
CURRENCY = "usd"

# Define the polling interval (in seconds)
POLL_INTERVAL = 30

# Connect to MongoDB
client = MongoClient(MONGO_CONNECTION_STRING)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

def get_crypto_prices(crypto_codes, currency):
    """
    Fetch the current prices of the given cryptocurrencies from CoinGecko.
    
    :param crypto_codes: Dictionary of cryptocurrency IDs with their token codes.
    :param currency: The fiat currency to convert prices to (e.g., 'usd').
    :return: Dictionary with cryptocurrency IDs as keys and prices as values.
    """
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": ",".join(crypto_codes.keys()),
        "vs_currencies": currency
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 429:  # Rate limited
        print("Rate limit reached. Retrying in 60 seconds...")
        time.sleep(60)  # Wait before retrying
        return {}
    else:
        print(f"Error fetching data: {response.status_code} - {response.text}")
        return {}

def save_to_mongodb(data):
    """
    Save cryptocurrency price data to MongoDB.
    
    :param data: Dictionary with cryptocurrency price data.
    """
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")  # UTC timestamp
    for crypto_id, details in data.items():
        document = {
            "name": crypto_id.capitalize(),
            "symbol": CRYPTO_CODES[crypto_id],
            "price_usd": details[CURRENCY],
            "timestamp": timestamp
        }
        collection.insert_one(document)  # Insert each document into the collection
    print(f"Saved data to MongoDB at {timestamp}")

def main():
    while True:
        prices = get_crypto_prices(CRYPTO_CODES, CURRENCY)
        if prices:
            save_to_mongodb(prices)
        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    main()
