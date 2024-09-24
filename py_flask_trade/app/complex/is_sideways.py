import numpy as np
import pandas as pd

def is_sideways(stock_data, days=30, threshold=0.05):
    """
    判断股票是否处于横盘状态
    
    参数:
    stock_data: DataFrame，包含日期和收盘价
    days: int，观察的天数，默认30天
    threshold: float，波动阈值，默认5%
    
    返回:
    bool: 是否处于横盘状态
    """
    # 确保数据足够
    if len(stock_data) < days:
        return False
    
    # 获取最近days天的收盘价
    recent_prices = stock_data['close'].tail(days)
    
    # 计算最高价和最低价
    highest_price = recent_prices.max()
    lowest_price = recent_prices.min()
    
    # 计算波动范围
    price_range = (highest_price - lowest_price) / lowest_price
    
    # 如果波动范围小于阈值，认为是横盘
    return price_range <= threshold

# 使用示例
# 假设 stock_data 是一个包含日期和收盘价的DataFrame
# stock_data = pd.DataFrame({'date': [...], 'close': [...]})

# is_sideways_status = is_sideways(stock_data)
# print(f"股票是否处于横盘状态: {is_sideways_status}")
