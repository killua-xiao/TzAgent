"""
股票数据API路由模块

提供股票数据的CRUD操作接口，包括：
- 获取股票列表
- 创建股票数据
- 更新股票数据
- 删除股票数据
- 批量操作
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

router = APIRouter()

# 数据模型
class StockData(BaseModel):
    id: str
    symbol: str
    name: str
    price: float
    change_percent: float
    market_cap: float
    industry: str
    update_time: datetime

class CreateStockRequest(BaseModel):
    symbol: str
    name: str
    price: float
    change_percent: float
    market_cap: float
    industry: str

class StockListResponse(BaseModel):
    data: List[StockData]
    total: int
    page: int
    page_size: int

class StockFilterParams(BaseModel):
    symbol: Optional[str] = None
    name: Optional[str] = None
    industry: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    page: int = 1
    page_size: int = 10

# 模拟数据 - 在实际应用中应该从数据库获取
mock_stocks = [
    {
        "id": "1",
        "symbol": "000001",
        "name": "平安银行",
        "price": 15.68,
        "change_percent": 2.45,
        "market_cap": 150000000000,
        "industry": "finance",
        "update_time": datetime.now()
    },
    {
        "id": "2",
        "symbol": "600036",
        "name": "招商银行",
        "price": 42.35,
        "change_percent": 1.23,
        "market_cap": 850000000000,
        "industry": "finance",
        "update_time": datetime.now()
    },
    {
        "id": "3",
        "symbol": "000858",
        "name": "五粮液",
        "price": 185.60,
        "change_percent": -0.87,
        "market_cap": 720000000000,
        "industry": "consumer",
        "update_time": datetime.now()
    },
    {
        "id": "4",
        "symbol": "601318",
        "name": "中国平安",
        "price": 48.92,
        "change_percent": 0.56,
        "market_cap": 950000000000,
        "industry": "finance",
        "update_time": datetime.now()
    },
    {
        "id": "5",
        "symbol": "000333",
        "name": "美的集团",
        "price": 72.35,
        "change_percent": 1.89,
        "market_cap": 520000000000,
        "industry": "consumer",
        "update_time": datetime.now()
    }
]

@router.get("", response_model=StockListResponse)
async def get_stocks(
    symbol: Optional[str] = Query(None),
    name: Optional[str] = Query(None),
    industry: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100)
):
    """
    获取股票列表
    
    支持按股票代码、名称、行业、价格区间进行筛选
    支持分页查询
    
    Args:
        symbol: 股票代码筛选
        name: 股票名称筛选
        industry: 行业筛选
        min_price: 最低价格
        max_price: 最高价格
        page: 页码
        page_size: 每页数量
    
    Returns:
        StockListResponse: 股票列表响应
    """
    try:
        # 筛选逻辑
        filtered_data = mock_stocks.copy()
        
        if symbol:
            filtered_data = [s for s in filtered_data if symbol.lower() in s["symbol"].lower()]
        
        if name:
            filtered_data = [s for s in filtered_data if name.lower() in s["name"].lower()]
        
        if industry:
            filtered_data = [s for s in filtered_data if s["industry"] == industry]
        
        if min_price is not None:
            filtered_data = [s for s in filtered_data if s["price"] >= min_price]
        
        if max_price is not None:
            filtered_data = [s for s in filtered_data if s["price"] <= max_price]
        
        # 分页逻辑
        total = len(filtered_data)
        start = (page - 1) * page_size
        end = start + page_size
        paged_data = filtered_data[start:end]
        
        return {
            "data": paged_data,
            "total": total,
            "page": page,
            "page_size": page_size
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取股票数据失败: {str(e)}")

@router.post("", response_model=StockData)
async def create_stock(request: CreateStockRequest):
    """
    创建股票数据
    
    Args:
        request: 创建股票请求
    
    Returns:
        StockData: 创建的股票数据
    """
    try:
        new_stock = {
            "id": str(len(mock_stocks) + 1),
            "symbol": request.symbol,
            "name": request.name,
            "price": request.price,
            "change_percent": request.change_percent,
            "market_cap": request.market_cap,
            "industry": request.industry,
            "update_time": datetime.now()
        }
        
        mock_stocks.append(new_stock)
        return new_stock
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建股票失败: {str(e)}")

@router.get("/{stock_id}", response_model=StockData)
async def get_stock(stock_id: str):
    """
    获取单个股票详情
    
    Args:
        stock_id: 股票ID
    
    Returns:
        StockData: 股票详情
    """
    stock = next((s for s in mock_stocks if s["id"] == stock_id), None)
    if not stock:
        raise HTTPException(status_code=404, detail="股票不存在")
    return stock

@router.put("/{stock_id}", response_model=StockData)
async def update_stock(stock_id: str, request: CreateStockRequest):
    """
    更新股票数据
    
    Args:
        stock_id: 股票ID
        request: 更新数据
    
    Returns:
        StockData: 更新后的股票数据
    """
    stock_index = next((i for i, s in enumerate(mock_stocks) if s["id"] == stock_id), None)
    if stock_index is None:
        raise HTTPException(status_code=404, detail="股票不存在")
    
    try:
        updated_stock = {
            "id": stock_id,
            "symbol": request.symbol,
            "name": request.name,
            "price": request.price,
            "change_percent": request.change_percent,
            "market_cap": request.market_cap,
            "industry": request.industry,
            "update_time": datetime.now()
        }
        
        mock_stocks[stock_index] = updated_stock
        return updated_stock
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新股票失败: {str(e)}")

@router.delete("/{stock_id}")
async def delete_stock(stock_id: str):
    """
    删除股票数据
    
    Args:
        stock_id: 股票ID
    """
    global mock_stocks
    original_length = len(mock_stocks)
    mock_stocks = [s for s in mock_stocks if s["id"] != stock_id]
    
    if len(mock_stocks) == original_length:
        raise HTTPException(status_code=404, detail="股票不存在")
    
    return {"message": "删除成功"}

@router.post("/batch", response_model=List[StockData])
async def batch_get_stocks(symbols: List[str]):
    """
    批量获取股票数据
    
    Args:
        symbols: 股票代码列表
    
    Returns:
        List[StockData]: 股票数据列表
    """
    try:
        result = []
        for symbol in symbols:
            stock = next((s for s in mock_stocks if s["symbol"] == symbol), None)
            if stock:
                result.append(stock)
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"批量获取股票失败: {str(e)}")