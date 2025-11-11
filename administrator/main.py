from fastapi import FastAPI
from routers import data_router, lend_record_router  # 导入路由

# 创建FastAPI应用实例
app = FastAPI(
    title="二次封装API服务",
    description="对现有接口进行二次封装的API服务",
    version="1.0.0"
)

# 包含路由
app.include_router(data_router.router, prefix="/api/v1", tags=["数据接口"])
app.include_router(lend_record_router.router)

# 根路径路由
@app.get("/")
async def root():
    return {"message": "二次封装API服务已启动", "status": "success"}

# 健康检查端点
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# 接口地址说明：
# 1. 获取领刀记录列表: GET /lend_record/list
# 2. 导出领刀记录: GET /lend_record/export
# 3. 刀柜补货: POST /lend_record/restock
# 4. 获取补货记录列表: GET /lend_record/replenish_list
# 5. 获取公共暂存记录列表: GET /lend_record/storage_list
# 6. 获取个人暂存柜信息: GET /lend_record/personal_storage
# 7. 设置取刀柜告警值: GET /lend_record/make_alarm
# 8. 获取取刀柜告警值: GET /lend_record/get_make_alarm