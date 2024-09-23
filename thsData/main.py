import sys
import os

# 将项目根目录添加到 Python 路径
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)
from scripts.search_stock import search_stock
from analyzer.stock_analyzer import StockAnalyzer
import matplotlib.pyplot as plt
def plot_price_chart(prices):
    plt.figure(figsize=(12, 6))
    plt.bar(range(len(prices)), prices, color='skyblue', edgecolor='navy')
    plt.title('Stock Price Movement', fontsize=16)
    plt.xlabel('Time', fontsize=12)
    plt.ylabel('Price', fontsize=12)
    
    # 添加阶段标记
    plt.axvline(x=10, color='r', linestyle='--', label='End of Sideways')
    plt.axvline(x=28, color='g', linestyle='--', label='Start of Uptrend')
    
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # 设置y轴范围，使图表更清晰
    plt.ylim(min(prices) - 5, max(prices) + 5)
    
    plt.tight_layout()
    plt.show()
def main():
    # 这里模拟了一个经历横盘、下跌，然后开始上涨的股票
    prices = [100, 101, 99, 100, 101, 100, 102, 101, 99, 100,  # 横盘
              98, 96, 94, 92, 90, 91, 89, 88, 87, 86,         # 下跌
              87, 89, 91, 93, 95, 98, 100, 102, 104, 106]     # 上涨

    analyzer = StockAnalyzer(sideways_threshold=0.1, trend_threshold=0.05, ma_period=10)
    # 分析股票
    result = analyzer.analyze_stock(prices, 10)

    print(f"Current is sideways: {result['current_is_sideways']}")
    print(f"Current volatility (relative std): {result['current_volatility']:.4f}")
    print(f"Overall trend: {result['overall_trend']:.4f}")
    print(f"Has sideways->down->up pattern: {result['has_sideways_down_up_pattern']}")
    print(f"Pattern description: {result['pattern_description']}")
    print(f"Analysis: {result['analysis']}")
    # 绘制价格柱状图
    plot_price_chart(prices)
if __name__ == "__main__":
    main()