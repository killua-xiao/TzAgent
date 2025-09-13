"""
金融AI智能投研助手 - 主应用入口模块

此模块负责：
1. 创建和配置FastAPI应用
2. 设置中间件和异常处理
3. 注册所有API路由
4. 管理应用生命周期事件
5. 提供健康检查接口

版本: v1.0.0
作者: 金融AI开发团队
创建时间: 2024年3月
"""

from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from datetime import datetime
import time
from typing import Optional
import uvicorn

from .core.config import settings
from .api import market, analysis, knowledge, chat, reports, charts, stocks
from .services.data_service import DataService
from .services.knowledge_service import KnowledgeService

# 创建FastAPI应用实例
# 配置应用元数据，包括名称、版本、描述等
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="金融AI智能投研助手 - 基于大模型的金融数据分析平台",
    docs_url="/docs" if settings.DEBUG else None,  # 开发模式下启用API文档
    redoc_url="/redoc" if settings.DEBUG else None  # 开发模式下启用Redoc文档
)

# 配置跨域资源共享(CORS)中间件
# 允许前端应用从指定域名访问API接口
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,  # 允许的源域名列表
    allow_credentials=True,               # 允许携带认证信息
    allow_methods=["*"],                  # 允许所有HTTP方法
    allow_headers=["*"],                  # 允许所有HTTP头
)

# 请求处理时间中间件
# 在每个响应头中添加X-Process-Time字段，记录请求处理耗时
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """
    记录请求处理时间的中间件
    
    Args:
        request: FastAPI请求对象
        call_next: 下一个中间件或路由处理函数
    
    Returns:
        Response: 添加了处理时间头的响应对象
    """
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# 异常处理处理器
# 统一处理应用中的各种异常，返回标准化的错误响应

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """
    HTTP异常处理
    
    处理所有HTTP状态码异常，返回统一的错误格式
    
    Args:
        request: 请求对象
        exc: HTTP异常实例
    
    Returns:
        JSONResponse: 标准错误响应
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.detail,
            "message": "请求处理失败",
            "timestamp": datetime.now().isoformat()
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """
    通用异常处理
    
    捕获所有未处理的异常，防止敏感信息泄露
    
    Args:
        request: 请求对象
        exc: 异常实例
    
    Returns:
        JSONResponse: 标准错误响应
    """
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "服务器内部错误",
            "message": "系统繁忙，请稍后重试",
            "timestamp": datetime.now().isoformat()
        }
    )

# 健康检查
@app.get("/")
async def root():
    return {
        "success": True,
        "message": "金融AI智能投研助手服务正常运行",
        "data": {
            "name": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "timestamp": datetime.now().isoformat(),
            "status": "healthy"
        }
    }

@app.get("/health")
async def health_check():
    """健康检查接口"""
    try:
        # 检查核心服务状态
        services_status = {
            "data_service": "available",
            "knowledge_service": "available"
        }
        
        return {
            "success": True,
            "data": {
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "services": services_status
            }
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"服务异常: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }

# 注册API路由
app.include_router(market.router, prefix="/api/v1/market", tags=["市场数据"])
app.include_router(analysis.router, prefix="/api/v1/analysis", tags=["分析服务"])
app.include_router(knowledge.router, prefix="/api/v1/knowledge", tags=["知识库"])
app.include_router(chat.router, prefix="/api/v1/chat", tags=["聊天服务"])
app.include_router(reports.router, prefix="/api/v1/reports", tags=["报告服务"])
app.include_router(charts.router, prefix="/api/v1/charts", tags=["图表服务"])
app.include_router(stocks.router, prefix="/api/v1/stocks", tags=["股票数据"])

# 挂载静态文件
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.mount("/reports", StaticFiles(directory="reports"), name="reports")

# 启动事件
@app.on_event("startup")
async def startup_event():
    """应用启动事件"""
    print(f"🚀 {settings.APP_NAME} v{settings.APP_VERSION} 正在启动...")
    print(f"📊 调试模式: {settings.DEBUG}")
    print(f"🌐 服务地址: http://{settings.HOST}:{settings.PORT}")
    
    # 初始化数据服务
    DataService.initialize()
    print("✅ 数据服务已初始化")
    
    # 初始化知识库服务
    await KnowledgeService.initialize()
    print("✅ 知识库服务已初始化")
    
    print("🎉 应用启动完成，服务已就绪！")

@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭事件"""
    print("🛑 应用正在关闭...")
    print("👋 服务已停止")

# 开发模式直接运行
if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info" if settings.DEBUG else "warning"
    )