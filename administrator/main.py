from fastapi import FastAPI
from app.routers import data_router  # 导入我们即将创建的路由

# 创建FastAPI应用实例
app = FastAPI(
    title="二次封装API服务",
    description="对现有接口进行二次封装的API服务",
    version="1.0.0"
)

# 包含路由
app.include_router(data_router.router, prefix="/api/v1", tags=["数据接口"])

# 根路径路由
@app.get("/")
async def root():
    return {"message": "二次封装API服务已启动", "status": "success"}

# 健康检查端点
@app.get("/health")
async def health_check():
    return {"status": "healthy"}