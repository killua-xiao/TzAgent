from typing import Dict, List, Optional
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from .data_service import DataService
from .ai_service import AIService

class AnalysisService:
    @staticmethod
    async def perform_technical_analysis(symbol: str, period: str = "1y") -> Dict:
        """执行技术面分析"""
        # 获取股票数据
        data = await DataService.get_stock_data(symbol, period)
        if data.empty:
            return {"error": "无法获取股票数据"}
        
        # 计算技术指标
        indicators = await DataService.calculate_technical_indicators(data)
        
        # 使用AI分析技术信号
        analysis_result = await AIService.analyze_technical_signals(
            symbol, data, indicators
        )
        
        return {
            "symbol": symbol,
            "period": period,
            "indicators": indicators,
            "analysis": analysis_result,
            "last_updated": datetime.now()
        }
    
    @staticmethod
    async def perform_fundamental_analysis(symbol: str, period: str = "1y") -> Dict:
        """执行基本面分析"""
        # 获取基本面数据（这里需要集成财务数据API）
        fundamental_data = await AnalysisService._get_fundamental_data(symbol)
        
        # 使用AI分析基本面
        analysis_result = await AIService.analyze_fundamentals(symbol, fundamental_data)
        
        return {
            "symbol": symbol,
            "period": period,
            "fundamental_data": fundamental_data,
            "analysis": analysis_result,
            "last_updated": datetime.now()
        }
    
    @staticmethod
    async def perform_comprehensive_analysis(symbol: str, period: str = "1y") -> Dict:
        """执行综合分析"""
        technical_result = await AnalysisService.perform_technical_analysis(symbol, period)
        fundamental_result = await AnalysisService.perform_fundamental_analysis(symbol, period)
        
        # 使用AI生成综合分析和投资建议
        comprehensive_analysis = await AIService.generate_comprehensive_analysis(
            symbol, technical_result, fundamental_result
        )
        
        return {
            "symbol": symbol,
            "period": period,
            "technical": technical_result,
            "fundamental": fundamental_result,
            "comprehensive": comprehensive_analysis,
            "last_updated": datetime.now()
        }
    
    @staticmethod
    async def get_technical_indicators(symbol: str, period: str = "1y") -> Dict:
        """获取详细技术指标"""
        data = await DataService.get_stock_data(symbol, period)
        if data.empty:
            return {}
        
        indicators = await DataService.calculate_technical_indicators(data)
        return indicators
    
    @staticmethod
    async def _get_fundamental_data(symbol: str) -> Dict:
        """获取基本面数据（模拟实现）"""
        # 这里需要集成腾讯云金融数据API或第三方财务数据API
        return {
            "financial_statements": {
                "revenue": 1000000000,
                "net_income": 150000000,
                "assets": 2000000000,
                "liabilities": 800000000,
                "equity": 1200000000
            },
            "valuation_metrics": {
                "pe_ratio": 15.5,
                "pb_ratio": 2.1,
                "dividend_yield": 2.5,
                "market_cap": 18500000000
            },
            "growth_metrics": {
                "revenue_growth": 12.5,
                "eps_growth": 8.3,
                "dividend_growth": 5.2
            }
        }
    
    @staticmethod
    def calculate_financial_ratios(financial_data: Dict) -> Dict:
        """计算财务比率"""
        # 实现各种财务比率计算
        return {
            "profitability_ratios": {
                "roa": financial_data.get("net_income", 0) / financial_data.get("assets", 1),
                "roe": financial_data.get("net_income", 0) / financial_data.get("equity", 1),
                "profit_margin": financial_data.get("net_income", 0) / financial_data.get("revenue", 1)
            },
            "liquidity_ratios": {
                "current_ratio": financial_data.get("current_assets", 0) / financial_data.get("current_liabilities", 1),
                "quick_ratio": (financial_data.get("current_assets", 0) - financial_data.get("inventory", 0)) / financial_data.get("current_liabilities", 1)
            },
            "leverage_ratios": {
                "debt_to_equity": financial_data.get("liabilities", 0) / financial_data.get("equity", 1),
                "debt_to_assets": financial_data.get("liabilities", 0) / financial_data.get("assets", 1)
            }
        }