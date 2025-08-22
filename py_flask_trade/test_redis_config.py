#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from app import create_app

def test_redis_config():
    """测试Redis配置加载"""
    print("=" * 50)
    print("Testing Redis Configuration")
    print("=" * 50)
    
    # 检查环境
    is_packaged = getattr(sys, 'frozen', False) or getattr(os, '_MEIPASS', None)
    print(f"Packaged environment: {is_packaged}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Python executable: {sys.executable}")
    
    # 检查.env文件
    env_files = ['.development.env', '.production.env', '.flaskenv']
    for env_file in env_files:
        if os.path.exists(env_file):
            print(f"Found env file: {env_file}")
            with open(env_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'REDIS_SUB' in content:
                    print(f"  - Contains REDIS_SUB configuration")
        else:
            print(f"Missing env file: {env_file}")
    
    # 创建应用
    try:
        app = create_app(register_all=False)  # 不注册所有组件，只测试配置
        
        # 检查配置
        print(f"\nApp configuration:")
        print(f"  - ENV: {app.config.get('ENV', 'unknown')}")
        print(f"  - REDIS_URL: {app.config.get('REDIS_URL', 'not set')}")
        print(f"  - REDIS_SUB: {app.config.get('REDIS_SUB', 'not set')}")
        
        # 检查环境变量
        print(f"\nEnvironment variables:")
        print(f"  - REDIS_URL: {os.getenv('REDIS_URL', 'not set')}")
        print(f"  - REDIS_SUB: {os.getenv('REDIS_SUB', 'not set')}")
        
    except Exception as e:
        print(f"Error creating app: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_redis_config() 