#!/bin/bash

echo "🚀 开始打包Flask应用为exe..."

# 检查环境
if ! command -v pyinstaller &> /dev/null; then
    echo "❌ PyInstaller未安装，正在安装..."
    pip install pyinstaller
fi

# 创建必要的目录
mkdir -p logs
mkdir -p data

# 创建本地配置文件（如果不存在）
if [ ! -f ".env" ]; then
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
fi

# 清理之前的构建
echo "🧹 清理之前的构建文件..."
rm -rf build dist __pycache__

# 使用spec文件打包
echo "📦 开始打包..."
pyinstaller pyinstaller_config.spec

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