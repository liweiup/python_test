import time
from app import create_app
from .redis_helper import RedisHelper
import threading
import json
from app.service.auto_trade import AutoTrade
app = create_app(register_all=False)
class RedisSub(threading.Thread):
    def __init__(self, chan_sub):
        threading.Thread.__init__(self)
        self.chan_sub = chan_sub
    def run(self):
            obj = RedisHelper()
            while True:
                try:
                    redis_sub = obj.subscribe(self.chan_sub)
                    if redis_sub != None:
                        message = redis_sub.get_message()
                        if message:
                            if message["type"] == "message":
                                app.logger.info(str(message["channel"], encoding="utf-8") + ":" + str(message["data"], encoding="utf-8"))
                                autoTrade = AutoTrade(str(message["channel"], encoding="utf-8"),str(message["data"], encoding="utf-8"))
                                autoTrade.auto_trade()
                            elif message["type"] == "subscrube":
                                app.logger.info(str(message["chennel"], encoding="utf-8"))
                            time.sleep(0.3)  # be nice to the system :)
                except json.decoder.JSONDecodeError as err:
                    app.logger.info(err)
                except TimeoutError as err:
                    app.logger.info(err)
                    time.sleep(2)
                # except:
                #     time.sleep(2)
                #     app.logger.info("reids connect error")
