import redis
from contextlib import contextmanager
from typing import Optional, Any
import logging
from common.config import REDIS_CONFIG

class RedisUtils:
    def __init__(self, config=REDIS_CONFIG):
        self.config = {
            'host': config['host'],
            'port': config['port'],
            'db': config['db'],
            'password': config['password'],
            'decode_responses': True  # 自动将字节解码为字符串
        }
        self.pool = redis.ConnectionPool(**self.config)
        self.logger = logging.getLogger(__name__)

    @contextmanager
    def get_connection(self):
        connection = redis.Redis(connection_pool=self.pool)
        try:
            yield connection
        except redis.RedisError as e:
            self.logger.error(f"Redis error: {e}")
            raise
        finally:
            connection.close()

    def get_str(self, key: str) -> Optional[str]:
        with self.get_connection() as conn:
            try:
                return conn.get(key)
            except redis.RedisError as e:
                self.logger.error(f"Error getting key {key}: {e}")
                return None

    def set_str(self, key: str, value: str, ex: Optional[int] = None) -> bool:
        with self.get_connection() as conn:
            try:
                return conn.set(key, value, ex=ex)
            except redis.RedisError as e:
                self.logger.error(f"Error setting key {key}: {e}")
                return False

    def delete(self, key: str) -> int:
        with self.get_connection() as conn:
            try:
                return conn.delete(key)
            except redis.RedisError as e:
                self.logger.error(f"Error deleting key {key}: {e}")
                return 0

    def exists(self, key: str) -> bool:
        with self.get_connection() as conn:
            try:
                return conn.exists(key) > 0
            except redis.RedisError as e:
                self.logger.error(f"Error checking existence of key {key}: {e}")
                return False

    def lpush(self, key: str, *values: Any) -> Optional[int]:
        with self.get_connection() as conn:
            try:
                return conn.lpush(key, *values)
            except redis.RedisError as e:
                self.logger.error(f"Error pushing to list {key}: {e}")
                return None

    def rpop(self, key: str) -> Optional[str]:
        with self.get_connection() as conn:
            try:
                return conn.rpop(key)
            except redis.RedisError as e:
                self.logger.error(f"Error popping from list {key}: {e}")
                return None

    def lrange(self, key: str, start: int, end: int) -> Optional[list]:
        with self.get_connection() as conn:
            try:
                return conn.lrange(key, start, end)
            except redis.RedisError as e:
                self.logger.error(f"Error getting range from list {key}: {e}")
                return None