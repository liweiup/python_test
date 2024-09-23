import yfinance as yf
import pandas as pd
import numpy as np
import mplfinance as mpf
# 下载贵州茅台的历史数据
ticker = '600010.SS'
data = yf.download(ticker, start='2024-08-01', end='2024-09-23')

# 计算每日收益率
data['Daily_Return'] = data['Close'].pct_change()

# 去除 NaN 值
data = data.dropna()

# 计算过去N天的日收益率标准差
def calculate_volatility(df, window):
    return df['Daily_Return'].rolling(window=window).std() * np.sqrt(252)  # 年化标准差

# 选择一个窗口大小，例如20天
window_size = 20
data['Volatility'] = calculate_volatility(data, window_size)

# 计算简单移动平均线 (SMA)
short_window = 20
long_window = 50
data['SMA_short'] = data['Close'].rolling(window=short_window).mean()
data['SMA_long'] = data['Close'].rolling(window=long_window).mean()

# 判断横盘
def is_sideways_market(df, volatility_threshold, sma_diff_threshold):
    # 获取最近一天的数据
    last_day = df.iloc[-1]
    
    # 检查波动率是否低于阈值
    if last_day['Volatility'] < volatility_threshold:
        # 检查短期和长期移动平均线之间的差异是否小于阈值
        sma_diff = abs(last_day['SMA_short'] - last_day['SMA_long'])
        if sma_diff < sma_diff_threshold:
            return True
    return False

# 定义阈值
volatility_threshold = 0.05  # 波动率阈值
sma_diff_threshold = 0.05 * data['Close'].iloc[-1]  # 移动平均线差异阈值

# 检查最近一段时间内是否为横盘
if is_sideways_market(data, volatility_threshold, sma_diff_threshold):
    print(f"{ticker} 最近可能处于横盘状态。")
else:
    print(f"{ticker} 最近可能不处于横盘状态。")

# 打印结果
print(data[['Close', 'Daily_Return', 'Volatility', 'SMA_short', 'SMA_long']].tail())

# 绘制K线图
mpf.plot(data, type='candle', style='charles',
         title=f'{ticker} K线图',
         ylabel='价格',
         ylabel_lower='成交量',
         volume=True,
         figsize=(12, 8))