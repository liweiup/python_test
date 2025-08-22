import time
from app import create_app
from .redis_helper import RedisHelper
import threading
import json

app = create_app(register_all=False)


def _to_str(value):
    if isinstance(value, (bytes, bytearray)):
        try:
            return value.decode("utf-8", errors="ignore")
        except Exception:
            return str(value)
    return str(value)


class RedisSub(threading.Thread):
    def __init__(self, chan_sub):
        threading.Thread.__init__(self)
        # 标准化订阅集合，便于辅助类使用
        self.chan_sub = set(chan_sub) if isinstance(chan_sub, (set, list, tuple)) else {chan_sub}
        self.daemon = True

    def run(self):
            helper = RedisHelper()
            backoff_seconds = 1
            while True:
                try:
                    pubsub = helper.subscribe(self.chan_sub)
                    if pubsub is None:
                        time.sleep(backoff_seconds)
                        backoff_seconds = min(backoff_seconds * 2, 5)
                        continue

                    # 收到消息前小睡，避免空转高CPU
                    message = pubsub.get_message()
                    if not message:
                        time.sleep(0.05)
                        continue

                    msg_type = message.get("type")
                    if msg_type == "message":
                        channel = _to_str(message.get("channel"))
                        data = _to_str(message.get("data"))
                        app.logger.info(f"{channel}:{data}")
                        # from app.service.auto_trade import AutoTrade
                        # AutoTrade(channel)
                    elif msg_type == "subscribe":
                        channel = _to_str(message.get("channel"))
                        app.logger.info(f"subscribed: {channel}")

                    # 收到有效消息后重置退避时间
                    backoff_seconds = 1

                except json.decoder.JSONDecodeError as err:
                    app.logger.info(f"redis json decode error: {err}")
                    time.sleep(0.5)
                except TimeoutError as err:
                    app.logger.info(f"redis timeout: {err}")
                    time.sleep(3)
                except Exception as err:
                    app.logger.info(f"redis unknown connect error: {err}")
                    time.sleep(min(backoff_seconds, 5))
                    backoff_seconds = min(backoff_seconds * 2, 10)