#this version works:
#add/delete new coin ok
#add existing coin ok
#add delete multiple alerts
#set to brazil loacl time ok
#tbd: -coins that return a huge list like solana or sui 
#     -setting alarms that already exist
#     -always poll coin data after new coin is added , then refresh page

from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
from pytz import timezone, UTC
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
monitored_coins_collection = db["monitored_coins"]
alerts_collection = db["alerts"]

CURRENCY = "usd"
POLL_INTERVAL = 30
BOT_TOKEN = "8077133568:AAFuDX_WgoSgVE1Agfn_IfD-tIDzBZxTK34"
CHAT_ID = "6316855666"

# Fetch cryptocurrency prices from CoinGecko
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

# Save fetched data to MongoDB
def save_to_mongodb(data):
    timestamp = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")  # Use pytz.UTC explicitly
    for crypto_id, details in data.items():
        price = details.get(CURRENCY)
        if price is not None:
            monitored_coin = monitored_coins_collection.find_one({"id": crypto_id})
            if monitored_coin:
                document = {
                    "name": monitored_coin["id"].capitalize(),  # Name as capitalized
                    "symbol": monitored_coin["symbol"],         # Correct symbol
                    "price_usd": price,                         # Price in USD
                    "timestamp": timestamp                      # Current timestamp
                }
                crypto_prices_collection.insert_one(document)
    print(f"Saved data to MongoDB at {timestamp}")

# Poll for crypto prices at regular intervals
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

# Send Telegram alerts
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        print(f"Failed to send message. Error: {response.text}")

# Check alerts
def check_alarms():
    while True:
        now = datetime.now(UTC)  # Use pytz.UTC explicitly
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

