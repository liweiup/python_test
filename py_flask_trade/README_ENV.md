# 🐍 Python环境设置指南

## 📋 环境要求

- Python 3.8+
- Conda 或 pip
- macOS/Linux/Windows

## 🚀 快速开始

### 方案1: Conda环境 (推荐)

```bash
# 设置conda环境
chmod +x setup_conda.sh
./setup_conda.sh

# 启动应用
chmod +x start_conda.sh
./start_conda.sh
```

### 方案2: pip虚拟环境

```bash
# 设置虚拟环境
chmod +x setup_pip.sh
./setup_pip.sh

# 启动应用
source venv/bin/activate
python starter.py
```

## 📁 文件说明

- `environment.yml` - Conda环境配置
- `requirements.txt` - pip依赖列表
- `setup_conda.sh` - Conda环境设置脚本
- `setup_pip.sh` - pip虚拟环境设置脚本
- `start_conda.sh` - Conda环境启动脚本

## 🔧 手动设置

### Conda环境

```bash
# 创建环境
conda env create -f environment.yml

# 激活环境
conda activate py_flask_trade

# 启动应用
python starter.py
```

### pip虚拟环境

```bash
# 创建虚拟环境
python3 -m venv venv

# 激活环境
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt

# 启动应用
python starter.py
```

## 🌐 访问地址

- 应用主页: http://127.0.0.1:5000
- API文档: http://127.0.0.1:5000/apidoc/swagger

## 🗄️ 数据库配置

本地环境使用SQLite数据库：
- 文件: `lincms_local.db`
- 自动创建在项目根目录

## ⚠️ 注意事项

1. **Conda环境**: 确保已安装Miniconda或Anaconda
2. **虚拟环境**: 每次使用前需要激活环境
3. **Redis**: 本地开发需要Redis服务
4. **权限**: 脚本需要执行权限 (`chmod +x *.sh`)

## 🐛 常见问题

### Conda命令未找到
```bash
# 初始化conda
conda init zsh  # 或 bash
# 重启终端
```

### 依赖安装失败
```bash
# 更新conda
conda update conda

# 或使用pip
pip install -r requirements.txt --force-reinstall
```

### 环境激活失败
```bash
# 检查环境列表
conda env list

# 重新创建环境
conda env remove -n py_flask_trade
conda env create -f environment.yml
```

## 🔄 环境管理

### Conda
```bash
# 查看环境
conda env list

# 更新环境
conda env update -f environment.yml

# 删除环境
conda env remove -n py_flask_trade
```

### pip虚拟环境
```bash
# 删除环境
rm -rf venv

# 重新创建
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 📞 技术支持

如遇问题，请检查：
1. Python版本是否为3.8+
2. 环境是否正确激活
3. 依赖是否完整安装
4. 网络连接是否正常 