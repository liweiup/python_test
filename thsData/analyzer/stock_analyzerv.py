import numpy as np
from typing import List, Tuple

# 这个工具类提供了一个基本的框架来判断股票是否横盘，并进行简单的趋势分析。您可以根据具体需求进一步调整参数或添加更复杂的分析方法。
# 例如，您可能想要考虑成交量、移动平均线或其他技术指标来增强分析的准确性。
# 请注意，这个简单的实现主要基于价格波动和简单的线性趋势。在实际应用中，您可能需要结合更多的因素和更复杂的算法来做出更准确的判断。

# 这个 StockAnalyzer 类提供了以下功能：
# is_sideways: 判断股票是否处于横盘状态。它检查最近几天的价格波动是否在设定的阈值内。
# calculate_trend: 计算股票价格的趋势。它使用简单的线性回归来确定价格的整体趋势。
# analyze_stock: 综合分析股票，包括横盘判断和趋势计算。
# 使用这个类的示例：

class StockAnalyzer:
    def __init__(self, price_threshold: float = 0.03, days_threshold: int = 5):
        """
        初始化 StockAnalyzer
        
        :param price_threshold: 价格波动阈值，默认为 3%
        :param days_threshold: 判断横盘的天数阈值，默认为 5 天
        """
        self.price_threshold = price_threshold
        self.days_threshold = days_threshold

    def is_sideways(self, prices: List[float]) -> Tuple[bool, float]:
        """
        判断给定的价格序列是否处于横盘状态
        
        :param prices: 股票价格列表，按时间顺序排列（最新的价格在列表末尾）
        :return: 元组 (是否横盘, 波动幅度)
        """
        if len(prices) < self.days_threshold:
            return False, 0.0

        # 只考虑最近 days_threshold 天的价格
        recent_prices = prices[-self.days_threshold:]
        
        # 计算价格的最大值和最小值
        max_price = max(recent_prices)
        min_price = min(recent_prices)
        
        # 计算波动幅度
        fluctuation = (max_price - min_price) / min_price
        
        # 判断是否横盘
        is_sideways = fluctuation <= self.price_threshold
        
        return is_sideways, fluctuation

    def calculate_trend(self, prices: List[float]) -> float:
        """
        计算价格趋势
        
        :param prices: 股票价格列表，按时间顺序排列（最新的价格在列表末尾）
        :return: 趋势斜率
        """
        if len(prices) < 2:
            return 0.0

        x = np.arange(len(prices))
        y = np.array(prices)
        
        # 使用线性回归计算趋势
        slope, _ = np.polyfit(x, y, 1)
        
        return slope

    def analyze_stock(self, prices: List[float]) -> dict:
        """
        综合分析股票价格
        
        :param prices: 股票价格列表，按时间顺序排列（最新的价格在列表末尾）
        :return: 分析结果字典
        """
        sideways, fluctuation = self.is_sideways(prices)
        trend = self.calculate_trend(prices)
        
        result = {
            "is_sideways": sideways,
            "fluctuation": fluctuation,
            "trend": trend,
            "analysis": ""
        }
        
        if sideways:
            result["analysis"] = "股票处于横盘状态"
        elif trend > 0:
            result["analysis"] = "股票呈上升趋势"
        else:
            result["analysis"] = "股票呈下降趋势"
        
        return result

# from common.stock_utils import StockAnalyzer

# def analyze_stock_example():
#     # 创建 StockAnalyzer 实例
#     analyzer = StockAnalyzer(price_threshold=0.03, days_threshold=5)

#     # 示例价格数据（最新的价格在列表末尾）
#     prices = [100, 101, 99, 100.5, 101.2, 100.8, 100.3]

#     # 分析股票
#     result = analyzer.analyze_stock(prices)

#     # 打印结果
#     print(f"Is sideways: {result['is_sideways']}")
#     print(f"Fluctuation: {result['fluctuation']:.2%}")
#     print(f"Trend: {result['trend']:.4f}")
#     print(f"Analysis: {result['analysis']}")

# if __name__ == "__main__":
#     analyze_stock_example()