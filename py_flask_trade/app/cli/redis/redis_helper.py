from .client import redis_client               
import time
import redis
import threading
class RedisHelper(object):

    _instance_lock = threading.Lock()
    _conn = None #初始定义为空
    _pub = None

    def __init__(self):
        self._conn = redis_client
        pass

    def __new__(cls, *args, **kwargs):
            if not hasattr(RedisHelper, "_instance"):
                with RedisHelper._instance_lock:
                    if not hasattr(RedisHelper, "_instance"):
                        RedisHelper._instance = object.__new__(cls)  
            return RedisHelper._instance
    
    def subscribe(self,chan_sub):
        ping_flag = False
        try:
            ping_flag = redis_client.ping()
            if self._pub == None:
                print("------redis start:" + str(ping_flag))
                # 返回发布订阅对象，通过这个对象你能1）订阅频道 2）监听频道中的消息
                self._pub = self._conn.pubsub()
                # 订阅某个频道，与publish()中指定的频道一样。消息会发布到这个频道中
                self._pub.subscribe(chan_sub)
        except redis.exceptions.ConnectionError as err:
            time.sleep(3)
            print("redis.exceptions.ConnectionError" + str(ping_flag))
            self._pub = None
        except redis.ConnectionError as err:
            time.sleep(3)
            print("redis.ConnectionError:" + str(ping_flag))
            self._pub = None
        except redis.exceptions.ConnectionError as err:
            time.sleep(3)
            print("redis.exceptions.ConnectionError" + str(ping_flag))
            self._pub = None
        finally:
            return self._pub

# def task(arg):
#     obj = RedisHelper.instance()
#     print(obj)
    
# time.sleep(1)
# obj = RedisHelper()
# print(obj._conn)
# print(obj._pub)