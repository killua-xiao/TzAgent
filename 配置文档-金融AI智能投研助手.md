# 金融AI智能投研助手 - 配置文档

## 📋 配置概述

本文档详细说明金融AI智能投研助手的所有配置参数，包括参数名称、类型、默认值、可选值范围、配置示例、注意事项以及配置效果说明。

## 🏗️ 配置结构

### 后端配置 (backend/.env)
### 前端配置 (frontend/.env)
### 可选服务配置

---

## 🔧 后端配置参数

### 1. 应用基础配置

#### DEBUG
- **类型**: 布尔值
- **默认值**: true
- **可选值**: true, false
- **配置示例**: `DEBUG=true`
- **必填项**: 否
- **说明**: 启用调试模式，输出详细日志信息
- **注意事项**: 生产环境请设置为 false
- **配置效果**: 启用后会在控制台输出详细的请求和错误信息

#### PORT
- **类型**: 整数
- **默认值**: 8000
- **可选值**: 1024-65535
- **配置示例**: `PORT=8000`
- **必填项**: 否
- **说明**: 后端服务监听的端口号
- **注意事项**: 确保端口未被其他应用占用
- **配置效果**: 修改后端API服务的访问端口

### 2. 数据库配置

#### DATABASE_URL
- **类型**: 字符串
- **默认值**: sqlite:///./app.db
- **可选值**: SQLite/PostgreSQL/MySQL连接字符串
- **配置示例**: 
  - SQLite: `sqlite:///./app.db`
  - PostgreSQL: `postgresql://user:password@localhost:5432/dbname`
  - MySQL: `mysql://user:password@localhost:3306/dbname`
- **必填项**: 是
- **说明**: 数据库连接字符串
- **注意事项**: 生产环境建议使用PostgreSQL或MySQL
- **配置效果**: 指定应用数据存储的数据库类型和位置

### 3. AI模型API密钥配置

#### DEEPSEEK_API_KEY
- **类型**: 字符串
- **默认值**: 无
- **可选值**: 有效的Deepseek API密钥
- **配置示例**: `DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
- **必填项**: 是（如使用Deepseek模型）
- **说明**: Deepseek大模型API访问密钥
- **注意事项**: 从Deepseek官方平台获取，妥善保管
- **配置效果**: 启用Deepseek模型的金融分析和对话功能

#### DOUBAN_API_KEY
- **类型**: 字符串
- **默认值**: 无
- **可选值**: 有效的豆包API密钥
- **配置示例**: `DOUBAN_API_KEY=db-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
- **必填项**: 是（如使用豆包模型）
- **说明**: 豆包大模型API访问密钥
- **配置效果**: 启用豆包模型的金融知识问答功能

#### TONGYI_API_KEY
- **类型**: 字符串
- **默认值**: 无
- **可选值**: 有效的通义千问API密钥
- **配置示例**: `TONGYI_API_KEY=qw-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
- **必填项**: 是（如使用通义千问模型）
- **说明**: 通义千问大模型API访问密钥
- **配置效果**: 启用通义千问模型的投研分析功能

### 4. 腾讯云配置

#### TENCENT_CLOUD_API_KEY
- **类型**: 字符串
- **默认值**: 无
- **可选值**: 有效的腾讯云API密钥ID
- **配置示例**: `TENCENT_CLOUD_API_KEY=AKIDxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
- **必填项**: 是（如使用腾讯云服务）
- **说明**: 腾讯云API密钥ID
- **注意事项**: 从腾讯云控制台获取，具有相应权限
- **配置效果**: 启用腾讯云相关的数据服务和存储功能

#### TENCENT_CLOUD_API_SECRET
- **类型**: 字符串
- **默认值**: 无
- **可选值**: 有效的腾讯云API密钥
- **配置示例**: `TENCENT_CLOUD_API_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
- **必填项**: 是（如使用腾讯云服务）
- **说明**: 腾讯云API密钥
- **注意事项**: 高度敏感信息，务必妥善保管
- **配置效果**: 用于腾讯云服务的身份验证和API调用

### 5. Redis配置（可选）

#### REDIS_URL
- **类型**: 字符串
- **默认值**: redis://localhost:6379/0
- **可选值**: 有效的Redis连接字符串
- **配置示例**: `REDIS_URL=redis://:password@host:port/db`
- **必填项**: 否
- **说明**: Redis缓存服务器连接字符串
- **注意事项**: 用于会话缓存和请求缓存，提升性能
- **配置效果**: 启用Redis缓存，提高应用响应速度

