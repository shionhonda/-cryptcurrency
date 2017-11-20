import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
from datetime import datetime
import pybitflyer
from ipywidgets import FloatProgress
from IPython.display import display, clear_output

api = pybitflyer.API()

# 最終取引価格、移動平均、分散、乖離率を格納する配列
raws = []
sma1, sma2 = [], []
sgm1, sgm2 = [], []
dev1, dev2 = [], []

# 移動平均を取る幅
itr1 = 90 # 15 min
itr2 = 360  # 60 mins

current_price = api.ticker(product_code = "BTC_JPY")['ltp']
ltps2 = current_price*np.ones(itr2) # 60分間の最終取引価格の配列

plt.ion()
fig = plt.figure(figsize=(16,16))
axe1 = fig.add_subplot(211)
axe2 = fig.add_subplot(212)
axe1.set_title("Raw price and Bollinger band")
axe2.set_title("Deviation rate")

while True:
    # 10秒ごとに稼働
    if datetime.now().strftime('%S') [1]== '0':
        clear_output(wait = True)
        tick = api.ticker(product_code = "BTC_JPY")
        # 最終取引価格の更新
        ltps2 = np.hstack((ltps2[1:itr2], tick['ltp']))
        ltps1 = ltps2[itr2-itr1:itr2]
        # プロット用データの更新
        raws = np.append(raws, [ltps1[itr1-1]])
        sma1 = np.append(sma1, [ltps1.mean()])
        sma2.append(ltps2.mean())
        sgm1 = np.append(sgm1, [ltps1.std()])
        sgm2 = np.append(sgm2, [ltps2.std()])
        size = len(raws)
        dev1.append((raws[size-1]-sma1[size-1])/sma1[size-1])
        dev2.append((raws[size-1]-sma2[size-1])/sma2[size-1])
        # 1つめのプロット
        axe1.plot(raws, "black", linewidth=2, label="Raw price")
        axe1.plot(sma1, "r", linewidth=1, label="15min SMA")
        axe1.plot(sma2, "g", linewidth=1, label="60min SMA")
        axe1.plot(sma1+2*sgm1, "r", linewidth=1, linestyle="dashed", label="15min 2sigma")
        axe1.plot(sma1-2*sgm1, "r", linewidth=1, linestyle="dashed")
        axe1.plot(sma2+2*sgm2, "g", linewidth=1, linestyle="dashed", label="60min 2sigma")
        axe1.plot(sma2-2*sgm2, "g", linewidth=1, linestyle="dashed")
        axe1.legend(loc='upper left')
        # 2つめのプロット
        axe2.plot(dev1, "r", linewidth=2, label="15min Dev rate")
        axe2.plot(dev2, "g", linewidth=2, label="60min Dev rate")
        axe2.plot(np.zeros(size), "black", linewidth=1)
        axe2.legend(loc='upper left')
        axe2.plot(0.005*np.ones(size), "grey", linewidth=1)
        axe2.plot(-0.005*np.ones(size), "grey", linewidth=1)
        display(fig)
        # 次の00秒まで休憩
        time.sleep(7)
        axe1.cla()
        axe2.cla()
