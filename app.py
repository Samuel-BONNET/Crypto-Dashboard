from flask import Flask, render_template, jsonify
import requests
import time

app = Flask(__name__)

# --- Configuration ---
TOKENS = [
    ("BTCUSDT", "BTC"),
    ("ETHUSDT", "ETH"),
    ("SOLUSDT", "SOL"),
    ("LTCUSDT", "LTC"),
    ("XRPUSDT", "XRP"),
    ("DOGEUSDT", "DOGE"),
    ("ADAUSDT", "ADA"),
    ("DOTUSDT", "DOT"),
    ("AVAXUSDT", "AVAX"),
    ("TRXUSDT", "TRX"),
]

last_prices = None
last_fetch_time = 0

@app.route("/")
def home():
    return render_template("index.html", tokens=TOKENS)

@app.route("/token/<token_id>")
def token_page(token_id):
    if token_id not in [t[0] for t in TOKENS]:
        return "Token inconnu", 404
    return render_template("token.html", token_id=token_id)

@app.route("/api/prices")
def get_prices():
    global last_prices, last_fetch_time
    now = time.time()
    if last_prices is None or now - last_fetch_time > 5:  # cache 5 sec
        last_prices = {}
        for token, _ in TOKENS:
            r = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={token}")
            r.raise_for_status()
            data = r.json()
            last_prices[token] = {"usd": float(data["price"])}
        last_fetch_time = now
    return jsonify(last_prices)

@app.route("/api/history/<token_id>")
def token_history(token_id):
    if token_id not in [t[0] for t in TOKENS]:
        return jsonify({"error": "Token inconnu"}), 404

    # lire interval et limit depuis query params
    from flask import request
    interval = request.args.get("interval", "1m")
    limit = int(request.args.get("limit", 1440))

    url = "https://api.binance.com/api/v3/klines"
    params = {"symbol": token_id, "interval": interval, "limit": limit}
    r = requests.get(url, params=params)
    r.raise_for_status()
    data = r.json()

    prices = [[item[0], float(item[4])] for item in data]  # timestamp et close
    return jsonify({"prices": prices})


if __name__ == "__main__":
    app.run(debug=True)