### 6. 文件存储配置

#### UPLOAD_DIR
- **类型**: 字符串
- **默认值**: ./uploads
- **可选值**: 有效的目录路径
- **配置示例**: `UPLOAD_DIR=./uploads`
- **必填项**: 否
- **说明**: 文件上传存储目录
- **注意事项**: 确保目录有写入权限
- **配置效果**: 指定用户上传文件的存储位置

#### REPORT_DIR
- **类型**: 字符串
- **默认值**: ./reports
- **可选值**: 有效的目录路径
- **配置示例**: `REPORT_DIR=./reports`
- **必填项**: 否
- **说明**: 分析报告存储目录
- **配置效果**: 指定生成的分析报告文件存储位置

### 7. 知识库配置

#### KNOWLEDGE_BASE_DIR
- **类型**: 字符串
- **默认值**: ./knowledge_base
- **可选值**: 有效的目录路径
- **配置示例**: `KNOWLEDGE_BASE_DIR=./knowledge_base`
- **必填项**: 否
- **说明**: 金融知识库文档存储目录
- **配置效果**: 指定本地知识库文档的存储位置

#### CHROMA_DB_PATH
- **类型**: 字符串
- **默认值**: ./data/chroma_db
- **可选值**: 有效的目录路径
- **配置示例**: `CHROMA_DB_PATH=./data/chroma_db`
- **必填项**: 否
- **说明**: ChromaDB向量数据库存储路径
- **配置效果**: 指定向量数据库的持久化存储位置

---

## 🎨 前端配置参数

### VITE_API_BASE_URL
- **类型**: 字符串
- **默认值**: http://localhost:8000
- **可选值**: 有效的URL地址
- **配置示例**: `VITE_API_BASE_URL=http://localhost:8000`
- **必填项**: 是
- **说明**: 后端API服务的基础URL
- **注意事项**: 确保与后端服务端口一致
- **配置效果**: 前端调用后端API的基准地址

### VITE_APP_TITLE
- **类型**: 字符串
- **默认值**: 金融AI智能投研助手
- **可选值**: 任意字符串
- **配置示例**: `VITE_APP_TITLE=金融AI智能投研助手`
- **必填项**: 否
- **说明**: 应用标题，显示在浏览器标签页
- **配置效果**: 修改浏览器中显示的应用标题

### VITE_APP_DESCRIPTION
- **类型**: 字符串
- **默认值**: 基于大模型的金融数据分析与投研平台
- **可选值**: 任意字符串
- **配置示例**: `VITE_APP_DESCRIPTION=基于大模型的金融数据分析与投研平台`
- **必填项**: 否
- **说明**: 应用描述，用于SEO和元数据
- **配置效果**: 设置应用的meta描述信息

---

## ⚙️ 可选服务配置

### 邮件服务配置（如需报告邮件发送）

#### SMTP_HOST
- **类型**: 字符串
- **默认值**: 无
- **可选值**: 有效的SMTP服务器地址
- **配置示例**: `SMTP_HOST=smtp.gmail.com`
- **必填项**: 否
- **说明**: SMTP邮件服务器地址

#### SMTP_PORT
- **类型**: 整数
- **默认值**: 587
- **可选值**: 25, 465, 587等
- **配置示例**: `SMTP_PORT=587`
- **必填项**: 否
- **说明**: SMTP邮件服务器端口

#### SMTP_USER
- **类型**: 字符串
- **默认值**: 无
- **可选值**: 有效的邮箱地址
- **配置示例**: `SMTP_USER=your_email@gmail.com`
- **必填项**: 否
- **说明**: SMTP认证用户名

#### SMTP_PASSWORD
- **类型**: 字符串
- **默认值**: 无
- **可选值**: 有效的邮箱密码或应用专用密码
- **配置示例**: `SMTP_PASSWORD=your_app_password`
- **必填项**: 否
- **说明**: SMTP认证密码

