from fastapi import FastAPI
from lend_record.routers import lend_record_router

app = FastAPI(title="领刀记录管理系统", version="1.0.0")

# 包含路由
app.include_router(lend_record_router.router)

@app.get("/")
async def root():
    return {"message": "领刀记录管理系统"}

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