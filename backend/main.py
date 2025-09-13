from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import uvicorn
from dotenv import load_dotenv
import os

from app.api import router as api_router
from app.core.config import settings
from app.core.database import init_db
from app.services.data_service import DataService

# 加载环境变量
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时初始化
    print("🚀 启动金融AI Agent服务...")
    await init_db()
    # 初始化数据服务
    DataService.initialize()
    yield
    # 关闭时清理
    print("🛑 关闭金融AI Agent服务...")

app = FastAPI(
    title="金融AI智能投研助手",
    description="基于大模型的金融数据分析与投研平台",
    version="1.0.0",
    lifespan=lifespan
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载API路由
app.include_router(api_router, prefix="/api/v1")

# 挂载静态文件
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return {
        "message": "欢迎使用金融AI智能投研助手",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "financial-ai-agent"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        workers=settings.WORKERS
    )