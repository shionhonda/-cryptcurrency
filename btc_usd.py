# coding: utf-8

# import library
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import requests

# compute trade amount from return
# x must not be negative
def compute(x, th1, th2, sat):
    if 0 < x and x < th1:
        out = 0
    elif th1 <= x and x <= th2:
        out = sat/(th2-th1)**2*(x-th2)**2
    elif th2 < x:
        out = sat
    else:
        out = 0
    return out        

df = pd.read_csv('data.csv')
df = df.dropna()
# data number
n = df.shape[0]
y = np.array(df['Close Price'].values)
t = np.linspace(0,n,n)
# 移動平均
ite = 19
y2 = np.zeros(y.shape)
for i in range(ite):
    y2 = y2 + np.r_[y[0]*np.ones(i), y[0:len(y)-i]] 
y2 = y2/ite
# 移動平均をプロット
plt.figure(figsize=(16,8))
plt.plot(t, y, "grey", linewidth=1)
plt.plot(t, y2, "g", linewidth=2)

# auto trade simulation
# initialize parameters
usd = 100*np.ones(n)
btc = 0.02*np.ones(n)
r = np.zeros(n-1)
th2 = 1/800
th1 = th2*0.7
sat = 1
min_btc = 0.001
commission = 0.0015
com = 1-commission
BtoD = 0
DtoB = 0
# start simulation
for i in range(n-1):
    usd[i+1] = usd[i]
    btc[i+1] = btc[i]
    r[i] = (y2[i+1]-y2[i])/y2[i]
    # if return is positive
    if r[i] > 0:
        amt_usd = compute(r[i], th1, th2, sat)*usd[i]
        if amt_usd/y[i+1] > min_btc:
            usd[i+1] -= amt_usd
            btc[i+1] += amt_usd/y[i+1]*com
            DtoB += 1
    # if return is negative
    if r[i] < 0:
        amt_btc = compute(-r[i], th1, th2, sat)*btc[i]
        if amt_btc > min_btc:
            btc[i+1] -= amt_btc
            usd[i+1] += amt_btc*y[i+1]*com
            BtoD += 1
total = usd+btc*y
balance = total[n-1]-total[0]
print("\nUSD: ", usd[n-1])
print("BTC: ", btc[n-1])
print("Total in USD: ", total[n-1])
print("Balance in USD: ", balance)
print("Increase rate: " , balance/total[0]*100 , "%")
# if you kept all the assets as btc...?
print("Interest", (y[n-1]-y[0])/y[0]*100, "%")
print("DtoB: ", DtoB)
print("BtoD: ", BtoD)

# return, risk, sharp ratio
z = np.diff(y)/y[0:n-1]
my = np.diff(total)/total[0:n-1]
print("My Return: ", my.mean())
print("Natural Return: ", z.mean())
print("My Risk: ", my.std())
print("Natural Risk: ", z.std())
print("My Ratio: ", my.mean()/my.std())
print("Natural Ratio: ", z.mean()/z.std())

# plot total assets against time
plt.figure(figsize=(16,8))
plt.plot(t, total, "r", linewidth=3)

# plot return against time
plt.figure(figsize=(16,8))
plt.plot(t[0:n-1], r)
plt.plot(th2*np.ones(n-1), "r")
plt.plot(-th2*np.ones(n-1), "r")
plt.plot(th1*np.ones(n-1), "g")
plt.plot(-th1*np.ones(n-1), "g")

# plot btc price and total assets in standardized values
plt.figure(figsize=(16,8))
plt.plot(t, y/y.mean(), "g", linewidth=1)
plt.plot(t, y2/y2.mean(), "b", linewidth=1)
plt.plot(t, total/total.mean(), "r", linewidth=1)

