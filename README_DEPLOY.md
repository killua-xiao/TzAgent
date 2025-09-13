# 金融AI智能投研助手 - 部署指南

## 部署方式

### 1. 传统部署（推荐）
```bash
# 给部署脚本执行权限
chmod +x deploy.sh

# 运行部署脚本
./deploy.sh
```

### 2. Docker部署
```bash
# 构建并启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

### 3. 手动部署

#### 后端部署
```bash
cd backend

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件配置API密钥

# 启动服务
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

#### 前端部署
```bash
cd frontend

# 安装依赖
npm install

# 构建生产版本
npm run build

# 启动服务（开发模式）
npm run dev
```

## 环境配置

### 必需配置
在 `backend/.env` 中配置以下API密钥：

```env
# DeepSeek API密钥
DEEPSEEK_API_KEY=your_deepseek_api_key

# 腾讯云API密钥  
TENCENT_CLOUD_API_KEY=your_tencent_api_key
TENCENT_CLOUD_API_SECRET=your_tencent_api_secret

# 其他可选API
DOUBAN_API_KEY=your_douban_api_key
TONGYI_API_KEY=your_tongyi_api_key
```

### 可选配置
- Redis连接：配置 `REDIS_URL` 启用缓存
- 数据库：默认使用SQLite，可配置其他数据库

## 服务管理

### Systemd服务管理
```bash
# 启动服务
sudo systemctl start financial-ai-agent

# 停止服务  
sudo systemctl stop financial-ai-agent

# 查看状态
sudo systemctl status financial-ai-agent

# 重启服务
sudo systemctl restart financial-ai-agent
```

### Docker服务管理
```bash
# 启动所有服务
docker-compose up -d

# 停止所有服务
docker-compose down

# 重启特定服务
docker-compose restart backend
```

## 监控和维护

### 日志查看
```bash
# 查看后端日志
journalctl -u financial-ai-agent -f

# 查看Docker日志
docker-compose logs -f backend

# 查看Nginx访问日志
tail -f /var/log/nginx/access.log
```

### 健康检查
```bash
# API健康检查
curl http://localhost:8000/health

# 前端健康检查  
curl http://localhost:3000
```

## 故障排除

### 常见问题

1. **端口冲突**：修改配置中的端口号
2. **API密钥错误**：检查 `.env` 文件配置
3. **依赖安装失败**：检查Python和Node.js版本
4. **权限问题**：确保数据目录有写入权限

### 性能优化

1. 启用Redis缓存
2. 调整UVICORN workers数量
3. 配置Nginx缓存
4. 启用Gzip压缩

## 安全建议

1. 使用HTTPS加密传输
2. 定期更新API密钥
3. 配置防火墙规则
4. 启用访问日志监控
5. 定期备份数据

## 更新部署

```bash
# 拉取最新代码
git pull

# 重启服务
sudo systemctl restart financial-ai-agent

# 或使用Docker
docker-compose up -d --build