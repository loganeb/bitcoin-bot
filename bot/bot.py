import json
import requests
import math
import dateutil.tz
from datetime import datetime, timezone
import distutils
import plotly.graph_objects as go
import time
import uuid

import state

ONE_MINUTE = '1m'
FIVE_MINUTES = '5m'
ONE_HOUR = '1h'
ONE_DAY = '1d'

def get_candlestick_data(headers, symbol, interval, start_time):
    print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S - ") + 'Retrieving price data')
    url = 'https://api.binance.us/api/v3/klines?symbol={}&interval={}&startTime={}&limit=1000'.format(symbol, interval, start_time)
    response = requests.get(url, headers=headers)
    print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S - ") + 'Last price: ' + str(response.json()[-1][4]))
    return response.json()

def create_price_volume_list(candlestick_data):
    final_list = []
    for dp in candlestick_data:
        date = datetime.fromtimestamp(dp[0]/1000, tz=timezone.utc)
        avg_price = (float(dp[2]) + float(dp[3]) + float(dp[4]))/3
        final_list.append({'avg_price': avg_price, 'volume': float(dp[5]), 'date': date, 'close': float(dp[4]) })
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
    six_am = (datetime
                .now(dateutil.tz.gettz('America/Denver'))
                .replace(hour=0, minute=0, second=0, microsecond=0)
                .astimezone(dateutil.tz.tzutc()))
    return math.floor(six_am.timestamp())*1000

def plot_vwap(raw_data, vwap):
    dates = [datetime.fromtimestamp(dp[0]/1000, tz=timezone.utc) for dp in raw_data]
    opens =  [dp[1] for dp in raw_data]
    highs = [dp[2] for dp in raw_data]
    lows = [dp[3] for dp in raw_data]
    closes = [dp[4] for dp in raw_data]
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=dates,open=opens, high=highs, low=lows,close=closes, name=symbol))
    fig.add_trace(go.Scatter(x=dates, y=vwap, mode='lines', name='VWAP'))
    fig.show()

def get_avg_price(headers, symbol):
    url = 'https://api.binance.us/api/v3/avgPrice?symbol={}'.format(symbol)
    response = requests.get(url, headers=headers)
    return float(response.json()['price'])

def buy(headers, symbol, usd):
    avg_price = get_avg_price(headers, symbol)
    trade_qty = usd/avg_price
    print('{} {} bought for ${}'.format(trade_qty, symbol, usd))
    return trade_qty

def sell(headers, symbol, qty):
    avg_price = get_avg_price(headers, symbol)
    return_usd = avg_price * qty
    print('{} {} sold for ${}'.format(qty, symbol, return_usd))
    return return_usd

def log_trade(file_path, string):
    with open(file_path, 'a+') as log_file:
        log_file.write(string + '\n')

# vwap = [dp['vwap'] for dp in pvl]
# plot_vwap(data, vwap)

def main():
    with open('../common/config.json') as config_file:
        config = json.load(config_file)

    headers = {
        'X-MBX-APIKEY': config['api_key']
    }

    symbol = config['symbol']
    state.set_position_open(False)
    entry_price = 0
    exit_price = 0
    open_qty = 0
    trade_count = 1
    position_uuid=str(uuid.uuid4())

    while True:
        day_open = get_open_time_utc_milliseconds()
        data = get_candlestick_data(headers, symbol, FIVE_MINUTES, day_open)
        pvl = calc_vwap(data)
        if not state.get_position_open() == "True":
            if pvl[-1]['close'] >= pvl[-1]['vwap'] and pvl[-2]['close'] >= pvl[-2]['vwap']:
                entry_price = get_avg_price(headers, symbol)
                open_qty = buy(headers, symbol, 20.00)
                now = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
                log_trade('trades.log', '{} - Position {} opened - {} {} bought at ${} for ${}'.format(
                    now, trade_count, open_qty, 'BTCUDST', entry_price, 20.00
                ))
                state.set_position_open(True)
                state.add_open_position(position_uuid, 'BTCUDST', open_qty, now)
        elif state.get_position_open() == "True":
            if pvl[-1]['close'] < pvl[-1]['vwap'] or (entry_price - pvl[-1]['close']) / entry_price > 0.02 or (pvl[-3]['close'] - pvl[-1]['close']) / pvl[-3]['close'] > 0.04:
                exit_price = get_avg_price(headers, symbol)
                return_pct = ((exit_price - entry_price)/entry_price)*100
                now = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
                sell(headers, symbol, open_qty)
                log_trade('trades.log', '{} - Position {} closed at ${} for {}% return'.format(
                    now, trade_count, exit_price, return_pct
                ))
                trade_count += 1
                state.set_position_open(False)
        time.sleep(30)


if __name__ == "__main__":
    main()