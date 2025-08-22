#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from dotenv import load_dotenv
from flask import Flask

# 加载 .flaskenv 文件
load_dotenv('.flaskenv')

print("=== 环境变量检查 ===")
print(f"FLASK_ENV: {os.getenv('FLASK_ENV')}")
print(f"ENV: {os.getenv('ENV')}")

print("\n=== Flask应用配置检查 ===")
app = Flask(__name__)

# 检查初始状态
print(f"初始 app.config.get('ENV'): {app.config.get('ENV')}")
print(f"初始 app.config.get('FLASK_ENV'): {app.config.get('FLASK_ENV')}")

# 手动设置ENV
app.config['ENV'] = 'development'
print(f"设置后 app.config.get('ENV'): {app.config.get('ENV')}")

# 检查Flask的默认配置
print(f"app.config.get('DEBUG'): {app.config.get('DEBUG')}")
print(f"app.config.get('TESTING'): {app.config.get('TESTING')}")

print("\n=== 所有相关配置 ===")
for key in ['ENV', 'FLASK_ENV', 'DEBUG', 'TESTING']:
    print(f"{key}: {app.config.get(key)}") 