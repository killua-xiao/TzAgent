import httpx
import json
from typing import Dict, List, Optional, Any
from loguru import logger
from app.core.config import settings

class AIService:
    """AI模型服务 - 集成多个大模型API"""
    
    def __init__(self):
        self.models = {
            "deepseek": {
                "name": "Deepseek",
                "base_url": "https://api.deepseek.com/v1",
                "api_key": settings.DEEPSEEK_API_KEY,
                "headers": {
                    "Authorization": f"Bearer {settings.DEEPSEEK_API_KEY}",
                    "Content-Type": "application/json"
                }
            },
            "douban": {
                "name": "豆包",
                "base_url": "https://open.douban.com/v1",
                "api_key": settings.DOUBAN_API_KEY,
                "headers": {
                    "Authorization": f"Bearer {settings.DOUBAN_API_KEY}",
                    "Content-Type": "application/json"
                }
            },
            "tongyi": {
                "name": "通义千问",
                "base_url": "https://dashscope.aliyuncs.com/api/v1",
                "api_key": settings.TONGYI_API_KEY,
                "headers": {
                    "Authorization": f"Bearer {settings.TONGYI_API_KEY}",
                    "Content-Type": "application/json",
                    "X-DashScope-Async": "enable"
                }
            }
        }
    
    async def chat_completion(self, model: str, messages: List[Dict[str, str]], 
                             temperature: float = 0.7, max_tokens: int = 2000) -> Dict[str, Any]:
        """通用聊天补全接口"""
        if model not in self.models:
            raise ValueError(f"不支持的模型: {model}")
        
        model_config = self.models[model]
        
        if not model_config["api_key"]:
            logger.warning(f"{model_config['name']} API密钥未配置，使用模拟响应")
            return self._get_mock_response(messages)
        
        try:
            payload = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "stream": False
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{model_config['base_url']}/chat/completions",
                    json=payload,
                    headers=model_config["headers"],
                    timeout=30
                )
                response.raise_for_status()
                return response.json()
                
        except Exception as e:
            logger.error(f"{model_config['name']} API调用失败: {str(e)}")
            raise
    
    async def analyze_financial_data(self, model: str, symbol: str, data: Dict[str, Any], 
                                   analysis_type: str = "comprehensive") -> Dict[str, Any]:
        """金融数据分析"""
        prompt = self._build_financial_analysis_prompt(symbol, data, analysis_type)
        
        messages = [
            {
                "role": "system",
                "content": """你是一个专业的金融分析师，擅长股票基本面分析、技术面分析和投资建议。
请基于提供的金融数据，给出专业、客观、深入的分析报告。"""
            },
            {
                "role": "user", 
                "content": prompt
            }
        ]
        
        try:
            response = await self.chat_completion(model, messages, temperature=0.3)
            return self._parse_analysis_response(response, analysis_type)
        except Exception as e:
            logger.error(f"金融数据分析失败: {str(e)}")
            return self._get_mock_analysis(symbol, analysis_type)
    
    async def generate_investment_report(self, model: str, symbol: str, 
                                       historical_data: List[Dict[str, Any]],
                                       financial_data: Dict[str, Any],
                                       market_conditions: Dict[str, Any]) -> Dict[str, Any]:
        """生成投资研究报告"""
        prompt = self._build_report_prompt(symbol, historical_data, financial_data, market_conditions)
        
        messages = [
            {
                "role": "system",
                "content": """你是一个顶级的投资研究分析师，需要撰写专业的投资研究报告。
报告应该包含：公司概况、行业分析、财务分析、估值分析、技术分析、风险提示和投资建议。"""
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
        
        try:
            response = await self.chat_completion(model, messages, temperature=0.2, max_tokens=4000)
            return self._parse_report_response(response)
        except Exception as e:
            logger.error(f"生成投资报告失败: {str(e)}")
            return self._get_mock_report(symbol)
    
    async def answer_financial_question(self, model: str, question: str, 
                                      context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """回答金融相关问题"""
        messages = [
            {
                "role": "system",
                "content": """你是一个专业的金融顾问，精通股票、基金、债券、衍生品等金融产品。
请用专业但易懂的语言回答用户的金融问题，提供准确的信息和实用的建议。"""
            }
        ]
        
        if context:
            messages.append({
                "role": "system",
                "content": f"上下文信息: {json.dumps(context, ensure_ascii=False)}"
            })
        
        messages.append({
            "role": "user",
            "content": question
        })
        
        try:
            response = await self.chat_completion(model, messages, temperature=0.5)
            return self._parse_qa_response(response)
        except Exception as e:
            logger.error(f"回答金融问题失败: {str(e)}")
            return self._get_mock_answer(question)
    
    def _build_financial_analysis_prompt(self, symbol: str, data: Dict[str, Any], 
                                       analysis_type: str) -> str:
        """构建金融分析提示词"""
        base_prompt = f"""请对股票 {symbol} 进行{analysis_type}分析。

当前数据：
{json.dumps(data, ensure_ascii=False, indent=2)}

请提供以下分析内容："""
        
        if analysis_type == "technical":
            base_prompt += """
1. 技术指标分析（MACD、RSI、布林带等）
2. 价格趋势分析
3. 支撑阻力位分析
4. 交易信号建议"""
        elif analysis_type == "fundamental":
            base_prompt += """
1. 财务指标分析（PE、PB、ROE等）
2. 盈利能力分析
3. 成长性分析
4. 估值水平分析"""
        else:
            base_prompt += """
1. 综合技术面分析
2. 综合基本面分析
3. 市场情绪分析
4. 投资建议和风险提示"""

        base_prompt += "\n\n请用专业、客观的语言进行分析，给出具体的建议。"
        return base_prompt
    
    def _build_report_prompt(self, symbol: str, historical_data: List[Dict[str, Any]],
                           financial_data: Dict[str, Any], market_conditions: Dict[str, Any]) -> str:
        """构建研究报告提示词"""
        return f"""请为股票 {symbol} 撰写一份专业的投资研究报告。

历史价格数据（最近10条）：
{json.dumps(historical_data[-10:], ensure_ascii=False, indent=2)}

财务数据：
{json.dumps(financial_data, ensure_ascii=False, indent=2)}

市场环境：
{json.dumps(market_conditions, ensure_ascii=False, indent=2)}

请生成包含以下章节的完整报告：
1. 执行摘要
2. 公司概况
3. 行业分析
4. 财务分析
5. 估值分析
6. 技术分析
7. 风险提示
8. 投资建议

报告要求专业、详细、数据支撑充分。"""
    
    def _parse_analysis_response(self, response: Dict[str, Any], analysis_type: str) -> Dict[str, Any]:
        """解析分析响应"""
        content = response.get("choices", [{}])[0].get("message", {}).get("content", "")
        
        return {
            "analysis_type": analysis_type,
            "content": content,
            "model": response.get("model", ""),
            "timestamp": response.get("created", ""),
            "usage": response.get("usage", {})
        }
    
    def _parse_report_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """解析报告响应"""
        content = response.get("choices", [{}])[0].get("message", {}).get("content", "")
        
        return {
            "report_type": "investment",
            "content": content,
            "model": response.get("model", ""),
            "timestamp": response.get("created", ""),
            "usage": response.get("usage", {})
        }
    
    def _parse_qa_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """解析问答响应"""
        content = response.get("choices", [{}])[0].get("message", {}).get("content", "")
        
        return {
            "answer": content,
            "model": response.get("model", ""),
            "timestamp": response.get("created", ""),
            "usage": response.get("usage", {})
        }
    
    # 模拟响应方法（API密钥未配置时使用）
    def _get_mock_response(self, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        """生成模拟响应"""
        user_message = messages[-1]["content"] if messages else ""
        
        return {
            "id": "mock-response-12345",
            "object": "chat.completion",
            "created": 1700000000,
            "model": "mock-model",
            "choices": [{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": f"这是对您消息的模拟响应: {user_message[:100]}... (API密钥未配置)"
                },
                "finish_reason": "stop"
            }],
            "usage": {
                "prompt_tokens": len(str(messages)),
                "completion_tokens": 100,
                "total_tokens": len(str(messages)) + 100
            }
        }
    
    def _get_mock_analysis(self, symbol: str, analysis_type: str) -> Dict[str, Any]:
        """生成模拟分析"""
        return {
            "analysis_type": analysis_type,
            "content": f"这是对{symbol}的模拟{analysis_type}分析报告。请配置API密钥获取真实分析。",
            "model": "mock-model",
            "timestamp": 1700000000,
            "usage": {"prompt_tokens": 100, "completion_tokens": 200, "total_tokens": 300}
        }
    
    def _get_mock_report(self, symbol: str) -> Dict[str, Any]:
        """生成模拟报告"""
        return {
            "report_type": "investment",
            "content": f"# {symbol}投资研究报告\n\n这是模拟报告内容。请配置API密钥获取真实报告。",
            "model": "mock-model",
            "timestamp": 1700000000,
            "usage": {"prompt_tokens": 200, "completion_tokens": 800, "total_tokens": 1000}
        }
    
    def _get_mock_answer(self, question: str) -> Dict[str, Any]:
        """生成模拟答案"""
        return {
            "answer": f"这是对问题的模拟回答: {question[:50]}... (API密钥未配置)",
            "model": "mock-model",
            "timestamp": 1700000000,
            "usage": {"prompt_tokens": 50, "completion_tokens": 100, "total_tokens": 150}
        }

# 全局服务实例
ai_service = AIService()