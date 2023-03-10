import json
from app import create_app
import easytrader
import time
import win32gui
import win32con
import win32com.client
import pywinauto
import subprocess
import os
app = create_app(register_all=False)

class AutoTrade:
    hwnd_map = {}#所有窗口
    def __init__(self, bs_type,stock_json=""):
        self.stock_json = json.loads(stock_json)
        self.bs_type = bs_type
    def get_all_hwnd(self,hwnd, mouse):
        if (win32gui.IsWindow(hwnd) and
            win32gui.IsWindowEnabled(hwnd) and
            win32gui.IsWindowVisible(hwnd)):
            self.hwnd_map.update({hwnd: win32gui.GetWindowText(hwnd)})
    #cmd窗口置顶
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

    def auto_trade(self,try_num=0):
        try:
            thx_path = r'D:\同花顺软件\同花顺\xiadan.exe'
            self.trade_user = easytrader.use('universal_client')
            self.trade_user.connect(thx_path)
            self.trade_user.enable_type_keys_for_editor()
            self.set_cmd_top()
            if len(self.stock_json) > 0:
                for stock_row in self.stock_json:
                    price = 0#价格
                    bs_num = 0#数量
                    in_num = 0#余数大于50增加100股
                    individual_code = stock_row['individual_code']#股票编码
                    rs_num = stock_row['stock_buy_num'] % 100
                    if rs_num > 50:
                        in_num = 100
                    else:
                        in_num = 0
                    try:
                        # 买入还是卖出
                        if self.bs_type == 'diff_buy':
                            price = stock_row['buy_price']
                            bs_num = stock_row['stock_buy_num'] - rs_num + in_num
                            msg = self.trade_user.market_buy(individual_code,amount=bs_num)
                            # msg = self.trade_user.buy(individual_code, price=price, amount=bs_num)
                            app.logger.info(msg)
                        elif self.bs_type == 'diff_sell':
                            price = stock_row['now_price']
                            bs_num = stock_row['stock_buy_num'] - rs_num + in_num
                            msg = self.trade_user.market_sell(individual_code,amount=bs_num)
                            app.logger.info(msg)
                    except easytrader.exceptions.TradeError as err:
                        app.logger.info("自动交易失败:{0}".format(err))
                    # print(user.balance)
                    # print(user.position)
                    # msg = user.buy(individual_code, price=price, amount=bs_num)
        except pywinauto.application.ProcessNotFoundError as err:
             app.logger.info("检查同花顺客户端是否打开:{0}".format(err))
        except pywinauto.timings.TimeoutError:
            app.logger.info("自动交易失败，pywinauto超时")
            while try_num < 3:
                time.sleep(3)
                try_num = try_num + 1
                app.logger.info("try_num:{0}".format(try_num))
                self.auto_trade(try_num)
                break
        except:
            app.logger.info("自动交易失败，未知错误")

if __name__ == "__main__":
    str = '[{"individual_code":"605162","individual_name":"新中港","stype":1,"rank_num":3700,"stock_buy_num":565,"now_price":0,"buy_price":9.53,"today_ratio":3.813,"clean_ratio":0,"c_date":"2023-03-06","c_hour":9,"c_min":40,"strategy_type":2}]'
    autoTrade = AutoTrade('diff_buy',str)
    autoTrade.auto_trade()

    str = '[{"individual_code":"605001","individual_name":"威奥股份","stype":1,"rank_num":2987,"stock_buy_num":625,"now_price":7.88,"buy_price":8.01,"today_ratio":0.25,"clean_ratio":-1.6230000000000002,"c_date":"2023-03-03","c_hour":9,"c_min":40,"strategy_type":2}]'
    autoTrade = AutoTrade('diff_sell',str)
    autoTrade.auto_trade()
    exit
