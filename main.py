import requests
from playsound import playsound
import time
import datetime
import json
import os

cmc_latest_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

gecko_coin_list_url = 'https://api.coingecko.com/api/v3/coins/list'

with open('x-cmc-pro-api-key.txt', 'r') as f:
    api_key = f.read()

cmc_headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': api_key[:-1],
}

gecko_headers = {
    'accept': 'application/json'
}

cmc_params = {
    'start': '1',
    'limit': '10',
    'convert': 'USD',
    'sort': 'date_added',
    'sort_dir': 'desc'
}

gecko_params = {
    'market_data': 'false'
}

cmc_latest_response = requests.get(cmc_latest_url, headers=cmc_headers, params=cmc_params)
cmc_latest = cmc_latest_response.json()
for c in cmc_latest['data']:
    print(c)

cmc_last_coin_id = cmc_latest['data'][0]['id']

print()

cmc_quotes_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'

while True:
    print(datetime.datetime.now())

    # CMC

    for i in range(cmc_last_coin_id+1, cmc_last_coin_id+6):

        cmc_quotes_params = {
            'id': str(i),
            'convert': 'USD'
        }

        cmc_quotes_response = requests.get(cmc_quotes_url, headers=cmc_headers, params=cmc_quotes_params)
        quotes = cmc_quotes_response.json()
        if quotes['status']['error_code'] == 0:
            print(quotes)
            playsound('ja.mp3')
            cmc_last_coin_id += 1

    # CoinGecko

    gecko_coin_list_response = requests.get(gecko_coin_list_url, headers=gecko_headers)

    gecko_new_coin_list = gecko_coin_list_response.json()

    if not os.path.isfile('coingecko.txt'):
        with open('coingecko.txt', 'w') as f:
            f.write(json.dumps(gecko_new_coin_list))

    with open('coingecko.txt', 'r') as f:
        saved_coin_list = f.read()

    saved_coin_list = json.loads(saved_coin_list)

    for coin in gecko_new_coin_list:
        if coin['id'] not in [c['id'] for c in saved_coin_list]:
            coin_url = 'https://api.coingecko.com/api/v3/coins/' + coin['id']
            coin_response = requests.get(coin_url, headers=gecko_headers, params=gecko_params)
            print(coin_response.json())
            playsound('ja.mp3')

    with open('coingecko.txt', 'w') as f:
        f.write(json.dumps(gecko_new_coin_list))

    time.sleep(50)
