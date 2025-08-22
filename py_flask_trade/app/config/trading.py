# -*- coding: utf-8 -*-
"""
交易配置模块
"""

import os

class TradingConfig:
    """交易配置类"""
    
    # 同花顺默认路径
    DEFAULT_THX_PATH = r'D:\同花顺软件\同花顺\xiadan.exe'
    
    # 重试配置
    MAX_RETRIES = 9
    RETRY_DELAY = 2  # 秒
    
    # 交易配置
    BUY_PRICE_OFFSET = 0.01  # 买入价格偏移
    SELL_PRICE_OFFSET = 0.02  # 卖出价格偏移
    MIN_TRADE_AMOUNT = 100   # 最小交易数量
    AMOUNT_ROUND_THRESHOLD = 60  # 数量取整阈值
    
    @classmethod
    def get_thx_path(cls):
        """获取同花顺路径"""
        # 优先从环境变量读取
        env_path = os.getenv('THX_PATH')
        if env_path and os.path.exists(env_path):
            return env_path
        
        # 使用默认路径
        if os.path.exists(cls.DEFAULT_THX_PATH):
            return cls.DEFAULT_THX_PATH
        
        # 尝试其他常见路径
        common_paths = [
            r'C:\同花顺软件\同花顺\xiadan.exe',
            r'D:\同花顺\xiadan.exe',
            r'C:\同花顺\xiadan.exe',
        ]
        
        for path in common_paths:
            if os.path.exists(path):
                return path
        
        return cls.DEFAULT_THX_PATH
    
    @classmethod
    def validate_config(cls):
        """验证配置"""
        thx_path = cls.get_thx_path()
        if not os.path.exists(thx_path):
            raise FileNotFoundError(f"同花顺客户端未找到: {thx_path}")
        
        return True 