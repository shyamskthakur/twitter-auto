import os
import requests
import tweepy
from datetime import datetime

# Twitter credentials
api_key = os.environ["API_KEY"]
api_secret = os.environ["API_SECRET"]
access_token = os.environ["ACCESS_TOKEN"]
access_secret = os.environ["ACCESS_SECRET"]

auth = tweepy.OAuth1UserHandler(
    api_key,
    api_secret,
    access_token,
    access_secret
)

api = tweepy.API(auth)

# Fetch data from CoinGecko
response = requests.get(
    "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,pax-gold,silver-token&vs_currencies=usd&include_24hr_change=true"
)

data = response.json()

# Safe extraction function
def safe_round(value):
    if value is None:
        return "N/A"
    return round(value, 2)

btc_price = safe_round(data.get("bitcoin", {}).get("usd"))
btc_change = safe_round(data.get("bitcoin", {}).get("usd_24h_change"))

gold_price = safe_round(data.get("pax-gold", {}).get("usd"))
gold_change = safe_round(data.get("pax-gold", {}).get("usd_24h_change"))

silver_price = safe_round(data.get("silver-token", {}).get("usd"))
silver_change = safe_round(data.get("silver-token", {}).get("usd_24h_change"))

time_now = datetime.utcnow().strftime("%H:%M UTC")

tweet = f"""📊 Market Update ({time_now})

🟡 Gold: ${gold_price} ({gold_change}%)
⚪ Silver: ${silver_price} ({silver_change}%)
₿ Bitcoin: ${btc_price} ({btc_change}%)

#Gold #Silver #Bitcoin #Crypto #Forex"""

api.update_status(tweet)

print("Market update posted successfully!")
