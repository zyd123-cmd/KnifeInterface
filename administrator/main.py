from fastapi import FastAPI
import sys
import os
# 将上级目录添加到Python路径中
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from routers import data_router
from config.config import settings

# 创建FastAPI应用实例
app = FastAPI(
    title="二次封装API服务",
    description="对现有接口进行二次封装的API服务",
    version="1.0.0"
)
app.include_router(data_router.router)

# 包含路由


# 根路径路由
@app.get("/")
async def root():
    return {"message": "二次封装API服务已启动", "status": "success"}

# 健康检查端点
@app.get("/health")
async def health_check():
    return {"status": "healthy"}