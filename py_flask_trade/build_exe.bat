@echo off
echo 🚀 开始打包Flask应用为exe...

REM 检查环境
python -c "import pyinstaller" 2>nul
if errorlevel 1 (
    echo ❌ PyInstaller未安装，正在安装...
    pip install pyinstaller
)

REM 创建必要的目录
if not exist "logs" mkdir logs
if not exist "data" mkdir data

REM 创建本地配置文件（如果不存在）
if not exist ".env" (
    echo ⚙️ 创建本地环境配置...
    (
        echo SQLALCHEMY_DATABASE_URI = 'sqlite:///./lincms_local.db'
        echo SECRET_KEY = 'local_development_secret_key_2024'
        echo REDIS_URL = "redis://localhost:6379/0"
        echo REDIS_SUB = "diff_buy,diff_sell,diff_cancel,diff_search"
        echo ENV = "local"
        echo DEBUG = True
        echo FLASK_APP = "starter:app"
        echo FLASK_ENV = "local"
        echo FLASK_DEBUG = True
    ) > .env
)

REM 清理之前的构建
echo 🧹 清理之前的构建文件...
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist
if exist "__pycache__" rmdir /s /q __pycache__

REM 使用spec文件打包
echo 📦 开始打包...
pyinstaller pyinstaller_config.spec

REM 检查打包结果
if exist "dist\flask_cms_app.exe" (
    echo ✅ 打包成功！
    echo 📍 可执行文件位置: dist\flask_cms_app.exe
    echo.
    echo 🔧 使用方法：
    echo 1. 进入dist目录: cd dist
    echo 2. 运行程序: flask_cms_app.exe
    echo 3. 访问地址: http://127.0.0.1:5000
) else (
    echo ❌ 打包失败，请检查错误信息
    pause
    exit /b 1
)

pause 