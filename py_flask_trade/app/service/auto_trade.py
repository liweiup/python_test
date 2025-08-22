import json
import easytrader
import time
import win32gui
import win32con
import win32com.client
import pywinauto
from app.config import commonkey
from app.config.trading import TradingConfig
from app.cli.redis.client import redis_client

class AutoTrade:
    """自动交易类 - 优化版本"""
    
    def __init__(self, bs_type, app_instance=None, thx_path=None):
        """
        初始化自动交易
        
        Args:
            bs_type: 交易类型 ('diff_buy', 'diff_sell', 'diff_search', 'diff_cancel')
            app_instance: Flask应用实例
            thx_path: 同花顺路径，如果为None则使用默认路径
        """
        self.app = app_instance
        self.bs_type = bs_type
        self.trynum = 1
        self.max_retries = TradingConfig.MAX_RETRIES
        
        # 配置同花顺路径
        self.thx_path = thx_path or TradingConfig.get_thx_path()
        
        # 设置Redis键
        self._setup_redis_keys()
        
        # 初始化交易客户端
        self._init_trade_client()
        
        # 执行交易逻辑
        self._execute_trade_logic()
    
    def _setup_redis_keys(self):
        """设置Redis键"""
        if self.bs_type == 'diff_buy':
            self.bs_key = commonkey.BUYSTOCKINFO
        elif self.bs_type == 'diff_sell':
            self.bs_key = commonkey.SELLSTOCKINFO
        elif self.bs_type == 'diff_cancel':
            self.bs_key = commonkey.CANCELSTOCKINFO
    
    def _init_trade_client(self):
        """初始化交易客户端"""
        try:
            self.trade_user = easytrader.use('universal_client')
            self.trade_user.connect(self.thx_path)
            self.trade_user.enable_type_keys_for_editor()
            self._set_cmd_top()
            self._log("交易客户端初始化成功")
        except Exception as e:
            self._log(f"自动交易失败，客户端连接错误: {e}", level="error")
            raise
    
    def _execute_trade_logic(self):
        """执行交易逻辑"""
        if self.bs_type in ['diff_buy', 'diff_sell']:
            self._process_trade_queue()
        elif self.bs_type == 'diff_search':
            self._log("查询持仓信息")
            self.auto_search()
        elif self.bs_type == 'diff_cancel':
            self._log("开始全部撤单")
            self.auto_cancel()
    
    def _process_trade_queue(self):
        """处理交易队列"""
        while self.trynum <= self.max_retries:
            llen = redis_client.llen(self.bs_key)
            if llen == 0:
                break
                
            stock_json_str = redis_client.lpop(self.bs_key)
            if not stock_json_str:
                break
                
            try:
                self._process_single_trade(stock_json_str)
                self.trynum = 1  # 成功后重置重试次数
            except Exception as e:
                self._log(f"处理交易失败: {e}", level="error")
                redis_client.rpush(self.bs_key, stock_json_str)
                self.trynum += 1
                
                if self.trynum >= self.max_retries:
                    self._log(f"交易程序出错,重试次数: {self.trynum}", level="error")
                    break
    
    def _process_single_trade(self, stock_json_str):
        """处理单笔交易"""
        stock_json = json.loads(stock_json_str)
        if not stock_json:
            return
            
        for stock_row in stock_json:
            self._execute_stock_trade(stock_row)
    
    def _execute_stock_trade(self, stock_row):
        """执行股票交易"""
        try:
            individual_code = stock_row['individual_code']
            bs_num = self._calculate_trade_amount(stock_row)
            
            if self.bs_type == 'diff_buy':
                self._execute_buy_trade(stock_row, individual_code, bs_num)
            elif self.bs_type == 'diff_sell':
                self._execute_sell_trade(stock_row, individual_code, bs_num)
                
        except Exception as e:
            self._log(f"执行股票交易失败: {e}", level="error")
            raise
    
    def _calculate_trade_amount(self, stock_row):
        """计算交易数量"""
        rs_num = stock_row['stock_buy_num'] % TradingConfig.MIN_TRADE_AMOUNT
        in_num = TradingConfig.MIN_TRADE_AMOUNT if rs_num > TradingConfig.AMOUNT_ROUND_THRESHOLD else 0
        return stock_row['stock_buy_num'] - rs_num + in_num
    
    def _execute_buy_trade(self, stock_row, individual_code, bs_num):
        """执行买入交易"""
        if stock_row['deal_type'] == 0:  # 限价单
            price = self._calculate_buy_price(stock_row)
            msg = self.trade_user.buy(individual_code, price=price, amount=bs_num)
        else:  # 市价单
            msg = self.trade_user.market_buy(individual_code, amount=bs_num)
            price = "市价"
        
        self._handle_trade_result(msg, individual_code, "买入", price, bs_num)
    
    def _execute_sell_trade(self, stock_row, individual_code, bs_num):
        """执行卖出交易"""
        if stock_row['deal_type'] == 0:  # 限价单
            price = stock_row['now_price'] - TradingConfig.SELL_PRICE_OFFSET
            price = '{:.2f}'.format(price)
            msg = self.trade_user.sell(individual_code, price=price, amount=bs_num)
        else:  # 市价单
            msg = self.trade_user.market_sell(individual_code, amount=bs_num)
            price = "市价"
        
        self._handle_trade_result(msg, individual_code, "卖出", price, bs_num)
    
    def _calculate_buy_price(self, stock_row):
        """计算买入价格"""
        buy_price = stock_row['buy_price']
        newet_price = stock_row.get('newet_price', 0)
        
        if newet_price != 0 and newet_price < buy_price:
            price = newet_price + TradingConfig.BUY_PRICE_OFFSET
        else:
            price = buy_price + TradingConfig.BUY_PRICE_OFFSET
        
        return '{:.2f}'.format(price)
    
    def _handle_trade_result(self, msg, individual_code, action, price, bs_num):
        """处理交易结果"""
        entrust_no = msg.get('entrust_no', "")
        if entrust_no and hasattr(self, 'recall_key'):
            redis_client.rpush(self.recall_key, entrust_no)
        
        self._log(f"{action}-股票:{individual_code},价格:{price},数量:{bs_num},结果:{msg},委托号:{entrust_no}")
    
    def _get_all_hwnd(self, hwnd, mouse):
        """获取所有窗口句柄"""
        if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
            self.hwnd_map.update({hwnd: win32gui.GetWindowText(hwnd)})
    
    def _set_cmd_top(self):
        """设置CMD窗口置顶"""
        self.hwnd_map = {}
        win32gui.EnumWindows(self._get_all_hwnd, 0)
        
        for h, t in self.hwnd_map.items():
            if t and 'cmd.exe' in t:
                win32gui.BringWindowToTop(h)
                shell = win32com.client.Dispatch("WScript.Shell")
                shell.SendKeys('%')
                win32gui.SetForegroundWindow(h)
                win32gui.ShowWindow(h, win32con.SW_RESTORE)
                break
    
    def auto_cancel(self):
        """全部撤单"""
        try:
            msg = self.trade_user.cancel_all_entrusts()
            self._log(f"全部撤单-股票,结果:{msg}")
        except Exception as e:
            self._log(f"撤单失败: {e}", level="error")
    
    def auto_search(self):
        """查询持仓信息"""
        try:
            position = self.trade_user.position
            self._log(f"查询挂单信息-股票:{position}")
        except Exception as e:
            self._log(f"查询持仓失败: {e}", level="error")
    
    def _log(self, message, level="warning"):
        """统一日志输出"""
        if self.app and hasattr(self.app, 'logger'):
            if level == "error":
                self.app.logger.error(message)
            else:
                self.app.logger.warning(message)
        else:
            print(f"[{level.upper()}] {message}")


# 工厂函数，用于创建AutoTrade实例
def create_auto_trade(bs_type, app_instance=None, thx_path=None):
    """
    创建AutoTrade实例的工厂函数
    
    Args:
        bs_type: 交易类型
        app_instance: Flask应用实例
        thx_path: 同花顺路径
    
    Returns:
        AutoTrade实例
    """
    return AutoTrade(bs_type, app_instance, thx_path)


if __name__ == "__main__":
    # 测试代码
    auto_trade_buy = create_auto_trade('diff_buy')
    auto_trade_sell = create_auto_trade('diff_sell')