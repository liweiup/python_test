# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['starter.py'],
    pathex=[],
    binaries=[],
    datas=[('app', 'app'), ('local_config.py', '.'), ('lincms.db', '.')],
    hiddenimports=['flask', 'flask_cors', 'flask_socketio', 'flask_sqlalchemy', 'flask_redis', 'redis', 'gevent', 'gevent.websocket', 'pydantic', 'spectree', 'lin', 'lin.apidoc', 'lin.cms', 'sqlalchemy', 'sqlalchemy.orm', 'sqlalchemy.sql', 'sqlalchemy.ext.declarative', 'sqlalchemy.pool', 'sqlalchemy.engine', 'sqlalchemy.event', 'sqlalchemy.dialects.sqlite', 'sqlalchemy.dialects.mysql', 'sqlalchemy.dialects.postgresql'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='flask_cms_app',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
