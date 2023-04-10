import time
from app import create_app
from .redis_helper import RedisHelper
import threading
import json
app = create_app(register_all=False)
class RedisSub(threading.Thread):
    def __init__(self, chan_sub):
        threading.Thread.__init__(self)
        self.chan_sub = chan_sub
    def run(self):
            while True:
                obj = RedisHelper()
                try:
                    redis_sub = obj.subscribe(self.chan_sub)
                    if redis_sub != None:
                        message = redis_sub.get_message()
                        if message:
                            if message["type"] == "message":
                                channel = str(message["channel"], encoding="utf-8")
                                data = str(message["data"], encoding="utf-8")
                                app.logger.info(channel + ":" + data)
                                from app.service.auto_trade import AutoTrade
                                AutoTrade(channel)
                            elif message["type"] == "subscrube":
                                app.logger.info(str(message["chennel"], encoding="utf-8"))
                except json.decoder.JSONDecodeError as err:
                    app.logger.info(err)
                except TimeoutError as err:
                    app.logger.info(err)
                    time.sleep(3)
                except:
                    app.logger.info("reids unknow connect error")
                    time.sleep(3)