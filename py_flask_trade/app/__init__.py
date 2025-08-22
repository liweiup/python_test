"""
    :copyright: © 2020 by the Lin team.
    :license: MIT, see LICENSE for more details.
"""

import os

from dotenv import load_dotenv
from flask import Flask
from app.util.common import basedir


def register_blueprints(app):
    from app.api.cms import create_cms
    from app.api.v1 import create_v1

    app.register_blueprint(create_v1(), url_prefix="/v1")
    app.register_blueprint(create_cms(), url_prefix="/cms")


def register_cli(app):
    from app.cli import db_cli, plugin_cli

    app.cli.add_command(db_cli)
    app.cli.add_command(plugin_cli)

def register_redis(app):
    from app.cli.redis.client import redis_client
    from app.cli.redis.redis_sub import RedisSub
    import os
    
    try:
        # 检查是否在打包环境中
        if getattr(os, '_MEIPASS', None):
            # PyInstaller打包环境，跳过Redis启动
            app.logger.info("Running in packaged environment, skipping Redis subscription")
            return
            
        redis_client.init_app(app, health_check_interval=30)
        
        # 获取Redis订阅配置
        redis_sub_config = app.config.get("REDIS_SUB", "")
        if not redis_sub_config:
            app.logger.info("No Redis subscription configured, skipping RedisSub")
            return
            
        # 启动Redis订阅线程
        redis_sub = RedisSub(set(str.split(redis_sub_config, ",")))
        redis_sub.start()
        app.logger.info(f"Redis subscription started for channels: {redis_sub_config}")
        
    except Exception as e:
        app.logger.warning(f"Failed to initialize Redis: {e}")
        app.logger.info("Application will continue without Redis functionality")
        # 不抛出异常，让应用继续运行

def register_api(app):
    from app.api import api

    api.register(app)


def apply_cors(app):
    from flask_cors import CORS

    CORS(app)


# def init_socketio(app):
#     from app.extension.notify.socketio import socketio
#     socketio.init_app(app, cors_allowed_origins="*")

def load_app_config(app):
    """
    根据指定配置环境自动加载对应环境变量和配置类到app config
    """
    # 根据传入环境加载对应配置
    env = app.config.get("ENV", "development")
    
    # 读取 .env 文件
    env_file = os.path.join(basedir, ".{env}.env".format(env=env))
    if os.path.exists(env_file):
        load_dotenv(env_file)
    
    # 尝试加载配置类
    try:
        config_path = "app.config.{env}.{Env}Config".format(env=env, Env=env.capitalize())
        app.config.from_object(config_path)
    except ImportError:
        # 如果配置类不存在，使用基础配置
        print(f"Warning: 配置类 {config_path} 不存在，使用基础配置")
        from app.config.base import BaseConfig
        app.config.from_object(BaseConfig)


def set_global_config(**kwargs):
    from lin import global_config

    # 获取config_*参数对象并挂载到脱离上下文的global config
    for k, v in kwargs.items():
        if k.startswith("config_"):
            global_config[k[7:]] = v


def create_app(register_all=True, **kwargs):
    # 全局配置优先生效
    set_global_config(**kwargs)
    
    # 创建Flask应用
    app = Flask(__name__, static_folder=os.path.join(basedir, "assets"))
    
    # 设置默认环境
    app.config['ENV'] = 'development'
    
    # 加载配置
    load_app_config(app)
    
    # 配置日志
    setup_logging(app)
    
    if register_all:
        from lin import Lin
        register_blueprints(app)
        register_api(app)
        apply_cors(app)
        # init_socketio(app)
        Lin(app, **kwargs)
        register_cli(app)
        register_redis(app)
    return app


def setup_logging(app):
    """配置应用日志"""
    # 检查是否已经配置过日志，避免重复配置
    if hasattr(app, '_logging_configured') and app._logging_configured:
        return
    
    import logging
    from logging.handlers import RotatingFileHandler
    import os
    from datetime import datetime
    
    log_config = app.config.get("LOG", {})
    
    # 创建日志目录
    log_dir = log_config.get("DIR", "logs")
    os.makedirs(log_dir, exist_ok=True)
    
    # 设置日志级别
    log_level = getattr(logging, log_config.get("LEVEL", "DEBUG").upper(), logging.DEBUG)
    app.logger.setLevel(log_level)
    
    # 初始化日志文件路径
    log_file = "Console only"
    
    # 如果配置了文件日志且还没有文件handler
    if log_config.get("FILE", True):
        # 生成带日期的日志文件名
        timestamp = datetime.now().strftime("%Y-%m-%d")
        log_file = os.path.join(log_dir, f"{timestamp}.log")
        max_bytes = log_config.get("SIZE_LIMIT", 5 * 1024 * 1024)  # 5MB
        
        # 检查是否已有文件handler
        has_file_handler = any(
            isinstance(handler, RotatingFileHandler) 
            for handler in app.logger.handlers
        )
        
        if not has_file_handler:
            # 使用RotatingFileHandler，每天手动创建新文件
            file_handler = RotatingFileHandler(
                log_file, 
                maxBytes=max_bytes,
                backupCount=30,   # 保留30天的日志
                encoding="utf-8"
            )
            file_handler.setLevel(log_level)
            
            # 设置格式
            formatter = logging.Formatter(
                "%(asctime)s %(levelname)s %(name)s %(message)s"
            )
            file_handler.setFormatter(formatter)
            
            app.logger.addHandler(file_handler)
            app.logger.info(f"Logging configured - file: {log_file}")
    
    # 标记日志已配置，避免重复配置
    app._logging_configured = True
    
    # # 添加启动信息
    # app.logger.info("=" * 50)
    # app.logger.info("Flask application starting...")
    # app.logger.info(f"Environment: {app.config.get('ENV', 'unknown')}")
    # app.logger.info(f"Debug mode: {app.config.get('DEBUG', False)}")
    # app.logger.info(f"Log level: {log_config.get('LEVEL', 'DEBUG')}")
    # app.logger.info(f"Log file: {log_file}")
    # app.logger.info("=" * 50)
