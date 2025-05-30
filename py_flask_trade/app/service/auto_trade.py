import json
from app import create_app
import easytrader
import time
import win32gui
import win32con
import win32com.client
import pywinauto
from app.config import commonkey
from app.cli.redis.client import redis_client
app = create_app(register_all=False)

class AutoTrade:
    thx_path = r'D:\同花顺软件\同花顺\xiadan.exe'
    bs_type = ""
    bs_key = ""
    stock_json_str = ""
    trynum = 1

    stock_json = None
    hwnd_map = {}#所有窗口
    def __init__(self, bs_type):
        # 获取队列
        if bs_type == 'diff_buy':
            self.bs_key = commonkey.BUYSTOCKINFO
        elif bs_type == 'diff_sell':
            self.bs_key = commonkey.SELLSTOCKINFO
        try:
            self.trade_user = easytrader.use('universal_client')
            self.trade_user.connect(self.thx_path)
            self.trade_user.enable_type_keys_for_editor()
            self.set_cmd_top()
        except:
            app.logger.info("自动交易失败，客户端连接错误")
            return
        # 用來交易
        if bs_type == 'diff_buy' or bs_type == 'diff_sell':
            llen = redis_client.llen(self.bs_key)
            if llen > 0:
                while True:
                    if self.trynum >= 9:
                        app.logger.info("交易程序出错,重试次数:{num}".format(num=self.trynum))
                        self.stock_json_str = redis_client.lpop(self.bs_key)
                        break
                    llen = redis_client.llen(self.bs_key)
                    if llen == 0:
                        break
                    self.stock_json_str = redis_client.lpop(self.bs_key)
                    self.bs_type = bs_type
                    self.auto_trade()
                    # time.sleep(2)
        elif bs_type == 'diff_search':
            app.logger.info("查询持仓信息")
            self.auto_search()
        elif bs_type == 'diff_cancel':
            app.logger.info("开始全部撤单")
            self.auto_cancel()
    def get_all_hwnd(self,hwnd, mouse): 
        if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
            self.hwnd_map.update({hwnd: win32gui.GetWindowText(hwnd)})
    # cmd窗口置顶
    def set_cmd_top(self):
        win32gui.EnumWindows(self.get_all_hwnd, 0)
        for h, t in self.hwnd_map.items():
            if t :
                if 'cmd.exe' in t:
                    # h 为想要放到最前面的窗口句柄
                    win32gui.BringWindowToTop(h)
                    shell = win32com.client.Dispatch("WScript.Shell")
                    shell.SendKeys('%')
                    # 被其他窗口遮挡，调用后放到最前面
                    win32gui.SetForegroundWindow(h)
                    # 解决被最小化的情况
                    win32gui.ShowWindow(h, win32con.SW_RESTORE)
    def auto_cancel(self):
        msg= self.trade_user.cancel_all_entrusts()
        app.logger.info("全部撤單-股票,结果:{msg}".format(msg=msg))
    def auto_search(self):
        # 当日成交
        # self.trade_user.today_trades
        # 当日委托
        # self.trade_user.today_entrusts
        msg = ""
        app.logger.info("查询挂单信息-股票:{msg}".format(msg=self.trade_user.position))
    def auto_trade(self):
        try:
            stock_json = json.loads(self.stock_json_str)
            if len(stock_json) > 0:
                for stock_row in stock_json:
                    price = 0#价格
                    bs_num = 0#数量
                    in_num = 0#余数大于50增加100股
                    individual_code = stock_row['individual_code']#股票编码
                    rs_num = stock_row['stock_buy_num'] % 100
                    if rs_num > 60:
                        in_num = 100
                    else:
                        in_num = 0
                    try:
                        # 买入还是卖出
                        if self.bs_type == 'diff_buy':
                            buy_price = stock_row['buy_price']
                            bs_num = stock_row['stock_buy_num'] - rs_num + in_num
                            if stock_row['deal_type'] == 0:
                                newet_price = stock_row['newet_price']
                                if newet_price != 0 and newet_price < buy_price:
                                    price = newet_price + 0.01
                                else:
                                    price = buy_price + 0.01
                                price = '{:.2f}'.format(price)
                                msg = self.trade_user.buy(individual_code, price=price, amount=bs_num)
                            else:
                                price = buy_price + 0.01
                                msg = self.trade_user.market_buy(individual_code,amount=bs_num)
                            entrust_no = ""
                            if 'entrust_no' in msg:
                                entrust_no = msg.get('entrust_no')
                                redis_client.rpush(self.recall_key,entrust_no)
                            app.logger.info("买入-股票:{individual_code},价格:{price},数量:{bs_num},结果:{msg}".format(individual_code=individual_code, price=price,bs_num=bs_num, msg=msg,entrust_no=entrust_no))
                        elif self.bs_type == 'diff_sell':
                            price = stock_row['now_price']
                            bs_num = stock_row['stock_buy_num'] - rs_num + in_num
                            if stock_row['deal_type'] == 0:
                                price = price - 0.02
                                price = '{:.2f}'.format(price)
                                msg= self.trade_user.sell(individual_code,price=price, amount=bs_num)
                            else:
                                msg = self.trade_user.market_sell(individual_code,amount=bs_num)
                            entrust_no = ""
                            if 'entrust_no' in msg:
                                entrust_no = msg.get('entrust_no')
                                redis_client.rpush(self.recall_key,entrust_no)
                            app.logger.info("卖出-股票:{individual_code},数量:{bs_num},结果:{msg},entrust_no:{entrust_no}".format(individual_code=individual_code, bs_num=bs_num, msg=msg,entrust_no=entrust_no))
                    except easytrader.exceptions.TradeError as err:
                        app.logger.info("自动交易失败:{0}".format(err))
                        redis_client.rpush(self.bs_key,self.stock_json_str)
                        self.trynum = self.trynum + 1
                    # print(user.balance)
                    # print(user.position)
                    # msg = user.buy(individual_code, price=price, amount=bs_num)
        except pywinauto.application.ProcessNotFoundError as err:
            app.logger.info("检查同花顺客户端是否打开:{0}".format(err))
            redis_client.rpush(self.bs_key,self.stock_json_str)
            self.trynum = self.trynum + 1
        except pywinauto.timings.TimeoutError:
            app.logger.info("自动交易失败，pywinauto超时")
            redis_client.rpush(self.bs_key,self.stock_json_str)
            self.trynum = self.trynum + 1
        except:
            app.logger.info("自动交易失败，未知错误")
            redis_client.rpush(self.bs_key,self.stock_json_str)
            self.trynum = self.trynum + 1

if __name__ == "__main__":
    autoTrade = AutoTrade('diff_buy')
    autoTrade.auto_trade()

    autoTrade = AutoTrade('diff_sell')
    autoTrade.auto_trade()