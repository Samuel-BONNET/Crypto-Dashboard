from flask import Flask, render_template, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

COINS = ["bitcoin", "ethereum", "solana", "litecoin", "ripple", "dogecoin", "cardano", "polkadot", "avalanche-2", "tron"]
VS = "usd"

def fetch_prices():
    """Appelle CoinGecko pour obtenir les prix actuels."""
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": ",".join(COINS),
        "vs_currencies": VS,
        "include_24hr_change": "true"
    }
    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    data = r.json()
    return {"timestamp": datetime.utcnow().isoformat() + "Z", "prices": data}

@app.route("/")
def token_dashboard():
    return render_template("index.html", coins=COINS)

@app.route("/settings")
def settings():
    return render_template("settings.html")

@app.route("/news")
def news():
    return render_template("news.html")

@app.route("/portfolio")
def portfolio():
    return render_template("portfolio.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/api/prices")
def api_prices():
    return jsonify(fetch_prices())

if __name__ == "__main__":
    app.run(debug=True)


