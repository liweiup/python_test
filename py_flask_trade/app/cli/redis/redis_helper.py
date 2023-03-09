from app.cli.redis.client import redis_client               
                
class RedisHelper(object):
    __conn = None #初始定义为空
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
        # 返回发布订阅对象，通过这个对象你能1）订阅频道 2）监听频道中的消息
        pub = self.__conn.pubsub()
        # 订阅某个频道，与publish()中指定的频道一样。消息会发布到这个频道中
        pub.subscribe(chan_sub)
        return pub