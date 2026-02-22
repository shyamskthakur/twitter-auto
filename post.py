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

# Get Bitcoin, Gold (PAXG), Silver (XAG) from CoinGecko
data = requests.get(
    "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,pax-gold,silver-token&vs_currencies=usd&include_24hr_change=true"
).json()

btc_price = round(data["bitcoin"]["usd"], 2)
btc_change = round(data["bitcoin"]["usd_24h_change"], 2)

gold_price = round(data["pax-gold"]["usd"], 2)
gold_change = round(data["pax-gold"]["usd_24h_change"], 2)

silver_price = round(data["silver-token"]["usd"], 2)
silver_change = round(data["silver-token"]["usd_24h_change"], 2)

time_now = datetime.utcnow().strftime("%H:%M UTC")

tweet = f"""📊 Market Update ({time_now})

🟡 Gold: ${gold_price} ({gold_change}%)
⚪ Silver: ${silver_price} ({silver_change}%)
₿ Bitcoin: ${btc_price} ({btc_change}%)

#Gold #Silver #Bitcoin #Crypto #Forex"""

api.update_status(tweet)

print("Market update posted successfully!")
