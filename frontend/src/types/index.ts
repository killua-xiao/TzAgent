// 通用类型定义

export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  message?: string;
  error?: string;
}

export interface StockQuote {
  symbol: string;
  name: string;
  price: number;
  change: number;
  changePercent: number;
  volume: number;
  marketCap?: number;
  peRatio?: number;
  high: number;
  low: number;
  open: number;
  prevClose: number;
  timestamp: string;
}

export interface TechnicalIndicator {
  name: string;
  value: number;
  signal: 'bullish' | 'bearish' | 'neutral';
  confidence: number;
}

export interface AnalysisResult {
  symbol: string;
  analysisType: 'technical' | 'fundamental' | 'comprehensive';
  result: any;
  generatedAt: string;
  confidence: number;
}

export interface KnowledgeItem {
  id: string;
  title: string;
  content: string;
  category: string;
  source: string;
  relevance: number;
}

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
  sources?: KnowledgeItem[];
}

export interface Report {
  id: string;
  symbol: string;
  title: string;
  type: string;
  content: any;
  generatedAt: string;
  downloadUrl?: string;
}

// API请求参数类型
export interface AnalysisRequest {
  symbol: string;
  analysisType: string;
  period?: string;
  startDate?: string;
  endDate?: string;
}

export interface KnowledgeQuery {
  question: string;
  maxResults?: number;
  context?: any;
}

// 股票数据列表相关类型
export interface StockData {
  id: string;
  symbol: string;
  name: string;
  price: number;
  changePercent: number;
  marketCap: number;
  industry: string;
  updateTime: string;
}

export interface StockListResponse {
  data: StockData[];
  total: number;
  page: number;
  pageSize: number;
  totalPages: number;
}

export interface StockFilterParams {
  symbol?: string;
  name?: string;
  industry?: string;
  minPrice?: number;
  maxPrice?: number;
  startDate?: string;
  endDate?: string;
  page?: number;
  pageSize?: number;
}

export interface CreateStockRequest {
  symbol: string;
  name: string;
  price: number;
  marketCap: number;
  industry: string;
}