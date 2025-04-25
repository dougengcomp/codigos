#this version v8 works:
#add/delete new coin ok
#add existing coin ok
#add delete multiple alerts
#set to brazil loacl time ok
#-reset mongo db totally, right now it is only disabling alarm but not deleting it ok
#-coins that return a huge list like solana or sui  ok
#always poll coin data after new coin is added , then refresh page ok
#added register.html and login.html functions and routes
#-setting alarms that already exist ok
#-when new user is created there's no feedback of success or fail ok
#-must check if username or email already exist on users db before accepting a new user. ok
#-when coin is deleted its price history is kept on mongo db crypto_prices (should be removed in case no other user monitors it) ok
#working on: 
# -whatsapp send alert (not allowed for crypto, and also requires webpage)
#tbd: 
#    -telegram mechanism for multiple users
#     -

from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from pymongo import MongoClient
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from pytz import timezone, UTC
import threading
import time
import requests


app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Initialize Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'


# MongoDB connection details
MONGO_CONNECTION_STRING = "mongodb+srv://douglasnascimento:Clg9xDHgAE7XmDyB@cluster0.rda0w.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DATABASE_NAME = "crypto_monitor_v1"
COLLECTION_NAME = "crypto_prices"

# Connect to MongoDB
client = MongoClient(MONGO_CONNECTION_STRING)
db = client[DATABASE_NAME]
users_collection = db["users"]
crypto_prices_collection = db[COLLECTION_NAME]
monitored_coins_collection = db["monitored_coins"]
alerts_collection = db["alerts"]

#generic vars
CURRENCY = "usd"
POLL_INTERVAL = 30

#Telegram config
BOT_TOKEN = "8077133568:AAFuDX_WgoSgVE1Agfn_IfD-tIDzBZxTK34"
CHAT_ID = "6316855666"

'''# WhatsApp API configuration
WHATSAPP_TOKEN = "EAAYTH2gsMOcBOyO2XcriREyLt1G3BL8ZCMJqhJeC9tOcy80QCO6ncqyza4qQ6DdotX23sXAuPf6kCBU9VER64hpTZC5FjZBM3Vq2C8hIUIILZBHLc5XZCnBFh3qHhET4aVAi3aLYAekTLo6dV8IcrkZB4Lqw4fQuxZBAylA3rPnviByOo9t8CFfgHkmXuS84WNtVsz0gUrncdKe2e6bzATZCVnQ5aExsleyy5soTeLw1vUAZD"  # Replace with your token
WHATSAPP_PHONE_ID = "563325190199189"  #caller id , senders number ID taken from meta api
WHATSAPP_API_URL = f"https://graph.facebook.com/v21.0/{WHATSAPP_PHONE_ID}/messages"
WHATSAPP_DESTINATION_NUMBER="5551999002063" #whtasapp destination recipient'''

# Flask-Login User class
class User(UserMixin):
    def __init__(self, user_id, username, email):
        self.id = user_id
        self.username = username
        self.email = email

