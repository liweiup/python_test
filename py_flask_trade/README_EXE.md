# 🚀 Flask应用打包为exe指南

## 📋 打包工具

- **PyInstaller** - 最成熟的Python打包工具
- **支持平台**: Windows, macOS, Linux
- **输出格式**: 单文件exe/可执行文件

## 🛠️ 打包方法

### 方法1：使用配置文件（推荐）

```bash
# 使用spec配置文件打包
pyinstaller pyinstaller_config.spec
```

### 方法2：使用简化脚本

```bash
# 使用简化打包脚本
./build_simple.sh
```

### 方法3：使用完整脚本

```bash
# 使用完整打包脚本
./build_exe.sh
```

### 方法4：Windows批处理

```cmd
# Windows用户双击运行
build_exe.bat
```

## 📁 打包文件说明

- `pyinstaller_config.spec` - PyInstaller配置文件
- `build_exe.sh` - Linux/macOS打包脚本
- `build_exe.bat` - Windows打包脚本
- `build_simple.sh` - 简化打包脚本

## 🔧 手动打包命令

### 基本命令
```bash
pyinstaller --onefile --add-data "app:app" starter.py
```

### 完整命令
```bash
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
    --hidden-import sqlalchemy \
    --name flask_cms_app \
    starter.py
```

## 📦 打包内容

### 包含的文件
- `starter.py` - 主程序入口
- `app/` - 应用代码目录
- `local_config.py` - 配置文件
- `lincms.db` - 数据库文件（如果存在）

### 包含的依赖
- Flask及其扩展
- SQLAlchemy数据库ORM
- Redis客户端
- Gevent异步库
- Lin-CMS框架
- 所有必要的Python包

## 🎯 打包选项

### 单文件模式
```bash
--onefile  # 打包成单个可执行文件
```

### 目录模式
```bash
--onedir   # 打包成目录（包含多个文件）
```

### 隐藏导入
```bash
--hidden-import package_name  # 强制包含特定包
```

### 数据文件
```bash
--add-data "source:destination"  # 添加数据文件
```

## 🚀 运行打包后的程序

### Linux/macOS
```bash
cd dist
./flask_cms_app
```

### Windows
```cmd
cd dist
flask_cms_app.exe
```

### 访问地址
- 应用主页: http://127.0.0.1:5000
- API文档: http://127.0.0.1:5000/apidoc/swagger

## ⚠️ 注意事项

1. **文件大小**: 单文件模式会产生较大的可执行文件
2. **启动时间**: 首次启动可能需要较长时间
3. **依赖管理**: 确保所有依赖都已正确安装
4. **平台兼容**: 在目标平台上打包以获得最佳兼容性

## 🐛 常见问题

### 导入错误
```bash
# 添加缺失的隐藏导入
--hidden-import missing_package
```

### 文件缺失
```bash
# 添加缺失的数据文件
--add-data "missing_file:destination"
```

### 权限问题
```bash
# 给脚本添加执行权限
chmod +x *.sh
```

## 🔄 更新打包

### 重新打包
```bash
# 清理之前的构建
rm -rf build dist __pycache__

# 重新打包
pyinstaller pyinstaller_config.spec
```

### 增量更新
```bash
# 只更新变化的文件
pyinstaller --clean pyinstaller_config.spec
```

## 📊 打包优化

### 减小文件大小
```bash
--exclude-module unnecessary_module
--strip  # 移除调试信息
```

### 提高启动速度
```bash
--onedir  # 使用目录模式
--runtime-tmpdir /tmp  # 指定临时目录
```

## 📞 技术支持

如遇打包问题，请检查：
1. PyInstaller版本是否最新
2. 所有依赖是否正确安装
3. 配置文件路径是否正确
4. 目标平台是否支持 