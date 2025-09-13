from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Dict, Optional
import json
from datetime import datetime, timedelta

from ..services.chart_service import chart_service
from ..services.data_service import DataService

router = APIRouter()

@router.get("/price/{symbol}")
async def get_price_chart(
    symbol: str,
    period: str = Query("1mo", description="时间周期: 1d, 1w, 1m, 3m, 6m, 1y, 2y, 5y"),
    chart_type: str = Query("candlestick", description="图表类型: candlestick, line")
):
    """获取价格图表"""
    try:
        # 获取价格数据
        price_data = await DataService.get_historical_prices(symbol, period)
        
        if not price_data:
            raise HTTPException(status_code=404, detail="未找到价格数据")
        
        # 生成图表
        chart_result = await chart_service.generate_price_chart(
            symbol, price_data, chart_type
        )
        
        if not chart_result.get("success"):
            raise HTTPException(status_code=500, detail=chart_result.get("error", "图表生成失败"))
        
        return chart_result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取价格图表失败: {str(e)}")

@router.get("/technical/{symbol}")
async def get_technical_chart(
    symbol: str,
    period: str = Query("3m", description="时间周期: 1m, 3m, 6m, 1y"),
    indicators: List[str] = Query(["sma", "rsi"], description="技术指标: sma, ema, rsi, macd, boll")
):
    """获取技术指标图表"""
    try:
        # 获取价格数据
        price_data = await DataService.get_historical_prices(symbol, period)
        
        if not price_data:
            raise HTTPException(status_code=404, detail="未找到价格数据")
        
        # 生成技术指标图表
        chart_result = await chart_service.generate_technical_indicators(
            symbol, price_data, indicators
        )
        
        if not chart_result.get("success"):
            raise HTTPException(status_code=500, detail=chart_result.get("error", "图表生成失败"))
        
        return chart_result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取技术指标图表失败: {str(e)}")

@router.get("/volume/{symbol}")
async def get_volume_chart(
    symbol: str,
    period: str = Query("1mo", description="时间周期: 1d, 1w, 1m, 3m")
):
    """获取成交量图表"""
    try:
        # 获取成交量数据
        volume_data = await DataService.get_volume_data(symbol, period)
        
        if not volume_data:
            raise HTTPException(status_code=404, detail="未找到成交量数据")
        
        # 生成成交量图表
        chart_result = await chart_service.generate_volume_chart(symbol, volume_data)
        
        if not chart_result.get("success"):
            raise HTTPException(status_code=500, detail=chart_result.get("error", "图表生成失败"))
        
        return chart_result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取成交量图表失败: {str(e)}")

@router.get("/financial/{symbol}")
async def get_financial_chart(
    symbol: str,
    ratio_type: str = Query("all", description="比率类型: profitability, liquidity, leverage, valuation, all")
):
    """获取财务比率图表"""
    try:
        # 获取财务比率数据
        ratios_data = await DataService.get_financial_ratios(symbol)
        
        if not ratios_data:
            raise HTTPException(status_code=404, detail="未找到财务比率数据")
        
        # 根据类型筛选数据
        filtered_ratios = {}
        if ratio_type != "all":
            for ratio_name, ratio_data in ratios_data.items():
                if ratio_type in ratio_name.lower():
                    filtered_ratios[ratio_name] = ratio_data
        else:
            filtered_ratios = ratios_data
        
        # 生成财务比率图表
        chart_result = await chart_service.generate_financial_ratio_chart(
            symbol, filtered_ratios
        )
        
        if not chart_result.get("success"):
            raise HTTPException(status_code=500, detail=chart_result.get("error", "图表生成失败"))
        
        return chart_result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取财务比率图表失败: {str(e)}")