def enforce_storage_limit():
    max_size_bytes = 200 * 1024 * 1024  # 200MB in bytes
    check_interval = 60 * 10  # Check every 10 minutes

    while True:
        try:
            # Get collection stats
            stats = db.command("collstats", COLLECTION_NAME)
            collection_size = stats.get("size", 0)

            if collection_size > max_size_bytes:
                excess_size = collection_size - max_size_bytes
                print(f"Collection exceeds size limit by {excess_size} bytes. Deleting old data...")

                # Sort by timestamp and delete oldest entries
                to_delete = list(crypto_prices_collection.find({}, {"_id": 1}).sort("timestamp", 1).limit(excess_size // stats["avgObjSize"]))
                if to_delete:
                    crypto_prices_collection.delete_many({"_id": {"$in": [doc["_id"] for doc in to_delete]}})
                    print(f"Deleted {len(to_delete)} documents to free up space.")
            else:
                print("Collection size is within limits.")

        except Exception as e:
            print(f"Error enforcing storage limit: {e}")

        time.sleep(check_interval)


@login_manager.user_loader
def load_user(user_id):
    user_data = users_collection.find_one({"_id": ObjectId(user_id)})
    if user_data:
        return User(str(user_data["_id"]), user_data["username"], user_data["email"])
    return None

def is_admin():
    return current_user.is_authenticated and users_collection.find_one({"_id": ObjectId(current_user.id), "is_admin": True})

# User Registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if username or email already exists
        if users_collection.find_one({"username": username}):
            return render_template('register.html', message="Username already exists. Please choose a different one.")
        if users_collection.find_one({"email": email}):
            return render_template('register.html', message="Email already exists. Please use a different email address.")

        try:
            # Hash the password and save the user with is_admin set to False
            hashed_password = generate_password_hash(password)
            users_collection.insert_one({
                "username": username,
                "email": email,
                "password_hash": hashed_password,
                "is_admin": False  # Default to non-admin
            })
            return render_template('login.html', message="User created successfully. You can now log in.")
        except Exception as e:
            return render_template('register.html', message=f"An error occurred: {str(e)}")

    return render_template('register.html', message=None)

# User Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user_data = users_collection.find_one({"email": email})
        if user_data and check_password_hash(user_data["password_hash"], password):
            user = User(str(user_data["_id"]), user_data["username"], user_data["email"])
            login_user(user)
            return redirect(url_for('index'))
        return "Invalid credentials!", 401
    return render_template('login.html')

# User Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

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

'''
# Send WhatsApp message
def send_whatsapp_message(phone_number, message):
    url = WHATSAPP_API_URL
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "text",
        "text": {"body": message}
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        print(f"WhatsApp message sent to {phone_number}: {message}")
    else:
        print(f"Failed to send WhatsApp message. Error: {response.text}")
'''

# Check alerts
def check_alarms():
    while True:
        now = datetime.now(UTC)
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
                # Send Telegram and WhatsApp messages
                send_telegram_message(message)
                #send_whatsapp_message(WHATSAPP_DESTINATION_NUMBER, message)

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
@login_required
def index():
    return render_template('index.html', username=current_user.username)

@app.route('/get_prices', methods=['GET'])
@login_required
def get_prices():
    try:
        # Fetch monitored coins for the current user
        user_coins = monitored_coins_collection.find({"user_id": current_user.id})
        user_symbols = [coin["symbol"] for coin in user_coins]

        # Use aggregation to fetch the latest price for each symbol monitored by the user
        pipeline = [
            {"$match": {"symbol": {"$in": user_symbols}}},
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

        if not coin_id or not symbol or not coin_name:
            return jsonify({"status": "error", "message": "Invalid coin data provided"}), 400

        # Check if the coin is already being monitored for the current user
        existing_coin = monitored_coins_collection.find_one({"user_id": current_user.id, "id": coin_id})
        if existing_coin:
            return jsonify({"status": "error", "message": "Coin is already being monitored"}), 400

        # Add coin to the database, associating it with the current user
        monitored_coins_collection.insert_one({
            "user_id": current_user.id,
            "id": coin_id,
            "name": coin_name,
            "symbol": symbol,
            "enabled": True
        })

        # Fetch the price immediately
        prices = get_crypto_prices([coin_id])
        if prices:
            save_to_mongodb(prices)
            return jsonify({"status": "success", "message": f"{symbol} has been added and price updated."}), 201
        else:
            return jsonify({"status": "error", "message": f"Failed to fetch price for {symbol}. Please try again."}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/clear_database', methods=['DELETE'])
@login_required
def clear_database():
    try:
        # Clear data only for the current user
        crypto_prices_collection.delete_many({"user_id": current_user.id})
        alerts_collection.delete_many({"user_id": current_user.id})
        monitored_coins_collection.delete_many({"user_id": current_user.id})

        print(f"Database cleared for user: {current_user.username}")
        return jsonify({"status": "success", "message": "Database cleared successfully for your account."}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/delete_coin/<symbol>', methods=['DELETE'])
@login_required
def delete_coin(symbol):
    try:
        # Convert symbol to uppercase for consistency
        symbol = symbol.upper()

        # Delete the monitored coin for the current user
        result_monitored = monitored_coins_collection.delete_one({"user_id": current_user.id, "symbol": symbol})

        if result_monitored.deleted_count > 0:
            # Check if any other user is monitoring this coin
            other_users_monitoring = monitored_coins_collection.find_one({"symbol": symbol})
            if not other_users_monitoring:
                # If no other users are monitoring, remove price history
                crypto_prices_collection.delete_many({"symbol": symbol})
                print(f"Price history for {symbol} deleted as no other users are monitoring it.")

            # Also remove associated alerts for the current user
            alerts_collection.delete_many({"user_id": current_user.id, "symbol": symbol})

            return jsonify({
                "status": "success",
                "message": f"Coin {symbol} and related data have been deleted for your account."
            }), 200
        else:
            return jsonify({
                "status": "error",
                "message": f"Coin {symbol} not found in your monitored coins collection."
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
        alert_frequency = data.get('alertFrequency', 'daily')  # Default to daily if not provided

        if not symbol or not alert_type or not alert_value:
            return jsonify({"status": "error", "message": "Invalid alert data provided."}), 400

        # Check if the coin exists for the current user
        coin_exists = monitored_coins_collection.find_one({"user_id": current_user.id, "symbol": symbol})
        if not coin_exists:
            return jsonify({"status": "error", "message": f"Coin {symbol} not found for the current user."}), 404

        # Check if an alert with the same parameters already exists for the current user
        existing_alert = alerts_collection.find_one({
            "user_id": current_user.id,
            "symbol": symbol,
            "alert_type": alert_type,
            "alert_value": alert_value
        })

        if existing_alert:
            return jsonify({"status": "error", "message": "An alert with the same parameters already exists."}), 400

        # Create a new alert
        alert_document = {
            "user_id": current_user.id,
            "symbol": symbol,
            "alert_type": alert_type,
            "alert_value": alert_value,
            "alert_frequency": alert_frequency,
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
        # Fetch alerts for the current user and the specified symbol
        alerts = list(alerts_collection.find({"user_id": current_user.id, "symbol": symbol}))

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
@login_required
def delete_alert(alert_id):
    try:
        alert_object_id = ObjectId(alert_id)

        # Delete the alert only if it belongs to the current user
        result = alerts_collection.delete_one({"_id": alert_object_id, "user_id": current_user.id})

        if result.deleted_count > 0:
            return jsonify({"status": "success", "message": "Alert deleted successfully."}), 200
        else:
            return jsonify({"status": "error", "message": "Alert not found or does not belong to you."}), 404
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
@login_required
def coin_details(symbol):
    try:
        # Convert symbol to uppercase for consistency
        symbol = symbol.upper()

        # Check if the coin exists in the monitored collection for the current user
        coin = monitored_coins_collection.find_one({"user_id": current_user.id, "symbol": symbol})
        if not coin:
            return "Coin not found in your monitored list", 404

        return render_template('coin_details.html', symbol=symbol)
    except Exception as e:
        return str(e), 500

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user_data = users_collection.find_one({"email": email, "is_admin": True})
        if user_data and check_password_hash(user_data['password_hash'], password):
            user = User(str(user_data['_id']), user_data['username'], user_data['email'])
            login_user(user)
            return redirect(url_for('admin_dashboard'))
        
        return render_template('admin_login.html', message="Invalid admin credentials.")

    return render_template('admin_login.html', message=None)

@app.route('/admin_dashboard')
@login_required
def admin_dashboard():
    # Ensure only admins can access
    if not is_admin():
        return redirect(url_for('index'))

    try:
        # Fetch all users and exclude password_hash
        users = list(users_collection.find({}, {"password_hash": 0}))
        print(users)  # Log users to confirm data is fetched
        return render_template('admin_dashboard.html', users=users)
    except Exception as e:
        return render_template('admin_dashboard.html', error=str(e))

@app.route('/admin_add_user', methods=['POST'])
@login_required
def admin_add_user():
    # Ensure the current user is an admin
    if not is_admin():
        return jsonify({"status": "error", "message": "Unauthorized"}), 403

    try:
        data = request.json
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        is_admin_flag = data.get('is_admin', False)  # Rename variable to avoid conflict

        # Validate inputs
        if not username or not email or not password:
            return jsonify({"status": "error", "message": "All fields are required."}), 400

        # Check if email already exists
        if users_collection.find_one({"email": email}):
            return jsonify({"status": "error", "message": "User with this email already exists."}), 400

        # Hash the password and insert into the database
        hashed_password = generate_password_hash(password)
        users_collection.insert_one({
            "username": username,
            "email": email,
            "password_hash": hashed_password,
            "is_admin": is_admin_flag  # Use the renamed variable here
        })

        return jsonify({"status": "success", "message": "User added successfully."}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/admin_delete_user/<user_id>', methods=['DELETE'])
@login_required
def admin_delete_user(user_id):
    if not is_admin():
        return jsonify({"status": "error", "message": "Unauthorized"}), 403

    users_collection.delete_one({"_id": ObjectId(user_id)})
    return jsonify({"status": "success", "message": "User deleted successfully."})

@app.route('/admin_update_user/<user_id>', methods=['PATCH'])
@login_required
def admin_update_user(user_id):
    if not is_admin():
        return jsonify({"status": "error", "message": "Unauthorized"}), 403

    try:
        data = request.json
        update_fields = {}

        if 'username' in data:
            update_fields['username'] = data['username']
        if 'email' in data:
            update_fields['email'] = data['email']
        if 'password' in data:
            update_fields['password_hash'] = generate_password_hash(data['password'])

        if update_fields:
            users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": update_fields})
            return jsonify({"status": "success", "message": "User updated successfully."}), 200
        else:
            return jsonify({"status": "error", "message": "No valid fields to update."}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    threading.Thread(target=poll_crypto_prices, daemon=True).start()
    threading.Thread(target=check_alarms, daemon=True).start()
    threading.Thread(target=enforce_storage_limit, daemon=True).start()
    app.run(debug=True)

