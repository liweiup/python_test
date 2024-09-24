import yfinance as yf
import pandas as pd
import numpy as np
import mplfinance as mpf
import matplotlib.pyplot as plt

def is_sideways(data, bb_width_threshold=0.25, price_range_threshold=0.05, period=20):
    # 计算布林带
    data['MA'] = data['Close'].rolling(window=period).mean()
    data['BB_Upper'] = data['MA'] + 2 * data['Close'].rolling(window=period).std()
    data['BB_Lower'] = data['MA'] - 2 * data['Close'].rolling(window=period).std()
    
    # 计算布林带宽度
    data['BB_Width'] = (data['BB_Upper'] - data['BB_Lower']) / data['MA']
    
    # 计算价格范围
    data['Price_Range'] = (data['High'] - data['Low']) / data['MA']

    # 判断是否横盘
    is_sideways = (data['BB_Width'] < bb_width_threshold) & (data['Price_Range'] < price_range_threshold)
    return is_sideways

def detect_trend(data, period=5, future_window=5):
    data['Trend'] = 0
    for i in range(len(data) - period - future_window):
        if data['IsSideways'].iloc[i] and not data['IsSideways'].iloc[i + period]:
            end_of_sideways = i + period
            future_prices = data['Close'].iloc[end_of_sideways + 1:end_of_sideways + 1 + future_window]
            future_avg_price = future_prices.mean()
            if future_avg_price > data['Close'].iloc[end_of_sideways]:
                data.loc[data.index[end_of_sideways], 'Trend'] = 1  # 向上
            elif future_avg_price < data['Close'].iloc[end_of_sideways]:
                data.loc[data.index[end_of_sideways], 'Trend'] = -1  # 向下
    return data

def predict_future_prices(data, prediction_days=5):
    # 使用简单移动平均线进行预测
    last_close = data['Close'].iloc[-1]
    ma_20 = data['Close'].rolling(window=20).mean().iloc[-1]
    ma_50 = data['Close'].rolling(window=50).mean().iloc[-1]
    
    # 计算预测斜率
    slope = (ma_20 - ma_50) / 30  # 假设 MA20 和 MA50 之间有 30 个交易日
    
    future_dates = pd.date_range(start=data.index[-1] + pd.Timedelta(days=1), periods=prediction_days)
    future_data = pd.DataFrame(index=future_dates, columns=['Open', 'High', 'Low', 'Close', 'Volume'])
    
    for i in range(prediction_days):
        predicted_close = last_close + slope * (i + 1)
        future_data.iloc[i] = {
            'Open': float(predicted_close * 0.99),
            'High': float(predicted_close * 1.01),
            'Low': float(predicted_close * 0.99),
            'Close': float(predicted_close),
            'Volume': float(data['Volume'].mean())
        }
    
    return future_data

# 下载股票数据
ticker = '603713.SS'
data = yf.download(ticker, start='2024-04-01', end='2024-08-01')

# 确保索引是 DatetimeIndex 类型
data.index = pd.to_datetime(data.index)
data = data.dropna()  # 删除包含任何NaN的行

# 检查数据集是否为空
if data.empty:
    print("Error: No valid data available after removing NaN values.")
    exit()

# 判断横盘
data['IsSideways'] = is_sideways(data)
data['Sideways_Marker'] = data['IsSideways'].apply(lambda x: np.nan if not x else 1) * data['Close']

# 检测横盘后的趋势
data = detect_trend(data)

# 预测未来价格
future_data = predict_future_prices(data)

# 合并历史数据和预测数据
combined_data = pd.concat([data, future_data])

# 重新计算技术指标
combined_data['MA'] = combined_data['Close'].rolling(window=20).mean()
combined_data['BB_Upper'] = combined_data['MA'] + 2 * combined_data['Close'].rolling(window=20).std()
combined_data['BB_Lower'] = combined_data['MA'] - 2 * combined_data['Close'].rolling(window=20).std()

# 填充缺失值
combined_data = combined_data.fillna(method='ffill').fillna(method='bfill')

# 创建新的列来存储向上和向下的价格
combined_data['Trend_Up'] = combined_data.apply(lambda row: row['Close'] if row.get('Trend') == 1 else np.nan, axis=1)
combined_data['Trend_Down'] = combined_data.apply(lambda row: row['Close'] if row.get('Trend') == -1 else np.nan, axis=1)

# 确保所有价格列都是浮点数类型
price_columns = ['Open', 'High', 'Low', 'Close']
for col in price_columns:
    combined_data[col] = combined_data[col].astype(float)
    future_data[col] = future_data[col].astype(float)

# 绘制K线图、布林带和预测
mc = mpf.make_marketcolors(up='red', down='green', edge='i', wick='i', volume='in')
s = mpf.make_mpf_style(marketcolors=mc)

apds = [
    mpf.make_addplot(combined_data['MA'], color='blue'),
    mpf.make_addplot(combined_data['BB_Upper'], color='gray'),
    mpf.make_addplot(combined_data['BB_Lower'], color='gray'),
    mpf.make_addplot(combined_data['Sideways_Marker'], type='scatter', markersize=50, marker='o', color='purple'),
    mpf.make_addplot(combined_data['Trend_Up'], type='scatter', markersize=50, marker='^', color='green'),
    mpf.make_addplot(combined_data['Trend_Down'], type='scatter', markersize=50, marker='v', color='red')
]

# 创建图形和轴
fig, axes = mpf.plot(combined_data, type='candle', style=s, addplot=apds,
                     title=f'{ticker} Bollinger Bands, Sideways Detection, and Prediction',
                     volume=True, figsize=(12, 8), returnfig=True)

# 在同一图上绘制预测数据
mpf.plot(future_data, type='candle', style=mpf.make_mpf_style(marketcolors=mpf.make_marketcolors(up='yellow', down='yellow', edge='yellow', wick='yellow')),
         ax=axes[0], volume=axes[2], figscale=1)

plt.show()

print("\nPredicted future prices:")
print(future_data[['Open', 'High', 'Low', 'Close']])