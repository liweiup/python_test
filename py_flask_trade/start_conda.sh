#!/bin/bash

echo "🚀 启动Conda环境应用..."

# 检查环境是否存在
if ! conda env list | grep -q "py_flask_trade"; then
    echo "❌ 环境 'py_flask_trade' 不存在，请先运行 setup_conda.sh"
    exit 1
fi

# 激活环境
echo "✅ 激活conda环境..."
conda activate py_flask_trade

# 检查环境配置
if [ ! -f ".env" ]; then
    echo "⚠️  环境配置文件不存在，创建本地配置..."
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
fi

# 创建必要目录
mkdir -p logs
mkdir -p data

# 启动应用
echo "🌐 启动Flask应用..."
echo "📍 访问地址: http://127.0.0.1:5000"
echo "📝 按 Ctrl+C 停止应用"
echo ""

python starter.py 


