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

def create_price_volume_list(candlestick_data):
    final_list = []
    for dp in candlestick_data:
        avg_price = (float(dp[2]) + float(dp[3]) + float(dp[4]))/3
        final_list.append({'avg_price': avg_price, 'volume': float(dp[5]) })
    return final_list

def calc_vwap(price_volume_list):
    return

with open('config.json') as config_file:
    config = json.load(config_file)

headers = {
    'X-MBX-APIKEY': config['api_key']
}

data = get_candlestick_data(headers, 'BTCUSDT', FIVE_MINUTES)
pvl = create_price_volume_list(data)
print(pvl)