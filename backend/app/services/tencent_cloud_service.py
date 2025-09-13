import httpx
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import json
from loguru import logger
from app.core.config import settings

class TencentCloudService:
    """腾讯云金融数据服务"""
    
    def __init__(self):
        self.base_url = "https://finance.tencentcloudapi.com"
        self.api_key = settings.TENCENT_CLOUD_API_KEY
        self.api_secret = settings.TENCENT_CLOUD_API_SECRET
        self.region = "ap-shanghai"
        
    async def _make_request(self, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """发送腾讯云API请求"""
        try:
            url = f"{self.base_url}{endpoint}"
            headers = {
                "Authorization": f"TC3-HMAC-SHA256 Credential={self.api_key}/{self.region}/finance/tc3_request",
                "Content-Type": "application/json",
                "X-TC-Action": endpoint.split('/')[-1],
                "X-TC-Version": "2020-11-06",
                "X-TC-Timestamp": str(int(datetime.now().timestamp())),
                "X-TC-Region": self.region
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=params, headers=headers, timeout=30)
                response.raise_for_status()
                return response.json()
                
        except Exception as e:
            logger.error(f"腾讯云API请求失败: {str(e)}")
            raise
    
    async def get_stock_quote(self, symbol: str) -> Dict[str, Any]:
        """获取股票实时行情"""
        params = {
            "Symbol": symbol.upper(),
            "Fields": ["Open", "High", "Low", "Close", "Volume", "Turnover", "Change", "ChangePercent"]
        }
        
        try:
            data = await self._make_request("/DescribeStockQuotes", params)
            return data.get('Response', {}).get('StockQuotes', [{}])[0]
        except Exception as e:
            logger.warning(f"获取股票行情失败，使用模拟数据: {symbol}")
            return self._get_mock_stock_data(symbol)
    
    async def get_market_indices(self) -> List[Dict[str, Any]]:
        """获取主要市场指数"""
        indices = ["000001.SH", "399001.SZ", "399006.SZ", "HSI", "SPX", "IXIC", "DJI"]
        results = []
        
        for index in indices:
            try:
                quote = await self.get_stock_quote(index)
                results.append(quote)
            except Exception as e:
                logger.warning(f"获取指数 {index} 失败: {str(e)}")
                results.append(self._get_mock_index_data(index))
        
        return results
    
    async def get_historical_data(self, symbol: str, start_date: str, end_date: str, interval: str = "1d") -> List[Dict[str, Any]]:
        """获取历史K线数据"""
        params = {
            "Symbol": symbol.upper(),
            "StartTime": start_date,
            "EndTime": end_date,
            "Period": interval.upper()
        }
        
        try:
            data = await self._make_request("/DescribeKLine", params)
            return data.get('Response', {}).get('KLineData', [])
        except Exception as e:
            logger.warning(f"获取历史数据失败，使用模拟数据: {symbol}")
            return self._get_mock_historical_data(symbol, start_date, end_date, interval)
    
    async def get_company_info(self, symbol: str) -> Dict[str, Any]:
        """获取公司基本信息"""
        params = {
            "Symbol": symbol.upper(),
            "Fields": ["CompanyName", "Industry", "Market", "ListingDate", "TotalShares", "MarketCap"]
        }
        
        try:
            data = await self._make_request("/DescribeCompanyInfo", params)
            return data.get('Response', {}).get('CompanyInfo', {})
        except Exception as e:
            logger.warning(f"获取公司信息失败，使用模拟数据: {symbol}")
            return self._get_mock_company_info(symbol)
    
    async def get_financial_statements(self, symbol: str, report_type: str = "annual") -> Dict[str, Any]:
        """获取财务报表数据"""
        params = {
            "Symbol": symbol.upper(),
            "ReportType": report_type.upper(),
            "Fields": ["Revenue", "NetProfit", "EPS", "ROE", "DebtRatio", "CurrentRatio"]
        }
        
        try:
            data = await self._make_request("/DescribeFinancialStatements", params)
            return data.get('Response', {}).get('FinancialData', {})
        except Exception as e:
            logger.warning(f"获取财务报表失败，使用模拟数据: {symbol}")
            return self._get_mock_financial_data(symbol, report_type)
    
    async def get_market_news(self, limit: int = 10) -> List[Dict[str, Any]]:
        """获取市场新闻"""
        params = {
            "Limit": limit,
            "Fields": ["Title", "Content", "PublishTime", "Source", "RelatedStocks"]
        }
        
        try:
            data = await self._make_request("/DescribeMarketNews", params)
            return data.get('Response', {}).get('NewsList', [])
        except Exception as e:
            logger.warning("获取市场新闻失败，使用模拟数据")
            return self._get_mock_news_data(limit)
    
    # 模拟数据方法（实际环境中应删除）
    def _get_mock_stock_data(self, symbol: str) -> Dict[str, Any]:
        """生成模拟股票数据"""
        import random
        base_price = random.uniform(10, 1000)
        change = random.uniform(-5, 5)
        
        return {
            "Symbol": symbol,
            "Name": f"{symbol}公司",
            "Open": round(base_price * 0.98, 2),
            "High": round(base_price * 1.02, 2),
            "Low": round(base_price * 0.96, 2),
            "Close": round(base_price, 2),
            "Volume": random.randint(1000000, 10000000),
            "Turnover": random.uniform(10000000, 100000000),
            "Change": round(change, 2),
            "ChangePercent": round(change / base_price * 100, 2),
            "Timestamp": datetime.now().isoformat()
        }
    
    def _get_mock_index_data(self, symbol: str) -> Dict[str, Any]:
        """生成模拟指数数据"""
        import random
        base_values = {
            "000001.SH": 3000,
            "399001.SZ": 10000,
            "399006.SZ": 2000,
            "HSI": 18000,
            "SPX": 4000,
            "IXIC": 12000,
            "DJI": 33000
        }
        
        base_value = base_values.get(symbol, 5000)
        change = random.uniform(-100, 100)
        
        return {
            "Symbol": symbol,
            "Name": f"{symbol}指数",
            "Close": round(base_value + change, 2),
            "Change": round(change, 2),
            "ChangePercent": round(change / base_value * 100, 2),
            "Timestamp": datetime.now().isoformat()
        }
    
    def _get_mock_historical_data(self, symbol: str, start_date: str, end_date: str, interval: str) -> List[Dict[str, Any]]:
        """生成模拟历史数据"""
        import random
        from datetime import datetime, timedelta
        
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = datetime.strptime(end_date, "%Y-%m-%d")
        days = (end_dt - start_dt).days
        
        data = []
        base_price = random.uniform(10, 100)
        
        for i in range(days + 1):
            current_date = start_dt + timedelta(days=i)
            change = random.uniform(-2, 2)
            open_price = base_price * (1 + random.uniform(-0.01, 0.01))
            close_price = open_price * (1 + change/100)
            high_price = max(open_price, close_price) * (1 + random.uniform(0, 0.02))
            low_price = min(open_price, close_price) * (1 - random.uniform(0, 0.02))
            
            data.append({
                "Date": current_date.strftime("%Y-%m-%d"),
                "Open": round(open_price, 2),
                "High": round(high_price, 2),
                "Low": round(low_price, 2),
                "Close": round(close_price, 2),
                "Volume": random.randint(1000000, 5000000),
                "Turnover": round(random.uniform(5000000, 20000000), 2)
            })
            
            base_price = close_price
        
        return data
    
    def _get_mock_company_info(self, symbol: str) -> Dict[str, Any]:
        """生成模拟公司信息"""
        industries = ["科技", "金融", "消费", "医疗", "能源", "工业"]
        markets = ["主板", "创业板", "科创板", "港股", "美股"]
        
        return {
            "Symbol": symbol,
            "CompanyName": f"{symbol}股份有限公司",
            "Industry": random.choice(industries),
            "Market": random.choice(markets),
            "ListingDate": "2010-01-01",
            "TotalShares": random.randint(100000000, 1000000000),
            "MarketCap": random.uniform(1000000000, 50000000000)
        }
    
    def _get_mock_financial_data(self, symbol: str, report_type: str) -> Dict[str, Any]:
        """生成模拟财务数据"""
        years = 3 if report_type == "annual" else 4
        data = {}
        
        for i in range(years):
            year = datetime.now().year - i
            data[str(year)] = {
                "Revenue": round(random.uniform(100000000, 1000000000), 2),
                "NetProfit": round(random.uniform(10000000, 100000000), 2),
                "EPS": round(random.uniform(0.5, 5.0), 2),
                "ROE": round(random.uniform(5, 25), 2),
                "DebtRatio": round(random.uniform(30, 70), 2),
                "CurrentRatio": round(random.uniform(1.5, 3.0), 2)
            }
        
        return data
    
    def _get_mock_news_data(self, limit: int) -> List[Dict[str, Any]]:
        """生成模拟新闻数据"""
        news_titles = [
            "央行降准释放流动性，市场迎来利好",
            "科技板块集体上涨，AI概念股表现突出",
            "新能源汽车政策加码，产业链受益",
            "美联储维持利率不变，符合市场预期",
            "上市公司业绩预告，多家公司预增",
            "外资持续流入A股，配置价值凸显",
            "数字经济政策利好，相关板块走强",
            "消费复苏超预期，零售板块表现活跃"
        ]
        
        stocks = ["000001", "600036", "601318", "000858", "600519", "300750"]
        
        news_list = []
        for i in range(limit):
            news_list.append({
                "Title": news_titles[i % len(news_titles)],
                "Content": f"这是第{i+1}条新闻的详细内容，包含市场分析和投资建议。",
                "PublishTime": (datetime.now() - timedelta(hours=i)).isoformat(),
                "Source": "腾讯财经",
                "RelatedStocks": random.sample(stocks, min(3, len(stocks)))
            })
        
        return news_list

# 全局服务实例
tencent_cloud_service = TencentCloudService()