---

## 🔍 配置验证方法

### 后端配置验证
```bash
# 检查环境变量是否设置正确
cd backend
python -c "
import os
required_vars = ['DEEPSEEK_API_KEY', 'TENCENT_CLOUD_API_KEY']
for var in required_vars:
    if not os.getenv(var):
        print(f'警告: {var} 未设置')
    else:
        print(f'✓ {var} 已设置')
"

# 测试数据库连接
python -c "
from app.core.database import engine
try:
    with engine.connect():
        print('✓ 数据库连接成功')
except Exception as e:
    print(f'数据库连接失败: {e}')
"
```

### 前端配置验证
```bash
# 检查环境变量
cd frontend
npm run build
# 如果构建成功，说明配置正确
```

### API密钥验证
```bash
# 测试Deepseek API连接
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "测试连接"}'
```

---

## 🚨 常见问题解决方案

### 1. API密钥无效
**症状**: API调用返回401错误
**解决方案**: 
- 检查API密钥是否正确复制
- 确认API密钥是否有足够的权限
- 检查API服务商账户余额或配额

### 2. 端口冲突
**症状**: 服务启动失败，提示端口被占用
**解决方案**:
- 修改PORT环境变量为其他端口
- 或者终止占用端口的进程

### 3. 数据库连接失败
**症状**: 应用启动时报数据库连接错误
**解决方案**:
- 检查DATABASE_URL格式是否正确
- 确认数据库服务是否正常运行
- 检查数据库用户权限

### 4. 文件权限问题
**症状**: 文件上传或报告生成失败
**解决方案**:
- 检查UPLOAD_DIR和REPORT_DIR目录权限
- 确保应用有写入权限

### 5. 跨域问题
**症状**: 前端无法访问后端API
**解决方案**:
- 检查VITE_API_BASE_URL是否配置正确
- 确认后端CORS配置允许前端域名

---

## 📊 配置示例

### 开发环境配置示例 (backend/.env)
```env
# 应用配置
DEBUG=true
PORT=8000

# 数据库配置
DATABASE_URL=sqlite:///./app.db

# API密钥配置
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
DOUBAN_API_KEY=db-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TONGYI_API_KEY=qw-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# 腾讯云配置
TENCENT_CLOUD_API_KEY=AKIDxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TENCENT_CLOUD_API_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# 文件存储配置
UPLOAD_DIR=./uploads
REPORT_DIR=./reports

# 知识库配置
KNOWLEDGE_BASE_DIR=./knowledge_base
CHROMA_DB_PATH=./data/chroma_db
```

### 生产环境配置示例 (backend/.env)
```env
# 应用配置
DEBUG=false
PORT=8000

# 数据库配置
DATABASE_URL=postgresql://user:password@localhost:5432/finance_ai

# API密钥配置
DEEPSEEK_API_KEY=sk-prod-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# 腾讯云配置
TENCENT_CLOUD_API_KEY=AKIDPRODxxxxxxxxxxxxxxxxxxxxxxxx
TENCENT_CLOUD_API_SECRET=prodxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Redis配置
REDIS_URL=redis://:password@redis-server:6379/0

# 文件存储配置
UPLOAD_DIR=/data/uploads
REPORT_DIR=/data/reports

# 知识库配置
KNOWLEDGE_BASE_DIR=/data/knowledge_base
CHROMA_DB_PATH=/data/chroma_db
```

### 前端配置示例 (frontend/.env)
```env
VITE_API_BASE_URL=https://api.yourdomain.com
VITE_APP_TITLE=金融AI智能投研助手
VITE_APP_DESCRIPTION=专业的金融数据分析平台
```

---

## 🔐 安全最佳实践

1. **密钥管理**: 永远不要将API密钥提交到版本控制系统
2. **环境隔离**: 为开发、测试、生产环境使用不同的密钥
3. **权限最小化**: 为API密钥分配最小必要权限
4. **定期轮换**: 定期更换API密钥，特别是发现安全事件时
5. **监控告警**: 设置API使用监控和异常告警

---

*最后更新: 2024年3月15日*
*版本: v1.0.0*