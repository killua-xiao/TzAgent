import axios from 'axios';
import { 
  ApiResponse, 
  StockQuote, 
  AnalysisResult, 
  KnowledgeItem,
  AnalysisRequest,
  KnowledgeQuery
} from '../types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8001';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    return response.data;
  },
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// 市场数据API
export const marketApi = {
  // 获取股票行情
  getStockQuote: (symbol: string): Promise<ApiResponse<StockQuote>> =>
    api.get(`/api/v1/market/quotes/${symbol}`),

  // 获取市场指数
  getMarketIndices: (): Promise<ApiResponse<StockQuote[]>> =>
    api.get('/api/v1/market/indices'),

  // 获取历史数据
  getHistoricalData: (symbol: string, startDate: string, endDate: string, interval: string = '1d') =>
    api.post('/api/v1/market/historical', { symbol, startDate, endDate, interval }),

  // 获取行业板块
  getSectors: (): Promise<ApiResponse<any[]>> =>
    api.get('/api/v1/market/sectors'),

  // 获取市场新闻
  getMarketNews: (): Promise<ApiResponse<any[]>> =>
    api.get('/api/v1/market/news'),
};

// 分析服务API
export const analysisApi = {
  // 技术分析
  technicalAnalysis: (request: AnalysisRequest): Promise<ApiResponse<AnalysisResult>> =>
    api.post('/api/v1/analysis/technical', request),

  // 基本面分析
  fundamentalAnalysis: (request: AnalysisRequest): Promise<ApiResponse<AnalysisResult>> =>
    api.post('/api/v1/analysis/fundamental', request),

  // 综合分析
  comprehensiveAnalysis: (request: AnalysisRequest): Promise<ApiResponse<AnalysisResult>> =>
    api.post('/api/v1/analysis/comprehensive', request),

  // 获取技术指标
  getTechnicalIndicators: (symbol: string, period: string = '1y'): Promise<ApiResponse<any>> =>
    api.get(`/api/v1/analysis/indicators/${symbol}?period=${period}`),

  // 股票筛选
  stockScreener: (params: any): Promise<ApiResponse<any[]>> =>
    api.get('/api/v1/analysis/screener', { params }),
};

// 知识库API
export const knowledgeApi = {
  // 查询知识
  searchKnowledge: (query: KnowledgeQuery): Promise<ApiResponse<KnowledgeItem[]>> =>
    api.post('/api/v1/knowledge/query', query),

  // 获取分类
  getCategories: (): Promise<ApiResponse<string[]>> =>
    api.get('/api/v1/knowledge/categories'),

  // 获取知识条目
  getKnowledgeItem: (id: string): Promise<ApiResponse<KnowledgeItem>> =>
    api.get(`/api/v1/knowledge/item/${id}`),

  // 获取相关股票知识
  getRelatedKnowledge: (symbol: string): Promise<ApiResponse<KnowledgeItem[]>> =>
    api.get(`/api/v1/knowledge/related/${symbol}`),
};

// 聊天API
export const chatApi = {
  // 发送消息
  sendMessage: (message: string, sessionId?: string, context?: any): Promise<ApiResponse<any>> =>
    api.post('/api/v1/chat/message', { message, sessionId, context }),

  // 获取聊天历史
  getChatHistory: (sessionId: string): Promise<ApiResponse<any>> =>
    api.get(`/api/v1/chat/sessions/${sessionId}`),

  // 清空聊天历史
  clearChatHistory: (sessionId: string): Promise<ApiResponse<void>> =>
    api.delete(`/api/v1/chat/sessions/${sessionId}`),
};

// 报告API
export const reportApi = {
  // 生成报告
  generateReport: (request: any): Promise<ApiResponse<any>> =>
    api.post('/api/v1/reports/generate', request),

  // 获取报告列表
  listReports: (symbol?: string, reportType?: string, limit: number = 10, offset: number = 0): Promise<ApiResponse<any[]>> =>
    api.get('/api/v1/reports/list', { params: { symbol, reportType, limit, offset } }),

  // 获取报告详情
  getReport: (id: string): Promise<ApiResponse<any>> =>
    api.get(`/api/v1/reports/${id}`),

  // 删除报告
  deleteReport: (id: string): Promise<ApiResponse<void>> =>
    api.delete(`/api/v1/reports/${id}`),

  // 导出报告
  exportReport: (id: string, format: string = 'pdf'): Promise<ApiResponse<{ exportUrl: string }>> =>
    api.post(`/api/v1/reports/${id}/export`, { format }),

  // 获取报告模板
  getTemplates: (): Promise<ApiResponse<any[]>> =>
    api.get('/api/v1/reports/templates'),
};

// 股票数据API
export const stockApi = {
  // 获取股票列表
  getStocks: (params: StockFilterParams): Promise<ApiResponse<StockListResponse>> =>
    api.get('/api/v1/stocks', { params }),

  // 创建股票数据
  createStock: (data: CreateStockRequest): Promise<ApiResponse<StockData>> =>
    api.post('/api/v1/stocks', data),

  // 更新股票数据
  updateStock: (id: string, data: Partial<CreateStockRequest>): Promise<ApiResponse<StockData>> =>
    api.put(`/api/v1/stocks/${id}`, data),

  // 删除股票数据
  deleteStock: (id: string): Promise<ApiResponse<void>> =>
    api.delete(`/api/v1/stocks/${id}`),

  // 批量获取股票数据
  batchGetStocks: (symbols: string[]): Promise<ApiResponse<StockData[]>> =>
    api.post('/api/v1/stocks/batch', { symbols }),
};

// 导出常用函数别名
export const fetchStocks = stockApi.getStocks;
export const createStock = stockApi.createStock;
export const updateStock = stockApi.updateStock;
export const deleteStock = stockApi.deleteStock;

export default api;