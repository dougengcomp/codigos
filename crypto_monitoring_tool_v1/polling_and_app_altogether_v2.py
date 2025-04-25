from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime, timezone
import pytz
import threading
import time
import requests

app = Flask(__name__)

# MongoDB connection details
MONGO_CONNECTION_STRING = "mongodb+srv://douglasnascimento:Clg9xDHgAE7XmDyB@cluster0.rda0w.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DATABASE_NAME = "crypto_monitor_v1"
COLLECTION_NAME = "crypto_prices"

# Connect to MongoDB
client = MongoClient(MONGO_CONNECTION_STRING)
db = client[DATABASE_NAME]
crypto_prices_collection = db[COLLECTION_NAME]
alerts_collection = db["alerts"]

# Define the list of cryptocurrencies to monitor with their codes
CRYPTO_CODES = {
    "bitcoin": "BTC",
    "ethereum": "ETH",
    "solana": "SOL",
    "avalanche-2": "AVAX",
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

# Telegram Bot API credentials
BOT_TOKEN = "8077133568:AAFuDX_WgoSgVE1Agfn_IfD-tIDzBZxTK34"
CHAT_ID = "6316855666"  # Your Telegram Chat ID

def send_telegram_message(message):
    """Send a message to a Telegram chat."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("Message sent successfully!")
    else:
        print(f"Failed to send message. Error: {response.text}")

def get_crypto_prices(crypto_codes, currency):
    """Fetch the current prices of the given cryptocurrencies from CoinGecko."""
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": ",".join(crypto_codes.keys()),  # Dynamically use updated keys
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
    """Save cryptocurrency price data to MongoDB."""
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")  # UTC timestamp
    for crypto_id, details in data.items():
        document = {
            "name": crypto_id.capitalize(),
            "symbol": CRYPTO_CODES[crypto_id],
            "price_usd": details[CURRENCY],
            "timestamp": timestamp
        }
        crypto_prices_collection.insert_one(document)
    print(f"Saved data to MongoDB at {timestamp}")

def poll_crypto_prices():
    """Continuously poll cryptocurrency prices and save to MongoDB."""
    while True:
        global CRYPTO_CODES  # Ensure global reference is used
        if not CRYPTO_CODES:
            print("No cryptocurrencies to poll. Waiting for additions.")
            time.sleep(POLL_INTERVAL)
            continue

        # Poll prices for the current list of cryptocurrencies
        prices = get_crypto_prices(CRYPTO_CODES, CURRENCY)
        if prices:
            # Ensure we only save data for currently monitored cryptocurrencies
            filtered_prices = {k: v for k, v in prices.items() if k in CRYPTO_CODES}
            save_to_mongodb(filtered_prices)
        else:
            print("No prices fetched during this poll.")
        time.sleep(POLL_INTERVAL)

def check_alarms():
    """Check alarms and trigger Telegram messages when conditions are met."""
    while True:
        now = datetime.utcnow()
        alerts = list(alerts_collection.find({"state": "enabled"}))
        
        for alert in alerts:
            symbol = alert["symbol"]
            alert_type = alert["alert_type"]
            alert_value = alert["alert_value"]
            alert_frequency = alert["alert_frequency"]
            last_triggered = alert.get("last_triggered")

            # Fetch the latest price for the cryptocurrency
            latest_price_doc = crypto_prices_collection.find_one({"symbol": symbol}, sort=[("timestamp", -1)])
            if not latest_price_doc:
                continue
            current_price = latest_price_doc["price_usd"]

            # Check if the alarm condition is met
            if (alert_type == "price_drops" and current_price <= alert_value) or \
               (alert_type == "price_rises" and current_price >= alert_value):
                
                # Check frequency logic
                if alert_frequency == "once" and last_triggered:
                    continue  # Skip if the alarm has already been triggered

                if alert_frequency == "daily" and last_triggered:
                    last_triggered_date = datetime.strptime(last_triggered, "%Y-%m-%dT%H:%M:%SZ").date()
                    if last_triggered_date == now.date():
                        continue  # Skip if the message has already been sent today

                # Send Telegram message
                message = f"ALERT: {symbol} has {'dropped below' if alert_type == 'price_drops' else 'risen above'} {alert_value} USD. Current price: {current_price:.2f} USD."
                send_telegram_message(message)

                # Update the alarm's last_triggered field
                alerts_collection.update_one(
                    {"_id": alert["_id"]},
                    {"$set": {"last_triggered": now.strftime("%Y-%m-%dT%H:%M:%SZ")}}
                )

                # Disable the alarm if it's a "once" alarm
                if alert_frequency == "once":
                    alerts_collection.update_one(
                        {"_id": alert["_id"]},
                        {"$set": {"state": "disabled"}}
                    )
        time.sleep(30)  # Check alarms every 30 seconds

# Run the polling and alarm checker in separate threads
threading.Thread(target=poll_crypto_prices, daemon=True).start()
threading.Thread(target=check_alarms, daemon=True).start()

@app.route('/')
def index():
    """Render the main dashboard page with the lateral menu."""
    return render_template('index.html')

@app.route('/get_prices')
def get_prices():
    """Fetch the latest cryptocurrency prices from MongoDB."""
    latest_prices = []
    cursor = crypto_prices_collection.aggregate([
        {"$sort": {"timestamp": -1}},
        {"$group": {
            "_id": "$symbol",
            "name": {"$first": "$name"},
            "symbol": {"$first": "$symbol"},
            "price_usd": {"$first": "$price_usd"},
            "timestamp": {"$first": "$timestamp"}
        }}
    ])

    brazil_tz = pytz.timezone('America/Sao_Paulo')
    for doc in cursor:
        utc_time = datetime.strptime(doc["timestamp"], "%Y-%m-%dT%H:%M:%SZ")
        local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(brazil_tz)
        formatted_time = local_time.strftime("%d/%m/%Y %H:%M:%S")
        latest_prices.append({
            "name": doc["name"],
            "symbol": doc["symbol"],
            "price_usd": doc["price_usd"],
            "timestamp": formatted_time
        })

    latest_prices = sorted(latest_prices, key=lambda x: x["name"])
    return jsonify(latest_prices)

@app.route('/coin/<symbol>')
def coin_details(symbol):
    """Render the coin details page for a specific cryptocurrency."""
    return render_template('coin_details.html', symbol=symbol.upper())

@app.route('/get_alerts/<symbol>')
def get_alerts(symbol):
    """Fetch all alerts for a specific cryptocurrency."""
    alerts = list(alerts_collection.find({"symbol": symbol.upper()}))
    for alert in alerts:
        alert["_id"] = str(alert["_id"])  # Convert ObjectId to string for JSON
    return jsonify(alerts)

@app.route('/set_alert', methods=['POST'])
@app.route('/set_alert', methods=['POST'])
@app.route('/set_alert', methods=['POST'])
def set_alert():
    """Set or update a price alert for a specific cryptocurrency."""
    data = request.json
    symbol = data.get('symbol')
    alert_type = data.get('alertType')  # price_drops or price_rises
    alert_value = data.get('alertValue')
    alert_frequency = data.get('alertFrequency')  # once or daily

    # Enforce specific format for alert_value
    try:
        # Check for valid format (e.g., 0.00001)
        if not isinstance(alert_value, str) or not alert_value.replace('.', '', 1).isdigit():
            raise ValueError("Alert value must be a number with a period as the decimal separator.")
        alert_value = float(alert_value)  # Convert to float
        if alert_value <= 0:
            raise ValueError("Alert value must be a positive number.")
    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 400

    if not symbol or not alert_type or not alert_frequency:
        return jsonify({"status": "error", "message": "Invalid input."}), 400

    # Save alert to MongoDB
    alert = {
        "symbol": symbol,
        "alert_type": alert_type,
        "alert_value": alert_value,
        "alert_frequency": alert_frequency,
        "state": "enabled",
        "triggered": False,
        "last_triggered": None,
        "created_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    }
    alerts_collection.insert_one(alert)

    return jsonify({"status": "success", "message": f"Alert set for {symbol} with value {alert_value} USD."}), 200

@app.route('/update_alert/<alert_id>', methods=['PUT'])
def update_alert(alert_id):
    """Update the state or value of an existing alert."""
    data = request.json
    updated_fields = {}

    if "state" in data:
        updated_fields["state"] = data["state"]
    if "alert_value" in data:
        updated_fields["alert_value"] = float(data["alert_value"])

    result = alerts_collection.update_one({"_id": ObjectId(alert_id)}, {"$set": updated_fields})

    if result.matched_count > 0:
        return jsonify({"status": "success", "message": "Alert updated successfully."}), 200
    else:
        return jsonify({"status": "error", "message": "Alert not found."}), 404

@app.route('/delete_alert/<alert_id>', methods=['DELETE'])
def delete_alert(alert_id):
    """Delete an alert by its ID."""
    result = alerts_collection.delete_one({"_id": ObjectId(alert_id)})
    if result.deleted_count > 0:
        return jsonify({"status": "success", "message": "Alert deleted successfully."}), 200
    else:
        return jsonify({"status": "error", "message": "Alert not found."}), 404

@app.route('/delete_coin/<symbol>', methods=['DELETE'])
def delete_coin(symbol):
    """Delete a monitored coin and all related alerts and historical data."""
    global CRYPTO_CODES
    symbol = symbol.upper()

    # Remove historical price data
    historical_result = crypto_prices_collection.delete_many({"symbol": symbol})

    # Remove associated alerts
    alert_result = alerts_collection.delete_many({"symbol": symbol})

    # Remove from monitored coins (CRYPTO_CODES)
    for key, value in list(CRYPTO_CODES.items()):
        if value == symbol:
            del CRYPTO_CODES[key]
            print(f"Deleted {symbol} from monitored cryptocurrencies.")
            break

    return jsonify({
        "status": "success",
        "message": f"Removed {symbol} with {historical_result.deleted_count} historical records and {alert_result.deleted_count} alerts."
    }), 200


if __name__ == '__main__':
    app.run(debug=True)



