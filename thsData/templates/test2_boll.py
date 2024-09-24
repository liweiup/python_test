import yfinance as yf
import pandas as pd
import numpy as np
import mplfinance as mpf

def is_sideways(data, bb_width_threshold=0.3, price_range_threshold=0.1, period=20):
    # 计算布林带
    data['MA'] = data['Close'].rolling(window=period).mean()
    data['BB_Upper'] = data['MA'] + 2 * data['Close'].rolling(window=period).std()
    data['BB_Lower'] = data['MA'] - 2 * data['Close'].rolling(window=period).std()
    
    # 计算布林带宽度
    data['BB_Width'] = (data['BB_Upper'] - data['BB_Lower']) / data['MA']
    
    # 计算价格范围
    data['Price_Range'] = (data['High'] - data['Low']) / data['MA']
    
    # 判断是否横盘
    is_sideways = (data['BB_Width'] < bb_width_threshold) | (data['Price_Range'] < price_range_threshold)
    return is_sideways

# 下载股票数据
ticker = '600550.SS'  
ticker = '000088.SZ'  
ticker = '603259.SS'
ticker = '603713.SS'
data = yf.download(ticker, start='2024-04-01', end='2024-09-30')

# 判断横盘
data['IsSideways'] = is_sideways(data)
# 只保留横盘为 True 的标记
data['Sideways_Marker'] = data['IsSideways'].apply(lambda x: np.nan if not x else 1) * data['Close']

# 绘制K线图和布林带
mc = mpf.make_marketcolors(up='red', down='green', edge='i', wick='i', volume='in')
s = mpf.make_mpf_style(marketcolors=mc)

apds = [
    mpf.make_addplot(data['MA'], color='blue'),
    mpf.make_addplot(data['BB_Upper'], color='gray'),
    mpf.make_addplot(data['BB_Lower'], color='gray'),
    mpf.make_addplot(data['Sideways_Marker'], type='scatter', markersize=10, marker='o', color='purple')
]

mpf.plot(data, type='candle', style=s, addplot=apds,
         title=f'{ticker} Bollinger Bands and Sideways Detection',
         volume=True, figsize=(12, 8))

# 打印横盘时期
sideways_periods = data[data['IsSideways']].index
print("Sideways periods:")
for period in sideways_periods:
    print(period.date())
# 将数据导出为 CSV 文件
data.to_csv('./views/output_data.csv', index=True)