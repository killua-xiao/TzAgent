# 金融AI智能投研助手

基于大模型的金融数据分析与投研平台，集成多模型API和腾讯云金融数据服务。

## 🚀 功能特性

- **多模型金融知识问答** - 集成Deepseek、豆包、通义千问等大模型
- **实时市场数据搜索** - 腾讯云金融数据API实时行情
- **专业金融图表绘制** - Plotly + ECharts专业可视化
- **基本面技术面深度分析** - 专业金融分析算法
- **AI投资建议生成** - 智能投研报告生成

## 🛠️ 技术栈

### 后端
- **FastAPI** - 高性能异步Web框架
- **Pandas + NumPy** - 金融数据处理
- **Plotly + Matplotlib** - 金融图表绘制
- **ChromaDB** - 向量知识库存储
- **腾讯云金融API** - 实时市场数据

### 前端
- **React 18 + TypeScript** - 现代化前端框架
- **TDesign Enterprise** - 企业级UI组件库
- **ECharts** - 专业金融图表
- **Tailwind CSS** - 原子化CSS框架

## 📦 安装部署

### 后端安装

1. 克隆项目
```bash
git clone <repository-url>
cd TzAgent/backend
```

2. 创建虚拟环境
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

4. 配置环境变量
```bash
cp .env.example .env
# 编辑 .env 文件，配置API密钥等参数
```

5. 启动服务
```bash
python run.py
```

### 前端安装

1. 进入前端目录
```bash
cd ../frontend
```

2. 安装依赖
```bash
npm install
```

3. 启动开发服务器
```bash
npm run dev
```

## 🔧 配置说明

### 必需配置
- `TENCENT_CLOUD_API_KEY` - 腾讯云API密钥
- `TENCENT_CLOUD_API_SECRET` - 腾讯云API密钥

### 可选配置
- `DEEPSEEK_API_KEY` - Deepseek模型API密钥
- `DOUBAN_API_KEY` - 豆包模型API密钥  
- `TONGYI_API_KEY` - 通义千问模型API密钥
- `REDIS_URL` - Redis连接URL（用于缓存）

## 📊 API接口

### 市场数据
- `GET /api/v1/market/quotes/{symbol}` - 获取股票行情
- `GET /api/v1/market/indices` - 获取市场指数
- `POST /api/v1/market/historical` - 获取历史数据
- `GET /api/v1/market/sectors` - 获取行业板块
- `GET /api/v1/market/news` - 获取市场新闻

### 分析服务
- `POST /api/v1/analysis/technical` - 技术分析
- `POST /api/v1/analysis/fundamental` - 基本面分析  
- `POST /api/v1/analysis/comprehensive` - 综合分析
- `GET /api/v1/analysis/indicators/{symbol}` - 技术指标
- `GET /api/v1/analysis/screener` - 股票筛选

### 知识库
- `POST /api/v1/knowledge/query` - 知识查询
- `GET /api/v1/knowledge/categories` - 获取分类
- `GET /api/v1/knowledge/item/{id}` - 获取知识条目
- `GET /api/v1/knowledge/related/{symbol}` - 相关股票知识

### 聊天服务
- `POST /api/v1/chat/message` - 发送消息
- `GET /api/v1/chat/sessions/{sessionId}` - 聊天历史
- `DELETE /api/v1/chat/sessions/{sessionId}` - 清空历史

### 报告服务
- `POST /api/v1/reports/generate` - 生成报告
- `GET /api/v1/reports/list` - 报告列表
- `GET /api/v1/reports/{id}` - 报告详情
- `DELETE /api/v1/reports/{id}` - 删除报告
- `POST /api/v1/reports/{id}/export` - 导出报告
- `GET /api/v1/reports/templates` - 报告模板

## 🎯 使用示例

### 获取股票行情
```bash
curl "http://localhost:8000/api/v1/market/quotes/000001.SZ"
```

### 技术分析
```bash
curl -X POST "http://localhost:8000/api/v1/analysis/technical" \
  -H "Content-Type: application/json" \
  -d '{"symbol": "000001.SZ", "analysisType": "technical", "period": "1y"}'
```

### 知识查询
```bash
curl -X POST "http://localhost:8000/api/v1/knowledge/query" \
  -H "Content-Type: application/json" \
  -d '{"question": "什么是市盈率？", "maxResults": 5}'
```

## 📈 项目结构

```
TzAgent/
├── backend/                 # 后端服务
│   ├── app/                # 应用核心
│   │   ├── api/           # API路由
│   │   ├── core/          # 核心配置
│   │   ├── models/        # 数据模型
│   │   ├── services/      # 业务服务
│   │   └── utils/         # 工具函数
│   ├── data/              # 数据存储
│   ├── knowledge_base/    # 知识库文件
│   ├── uploads/           # 文件上传
│   ├── reports/           # 生成报告
│   ├── requirements.txt   # Python依赖
│   └── run.py             # 启动脚本
├── frontend/               # 前端应用
│   ├── src/               # 源代码
│   │   ├── components/    # 公共组件
│   │   ├── pages/         # 页面组件
│   │   ├── services/      # API服务
│   │   ├── types/         # TypeScript类型
│   │   └── utils/         # 工具函数
│   ├── public/            # 静态资源
│   ├── package.json       # 项目配置
│   └── vite.config.ts     # 构建配置
└── README.md              # 项目说明
```

## 🤝 开发贡献

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🆘 技术支持

如有问题或建议，请提交 Issue 或联系开发团队。

---
**金融AI智能投研助手** - 让投资更智能 📈