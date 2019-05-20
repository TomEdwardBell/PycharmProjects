import urllib.request
import json
from datetime import datetime
import time

def check(address, file):
    with urllib.request.urlopen(address) as url:
        data = json.loads(url.read().decode())
        price = data['data']['1']['quotes']['GBP']['price']
        timestamp = data['data']['1']['last_updated']
        timestamp = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        #file.write(str(price) + "," + timestamp)
        print(price)
        print(timestamp)
        time.sleep(150)

address = "https://api.alternative.me/v2/ticker/1/?convert=GBP"
file = open("btc.csv", "r")
print("..." + file.read())

check(address, file)