@router.get("/sector-comparison")
async def get_sector_comparison(
    sector: str = Query(..., description="行业名称"),
    metric: str = Query("pe_ratio", description="比较指标: pe_ratio, pb_ratio, roe, dividend_yield")
):
    """获取行业对比图表"""
    try:
        # 获取行业数据
        sector_data = await DataService.get_sector_companies(sector, metric)
        
        if not sector_data:
            raise HTTPException(status_code=404, detail="未找到行业数据")
        
        # 生成行业对比图表
        chart_result = await chart_service.generate_sector_comparison(sector_data, metric)
        
        if not chart_result.get("success"):
            raise HTTPException(status_code=500, detail=chart_result.get("error", "图表生成失败"))
        
        return chart_result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取行业对比图表失败: {str(e)}")

@router.get("/portfolio")
async def get_portfolio_chart(
    portfolio: List[str] = Query(..., description="投资组合股票代码列表")
):
    """获取投资组合饼图"""
    try:
        # 获取投资组合数据
        portfolio_data = await DataService.get_portfolio_weights(portfolio)
        
        if not portfolio_data:
            raise HTTPException(status_code=404, detail="未找到投资组合数据")
        
        # 生成投资组合饼图
        chart_result = await chart_service.generate_portfolio_pie_chart(portfolio_data)
        
        if not chart_result.get("success"):
            raise HTTPException(status_code=500, detail=chart_result.get("error", "图表生成失败"))
        
        return chart_result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取投资组合图表失败: {str(e)}")

@router.get("/correlation")
async def get_correlation_chart(
    symbols: List[str] = Query(..., description="股票代码列表")
):
    """获取相关性矩阵图表"""
    try:
        # 获取相关性数据
        correlation_data = await DataService.get_correlation_matrix(symbols)
        
        if not correlation_data:
            raise HTTPException(status_code=404, detail="未找到相关性数据")
        
        # 生成相关性矩阵
        chart_result = await chart_service.generate_correlation_matrix(symbols, correlation_data)
        
        if not chart_result.get("success"):
            raise HTTPException(status_code=500, detail=chart_result.get("error", "图表生成失败"))
        
        return chart_result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取相关性矩阵图表失败: {str(e)}")

@router.get("/performance")
async def get_performance_chart(
    symbols: List[str] = Query(..., description="股票代码列表"),
    benchmarks: List[str] = Query(["^GSPC"], description="基准指数代码列表"),
    period: str = Query("1y", description="时间周期: 1m, 3m, 6m, 1y, 2y, 5y")
):
    """获取业绩对比图表"""
    try:
        # 获取业绩数据
        performance_data = await DataService.get_performance_comparison(symbols, benchmarks, period)
        
        if not performance_data:
            raise HTTPException(status_code=404, detail="未找到业绩数据")
        
        # 生成业绩对比图表
        chart_result = await chart_service.generate_performance_comparison(
            performance_data, benchmarks
        )
        
        if not chart_result.get("success"):
            raise HTTPException(status_code=500, detail=chart_result.get("error", "图表生成失败"))
        
        return chart_result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取业绩对比图表失败: {str(e)}")

@router.get("/comprehensive/{symbol}")
async def get_comprehensive_chart_report(
    symbol: str,
    period: str = Query("1y", description="时间周期: 3m, 6m, 1y, 2y")
):
    """获取综合分析图表报告"""
    try:
        # 获取综合分析数据
        analysis_data = await DataService.get_comprehensive_analysis_data(symbol, period)
        
        if not analysis_data:
            raise HTTPException(status_code=404, detail="未找到分析数据")
        
        # 生成综合图表报告
        chart_report = await chart_service.generate_comprehensive_report(symbol, analysis_data)
        
        if not chart_report.get("success"):
            raise HTTPException(status_code=500, detail=chart_report.get("error", "图表报告生成失败"))
        
        return chart_report
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取综合分析图表报告失败: {str(e)}")

@router.get("/health")
async def chart_service_health():
    """图表服务健康检查"""
    return {
        "status": "healthy",
        "service": "chart_service",
        "timestamp": datetime.now().isoformat(),
        "capabilities": [
            "price_chart", "technical_chart", "volume_chart", 
            "financial_chart", "sector_comparison", "portfolio_chart",
            "correlation_matrix", "performance_comparison", "comprehensive_report"
        ]
    }