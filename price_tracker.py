import json
import requests
import math
import dateutil.tz
import datetime

ONE_MINUTE = '1m'
FIVE_MINUTES = '5m'
ONE_HOUR = '1h'
ONE_DAY = '1d'

def get_candlestick_data(headers, symbol, interval, start_time):
    url = 'https://api.binance.us/api/v3/klines?symbol={}&interval={}&startTime={}&limit=1000'.format(symbol, interval, start_time)
    response = requests.get(url, headers=headers)
    return response.json()

def create_price_volume_list(candlestick_data):
    final_list = []
    for dp in candlestick_data:
        avg_price = (float(dp[2]) + float(dp[3]) + float(dp[4]))/3
        final_list.append({'avg_price': avg_price, 'volume': float(dp[5]) })
    return final_list

def calc_vwap(price_volume_list):
    pvl = create_price_volume_list(price_volume_list)
    pvl = calc_cumulative_price(pvl)
    pvl = calc_cumulative_volume(pvl)
    for dp in pvl:
        dp['vwap'] = dp['cumulative_price']/dp['cumulative_volume']
    return pvl

def calc_cumulative_price(price_volume_list):
    for i,dp in enumerate(price_volume_list):
        if i == 0:
            dp['cumulative_price'] = dp['avg_price']*dp['volume']
        else:
            dp['cumulative_price'] = (dp['avg_price']*dp['volume']) + price_volume_list[i-1]['cumulative_price']
    return price_volume_list

def calc_cumulative_volume(price_volume_list):
    for i,dp in enumerate(price_volume_list):
        if i == 0:
            dp['cumulative_volume'] = dp['volume']
        else:
            dp['cumulative_volume'] = dp['volume'] + price_volume_list[i-1]['cumulative_volume']
    return price_volume_list

def get_open_time_utc_milliseconds():
    six_am = (datetime.datetime
                .now(dateutil.tz.gettz('America/Denver'))
                .replace(hour=6, minute=0, second=0, microsecond=0)
                .astimezone(dateutil.tz.tzutc()))
    return math.floor(six_am.timestamp())*1000

with open('config.json') as config_file:
    config = json.load(config_file)

headers = {
    'X-MBX-APIKEY': config['api_key']
}
day_open = get_open_time_utc_milliseconds()
data = get_candlestick_data(headers, 'ETHUSD', FIVE_MINUTES, day_open)
print(data[-5:])
pvl = calc_vwap(data)
print(pvl[-5:])