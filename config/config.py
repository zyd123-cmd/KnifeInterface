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
    ORIGINAL_API_BASE_URL: str = os.getenv("ORIGINAL_API_BASE_URL", "http://39.98.115.114:8983")
    ORIGINAL_API_KEY: str = os.getenv("ORIGINAL_API_KEY", "")
    
    # Token文件配置
    TOKEN_FILE_PATH: str = os.getenv("TOKEN_FILE_PATH", "token.txt")

    # 应用配置
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    def get_token_from_file(self) -> str:
        """从文件读取Token"""
        try:
            token_path = self.TOKEN_FILE_PATH
            # 如果是相对路径，转换为绝对路径
            if not os.path.isabs(token_path):
                current_dir = os.path.dirname(os.path.abspath(__file__))
                project_root = os.path.dirname(current_dir)
                token_path = os.path.join(project_root, token_path)
            
            with open(token_path, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except Exception as e:
            print(f"读取Token文件失败: {e}")
            return ""


settings = Settings()