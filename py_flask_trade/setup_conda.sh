#!/bin/bash

echo "🐍 设置Conda环境..."

# 检查conda是否安装
if ! command -v conda &> /dev/null; then
    echo "❌ Conda未安装，请先安装Miniconda或Anaconda"
    echo "📥 下载地址: https://docs.conda.io/en/latest/miniconda.html"
    exit 1
fi

# 显示conda版本
echo "📋 Conda版本:"



# 创建环境
echo "🔧 创建conda环境 'py_flask_trade'..."
conda env create -f environment.yml

# 激活环境
echo "✅ 激活环境..."
conda activate py_flask_trade

# 验证环境
echo "🧪 验证环境..."
python --version
pip list | grep -E "(flask|Lin-CMS|redis)"

echo "🎉 Conda环境设置完成！"
echo ""
echo "📝 使用说明："
echo "1. 激活环境: conda activate py_flask_trade"
echo "2. 启动应用: python starter.py"
echo "3. 退出环境: conda deactivate"
echo ""
echo "🔧 环境管理："
echo "- 查看环境: conda env list"
echo "- 删除环境: conda env remove -n py_flask_trade"
echo "- 更新环境: conda env update -f environment.yml" 