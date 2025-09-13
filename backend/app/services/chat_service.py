from typing import Dict, List, Optional
import uuid
import json
from datetime import datetime
from .ai_service import AIService
from .knowledge_service import KnowledgeService

class ChatService:
    _sessions = {}  # 内存存储聊天会话，生产环境应使用数据库
    
    async def process_message(self, message: str, session_id: Optional[str] = None, context: Optional[Dict] = None) -> Dict:
        """处理聊天消息"""
        # 创建或获取会话
        if not session_id:
            session_id = str(uuid.uuid4())
            self._sessions[session_id] = {
                "created_at": datetime.now(),
                "messages": []
            }
        
        # 保存用户消息
        user_message = {
            "role": "user",
            "content": message,
            "timestamp": datetime.now()
        }
        self._sessions[session_id]["messages"].append(user_message)
        
        try:
            # 从知识库搜索相关信息
            knowledge_results = await KnowledgeService.search_knowledge(message, context, max_results=3)
            
            # 构建AI提示词
            prompt = self._build_prompt(message, knowledge_results, context)
            
            # 调用AI服务生成响应
            ai_response = await AIService.answer_financial_question(prompt, {
                "knowledge_context": knowledge_results,
                "user_context": context
            })
            
            # 保存AI响应
            assistant_message = {
                "role": "assistant",
                "content": ai_response.get("answer", "抱歉，我无法回答这个问题。"),
                "sources": knowledge_results,
                "timestamp": datetime.now()
            }
            self._sessions[session_id]["messages"].append(assistant_message)
            
            # 构建响应
            response = {
                "response": assistant_message["content"],
                "session_id": session_id,
                "sources": knowledge_results,
                "suggestions": self._generate_suggestions(message)
            }
            
            return response
            
        except Exception as e:
            print(f"聊天消息处理失败: {e}")
            error_response = {
                "response": "抱歉，处理您的请求时出现错误。请稍后再试。",
                "session_id": session_id,
                "sources": [],
                "suggestions": ["重新提问", "联系支持"]
            }
            return error_response
    
    def _build_prompt(self, message: str, knowledge_results: List[Dict], context: Optional[Dict] = None) -> str:
        """构建AI提示词"""
        knowledge_context = "\n".join([
            f"相关知识 {i+1}: {item['title']} - {item['content'][:200]}..."
            for i, item in enumerate(knowledge_results)
        ])
        
        prompt = f"""
        作为专业的金融AI助手，请基于以下知识回答用户问题：
        
        用户问题: {message}
        
        相关知识背景:
        {knowledge_context}
        
        {f"用户上下文: {json.dumps(context, indent=2)}" if context else ""}
        
        请提供专业、准确、全面的金融回答，包括：
        1. 核心答案
        2. 详细解释和分析
        3. 相关数据支持（如适用）
        4. 风险提示和建议
        
        回答要专业且易于理解。
        """
        
        return prompt
    
    def _generate_suggestions(self, message: str) -> List[str]:
        """生成建议问题"""
        suggestions = [
            "请详细解释这个金融概念",
            "相关的投资策略有哪些？",
            "这个指标如何计算？",
            "最新的市场趋势如何？"
        ]
        
        # 根据消息内容生成更相关的建议
        if "股票" in message:
            suggestions = ["技术分析", "基本面分析", "估值水平", "行业对比"]
        elif "基金" in message:
            suggestions = ["基金类型", "投资策略", "风险评估", "历史表现"]
        elif "债券" in message:
            suggestions = ["债券类型", "收益率曲线", "信用评级", "久期分析"]
            
        return suggestions
    
    async def get_chat_history(self, session_id: str) -> List[Dict]:
        """获取聊天历史"""
        session = self._sessions.get(session_id)
        if not session:
            return []
        
        # 只返回最近50条消息
        return session["messages"][-50:]
    
    async def clear_chat_history(self, session_id: str) -> bool:
        """清空聊天历史"""
        if session_id in self._sessions:
            self._sessions[session_id]["messages"] = []
            return True
        return False
    
    def get_session_stats(self, session_id: str) -> Dict:
        """获取会话统计信息"""
        session = self._sessions.get(session_id)
        if not session:
            return {}
        
        return {
            "message_count": len(session["messages"]),
            "created_at": session["created_at"],
            "last_active": session["messages"][-1]["timestamp"] if session["messages"] else None
        }