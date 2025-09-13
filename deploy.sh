#!/bin/bash

# 金融AI智能投研助手部署脚本
set -e

echo "🚀 开始部署金融AI智能投研助手..."

# 检查系统
if [ -f /etc/redhat-release ]; then
    OS="centos"
elif [ -f /etc/lsb-release ]; then
    OS="ubuntu"
else
    echo "❌ 不支持的操作系统"
    exit 1
fi

# 安装系统依赖
echo "📦 安装系统依赖..."
if [ "$OS" = "ubuntu" ]; then
    sudo apt update
    sudo apt install -y python3 python3-pip python3-venv nodejs npm nginx redis-server
elif [ "$OS" = "centos" ]; then
    sudo yum install -y python3 python3-pip nodejs npm nginx redis
    sudo systemctl enable redis
    sudo systemctl start redis
fi

# 创建项目目录
echo "📁 创建项目目录..."
sudo mkdir -p /opt/financial-ai-agent
sudo chown $USER:$USER /opt/financial-ai-agent
cd /opt/financial-ai-agent

# 复制项目文件
echo "📋 复制项目文件..."
# 假设项目文件已经在当前目录，或者从git克隆
# git clone <your-repo> .

# 部署后端
echo "🐍 部署后端服务..."
cd backend

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装Python依赖
pip install -r requirements.txt

# 创建数据目录
mkdir -p data/chroma_persist uploads reports

# 配置环境变量
if [ ! -f .env ]; then
    cp .env.example .env
    echo "⚠️  请编辑 .env 文件配置API密钥"
fi

# 部署前端
echo "⚛️  部署前端..."
cd ../frontend
npm install
npm run build

# 创建生产环境配置文件
echo "⚙️  创建生产配置..."
cat > /etc/systemd/system/financial-ai-agent.service << EOF
[Unit]
Description=Financial AI Agent Backend
After=network.target

[Service]
User=$USER
Group=$USER
WorkingDirectory=/opt/financial-ai-agent/backend
Environment=PYTHONPATH=/opt/financial-ai-agent/backend
ExecStart=/opt/financial-ai-agent/backend/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# 配置Nginx
echo "🌐 配置Nginx..."
sudo tee /etc/nginx/sites-available/financial-ai-agent > /dev/null << EOF
server {
    listen 80;
    server_name your-domain.com;  # 替换为您的域名

    # 前端静态文件
    location / {
        root /opt/financial-ai-agent/frontend/dist;
        index index.html;
        try_files \$uri \$uri/ /index.html;
    }

    # API反向代理
    location /api {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    # 静态文件服务
    location /static {
        alias /opt/financial-ai-agent/backend/static;
    }

    # 文件上传
    location /uploads {
        alias /opt/financial-ai-agent/backend/uploads;
    }
}
EOF

# 启用站点
sudo ln -sf /etc/nginx/sites-available/financial-ai-agent /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# 启动后端服务
echo "🔧 启动后端服务..."
sudo systemctl daemon-reload
sudo systemctl enable financial-ai-agent
sudo systemctl start financial-ai-agent

echo "✅ 部署完成！"
echo "🌐 访问地址: http://your-domain.com"
echo "📊 API文档: http://your-domain.com/docs"
echo "⚡ 服务状态: sudo systemctl status financial-ai-agent"