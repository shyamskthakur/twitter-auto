import os
import requests
import tweepy
from datetime import datetime

# Twitter credentials from GitHub secrets
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

# Get Bitcoin price
btc_data = requests.get(
    "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd&include_24hr_change=true"
).json()

btc_price = round(btc_data["bitcoin"]["usd"], 2)
btc_change = round(btc_data["bitcoin"]["usd_24h_change"], 2)

# Get Gold & Silver prices
metals = requests.get("https://api.metals.live/v1/spot").json()

gold_price = None
silver_price = None

for item in metals:
    if "gold" in item:
        gold_price = round(item["gold"], 2)
    if "silver" in item:
        silver_price = round(item["silver"], 2)

time_now = datetime.utcnow().strftime("%H:%M UTC")

tweet = f"""📊 Market Update ({time_now})

🟡 Gold: ${gold_price}
⚪ Silver: ${silver_price}
₿ Bitcoin: ${btc_price} ({btc_change}%)

#Gold #Silver #Bitcoin #Crypto #Forex"""

api.update_status(tweet)

print("Market update posted successfully!")
