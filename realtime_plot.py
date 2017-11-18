import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
from datetime import datetime
import pybitflyer
from ipywidgets import FloatProgress
from IPython.display import display, clear_output

api = pybitflyer.API()

# 最終取引価格、移動平均、利率を格納する配列（確認用）
raws = []
smoothed = [] 
returns = []
itr = 20 # 移動平均を取る幅

current_price =  api.ticker(product_code = "BTC_JPY")['ltp']
ltps = current_price*np.ones(itr) # 20サンプリング間の最終取引価格の配列
smas = current_price*np.ones(2) # 1サンプリング前と現在の移動平均の配列

plt.ion()
fig = plt.figure(figsize=(16,8))
# 2行1列に分けて1番目にプロット
axe1 = fig.add_subplot(211)
axe1.set_title("Raw price and Simple Moving Average")
# 2行1列に分けて2番目にプロット
axe2 = fig.add_subplot(212)
axe2.set_title("Return per 10 seconds")

while True:
    # 00秒に稼働
    if datetime.now().strftime('%S') [1]== '0':
        clear_output(wait = True)
        tick = api.ticker(product_code = "BTC_JPY")
        # 最終取引価格と移動平均の更新
        ltps = np.hstack((ltps[1:itr], tick['ltp']))
        smas = np.hstack((smas[1], ltps.mean()))
        # 確認用データの更新
        raws.append(ltps[itr-1])
        smoothed.append(smas[1])
        # 移動平均の1サンプリングあたりの利率
        r = (smas[1]-smas[0])/smas[0]
        returns.append(r)
            
        axe1.set_title("Raw price and Simple Moving Average")
        axe2.set_title("Return per 10 seconds")
        axe1.plot(raws, "grey", linewidth=1)
        axe1.plot(smoothed, "g", linewidth=2)
        axe2.plot(returns, "b", linewidth=2)
        size = len(returns)
        axe2.plot(np.zeros(size), "black", linewidth=1)
        axe2.plot(0.0001*np.ones(size), "grey", linewidth=1)
        axe2.plot(-0.0001*np.ones(size), "grey", linewidth=1)
        axe2.plot(0.0003*np.ones(size), "grey", linewidth=1)
        axe2.plot(-0.0003*np.ones(size), "grey", linewidth=1)
        plt.pause(1)
        # 次の10秒まで休憩
        time.sleep(7)
        axe1.cla()
        axe2.cla()
