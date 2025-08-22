from flask_socketio import SocketIO

socketio = SocketIO(
    async_mode='threading',
    cors_allowed_origins="*",
    logger=True,
    engineio_logger=True
)