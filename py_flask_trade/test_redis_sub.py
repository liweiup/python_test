#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import redis
from app import create_app

def test_redis_subscription():
    """测试Redis订阅功能"""
    print("=" * 50)
    print("Testing Redis Subscription")
    print("=" * 50)
    
    try:
        # 创建应用
        app = create_app(register_all=True)
        
        # 检查配置
        redis_url = app.config.get("REDIS_URL", "")
        redis_sub = app.config.get("REDIS_SUB", "")
        
        print(f"Redis URL: {redis_url}")
        print(f"Redis SUB: {redis_sub}")
        
        if not redis_sub:
            print("No Redis subscription configured!")
            return
        
        # 测试Redis连接
        try:
            r = redis.from_url(redis_url)
            r.ping()
            print("✓ Redis connection successful")
        except Exception as e:
            print(f"✗ Redis connection failed: {e}")
            return
        
        # 测试发布消息
        channels = redis_sub.split(',')
        print(f"Testing channels: {channels}")
        
        for channel in channels:
            message = f"Test message from {channel} at {time.strftime('%H:%M:%S')}"
            r.publish(channel, message)
            print(f"Published to {channel}: {message}")
        
        print("\nWaiting 5 seconds for subscription to receive messages...")
        time.sleep(5)
        
        print("Test completed!")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_redis_subscription() 