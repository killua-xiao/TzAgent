"""
应用配置管理模块

此模块负责：
1. 定义所有环境变量和配置参数
2. 处理配置的默认值和类型验证
3. 管理敏感信息的加载和安全性
4. 提供全局配置实例

版本: v1.0.0
"""

from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional
import os

class Settings(BaseSettings):
    # 应用配置
    APP_NAME: str = "金融AI智能投研助手"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # 服务器配置
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    CORS_ORIGINS: list = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    # 数据库配置
    DATABASE_URL: str = "sqlite:///./app.db"
    
    # 向量数据库配置
    CHROMA_DB_PATH: str = "./data/chroma_db"
    CHROMA_PERSIST_DIR: str = "./data/chroma_persist"
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    
    # API密钥配置
    DEEPSEEK_API_KEY: Optional[str] = Field(None, env="DEEPSEEK_API_KEY")
    DOUBAN_API_KEY: Optional[str] = Field(None, env="DOUBAN_API_KEY") 
    TONGYI_API_KEY: Optional[str] = Field(None, env="TONGYI_API_KEY")
    
    # 腾讯云配置
    TENCENT_CLOUD_API_KEY: Optional[str] = Field(None, env="TENCENT_CLOUD_API_KEY")
    TENCENT_CLOUD_API_SECRET: Optional[str] = Field(None, env="TENCENT_CLOUD_API_SECRET")
    
    # 文件存储配置
    UPLOAD_DIR: str = "./uploads"
    REPORT_DIR: str = "./reports"
    
    # 知识库配置
    KNOWLEDGE_BASE_DIR: str = "./knowledge_base"
    MAX_KNOWLEDGE_ITEMS: int = 10000
    
    # 缓存配置
    REDIS_URL: Optional[str] = Field(None, env="REDIS_URL")
    CACHE_TTL: int = 3600  # 1小时
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# 全局配置实例
settings = Settings()

# 环境变量默认值处理
if not settings.DEEPSEEK_API_KEY:
    settings.DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

if not settings.DOUBAN_API_KEY:
    settings.DOUBAN_API_KEY = os.getenv("DOUBAN_API_KEY")

if not settings.TONGYI_API_KEY:
    settings.TONGYI_API_KEY = os.getenv("TONGYI_API_KEY")

if not settings.TENCENT_CLOUD_API_KEY:
    settings.TENCENT_CLOUD_API_KEY = os.getenv("TENCENT_CLOUD_API_KEY")

if not settings.TENCENT_CLOUD_API_SECRET:
    settings.TENCENT_CLOUD_API_SECRET = os.getenv("TENCENT_CLOUD_API_SECRET")