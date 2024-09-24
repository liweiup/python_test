import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 下载股票数据
ticker = '600550.SS'
data = yf.download(ticker, start='2024-06-01', end='2024-12-31')

# 计算移动平均线
data['MA20'] = data['Close'].rolling(window=20).mean()

# 计算价格波动率
data['PriceChange'] = data['Close'].pct_change()
data['Volatility'] = data['PriceChange'].rolling(window=20).std()

# 计算成交量变化率
data['VolumeChange'] = data['Volume'].pct_change()

# 判断是否经历了洗盘
shakeout_threshold_volatility = 0.02  # 波动率阈值
shakeout_threshold_volume = 0.5       # 成交量变化率阈值

data['IsShakeout'] = (data['Volatility'] > shakeout_threshold_volatility) & (data['VolumeChange'] > shakeout_threshold_volume)

# 打印结果
print(f"Summary for {ticker}:")
print(f"Latest Close Price: {data['Close'].iloc[-1]}")
print(f"Latest Volatility: {data['Volatility'].iloc[-1]}")
print(f"Latest VolumeChange: {data['VolumeChange'].iloc[-1]}")
print(f"Is Shakeout: {data['IsShakeout'].iloc[-1]}")

# 绘制K线图并标记洗盘区间
import mplfinance as mpf

mc = mpf.make_marketcolors(
    up='green', down='red', edge='i', wick='i', volume='in', inherit=True
)

s = mpf.make_mpf_style(
    marketcolors=mc, 
    gridstyle='-', 
    gridcolor='gray', 
    figcolor='(0.82, 0.83, 0.85)', 
    facecolor='(0.82, 0.83, 0.85)', 
    edgecolor='(0.82, 0.83, 0.85)'
)

apds = [
    mpf.make_addplot(data['MA20'], color='blue', width=1.0),
    mpf.make_addplot(data['IsShakeout'].astype(int) * data['Close'], type='scatter', markersize=50, marker='o', color='orange')
]

mpf.plot(data, type='candle', style=s,
         title=f'{ticker} K线图',
         ylabel='价格',
         ylabel_lower='成交量',
         volume=True,
         addplot=apds,
         figsize=(12, 8))