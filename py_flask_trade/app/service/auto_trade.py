import os
import json
import subprocess
import easytrader
import time
import win32gui
import win32con
import win32com.client
from app.config import commonkey
from app.config.trading import TradingConfig
from app.cli.redis.client import redis_client
from app.service.easytrader_patch import _patch_easytrader

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
        self.trynum = 0
        self.max_retries = TradingConfig.MAX_RETRIES
        
        # 配置同花顺路径
        self.thx_path = thx_path or TradingConfig.get_thx_path()
        
        # 设置Redis键
        self._setup_redis_keys()
        
        self.trade_user = easytrader.use('universal_client')  # 只初始化一次
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

    def _find_ths_hwnd(self):
        """查找同花顺主窗口句柄，支持模糊匹配"""
        target = "网上股票交易系统"
        hwnd = None
        def enum_handler(h, param):
            nonlocal hwnd
            if win32gui.IsWindowVisible(h):
                title = win32gui.GetWindowText(h)
                if target in title:
                    hwnd = h
        win32gui.EnumWindows(enum_handler, None)
        return hwnd
    
    def _init_trade_client(self):
        """初始化交易客户端（简化版）"""
        try:
            if not os.path.exists(self.thx_path):
                self._log(f"未找到同花顺交易客户端: {self.thx_path}", level="error")
                raise FileNotFoundError(self.thx_path)

            # 先尝试直接连接（如果已经运行）
            try:
                self.trade_user.connect(self.thx_path)
                self._log("已连接到已运行的同花顺客户端", level="warning")
            except Exception:
                # 未运行或连接失败，尝试启动并等待
                program_dir = os.path.dirname(self.thx_path)
                try:
                    # subprocess.Popen([self.thx_path], cwd=program_dir, shell=True)
                    import win32api
                    win32api.ShellExecute(None, "open", self.thx_path, None, program_dir, 1)
                    self._log("已启动同花顺客户端，等待窗口就绪...", level="warning")
                except Exception as e:
                    self._log(f"启动同花顺客户端失败: {e}", level="error")
                    raise

                # 等待窗口并重试连接
                max_wait = 30
                waited = 0
                connected = False
                while waited < max_wait and not connected:
                    time.sleep(1)
                    waited += 1
                    hwnd = self._find_ths_hwnd()
                    if hwnd:
                        try:
                            self.trade_user.connect(self.thx_path)
                            connected = True
                            break
                        except Exception as e:
                            self._log(f"检测到窗口但连接失败（第{waited}s）: {e}", level="warning")
                            # 把窗口置前再重试
                            try:
                                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                                win32gui.SetForegroundWindow(hwnd)
                            except Exception:
                                pass
                            time.sleep(1)
                    else:
                        self._log(f"等待同花顺窗口出现...({waited}s)", level="warning")

                if not connected:
                    self._log("同花顺客户端窗口或连接多次失败，启动失败", level="error")
                    raise RuntimeError("客户端连接失败")

            # 连接成功后初始化
            try:
                self.trade_user.enable_type_keys_for_editor()
            except Exception as e:
                self._log(f"启用 type keys 失败: {e}", level="warning")
            try:
                self._set_cmd_top()
            except Exception as e:
                self._log(f"设置 CMD 置顶失败: {e}", level="warning")

            self._log("交易客户端初始化成功", level="warning")
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
        elif self.bs_type == 'diff_clear':
            self._log("开始清仓操作")
            self.auto_clear()
    
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
            if not position:
                self._log("未查询到持仓信息")
                return
            pretty_lines = []
            for idx, pos in enumerate(position, 1):
                line = (
                    f"{idx}. 股票代码: {pos.get('证券代码', '')} | "
                    f"名称: {pos.get('证券名称', '')} | "
                    f"持仓: {pos.get('股票余额', '')} | "
                    f"可用: {pos.get('可用余额', '')} | "
                    f"成本价: {pos.get('成本价', '')} | "
                    f"现价: {pos.get('市价', '')} | "
                    f"盈亏: {pos.get('盈亏', '')}"
                )
                pretty_lines.append(line)
            pretty_output = "\n".join(pretty_lines)
            self._log(f"持仓信息:\n{pretty_output}")
        except Exception as e:
            self._log(f"查询持仓失败: {e}", level="error")
    

    def auto_clear(self):
        """清仓操作：根据DEALTYPE决定限价或市价卖出"""
        try:
            position = self.trade_user.position
            if not position:
                self._log("未查询到持仓信息，无法清仓")
                return
            for pos in position:
                code = pos.get('证券代码', '')
                available = pos.get('可用余额', 0)
                if code and float(available) > 0:
                    # 直接从redis获取DEALTYPE，纯数字字符串
                    deal_type = redis_client.hget(commonkey.DIFFBUYINFO, "DEALTYPE")
                    if isinstance(deal_type, bytes):
                        deal_type = deal_type.decode()
                    if deal_type == "0":
                        # 限价单
                        now_price = pos.get('市价') or pos.get('当前价') or pos.get('成本价')
                        try:
                            price = float(now_price) - TradingConfig.SELL_PRICE_OFFSET
                            price = '{:.2f}'.format(price)
                        except Exception:
                            price = now_price
                        self._log(f"清仓限价卖出 股票:{code} 可用:{available} 价格:{price}")
                        try:
                            msg = self.trade_user.sell(code, price=price, amount=int(float(available)))
                            self._log(f"清仓卖出结果: 股票:{code}, 数量:{available}, 价格:{price}, 结果:{msg}")
                        except Exception as e:
                            self._log(f"清仓卖出失败: 股票:{code}, 错误:{e}", level="error")
                    else:
                        # 市价单
                        self._log(f"清仓市价卖出 股票:{code} 可用:{available}")
                        try:
                            msg = self.trade_user.market_sell(code, amount=int(float(available)))
                            self._log(f"清仓卖出结果: 股票:{code}, 数量:{available}, 结果:{msg}")
                        except Exception as e:
                            self._log(f"清仓卖出失败: 股票:{code}, 错误:{e}", level="error")
        except Exception as e:
            self._log(f"清仓操作失败: {e}", level="error")
    
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