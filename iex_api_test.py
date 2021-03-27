import requests
import json

with open('config.json') as config_file:
    config = json.load(config_file)

response = requests.get("https://cloud.iexapis.com/stable/crypto/btcusd/price?token={}".format(config['api_token']))
print(response.text)