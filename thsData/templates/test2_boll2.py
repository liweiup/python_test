import yfinance as yf
import pandas as pd
import numpy as np
import mplfinance as mpf
import logging
# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
import logging
import numpy as np

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def is_sideways(data, bb_width_threshold=0.25, price_range_threshold=0.05, period=20, recent_days=3, rise_threshold=0.1):
    # 计算布林带
    data['MA'] = data['Close'].rolling(window=period).mean()
    data['BB_Upper'] = data['MA'] + 2 * data['Close'].rolling(window=period).std()
    data['BB_Lower'] = data['MA'] - 2 * data['Close'].rolling(window=period).std()
    
    # 计算布林带宽度
    data['BB_Width'] = (data['BB_Upper'] - data['BB_Lower']) / data['MA']
    
    # 计算价格范围
    data['Price_Range'] = (data['High'] - data['Low']) / data['MA']
    
    # 计算最近3日涨幅
    data['Recent_Rise'] = (data['Close'] / data['Close'].shift(recent_days) - 1)
    
    # 判断是否横盘
    is_sideways = (data['BB_Width'] < bb_width_threshold) & ((data['Price_Range'] < price_range_threshold) & (data['Recent_Rise'].abs() <= rise_threshold))

    logging.info(f"BB_Width range: {data['BB_Width'].min()} to {data['BB_Width'].max()}")
    logging.info(f"Price_Range range: {data['Price_Range'].min()} to {data['Price_Range'].max()}")
    logging.info(f"Recent_Rise range: {data['Recent_Rise'].min()} to {data['Recent_Rise'].max()}")
    logging.info(f"Number of sideways periods: {is_sideways.sum()}")

    return is_sideways
def detect_trend_realtime_improved(data, price_change_threshold=0.05, days_to_check=5):
    data['Trend'] = 0
    for i in range(1, len(data) - days_to_check + 1):
        if data['IsSideways'].iloc[i-1] and not data['IsSideways'].iloc[i]:
            start_price = data['Close'].iloc[i-1]
            cumulative_price_change = 0
            for j in range(days_to_check):
                current_price = data['Close'].iloc[i+j]
                price_change = (current_price - start_price) / start_price
                cumulative_price_change += price_change
                if cumulative_price_change >= price_change_threshold:
                    trend_direction = 1
                    break
                elif cumulative_price_change <= -price_change_threshold:
                    trend_direction = -1
                    break
            else:
                trend_direction = 0
            
            if trend_direction != 0:
                for k in range(days_to_check):
                    data.loc[data.index[i+k], 'Trend'] = (k + 1) * trend_direction

    # 确保 IsSideways 为 True 时 Trend 记为 0
    data.loc[data['IsSideways'], 'Trend'] = 0

    # 在 IsSideways 为 False 的情况下，持续累计 Trend
    for i in range(1, len(data)):
        if not data['IsSideways'].iloc[i] and data['Trend'].iloc[i] == 0:
            data.loc[data.index[i], 'Trend'] = data['Trend'].iloc[i-1] + (1 if data['Close'].iloc[i] > data['Close'].iloc[i-1] else -1)

    return data
def volume_surge(data, window=5, threshold=1.5):
    """
    比较最近5天的成交量和前5天的成交量
    :param data: DataFrame，包含成交量数据
    :param window: int，用于比较的天数
    :param threshold: float，判断成交量激增的阈值
    :return: Series，布尔值表示是否出现成交量激增
    """
    recent_volume = data['Volume'].rolling(window=window).mean()
    previous_volume = data['Volume'].shift(window).rolling(window=window).mean()
    return recent_volume > previous_volume * threshold

# 下载股票数据
ticker = '600550.SS'  
# ticker = '000088.SZ'  
# ticker = '603259.SS'
# ticker = '603713.SS'
# data = yf.download(ticker, start='2024-04-01', end='2024-08-05')
data = yf.download(ticker, start='2024-04-01', end='2024-09-04')
print(data)
# 确保索引是 DatetimeIndex 类型
data.index = pd.to_datetime(data.index, errors='coerce')

# 检查数据集是否为空
if data.empty:
    print("Error: No valid data available after removing NaN values.")
    exit()
# 应用成交量激增判断
data['Volume_Surge'] = volume_surge(data)
# 判断横盘
data['IsSideways'] = is_sideways(data)
# 检测横盘后的趋势
data = detect_trend_realtime_improved(data)
# 只保留横盘为 True 的标记
data['Sideways_Marker'] = data['IsSideways'].apply(lambda x: np.nan if not x else 1) * data['Close']

# 确保 Trend 列中有有效数据
if data['Trend'].isna().all():
    print("Error: No valid trend data available.")
    exit()

# 创建新的列来存储向上和向下的价格
data['Trend_Up'] = data.apply(lambda row: row['Close'] if row['Trend'] == 1 else np.nan, axis=1)
data['Trend_Down'] = data.apply(lambda row: row['Close'] if row['Trend'] == -1 else np.nan, axis=1)
data['Trend_Up_Strong'] = data.apply(lambda row: row['Close'] if row['Trend'] > 1 else np.nan, axis=1)
data['Trend_Down_Strong'] = data.apply(lambda row: row['Close'] if row['Trend'] < -1 else np.nan, axis=1)

# 绘制K线图和布林带
mc = mpf.make_marketcolors(up='red', down='green', edge='i', wick='i', volume='in')
s = mpf.make_mpf_style(marketcolors=mc)
apds = [
    mpf.make_addplot(data['MA'], color='blue'),
    mpf.make_addplot(data['BB_Upper'], color='gray'),
    mpf.make_addplot(data['BB_Lower'], color='gray'),
]
if not data['Sideways_Marker'].isna().all():
    apds.append(mpf.make_addplot(data['Sideways_Marker'], type='scatter', markersize=10, marker='o', color='purple'))
# 只有在 Trend_Up 包含非 NaN 值时才添加
if not data['Trend_Up'].isna().all():
    apds.append(mpf.make_addplot(data['Trend_Up'], type='scatter', markersize=20, marker='^', color='red'))  # 向上
# 只有在 Trend_Down 包含非 NaN 值时才添加
if not data['Trend_Down'].isna().all():
    apds.append(mpf.make_addplot(data['Trend_Down'], type='scatter', markersize=20, marker='v', color='green'))  # 向下
# 只有在 Trend_Up_Strong 包含非 NaN 值时才添加
if not data['Trend_Up_Strong'].isna().all():
    apds.append(mpf.make_addplot(data['Trend_Up_Strong'], type='scatter', markersize=20, marker='^', color='darkred'))  # 强烈向上
# 只有在 Trend_Down_Strong 包含非 NaN 值时才添加
if not data['Trend_Down_Strong'].isna().all():
    apds.append(mpf.make_addplot(data['Trend_Down_Strong'], type='scatter', markersize=20, marker='v', color='darkgreen'))  # 强烈向下


mpf.plot(data, type='candle', style=s, addplot=apds,
         title=f'{ticker} Bollinger Bands and Sideways Detection',
         volume=True, figsize=(12, 8))

# 打印所有时期和趋势
print("All periods and trends:")
for index, row in data.iterrows():
    if row['IsSideways']:
        trend_str = "Sideways"
    elif row['Trend'] == 1:
        trend_str = "Up"
    elif row['Trend'] == -1:
        trend_str = "Down"
    else:
        trend_str = "No Trend"
    print(f"{index.date()}: {trend_str}")
# 将数据导出为 CSV 文件
data.to_csv('./views/output_data.csv', index=True)