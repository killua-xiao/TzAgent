#!/bin/bash

# 金融AI Agent启动脚本

echo "🚀 启动金融AI智能投研助手..."

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3未安装，请先安装Python3.8+"
    exit 1
fi

# 检查依赖
if [ ! -d "venv" ]; then
    echo "📦 创建Python虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
echo "📦 安装依赖包..."
pip install -r requirements.txt

# 创建数据目录
mkdir -p data/chroma uploads

# 复制环境变量示例文件
if [ ! -f ".env" ]; then
    echo "📝 创建环境配置文件..."
    cp .env.example .env
    echo "⚠️  请编辑 .env 文件配置API密钥"
fi

# 启动服务
echo "🌐 启动FastAPI服务..."
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

echo "✅ 服务已启动！访问 http://localhost:8000 查看文档"