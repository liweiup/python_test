import numpy as np
from typing import List, Tuple
from enum import Enum

class TrendType(Enum):
    SIDEWAYS = 0
    DOWNTREND = 1
    UPTREND = 2

class StockAnalyzer:
    def __init__(self, sideways_threshold: float = 0.02, trend_threshold: float = 0.05, ma_period: int = 20):
        self.sideways_threshold = sideways_threshold
        self.trend_threshold = trend_threshold
        self.ma_period = ma_period

    def calculate_ma(self, prices: List[float]) -> List[float]:
        """计算移动平均线"""
        return np.convolve(prices, np.ones(self.ma_period), 'valid') / self.ma_period

    def is_sideways(self, prices: List[float]) -> Tuple[bool, float]:
        if len(prices) < self.ma_period:
            return False, 0.0
        
        # 计算移动平均线
        ma = self.calculate_ma(prices)
        
        # 计算价格相对于移动平均线的标准差
        relative_std = np.std([(p - m) / m for p, m in zip(prices[self.ma_period-1:], ma)])
        
        # 计算总体价格变化
        total_change = (prices[-1] - prices[0]) / prices[0]
        
        # 如果相对标准差低且总体变化小，则认为是横盘
        is_sideways = relative_std < self.sideways_threshold and abs(total_change) < self.trend_threshold
        
        return is_sideways, relative_std

    def calculate_trend(self, prices: List[float]) -> float:
        if len(prices) < 2:
            return 0.0
        return (prices[-1] - prices[0]) / prices[0]

    def analyze_phase(self, prices: List[float]) -> TrendType:
        is_sideways, _ = self.is_sideways(prices)
        if is_sideways:
            return TrendType.SIDEWAYS
        trend = self.calculate_trend(prices)
        if trend > self.trend_threshold:
            return TrendType.UPTREND
        elif trend < -self.trend_threshold:
            return TrendType.DOWNTREND
        else:
            return TrendType.SIDEWAYS

    def analyze_previous_phases(self, prices: List[float], phase_length: int) -> List[TrendType]:
        if len(prices) < phase_length * 3:
            raise ValueError(f"价格数据不足以分析三个阶段 (需要至少 {phase_length * 3} 个数据点)")

        phases = []
        for i in range(3):
            start = i * phase_length
            end = (i + 1) * phase_length
            phase_prices = prices[start:end]
            phases.append(self.analyze_phase(phase_prices))

        return phases

    def has_sideways_down_up_pattern(self, prices: List[float], phase_length: int) -> Tuple[bool, str]:
        try:
            phases = self.analyze_previous_phases(prices, phase_length)
        except ValueError as e:
            return False, str(e)

        if phases == [TrendType.SIDEWAYS, TrendType.DOWNTREND, TrendType.UPTREND]:
            return True, "股票经历了横盘、下跌，现在正在上涨"
        else:
            phase_description = " -> ".join([phase.name for phase in phases])
            return False, f"股票的趋势阶段为: {phase_description}"

    def analyze_stock(self, prices: List[float], phase_length: int) -> dict:
        if len(prices) < max(self.ma_period, phase_length * 3):
            raise ValueError(f"价格数据不足，需要至少 {max(self.ma_period, phase_length * 3)} 个数据点")

        current_sideways, relative_std = self.is_sideways(prices[-self.ma_period:])
        overall_trend = self.calculate_trend(prices)
        has_pattern, pattern_description = self.has_sideways_down_up_pattern(prices, phase_length)
        
        result = {
            "current_is_sideways": current_sideways,
            "current_volatility": relative_std,
            "overall_trend": overall_trend,
            "has_sideways_down_up_pattern": has_pattern,
            "pattern_description": pattern_description,
            "analysis": ""
        }
        
        if current_sideways:
            result["analysis"] = "股票当前处于横盘状态"
        elif overall_trend > self.trend_threshold:
            result["analysis"] = "股票当前呈上升趋势"
        elif overall_trend < -self.trend_threshold:
            result["analysis"] = "股票当前呈下降趋势"
        else:
            result["analysis"] = "股票当前趋势不明显"
        
        result["analysis"] += f"。{pattern_description}"
        
        return result