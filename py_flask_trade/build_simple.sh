#!/bin/bash

echo "🚀 简化版Flask应用打包..."

# 清理之前的构建
echo "🧹 清理之前的构建文件..."
rm -rf build dist __pycache__

# 创建必要的目录
mkdir -p logs data

# 创建本地配置文件
echo "⚙️ 创建本地环境配置..."
cat > .env << EOF
SQLALCHEMY_DATABASE_URI = 'sqlite:///./lincms_local.db'
SECRET_KEY = 'local_development_secret_key_2024'
REDIS_URL = "redis://localhost:6379/0"
REDIS_SUB = "diff_buy,diff_sell,diff_cancel,diff_search"
ENV = "local"
DEBUG = True
FLASK_APP = "starter:app"
FLASK_ENV = "local"
FLASK_DEBUG = True
EOF

# 使用PyInstaller基本命令打包
echo "📦 开始打包..."
pyinstaller \
    --onefile \
    --add-data "app:app" \
    --add-data "local_config.py:." \
    --add-data "lincms.db:." \
    --hidden-import flask \
    --hidden-import flask_cors \
    --hidden-import flask_socketio \
    --hidden-import flask_sqlalchemy \
    --hidden-import flask_redis \
    --hidden-import redis \
    --hidden-import gevent \
    --hidden-import gevent.websocket \
    --hidden-import pydantic \
    --hidden-import spectree \
    --hidden-import lin \
    --hidden-import lin.apidoc \
    --hidden-import lin.cms \
    --hidden-import sqlalchemy \
    --hidden-import sqlalchemy.orm \
    --hidden-import sqlalchemy.sql \
    --hidden-import sqlalchemy.ext.declarative \
    --hidden-import sqlalchemy.pool \
    --hidden-import sqlalchemy.engine \
    --hidden-import sqlalchemy.event \
    --hidden-import sqlalchemy.dialects.sqlite \
    --hidden-import sqlalchemy.dialects.mysql \
    --hidden-import sqlalchemy.dialects.postgresql \
    --name flask_cms_app \
    starter.py

# 检查打包结果
if [ -f "dist/flask_cms_app" ]; then
    echo "✅ 打包成功！"
    echo "📍 可执行文件位置: dist/flask_cms_app"
    echo "📁 文件大小: $(du -h dist/flask_cms_app | cut -f1)"
    echo ""
    echo "🔧 使用方法："
    echo "1. 进入dist目录: cd dist"
    echo "2. 运行程序: ./flask_cms_app"
    echo "3. 访问地址: http://127.0.0.1:5000"
else
    echo "❌ 打包失败，请检查错误信息"
    exit 1
fi 