from urllib2 import Request, urlopen
import json
import csv

headers = {
  'Content-Type': 'application/json',
  'X-API-KEY': 'your_api_key_here',
  'X-API-SECRET': 'your_api_secret_here'
}

pairs = [
    ('BITF','BTC/USD'),
    ('GDAX','BTC/USD'),
    ('BITF','BTC/ETH'),
    ('BINA','ADA/BTC'),
    ('BINA','LTC/BTC')
]

target_filename = 'pricedata.csv'

def get_data(exchange, market):
    values = '{"exchange_code":"' + exchange + '", "exchange_market":"' + market + '"}'
    request = Request('https://api.coinigy.com/api/v1/ticker', data=values, headers=headers)
    response_body = urlopen(request).read()
    return response_body

def create_line(values):
    res = ''
    for li in values:
        res = res + li.replace('.',',') + ';'
    return res[0:-1]

file = open(target_filename,'w')
counter = 0
for i, (ex, mkt) in enumerate(pairs):
    data_parsed = json.loads(get_data(ex, mkt))
    header = create_line(data_parsed['data'][0].keys())
    file.write(header + '\n')
    line = create_line(data_parsed['data'][0].values())
    file.write(line + '\n')
file.close()
