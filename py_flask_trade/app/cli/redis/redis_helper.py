from app.cli.redis.client import redis_client               
import time
import redis
class RedisHelper(object):
    __conn = None #初始定义为空
    __pub = None
    def __init__(self):
        if self.__conn is None:
            self.__conn = redis_client
    def publish(self, msg):
        """
        在指定频道上发布消息
        :param msg:
        :return:
        """
        # publish(): 在指定频道上发布消息，返回订阅者的数量
        self.__conn.publish(self.chan_sub, msg)
        return True

    def subscribe(self,chan_sub):
        ping_flag = False
        try:
            ping_flag = redis_client.ping()
            if self.__pub == None:
                print("redis start" + str(ping_flag))
                # 返回发布订阅对象，通过这个对象你能1）订阅频道 2）监听频道中的消息
                self.__pub = self.__conn.pubsub()
                # 订阅某个频道，与publish()中指定的频道一样。消息会发布到这个频道中
                self.__pub.subscribe(chan_sub)
        except redis.ConnectionError as err:
            time.sleep(3)
            print("redis connect error:" + str(ping_flag))
            self.__pub = None
        finally:
            return self.__pub