#!/usr/bin/env python3
"""
金融AI智能投研助手 - 启动脚本
"""

import uvicorn
from app.core.config import settings

def main():
    """主启动函数"""
    print("🚀 启动金融AI智能投研助手...")
    print(f"📊 应用名称: {settings.APP_NAME}")
    print(f"🔢 版本: {settings.APP_VERSION}")
    print(f"🌐 服务地址: http://{settings.HOST}:{settings.PORT}")
    print(f"🔧 调试模式: {settings.DEBUG}")
    
    # 启动FastAPI应用
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info" if settings.DEBUG else "warning"
    )

if __name__ == "__main__":
    main()