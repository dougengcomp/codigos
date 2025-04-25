from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime, timezone
import pytz
import threading
import time
import requests
from bson.objectid import ObjectId

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
monitored_coins_collection = db["monitored_coins"]

# Preload initial coins into MongoDB if the collection is empty
if monitored_coins_collection.count_documents({}) == 0:
    initial_coins = [
        {"id": "bitcoin", "symbol": "BTC", "enabled": True},
        {"id": "ethereum", "symbol": "ETH", "enabled": True},
        {"id": "solana", "symbol": "SOL", "enabled": True},
        {"id": "sui", "symbol": "SUI", "enabled": True},
        {"id": "ripple", "symbol": "XRP", "enabled": True},
        {"id": "dogecoin", "symbol": "DOGE", "enabled": True}
    ]
    monitored_coins_collection.insert_many(initial_coins)

CURRENCY = "usd"
POLL_INTERVAL = 30

BOT_TOKEN = "8077133568:AAFuDX_WgoSgVE1Agfn_IfD-tIDzBZxTK34"
CHAT_ID = "6316855666"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        print(f"Failed to send message. Error: {response.text}")

def get_crypto_prices(crypto_codes):
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": ",".join(crypto_codes), "vs_currencies": CURRENCY}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 429:
        print("Rate limit reached. Retrying in 60 seconds...")
        time.sleep(60)
        return {}
    else:
        print(f"Error fetching data: {response.status_code} - {response.text}")
        return {}

def save_to_mongodb(data):
    """Save cryptocurrency price data to MongoDB."""
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    for crypto_id, details in data.items():
        document = {
            "name": crypto_id.capitalize(),  # Name from CoinGecko IDs
            "symbol": monitored_coins_collection.find_one({"id": crypto_id})["symbol"],  # Fetch correct symbol
            "price_usd": details[CURRENCY],  # Correct price
            "timestamp": timestamp          # Save timestamp
        }
        crypto_prices_collection.insert_one(document)
    print(f"Saved data to MongoDB at {timestamp}")

def poll_crypto_prices():
    while True:
        enabled_coins = list(monitored_coins_collection.find({"enabled": True}))
        crypto_codes = [coin["id"] for coin in enabled_coins]

        if not crypto_codes:
            print("No cryptocurrencies to poll. Waiting for additions.")
            time.sleep(POLL_INTERVAL)
            continue

        prices = get_crypto_prices(crypto_codes)
        if prices:
            save_to_mongodb(prices)
        time.sleep(POLL_INTERVAL)

def check_alarms():
    while True:
        now = datetime.utcnow()
        alerts = list(alerts_collection.find({"state": "enabled"}))
        
        for alert in alerts:
            symbol = alert["symbol"]
            alert_type = alert["alert_type"]
            alert_value = alert["alert_value"]
            alert_frequency = alert["alert_frequency"]
            last_triggered = alert.get("last_triggered")

            latest_price_doc = crypto_prices_collection.find_one({"symbol": symbol}, sort=[("timestamp", -1)])
            if not latest_price_doc:
                continue
            current_price = latest_price_doc["price_usd"]

            if (alert_type == "price_drops" and current_price <= alert_value) or \
               (alert_type == "price_rises" and current_price >= alert_value):
                if alert_frequency == "once" and last_triggered:
                    continue

                if alert_frequency == "daily" and last_triggered:
                    last_triggered_date = datetime.strptime(last_triggered, "%Y-%m-%dT%H:%M:%SZ").date()
                    if last_triggered_date == now.date():
                        continue

                message = f"ALERT: {symbol} has {'dropped below' if alert_type == 'price_drops' else 'risen above'} {alert_value} USD. Current price: {current_price:.2f} USD."
                send_telegram_message(message)

                alerts_collection.update_one(
                    {"_id": alert["_id"]},
                    {"$set": {"last_triggered": now.strftime("%Y-%m-%dT%H:%M:%SZ")}}
                )

                if alert_frequency == "once":
                    alerts_collection.update_one(
                        {"_id": alert["_id"]},
                        {"$set": {"state": "disabled"}}
                    )
        time.sleep(30)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_prices')
