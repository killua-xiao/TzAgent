from typing import Dict, List, Optional
import uuid
import json
from datetime import datetime, date
import pandas as pd
from .analysis_service import AnalysisService
from .ai_service import AIService

class ReportService:
    _reports = {}  # 内存存储报告，生产环境应使用数据库
    
    @classmethod
    async def generate_report(
        cls,
        symbol: str,
        report_type: str,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        analysis_depth: str = "standard"
    ) -> Dict:
        """生成分析报告"""
        report_id = f"report_{uuid.uuid4().hex[:8]}"
        
        # 设置默认日期范围
        if not end_date:
            end_date = datetime.now().date()
        if not start_date:
            if report_type == "daily":
                start_date = end_date
            elif report_type == "weekly":
                start_date = end_date - pd.DateOffset(weeks=1)
            elif report_type == "monthly":
                start_date = end_date - pd.DateOffset(months=1)
            else:
                start_date = end_date - pd.DateOffset(years=1)
        
        try:
            # 执行分析
            if report_type == "comprehensive":
                analysis_result = await AnalysisService.perform_comprehensive_analysis(symbol, "1y")
            else:
                analysis_result = await AnalysisService.perform_technical_analysis(symbol, "1y")
            
            # 使用AI生成报告内容
            report_content = await cls._generate_report_content(
                symbol, report_type, analysis_result, analysis_depth
            )
            
            # 创建报告对象
            report = {
                "report_id": report_id,
                "symbol": symbol,
                "report_type": report_type,
                "title": f"{symbol} {report_type}分析报告",
                "content": report_content,
                "generated_at": datetime.now(),
                "analysis_depth": analysis_depth,
                "date_range": {
                    "start_date": start_date.isoformat(),
                    "end_date": end_date.isoformat()
                }
            }
            
            # 保存报告
            cls._reports[report_id] = report
            
            return report
            
        except Exception as e:
            print(f"报告生成失败: {e}")
            raise e
    
    @classmethod
    async def _generate_report_content(
        cls,
        symbol: str,
        report_type: str,
        analysis_result: Dict,
        analysis_depth: str
    ) -> Dict:
        """使用AI生成报告内容"""
        prompt = f"""
        作为资深金融分析师，请为以下股票生成一份{report_type}分析报告：
        
        股票代码: {symbol}
        报告类型: {report_type}
        分析深度: {analysis_depth}
        
        分析结果数据:
        {json.dumps(analysis_result, indent=2, ensure_ascii=False)}
        
        请生成包含以下内容的专业报告：
        1. 执行摘要（关键发现和建议）
        2. 市场环境分析
        3. 技术面分析（趋势、指标、信号）
        4. 基本面分析（财务健康度、估值、成长性）
        5. 风险评估
        6. 投资建议和操作策略
        7. 关键监控指标
        
        报告要专业、详细、数据驱动，适合机构投资者阅读。
        """
        
        try:
            response = await AIService.answer_financial_question(prompt)
            return response
        except Exception as e:
            print(f"AI报告生成失败: {e}")
            return {"error": "报告生成失败", "details": str(e)}
    
    @classmethod
    async def list_reports(
        cls,
        symbol: Optional[str] = None,
        report_type: Optional[str] = None,
        limit: int = 10,
        offset: int = 0
    ) -> List[Dict]:
        """获取报告列表"""
        reports = list(cls._reports.values())
        
        # 过滤
        if symbol:
            reports = [r for r in reports if r["symbol"] == symbol]
        if report_type:
            reports = [r for r in reports if r["report_type"] == report_type]
        
        # 排序（按生成时间倒序）
        reports.sort(key=lambda x: x["generated_at"], reverse=True)
        
        return reports[offset:offset + limit]
    
    @classmethod
    async def get_report(cls, report_id: str) -> Optional[Dict]:
        """获取报告详情"""
        return cls._reports.get(report_id)
    
    @classmethod
    async def delete_report(cls, report_id: str) -> bool:
        """删除报告"""
        if report_id in cls._reports:
            del cls._reports[report_id]
            return True
        return False
    
    @classmethod
    async def export_report(cls, report_id: str, format: str = "pdf") -> str:
        """导出报告"""
        report = cls._reports.get(report_id)
        if not report:
            raise ValueError("报告不存在")
        
        # 这里应该实现实际的导出逻辑（生成PDF/Excel等）
        # 返回下载URL
        return f"/api/reports/{report_id}/download.{format}"
    
    @classmethod
    async def get_report_templates(cls) -> List[Dict]:
        """获取报告模板列表"""
        return [
            {
                "id": "daily_template",
                "name": "每日报告模板",
                "description": "包含每日市场总结和技术指标分析",
                "type": "daily"
            },
            {
                "id": "weekly_template", 
                "name": "每周报告模板",
                "description": "包含周度市场回顾和基本面分析",
                "type": "weekly"
            },
            {
                "id": "comprehensive_template",
                "name": "综合分析模板",
                "description": "全面的基本面和技术面深度分析",
                "type": "comprehensive"
            }
        ]
    
    @classmethod
    async def generate_from_template(cls, template_id: str, symbol: str) -> Dict:
        """使用模板生成报告"""
        templates = cls.get_report_templates()
        template = next((t for t in templates if t["id"] == template_id), None)
        
        if not template:
            raise ValueError("模板不存在")
        
        return await cls.generate_report(symbol, template["type"])