from flask_socketio import SocketIO
import os

# 检测环境并设置合适的async_mode
async_mode = 'gevent'  # 默认使用gevent

# 在打包环境中强制使用gevent
if getattr(os, '_MEIPASS', None):
    # PyInstaller打包环境
    async_mode = 'gevent'
else:
    # 开发环境，尝试自动检测
    try:
        import gevent
        async_mode = 'gevent'
    except ImportError:
        try:
            import eventlet
            async_mode = 'eventlet'
        except ImportError:
            async_mode = 'threading'

socketio = SocketIO(
    async_mode=async_mode,
    cors_allowed_origins="*",
    logger=True,
    engineio_logger=True
)
