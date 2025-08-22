import time
from .redis_helper import RedisHelper
import threading
import json

# 移除重复的create_app调用，使用主应用传递的app实例
# app = create_app(register_all=False)


def _to_str(value):
    if isinstance(value, (bytes, bytearray)):
        try:
            return value.decode("utf-8", errors="ignore")
        except Exception:
            return str(value)
    return str(value)


class RedisSub(threading.Thread):
    def __init__(self, chan_sub, app_instance=None):
        threading.Thread.__init__(self)
        # 标准化订阅集合，便于辅助类使用
        self.chan_sub = set(chan_sub) if isinstance(chan_sub, (set, list, tuple)) else {chan_sub}
        self.daemon = True
        self.running = True
        self.app = app_instance  # 保存app实例

    def stop(self):
        """停止订阅线程"""
        self.running = False

    def run(self):
            helper = RedisHelper()
            backoff_seconds = 1
            max_backoff = 30  # 最大退避时间30秒
            
            while self.running:
                try:
                    # 添加连接超时
                    pubsub = helper.subscribe(self.chan_sub)
                    if pubsub is None:
                        if self.app:
                            self.app.logger.warning(f"Redis subscription failed, retrying in {backoff_seconds}s...")
                        time.sleep(backoff_seconds)
                        backoff_seconds = min(backoff_seconds * 2, max_backoff)
                        continue

                    # 收到消息前小睡，避免空转高CPU
                    message = pubsub.get_message(timeout=1.0)  # 1秒超时
                    if not message:
                        time.sleep(0.05)
                        continue

                    msg_type = message.get("type")
                    if msg_type == "message":
                        channel = _to_str(message.get("channel"))
                        data = _to_str(message.get("data"))
                        if self.app:
                            self.app.logger.warning(f"{channel}:{data}")
                        # from app.service.auto_trade import AutoTrade
                        # AutoTrade(channel)
                    elif msg_type == "subscribe":
                        channel = _to_str(message.get("channel"))
                        if self.app:
                            self.app.logger.warning(f"subscribed: {channel}")

                    # 收到有效消息后重置退避时间
                    backoff_seconds = 1

                except json.decoder.JSONDecodeError as err:
                    if self.app:
                        self.app.logger.warning(f"redis json decode error: {err}")
                    time.sleep(0.5)
                except TimeoutError as err:
                    if self.app:
                        self.app.logger.warning(f"redis timeout: {err}")
                    time.sleep(3)
                except Exception as err:
                    if self.app:
                        self.app.logger.warning(f"redis connection error: {err}")
                    time.sleep(min(backoff_seconds, 5))
                    backoff_seconds = min(backoff_seconds * 2, max_backoff)
                    
                    # 如果连续失败超过一定次数，增加更长的等待时间
                    if backoff_seconds >= max_backoff:
                        if self.app:
                            self.app.logger.error("Redis connection failed repeatedly, waiting longer...")
                        time.sleep(10)  # 额外等待10秒  