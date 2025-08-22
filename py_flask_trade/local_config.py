# 本地开发环境配置
import os

# 数据库配置
SQLALCHEMY_DATABASE_URI = 'sqlite:///./lincms_local.db'

# 安全配置
SECRET_KEY = 'local_development_secret_key_2024'

# Redis配置
REDIS_URL = "redis://:iphone5C,.@115.159.204.224:6020/2"
REDIS_SUB = "diff_buy,diff_sell,diff_cancel,diff_search"

# 环境配置
ENV = "local"
DEBUG = True
TESTING = False

# Flask配置
FLASK_APP = "starter:app"
FLASK_ENV = "local"
FLASK_DEBUG = True

# 日志配置
LOG_LEVEL = "INFO"
LOG_FILE = "./logs/local_app.log"

# 设置环境变量
for key, value in locals().items():
    if key.isupper() and not key.startswith('_'):
        os.environ[key] = str(value) 