import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


class Settings:
    # API配置
    API_TITLE: str = os.getenv("API_TITLE", "二次封装API服务")
    API_DESCRIPTION: str = os.getenv("API_DESCRIPTION", "对现有接口进行二次封装的API服务")
    API_VERSION: str = os.getenv("API_VERSION", "1.0.0")

    # 原始API配置
    ORIGINAL_API_BASE_URL: str = os.getenv("ORIGINAL_API_BASE_URL", "https://jsonplaceholder.typicode.com")
    ORIGINAL_API_KEY: str = os.getenv("ORIGINAL_API_KEY", "")

    # 应用配置
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))


settings = Settings()