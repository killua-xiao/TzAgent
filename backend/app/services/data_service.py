import pandas as pd
import numpy as np
import yfinance as yf
import requests
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import redis
import asyncio
from app.core.config import settings
from app.services.tencent_cloud_service import TencentCloudService

class DataService:
    _redis_client = None
    
    @classmethod
    def initialize(cls):
        """初始化数据服务"""
        if settings.REDIS_URL:
            cls._redis_client = redis.from_url(settings.REDIS_URL)
            print("✅ Redis连接已初始化")
    
    @classmethod
    def get_redis(cls):
        """获取Redis客户端"""
        return cls._redis_client
    
    @classmethod
    async def get_stock_data(cls, symbol: str, period: str = "1mo") -> pd.DataFrame:
        """获取股票数据"""
        cache_key = f"stock:{symbol}:{period}"
        
        # 检查缓存
        if cls._redis_client:
            cached_data = cls._redis_client.get(cache_key)
            if cached_data:
                return pd.read_json(cached_data)
        
        # 从API获取数据
        try:
            stock = yf.Ticker(symbol)
            hist = stock.history(period=period)
            
            # 缓存数据
            if cls._redis_client and not hist.empty:
                cls._redis_client.setex(cache_key, 3600, hist.to_json())  # 缓存1小时
            
            return hist
        except Exception as e:
            print(f"获取股票数据失败: {e}")
            return pd.DataFrame()
    
    @classmethod
    async def get_real_time_quote(cls, symbol: str) -> Dict[str, Any]:
        """获取实时行情 - 集成腾讯云金融数据API"""
        try:
            # 使用腾讯云API获取实时行情
            quote_data = await tencent_cloud_service.get_stock_quote(symbol)
            
            return {
                "symbol": quote_data.get("Symbol", symbol),
                "name": quote_data.get("Name", f"{symbol}公司"),
                "price": quote_data.get("Close", 0.0),
                "change": quote_data.get("Change", 0.0),
                "change_percent": quote_data.get("ChangePercent", 0.0),
                "volume": quote_data.get("Volume", 0),
                "open": quote_data.get("Open", 0.0),
                "high": quote_data.get("High", 0.0),
                "low": quote_data.get("Low", 0.0),
                "prev_close": quote_data.get("PrevClose", 0.0),
                "turnover": quote_data.get("Turnover", 0.0),
                "timestamp": quote_data.get("Timestamp", datetime.now().isoformat())
            }
        except Exception as e:
            print(f"获取实时行情失败: {e}")
            # 降级到模拟数据
            return {
                "symbol": symbol,
                "name": f"{symbol}公司",
                "price": 100.0,
                "change": 1.5,
                "change_percent": 1.5,
                "volume": 1000000,
                "open": 99.0,
                "high": 101.5,
                "low": 98.5,
                "prev_close": 98.5,
                "turnover": 100000000,
                "timestamp": datetime.now().isoformat()
            }
    
    @classmethod
    async def calculate_technical_indicators(cls, data: pd.DataFrame) -> Dict:
        """计算技术指标"""
        if data.empty:
            return {}
        
        # 计算各种技术指标
        indicators = {
            "sma_20": data['Close'].rolling(window=20).mean().iloc[-1],
            "sma_50": data['Close'].rolling(window=50).mean().iloc[-1],
            "rsi": cls._calculate_rsi(data['Close']),
            "macd": cls._calculate_macd(data['Close']),
            "bollinger_bands": cls._calculate_bollinger_bands(data['Close'])
        }
        
        return indicators
    
    @staticmethod
    def _calculate_rsi(prices: pd.Series, period: int = 14) -> float:
        """计算RSI指标"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi.iloc[-1] if not rsi.empty else 50
    
    @staticmethod
    def _calculate_macd(prices: pd.Series) -> Dict:
        """计算MACD指标"""
        exp12 = prices.ewm(span=12).mean()
        exp26 = prices.ewm(span=26).mean()
        macd = exp12 - exp26
        signal = macd.ewm(span=9).mean()
        histogram = macd - signal
        
        return {
            "macd": macd.iloc[-1],
            "signal": signal.iloc[-1],
            "histogram": histogram.iloc[-1]
        }
    
    @staticmethod
    def _calculate_bollinger_bands(prices: pd.Series, period: int = 20) -> Dict:
        """计算布林带"""
        sma = prices.rolling(window=period).mean()
        std = prices.rolling(window=period).std()
        upper_band = sma + (std * 2)
        lower_band = sma - (std * 2)
        
        return {
            "upper": upper_band.iloc[-1],
            "middle": sma.iloc[-1],
            "lower": lower_band.iloc[-1]
        }

    @classmethod
    async def get_market_indices(cls) -> List[Dict[str, Any]]:
        """获取主要市场指数"""
        try:
            indices_data = await tencent_cloud_service.get_market_indices()
            return indices_data
        except Exception as e:
            print(f"获取市场指数失败: {e}")
            return []
    
    @classmethod
    async def get_historical_data(cls, symbol: str, start_date: str, end_date: str, interval: str = "1d") -> List[Dict[str, Any]]:
        """获取历史K线数据"""
        try:
            historical_data = await tencent_cloud_service.get_historical_data(symbol, start_date, end_date, interval)
            return historical_data
        except Exception as e:
            print(f"获取历史数据失败: {e}")
            return []
    
    @classmethod
    async def get_company_info(cls, symbol: str) -> Dict[str, Any]:
        """获取公司基本信息"""
        try:
            company_info = await tencent_cloud_service.get_company_info(symbol)
            return company_info
        except Exception as e:
            print(f"获取公司信息失败: {e}")
            return {}
    
    @classmethod
    async def get_financial_statements(cls, symbol: str, report_type: str = "annual") -> Dict[str, Any]:
        """获取财务报表数据"""
        try:
            financial_data = await tencent_cloud_service.get_financial_statements(symbol, report_type)
            return financial_data
        except Exception as e:
            print(f"获取财务报表失败: {e}")
            return {}
    
    @classmethod
    async def get_market_news(cls, limit: int = 10) -> List[Dict[str, Any]]:
        """获取市场新闻"""
        try:
            news_data = await TencentCloudService.get_market_news(limit)
            return news_data
        except Exception as e:
            print(f"获取市场新闻失败: {e}")
            return []

    # 以下是为charts.py添加的方法
    @classmethod
    async def get_historical_prices(cls, symbol: str, period: str) -> List[Dict[str, Any]]:
        """获取历史价格数据"""
        try:
            data = await cls.get_stock_data(symbol, period)
            if not data.empty:
                return data.reset_index().to_dict('records')
            return []
        except Exception as e:
            print(f"获取历史价格失败: {e}")
            return []

    @classmethod
    async def get_volume_data(cls, symbol: str, period: str) -> List[Dict[str, Any]]:
        """获取成交量数据"""
        try:
            data = await cls.get_stock_data(symbol, period)
            if not data.empty:
                return [{"date": idx.strftime("%Y-%m-%d"), "volume": row.Volume} 
                       for idx, row in data.iterrows()]
            return []
        except Exception as e:
            print(f"获取成交量数据失败: {e}")
            return []

    @classmethod
    async def get_financial_ratios(cls, symbol: str) -> Dict[str, List[Dict[str, Any]]]:
        """获取财务比率数据"""
        try:
            # 模拟财务比率数据
            ratios = {
                "roe": [{"period": "2023-Q4", "value": 15.2}, {"period": "2024-Q1", "value": 16.8}],
                "pe_ratio": [{"period": "2023-Q4", "value": 18.5}, {"period": "2024-Q1", "value": 20.1}],
                "pb_ratio": [{"period": "2023-Q4", "value": 2.1}, {"period": "2024-Q1", "value": 2.3}]
            }
            return ratios
        except Exception as e:
            print(f"获取财务比率失败: {e}")
            return {}

    @classmethod
    async def get_sector_companies(cls, sector: str, metric: str) -> List[Dict[str, Any]]:
        """获取行业公司数据"""
        try:
            # 模拟行业数据
            sectors = {
                "technology": [{"sector": "科技", metric: 25.0}, {"sector": "金融", metric: 15.0}],
                "finance": [{"sector": "金融", metric: 12.0}, {"sector": "科技", metric: 22.0}]
            }
            return sectors.get(sector, [])
        except Exception as e:
            print(f"获取行业数据失败: {e}")
            return []

    @classmethod
    async def get_portfolio_weights(cls, portfolio: List[str]) -> List[Dict[str, Any]]:
        """获取投资组合权重"""
        try:
            # 模拟投资组合数据
            weights = [{"symbol": symbol, "weight": 100/len(portfolio)} for symbol in portfolio]
            return weights
        except Exception as e:
            print(f"获取投资组合权重失败: {e}")
            return []

    @classmethod
    async def get_correlation_matrix(cls, symbols: List[str]) -> List[List[float]]:
        """获取相关性矩阵"""
        try:
            # 模拟相关性矩阵
            n = len(symbols)
            return [[1.0 if i == j else 0.5 for j in range(n)] for i in range(n)]
        except Exception as e:
            print(f"获取相关性矩阵失败: {e}")
            return []

    @classmethod
    async def get_performance_comparison(cls, symbols: List[str], benchmarks: List[str], period: str) -> List[Dict[str, Any]]:
        """获取业绩对比数据"""
        try:
            # 模拟业绩数据
            dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
            data = []
            for date in dates:
                entry = {"date": date.strftime("%Y-%m-%d"), "return": np.random.uniform(-5, 10)}
                for symbol in symbols + benchmarks:
                    entry[symbol] = np.random.uniform(-3, 8)
                data.append(entry)
            return data
        except Exception as e:
            print(f"获取业绩对比数据失败: {e}")
            return []

    @classmethod
    async def get_comprehensive_analysis_data(cls, symbol: str, period: str) -> Dict[str, Any]:
        """获取综合分析数据"""
        try:
            price_data = await cls.get_historical_prices(symbol, period)
            volume_data = await cls.get_volume_data(symbol, period)
            ratios_data = await cls.get_financial_ratios(symbol)
            
            return {
                "price_data": price_data,
                "volume_data": volume_data,
                "financial_ratios": ratios_data
            }
        except Exception as e:
            print(f"获取综合分析数据失败: {e}")
            return {}

# 初始化数据服务
DataService.initialize()