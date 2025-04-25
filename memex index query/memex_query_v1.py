from web3 import Web3
import csv
from datetime import datetime
import time

# Set up connection to Ethereum node (using MetaMask Developer API Key)
INFURA_URL = "https://mainnet.infura.io/v3/c26e8349052b401b9e529b34d38180bf"  # Your API Key
CONTRACT_ADDRESS = Web3.to_checksum_address("0xb214b79eac9378a56D14D6e6d452150C80D6Ad79")
START_BLOCK = 0  # Start from the genesis block
END_BLOCK = "latest"  # End at the latest block
OUTPUT_FILE = "web3_transactions_and_transfers.csv"
BLOCK_CHUNK_SIZE = 7600  # Adjusted chunk size for a ~10-minute execution time
SAVE_INTERVAL = 5  # Save to CSV every 5 chunks

# Connect to Ethereum node
web3 = Web3(Web3.HTTPProvider(INFURA_URL))

if not web3.is_connected():
    print("Failed to connect to Ethereum node. Check your API key or internet connection.")
    exit()

# Fetch transactions for the specified contract
def fetch_transactions(contract_address, start_block, end_block):
    transactions = []
    latest_block = web3.eth.block_number if end_block == "latest" else end_block
    chunk_counter = 0  # Track how many chunks have been processed

    print(f"Fetching transactions from block {start_block} to {latest_block} in chunks of {BLOCK_CHUNK_SIZE}...")

    for start in range(start_block, latest_block + 1, BLOCK_CHUNK_SIZE):
        end = min(start + BLOCK_CHUNK_SIZE - 1, latest_block)
        print(f"Fetching blocks {start} to {end}...")
        chunk_counter += 1

        for block_number in range(start, end + 1):
            try:
                block = web3.eth.get_block(block_number, full_transactions=True)
                for tx in block.transactions:
                    if tx["to"] == contract_address or tx["from"] == contract_address:
                        transactions.append({
                            "blockNumber": tx["blockNumber"],
                            "timestamp": datetime.utcfromtimestamp(block["timestamp"]).strftime('%Y-%m-%d %H:%M:%S'),
                            "hash": tx["hash"].hex(),
                            "from": tx["from"],
                            "to": tx["to"],
                            "value": web3.from_wei(tx["value"], "ether"),
                            "gas": tx["gas"],
                            "gasPrice": web3.from_wei(tx["gasPrice"], "gwei"),
                            "input": tx["input"],
                        })
            except Exception as e:
                print(f"Error fetching block {block_number}: {e}")
                time.sleep(5)  # Pause before retrying

        # Save progress to CSV after every SAVE_INTERVAL chunks
        if chunk_counter % SAVE_INTERVAL == 0:
            append_to_csv(transactions)
            transactions.clear()  # Clear memory after saving

        # Pause between chunks to avoid rate limits
        time.sleep(2)

    return transactions

# Append transactions to CSV
def append_to_csv(transactions):
    with open(OUTPUT_FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        # Write header only if the file is empty
        if file.tell() == 0:
            writer.writerow(["Block Number", "Timestamp", "Transaction Hash", "From", "To", "Value (Ether)", "Gas", "Gas Price (Gwei)", "Input Data"])
        for tx in transactions:
            writer.writerow([tx["blockNumber"], tx["timestamp"], tx["hash"], tx["from"], tx["to"], tx["value"], tx["gas"], tx["gasPrice"], tx["input"]])
    print(f"Appended {len(transactions)} transactions to {OUTPUT_FILE}.")

# Main execution
if __name__ == "__main__":
    print("Connecting to Ethereum network...")
    transactions = fetch_transactions(CONTRACT_ADDRESS, START_BLOCK, END_BLOCK)
    if transactions:
        append_to_csv(transactions)  # Save remaining transactions
    print("Done!")
