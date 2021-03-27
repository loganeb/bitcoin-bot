import requests
import json

ONE_MINUTE = '1m'
FIVE_MINUTES = '5m'
ONE_HOUR = '1h'
ONE_DAY = '1d'

def get_candlestick_data(headers, symbol, interval):
    url = 'https://api.binance.us/api/v3/klines?symbol={}&interval={}'.format(symbol, interval)
    response = requests.get(url, headers=headers)
    return response.json()

with open('config.json') as config_file:
    config = json.load(config_file)

headers = {
    'X-MBX-APIKEY': config['api_key']
}

response = get_candlestick_data(headers, 'BTCUSDT', FIVE_MINUTES)
print(response)