@app.route('/get_prices', methods=['GET'])
def get_prices():
    try:
        # Use aggregation to fetch the latest price for each symbol
        pipeline = [
            {"$sort": {"symbol": 1, "timestamp": -1}},  # Sort by symbol and timestamp (latest first)
            {
                "$group": {
                    "_id": "$symbol",
                    "name": {"$first": "$name"},
                    "symbol": {"$first": "$symbol"},
                    "price_usd": {"$first": "$price_usd"},
                    "timestamp": {"$first": "$timestamp"}
                }
            },
            {"$sort": {"symbol": 1}}  # Optional: Sort the results alphabetically by symbol
        ]

        coins = list(crypto_prices_collection.aggregate(pipeline))

        # Brazil timezone
        brazil_tz = timezone("America/Sao_Paulo")

        # Format timestamps
        for doc in coins:
            if "timestamp" in doc and doc["timestamp"]:
                # Parse UTC time
                utc_time = datetime.strptime(doc["timestamp"], "%Y-%m-%dT%H:%M:%SZ")
                utc_time = utc_time.replace(tzinfo=UTC)  # Attach UTC timezone explicitly
                # Convert to Brazil local time
                local_time = utc_time.astimezone(brazil_tz)
                doc["timestamp"] = local_time.strftime("%Y-%m-%d %H:%M:%S")
            else:
                doc["timestamp"] = "N/A"

        return jsonify(coins), 200
    except Exception as e:
        print(f"Error in /get_prices: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
    

@app.route('/add_coin', methods=['POST'])
def add_coin():
    """Add a new coin for monitoring."""
    try:
        data = request.get_json()
        coin_id = data.get("id")
        coin_name = data.get("name")
        symbol = data.get("symbol").upper()  # Ensure symbol is uppercase

        # Validate the input data
        if not coin_id or not symbol or not coin_name:
            print(f"Invalid data received: {data}")
            return jsonify({"status": "error", "message": "Invalid coin data provided"}), 400

        # Check if the coin is already in the monitored_coins_collection
        existing_coin = monitored_coins_collection.find_one({"id": coin_id})
        if existing_coin:
            print(f"Coin {coin_id} is already being monitored.")
            return jsonify({"status": "error", "message": "Coin is already being monitored"}), 400

        # Insert the coin into the monitored_coins_collection
        monitored_coins_collection.insert_one({
            "id": coin_id,
            "name": coin_name,
            "symbol": symbol,
            "enabled": True
        })

        print(f"Successfully added coin: {coin_id} ({symbol})")
        return jsonify({"status": "success", "message": f"{symbol} has been added for monitoring"}), 201
    except Exception as e:
        print(f"Error in add_coin: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/clear_database', methods=['DELETE'])
def clear_database():
    try:
        crypto_prices_collection.delete_many({})
        alerts_collection.delete_many({})
        monitored_coins_collection.update_many({}, {"$set": {"enabled": False}})
        return jsonify({"status": "success", "message": "Database cleared successfully."}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/delete_coin/<symbol>', methods=['DELETE'])
def delete_coin(symbol):
    try:
        # Convert symbol to uppercase for consistency
        symbol = symbol.upper()

        # Delete all related data from the database
        result_monitored = monitored_coins_collection.delete_one({"symbol": symbol})
        result_prices = crypto_prices_collection.delete_many({"symbol": symbol})
        result_alerts = alerts_collection.delete_many({"symbol": symbol})

        if result_monitored.deleted_count > 0:
            return jsonify({
                "status": "success",
                "message": f"Coin {symbol} and all related data have been deleted."
            }), 200
        else:
            return jsonify({
                "status": "error",
                "message": f"Coin {symbol} not found in the monitored coins collection."
            }), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/fetch_coins', methods=['GET'])
def fetch_coins():
    try:
        url = "https://api.coingecko.com/api/v3/coins/list"
        response = requests.get(url)
        if response.status_code == 200:
            coins = response.json()
            valid_coins = [{"id": coin["id"], "name": coin["name"], "symbol": coin["symbol"]} for coin in coins if "id" in coin and "name" in coin and "symbol" in coin]
            return jsonify(valid_coins), 200
        else:
            return jsonify({"status": "error", "message": "Failed to fetch coin list"}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/set_alert', methods=['POST'])
def set_alert():
    try:
        data = request.json
        symbol = data.get('symbol').upper()
        alert_type = data.get('alertType')
        alert_value = float(data.get('alertValue'))

        if not symbol or not alert_type or not alert_value:
            return jsonify({"status": "error", "message": "Invalid alert data provided."}), 400

        coin_exists = monitored_coins_collection.find_one({"symbol": symbol})
        if not coin_exists:
            return jsonify({"status": "error", "message": f"Coin {symbol} not found."}), 404

        alert_document = {
            "symbol": symbol,
            "alert_type": alert_type,
            "alert_value": alert_value,
            "alert_frequency": "daily",
            "state": "enabled",
            "last_triggered": None
        }
        alerts_collection.insert_one(alert_document)

        return jsonify({"status": "success", "message": f"Alert set for {symbol}."}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/get_alerts/<symbol>', methods=['GET'])
def get_alerts(symbol):
    try:
        symbol = symbol.upper()
        alerts = list(alerts_collection.find({"symbol": symbol}))

        formatted_alerts = []
        for alert in alerts:
            formatted_alerts.append({
                "_id": str(alert["_id"]),
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
    try:
        alert_object_id = ObjectId(alert_id)

        result = alerts_collection.delete_one({"_id": alert_object_id})

        if result.deleted_count > 0:
            return jsonify({"status": "success", "message": "Alert deleted successfully."}), 200
        else:
            return jsonify({"status": "error", "message": "Alert not found."}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": f"Invalid alert ID: {str(e)}"}), 400

@app.route('/toggle_alert/<alert_id>', methods=['PATCH'])
def toggle_alert(alert_id):
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

@app.route('/coin/<symbol>')
def coin_details(symbol):
    try:
        # Convert symbol to uppercase for consistency
        symbol = symbol.upper()
        # Check if the coin exists in the monitored collection
        coin = monitored_coins_collection.find_one({"symbol": symbol})
        if not coin:
            return "Coin not found", 404
        return render_template('coin_details.html', symbol=symbol)
    except Exception as e:
        return str(e), 500


if __name__ == '__main__':
    threading.Thread(target=poll_crypto_prices, daemon=True).start()
    threading.Thread(target=check_alarms, daemon=True).start()
    app.run(debug=True)
