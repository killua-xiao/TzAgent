from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime, date
from ..services.report_service import ReportService

router = APIRouter()

class ReportRequest(BaseModel):
    symbol: str
    report_type: str  # daily, weekly, monthly, comprehensive
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    analysis_depth: str = "standard"  # quick, standard, deep

class ReportResponse(BaseModel):
    report_id: str
    symbol: str
    report_type: str
    title: str
    content: dict
    generated_at: datetime
    download_url: Optional[str] = None

@router.post("/generate")
async def generate_report(request: ReportRequest):
    """生成分析报告"""
    try:
        report = await ReportService.generate_report(
            request.symbol,
            request.report_type,
            request.start_date,
            request.end_date,
            request.analysis_depth
        )
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"报告生成失败: {str(e)}")

@router.get("/list")
async def list_reports(
    symbol: Optional[str] = None,
    report_type: Optional[str] = None,
    limit: int = 10,
    offset: int = 0
):
    """获取报告列表"""
    try:
        reports = await ReportService.list_reports(symbol, report_type, limit, offset)
        return {"reports": reports, "total": len(reports)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取报告列表失败: {str(e)}")

@router.get("/{report_id}")
async def get_report(report_id: str):
    """获取报告详情"""
    try:
        report = await ReportService.get_report(report_id)
        if not report:
            raise HTTPException(status_code=404, detail="报告不存在")
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取报告失败: {str(e)}")

@router.delete("/{report_id}")
async def delete_report(report_id: str):
    """删除报告"""
    try:
        success = await ReportService.delete_report(report_id)
        if not success:
            raise HTTPException(status_code=404, detail="报告不存在")
        return {"success": True, "message": "报告已删除"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除报告失败: {str(e)}")

@router.post("/{report_id}/export")
async def export_report(report_id: str, format: str = "pdf"):
    """导出报告"""
    try:
        export_url = await ReportService.export_report(report_id, format)
        return {"export_url": export_url, "format": format}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"导出报告失败: {str(e)}")

@router.get("/templates")
async def get_report_templates():
    """获取报告模板列表"""
    templates = await ReportService.get_report_templates()
    return {"templates": templates}

@router.post("/templates/{template_id}")
async def generate_from_template(template_id: str, symbol: str):
    """使用模板生成报告"""
    try:
        report = await ReportService.generate_from_template(template_id, symbol)
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"模板报告生成失败: {str(e)}")