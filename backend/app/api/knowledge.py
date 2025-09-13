from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel
from ..services.knowledge_service import KnowledgeService

router = APIRouter()

class KnowledgeQuery(BaseModel):
    question: str
    context: Optional[dict] = None
    max_results: int = 5

class KnowledgeItem(BaseModel):
    id: str
    title: str
    content: str
    category: str
    source: str
    relevance: float

@router.post("/query")
async def query_knowledge(query: KnowledgeQuery):
    """查询金融知识库"""
    try:
        results = await KnowledgeService.search_knowledge(
            query.question, query.context, query.max_results
        )
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"知识库查询失败: {str(e)}")

@router.get("/categories")
async def get_categories():
    """获取知识分类"""
    categories = await KnowledgeService.get_categories()
    return {"categories": categories}

@router.get("/item/{item_id}")
async def get_knowledge_item(item_id: str):
    """获取知识条目详情"""
    try:
        item = await KnowledgeService.get_knowledge_item(item_id)
        return item
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"知识条目不存在: {str(e)}")

@router.post("/add")
async def add_knowledge_item(item: dict):
    """添加知识条目（管理员功能）"""
    try:
        result = await KnowledgeService.add_knowledge_item(item)
        return {"success": True, "id": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"添加知识条目失败: {str(e)}")

@router.get("/related/{symbol}")
async def get_related_knowledge(symbol: str):
    """获取与股票相关的知识"""
    try:
        results = await KnowledgeService.get_related_knowledge(symbol)
        return {"symbol": symbol, "related_knowledge": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取相关知识失败: {str(e)}")