def get_prices():
    """Fetch the latest cryptocurrency prices from MongoDB."""
    latest_prices = []
    cursor = crypto_prices_collection.aggregate([
        {"$sort": {"timestamp": -1}},
        {"$group": {
            "_id": "$symbol",  # Group by symbol to prevent duplicates
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
            "name": doc["name"],           # Use the correct name
            "symbol": doc["symbol"],       # Ensure symbol is displayed
            "price_usd": doc["price_usd"], # Display the correct price
            "timestamp": formatted_time
        })

    return jsonify(latest_prices)

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

    return jsonify(latest_prices)

@app.route('/delete_coin/<symbol>', methods=['DELETE'])
def delete_coin(symbol):
    result = monitored_coins_collection.update_one(
        {"symbol": symbol.upper()},
        {"$set": {"enabled": False}}
    )
    if result.matched_count > 0:
        return jsonify({"status": "success", "message": f"{symbol.upper()} disabled for monitoring."}), 200
    else:
        return jsonify({"status": "error", "message": f"Coin {symbol.upper()} not found."}), 404

@app.route('/add_coin', methods=['POST'])
def add_coin():
    data = request.json
    coin_id = data.get("id")
    symbol = data.get("symbol")

    if not coin_id or not symbol:
        return jsonify({"status": "error", "message": "Invalid coin data."}), 400

    existing_coin = monitored_coins_collection.find_one({"id": coin_id})
    if existing_coin:
        monitored_coins_collection.update_one(
            {"id": coin_id},
            {"$set": {"enabled": True}}
        )
        return jsonify({"status": "success", "message": f"{symbol} enabled for monitoring."}), 200

    monitored_coins_collection.insert_one({"id": coin_id, "symbol": symbol.upper(), "enabled": True})
    return jsonify({"status": "success", "message": f"{symbol} added to monitoring list."}), 201

@app.route('/clear_database', methods=['DELETE'])
def clear_database():
    """Clear all data from the MongoDB collections."""
    try:
        crypto_prices_collection.delete_many({})
        alerts_collection.delete_many({})
        monitored_coins_collection.update_many({}, {"$set": {"enabled": False}})
        return jsonify({"status": "success", "message": "Database cleared successfully."}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": f"An error occurred: {str(e)}"}), 500

@app.route('/coin/<symbol>')
def coin_details(symbol):
    """Render the coin details page for a specific cryptocurrency."""
    # Normalize symbol to uppercase to match the database entries
    symbol = symbol.upper()

    # Check if the coin exists in the monitored_coins collection
    monitored_coin = monitored_coins_collection.find_one({"symbol": symbol})
    if not monitored_coin:
        return "Coin not found", 404

    # Pass the symbol to the template
    return render_template('coin_details.html', symbol=symbol)

@app.route('/set_alert', methods=['POST'])
def set_alert():
    """Set a new alert for a cryptocurrency."""
    try:
        data = request.json
        symbol = data.get('symbol').upper()
        alert_type = data.get('alertType')
        alert_value = float(data.get('alertValue'))
        
        # Validate input
        if not symbol or not alert_type or not alert_value:
            return jsonify({"status": "error", "message": "Invalid alert data provided."}), 400

        # Check if the coin exists in the monitored_coins collection
        coin_exists = monitored_coins_collection.find_one({"symbol": symbol})
        if not coin_exists:
            return jsonify({"status": "error", "message": f"Coin {symbol} not found."}), 404

        # Insert the alert into the alerts collection
        alert_document = {
            "symbol": symbol,
            "alert_type": alert_type,
            "alert_value": alert_value,
            "alert_frequency": "daily",  # Default frequency
            "state": "enabled",         # Default state
            "last_triggered": None     # Initially not triggered
        }
        alerts_collection.insert_one(alert_document)

        return jsonify({"status": "success", "message": f"Alert set for {symbol}."}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/get_alerts/<symbol>', methods=['GET'])
def get_alerts(symbol):
    """Retrieve all alerts for a specific cryptocurrency."""
    try:
        symbol = symbol.upper()
        alerts = list(alerts_collection.find({"symbol": symbol}))
        
        # Format the alerts for JSON response
        formatted_alerts = []
        for alert in alerts:
            formatted_alerts.append({
                "_id": str(alert["_id"]),  # Convert ObjectId to string
                "symbol": alert["symbol"],
                "alert_type": alert["alert_type"],
                "alert_value": alert["alert_value"],
                "alert_frequency": alert.get("alert_frequency", "daily"),
                "state": alert.get("state", "enabled"),
                "last_triggered": alert.get("last_triggered")
            })

        return jsonify(formatted_alerts), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/delete_alert/<alert_id>', methods=['DELETE'])
def delete_alert(alert_id):
    """Delete an alert by its ID."""
    try:
        # Convert alert_id to ObjectId for MongoDB query
        alert_object_id = ObjectId(alert_id)
        
        # Attempt to delete the alert
        result = alerts_collection.delete_one({"_id": alert_object_id})
        
        if result.deleted_count > 0:
            return jsonify({"status": "success", "message": "Alert deleted successfully."}), 200
        else:
            return jsonify({"status": "error", "message": "Alert not found."}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": f"Invalid alert ID: {str(e)}"}), 400

@app.route('/toggle_alert/<alert_id>', methods=['PATCH'])
def toggle_alert(alert_id):
    """Enable or disable an alert by its ID."""
    try:
        data = request.json
        new_state = data.get("state", "enabled").lower()
        if new_state not in ["enabled", "disabled"]:
            return jsonify({"status": "error", "message": "Invalid state provided."}), 400

        result = alerts_collection.update_one(
            {"_id": ObjectId(alert_id)},
            {"$set": {"state": new_state}}
        )
        if result.matched_count > 0:
            return jsonify({"status": "success", "message": f"Alert {new_state} successfully."}), 200
        else:
            return jsonify({"status": "error", "message": "Alert not found."}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    threading.Thread(target=poll_crypto_prices, daemon=True).start()
    threading.Thread(target=check_alarms, daemon=True).start()
    app.run(debug=True)
