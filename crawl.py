# Take out BTC price in JPY from bitFlyer every minute

import pybitflyer
import time

tm = []
ltp = []

api = pybitflyer.API()
while True:
      tick = api.ticker(product_code = "BTC_JPY")
      print(tick['timestamp'])
      ltp.append(tick['ltp'])
      time.sleep(10)
