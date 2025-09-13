from typing import List, Dict, Optional
import chromadb
from chromadb.config import Settings
from app.core.config import settings
import json
import os

class KnowledgeService:
    _client = None
    _collection = None
    
    @classmethod
    async def initialize(cls):
        """初始化知识库服务"""
        try:
            # 创建ChromaDB客户端
            cls._client = chromadb.PersistentClient(
                path=settings.CHROMA_PERSIST_DIR,
                settings=Settings(anonymized_telemetry=False)
            )
            
            # 获取或创建集合
            cls._collection = cls._client.get_or_create_collection(
                "financial_knowledge",
                metadata={"description": "金融专业知识库"}
            )
            
            # 初始化示例数据
            cls._initialize_sample_data()
            
            print("✅ 知识库服务初始化完成")
            
        except Exception as e:
            print(f"知识库初始化失败: {e}")
    
    @classmethod
    def _initialize_sample_data(cls):
        """初始化示例金融知识数据"""
        sample_data = [
            {
                "id": "knowledge_001",
                "title": "股票基本面分析指南",
                "content": "基本面分析是通过分析公司的财务报表、行业地位、管理团队等因素来评估股票价值的方法。主要包括财务比率分析、盈利能力分析、成长性分析等。",
                "category": "投资分析",
                "source": "金融知识库"
            },
            {
                "id": "knowledge_002", 
                "title": "技术分析常用指标",
                "content": "技术分析常用指标包括：移动平均线(MA)、相对强弱指数(RSI)、随机指标(KDJ)、MACD、布林带等。这些指标帮助分析价格趋势和买卖信号。",
                "category": "技术分析",
                "source": "金融知识库"
            },
            {
                "id": "knowledge_003",
                "title": "市盈率(P/E)解读",
                "content": "市盈率是股票价格与每股收益的比率，用于评估股票估值水平。一般来说，P/E较低可能表示股票被低估，但需要结合行业和成长性综合判断。",
                "category": "估值指标", 
                "source": "金融知识库"
            }
        ]
        
        # 添加示例数据
        for item in sample_data:
            cls._collection.upsert(
                documents=[item["content"]],
                metadatas=[{
                    "title": item["title"],
                    "category": item["category"],
                    "source": item["source"]
                }],
                ids=[item["id"]]
            )
    
    @classmethod
    async def search_knowledge(cls, query: str, context: Optional[dict] = None, max_results: int = 5) -> List[Dict]:
        """搜索金融知识"""
        try:
            results = cls._collection.query(
                query_texts=[query],
                n_results=max_results,
                where=context if context else {}
            )
            
            knowledge_items = []
            for i in range(len(results["ids"][0])):
                knowledge_items.append({
                    "id": results["ids"][0][i],
                    "title": results["metadatas"][0][i]["title"],
                    "content": results["documents"][0][i],
                    "category": results["metadatas"][0][i]["category"],
                    "source": results["metadatas"][0][i]["source"],
                    "relevance": results["distances"][0][i] if results["distances"] else 0.0
                })
            
            return knowledge_items
        except Exception as e:
            print(f"知识搜索失败: {e}")
            return []
    
    @classmethod
    async def get_categories(cls) -> List[str]:
        """获取知识分类"""
        # 从知识库中获取所有分类
        return ["投资分析", "技术分析", "估值指标", "宏观经济", "行业研究", "风险管理"]
    
    @classmethod
    async def get_knowledge_item(cls, item_id: str) -> Optional[Dict]:
        """获取知识条目详情"""
        try:
            result = cls._collection.get(ids=[item_id])
            if result["documents"]:
                return {
                    "id": item_id,
                    "title": result["metadatas"][0]["title"],
                    "content": result["documents"][0],
                    "category": result["metadatas"][0]["category"],
                    "source": result["metadatas"][0]["source"]
                }
            return None
        except Exception as e:
            print(f"获取知识条目失败: {e}")
            return None
    
    @classmethod
    async def add_knowledge_item(cls, item: Dict) -> str:
        """添加知识条目"""
        try:
            item_id = f"knowledge_{len(cls._collection.get()['ids']) + 1:03d}"
            cls._collection.upsert(
                documents=[item["content"]],
                metadatas=[{
                    "title": item["title"],
                    "category": item.get("category", "未分类"),
                    "source": item.get("source", "用户添加")
                }],
                ids=[item_id]
            )
            return item_id
        except Exception as e:
            print(f"添加知识条目失败: {e}")
            raise e
    
    @classmethod
    async def get_related_knowledge(cls, symbol: str) -> List[Dict]:
        """获取与股票相关的知识"""
        # 根据股票代码搜索相关知识
        query = f"{symbol} 股票 分析 投资"
        return await cls.search_knowledge(query, max_results=3)

# 初始化知识库服务（在main.py中异步调用）
# KnowledgeService.initialize()