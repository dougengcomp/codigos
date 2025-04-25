from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
import pytz
import threading
import time
import requests

app = Flask(__name__)

# MongoDB connection details
MONGO_CONNECTION_STRING = "mongodb+srv://douglasnascimento:Clg9xDHgAE7XmDyB@cluster0.rda0w.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DATABASE_NAME = "crypto_monitor_v1"

# Connect to MongoDB
client = MongoClient(MONGO_CONNECTION_STRING)
db = client[DATABASE_NAME]
crypto_prices_collection = db["crypto_prices"]
alerts_collection = db["alerts"]

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

# Run the alarm checker in a separate thread
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
def set_alert():
    """Set a price alert for a specific cryptocurrency."""
    data = request.json
    symbol = data.get('symbol')
    alert_type = data.get('alertType')  # price_drops or price_rises
    alert_value = data.get('alertValue')
    alert_frequency = data.get('alertFrequency')  # once or daily

    if not symbol or not alert_type or alert_value is None or not alert_frequency:
        return jsonify({"status": "error", "message": "Invalid input."}), 400

    if not isinstance(alert_value, (int, float)) or alert_value <= 0:
        return jsonify({"status": "error", "message": "Alert value must be a positive number."}), 400

    alert = {
        "symbol": symbol,
        "alert_type": alert_type,
        "alert_value": float(alert_value),
        "alert_frequency": alert_frequency,
        "state": "enabled",
        "triggered": False,
        "last_triggered": None,
        "created_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    }
    alerts_collection.insert_one(alert)
    return jsonify({"status": "success", "message": f"Alert set for {symbol} with value {alert_value} USD."}), 200

@app.route('/delete_alert/<alert_id>', methods=['DELETE'])
def delete_alert(alert_id):
    """Delete an alert by its ID."""
    result = alerts_collection.delete_one({"_id": ObjectId(alert_id)})
    if result.deleted_count > 0:
        return jsonify({"status": "success", "message": "Alert deleted successfully."}), 200
    else:
        return jsonify({"status": "error", "message": "Alert not found."}), 404

if __name__ == '__main__':
    app.run(debug=True)
