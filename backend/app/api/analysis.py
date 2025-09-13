from fastapi import APIRouter, HTTPException
from typing import Dict, List
from pydantic import BaseModel
from datetime import date
from ..services.analysis_service import AnalysisService

router = APIRouter()

class AnalysisRequest(BaseModel):
    symbol: str
    analysis_type: str  # fundamental, technical, comprehensive
    period: str = "1y"  # 1m, 3m, 6m, 1y, 5y

class TechnicalAnalysisResult(BaseModel):
    trend: str  # bullish, bearish, neutral
    indicators: Dict[str, float]
    signals: List[str]
    confidence: float

class FundamentalAnalysisResult(BaseModel):
    financial_health: str  # excellent, good, fair, poor
    valuation: Dict[str, float]
    growth_metrics: Dict[str, float]
    profitability: Dict[str, float]

class ComprehensiveAnalysisResult(BaseModel):
    technical: TechnicalAnalysisResult
    fundamental: FundamentalAnalysisResult
    overall_rating: str
    recommendation: str  # strong_buy, buy, hold, sell, strong_sell
    risk_level: str  # low, medium, high

@router.post("/technical")
async def technical_analysis(request: AnalysisRequest):
    """技术面分析"""
    try:
        result = await AnalysisService.perform_technical_analysis(
            request.symbol, request.period
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"技术分析失败: {str(e)}")

@router.post("/fundamental")
async def fundamental_analysis(request: AnalysisRequest):
    """基本面分析"""
    try:
        result = await AnalysisService.perform_fundamental_analysis(
            request.symbol, request.period
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"基本面分析失败: {str(e)}")

@router.post("/comprehensive")
async def comprehensive_analysis(request: AnalysisRequest):
    """综合分析"""
    try:
        result = await AnalysisService.perform_comprehensive_analysis(
            request.symbol, request.period
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"综合分析失败: {str(e)}")

@router.get("/indicators/{symbol}")
async def get_technical_indicators(symbol: str, period: str = "1y"):
    """获取技术指标数据"""
    try:
        indicators = await AnalysisService.get_technical_indicators(symbol, period)
        return indicators
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取技术指标失败: {str(e)}")

@router.get("/screener")
async def stock_screener(
    market_cap_min: float = 0,
    market_cap_max: float = float('inf'),
    pe_min: float = 0,
    pe_max: float = float('inf'),
    dividend_yield_min: float = 0
):
    """股票筛选器"""
    # 实现股票筛选逻辑
    return {"stocks": []}