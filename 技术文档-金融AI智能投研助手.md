# 金融AI智能投研助手 - 技术文档

## 📋 项目概述

金融AI智能投研助手是一款专业的金融分析工具，集成多个人工智能大模型，提供全面的金融数据分析、图表绘制、基本面和技术面分析功能。

## 🚀 快速开始

### 环境要求
- Python 3.8+
- Node.js 16+
- npm 8+

### 后端启动
```bash
# 安装依赖
cd backend
pip install -r requirements.txt

# 启动服务
python run.py
# 或使用uvicorn
uvicorn app.main:app --reload --port 8000
```

### 前端启动
```bash
# 安装依赖
cd frontend
npm install

# 启动开发服务器
npm run dev
```

### 环境配置
复制环境变量模板文件：
```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

在 `.env` 文件中配置您的API密钥：
- `DEEPSEEK_API_KEY`: Deepseek模型API密钥
- `DOUBAN_API_KEY`: 豆包模型API密钥  
- `TONGYI_API_KEY`: 通义千问API密钥
- `TENCENT_CLOUD_SECRET_ID`: 腾讯云SecretId
- `TENCENT_CLOUD_SECRET_KEY`: 腾讯云SecretKey

## 🏗️ 系统架构

### 后端架构 (FastAPI)
```
backend/
├── app/
│   ├── api/           # API路由层
│   ├── services/      # 业务服务层
│   └── core/          # 核心配置
├── main.py           # 应用入口
└── requirements.txt   # 依赖配置
```

### 前端架构 (React + TypeScript)
```
frontend/
├── src/
│   ├── pages/        # 页面组件
│   ├── components/   # 通用组件
│   ├── services/     # API服务
│   ├── router/       # 路由配置
│   └── types/        # 类型定义
├── package.json      # 项目配置
└── vite.config.ts    # 构建配置
```

## 🔧 核心功能模块

### 1. 市场数据模块
- 实时股票行情数据获取
- 历史数据查询和分析
- 市场指数监控

### 2. AI分析模块
- 多模型集成（Deepseek、豆包、通义千问）
- 金融知识问答
- 投资建议生成

### 3. 图表分析模块  
- 技术指标图表绘制
- K线图、趋势图生成
- 基本面数据可视化

### 4. 知识库模块
- 金融知识向量存储
- 智能检索和推荐
- 行业研究报告管理

### 5. 报告生成模块
- 自动化分析报告生成
- PDF导出功能
- 报告模板管理

## 📊 API接口文档

后端服务启动后，访问 `http://localhost:8000/docs` 查看完整的API文档。

### 主要API端点：
- `GET /api/market/quote/{symbol}` - 获取股票行情
- `POST /api/analysis/fundamental` - 基本面分析
- `POST /api/analysis/technical` - 技术面分析  
- `POST /api/chat` - AI对话接口
- `GET /api/knowledge/search` - 知识检索
- `POST /api/reports/generate` - 报告生成

## 🎨 前端功能说明

### 页面结构
1. **仪表盘** - 市场概览和关键指标
2. **股票分析** - 基本面和技术面分析
3. **知识库** - 金融知识检索和学习
4. **AI对话** - 智能金融问答
5. **分析报告** - 报告生成和管理

### 组件库
使用 TDesign React 组件库，提供一致的企业级UI体验。

## 🔐 安全配置

### API密钥管理
- 所有敏感密钥通过环境变量配置
- 禁止将密钥提交到版本控制
- 使用安全的密钥存储方案

### 数据安全
- HTTPS加密通信
- 输入验证和过滤
- SQL注入防护

## 📈 性能优化

### 后端优化
- 异步IO处理
- 数据库连接池
- 请求缓存机制

### 前端优化  
- 组件懒加载
- 代码分割
- 图片资源优化

## 🐛 故障排除

### 常见问题
1. **端口占用**：修改配置文件中的端口号
2. **依赖安装失败**：使用镜像源或代理
3. **API调用失败**：检查网络连接和API密钥

### 日志查看
```bash
# 查看后端日志
tail -f backend.log

# 查看前端构建日志
npm run build --verbose
```

## 🤝 开发规范

### 代码提交
- 遵循 Conventional Commits 规范
- 提交前运行代码检查
- 编写有意义的提交信息

### 文档要求
- 所有函数和方法添加注释
- 更新API接口文档
- 维护CHANGELOG文件

## 📞 技术支持

如有技术问题，请通过以下方式联系：
- 创建GitHub Issue
- 查看在线文档
- 加入开发社区

---

*最后更新: 2024年3月15日*
*版本: v1.0.0*