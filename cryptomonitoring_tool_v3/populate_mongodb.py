from pymongo import MongoClient
from datetime import datetime, timedelta
import numpy as np
import random
import string
from threading import Thread

# MongoDB connection details
MONGO_CONNECTION_STRING = "mongodb+srv://douglasnascimento:Clg9xDHgAE7XmDyB@cluster0.rda0w.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DATABASE_NAME = "crypto_monitor_v1"
COLLECTION_NAME = "crypto_prices"

# Connect to MongoDB
client = MongoClient(MONGO_CONNECTION_STRING)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

def generate_random_crypto_data(batch_size):
    """Generate a batch of random cryptocurrency price data using numpy for efficiency."""
    symbols = [''.join(random.choices(string.ascii_lowercase, k=4)) for _ in range(batch_size)]
    names = [''.join(random.choices(string.ascii_uppercase, k=3)) for _ in range(batch_size)]
    prices = np.round(np.random.uniform(0.01, 10000, batch_size), 2)
    timestamps = [(datetime.utcnow() - timedelta(seconds=random.randint(0, 3600))).strftime("%Y-%m-%dT%H:%M:%SZ") for _ in range(batch_size)]

    return [
        {
            "name": names[i],
            "symbol": symbols[i],
            "price_usd": float(prices[i]),
            "timestamp": timestamps[i]
        }
        for i in range(batch_size)
    ]

def populate_batch(batch_size, target_size_bytes):
    """Populate the MongoDB collection with large batches of data."""
    try:
        while True:
            # Check current size
            current_size = db.command("collstats", COLLECTION_NAME).get("size", 0)
            if current_size >= target_size_bytes:
                print(f"Reached target size: {current_size / (1024 * 1024):.2f} MB")
                break

            # Generate and insert a large batch of documents
            batch = generate_random_crypto_data(batch_size)
            collection.insert_many(batch)
            print(f"Inserted batch of {batch_size} documents. Current size: {current_size / (1024 * 1024):.2f} MB")
    except Exception as e:
        print(f"Error populating database: {e}")

def populate_db(target_size_bytes, batch_size=10000, threads=4):
    """Populate the MongoDB collection using multithreading for faster inserts."""
    thread_list = []
    for _ in range(threads):
        thread = Thread(target=populate_batch, args=(batch_size, target_size_bytes))
        thread.start()
        thread_list.append(thread)

    for thread in thread_list:
        thread.join()

if __name__ == "__main__":
    TARGET_SIZE_MB = 200
    TARGET_SIZE_BYTES = TARGET_SIZE_MB * 1024 * 1024
    BATCH_SIZE = 10000  # Number of documents per batch
    THREADS = 4  # Number of threads for parallel insertion

    populate_db(TARGET_SIZE_BYTES, BATCH_SIZE, THREADS)
