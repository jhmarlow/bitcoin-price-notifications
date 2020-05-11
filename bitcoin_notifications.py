import requests
import time
from datetime import datetime

BITCOIN_API_URL = 'https://api.coinmarketcap.com/v1/ticker/bitcoin/'
ifttt_webhook_url = 'https://maker.ifttt.com/trigger/{}/with/key/yh6FJ6BvybjhYSFIt-R6L'

def get_latest_bitcoin_price():
    response = requests.get(BITCOIN_API_URL)
    response_json = response.json()
    # convert price into float
    return round(float(response_json[0]['price_usd']), 3)

def post_ifttt_webhook(event, value):
    # payload to be sent to iftttt service
    data = {'value1':value}
    # insert our desired event
    ifttt_event_url = ifttt_webhook_url.format(event)
    # sends http post request to webhook url
    requests.post(ifttt_event_url, json=data)


bitcoin_price_thresh = 10000

def main():
    bitcoin_history = []
    while True:
        price = get_latest_bitcoin_price()
        date = datetime.now()
        bitcoin_history.append({'date':date, 'price':price})

        if price < bitcoin_price_thresh:
            post_ifttt_webhook('Bitcoin_price_emergency', price)

        if len(bitcoin_history) == 1:
            post_ifttt_webhook('Bitcoin_price_update', price)

            bitcoin_history = []

        # sleep for 2 mins
        time.sleep(1*30)

if __name__ == '__main__':
    main()