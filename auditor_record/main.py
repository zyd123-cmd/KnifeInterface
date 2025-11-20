from fastapi import FastAPI
from auditor_record.routers import lend_record_router

app = FastAPI(title="刀具管理系统", version="1.0.0")

# 包含路由
app.include_router(lend_record_router.router)

@app.get("/")
async def root():
    return {"message": "刀具管理系统"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# 接口地址说明：
# 1. 获取补货记录列表: GET /auditor_record/replenish_list
# 2. 导出补货记录: GET /auditor_record/export_replenish
# 3. 获取领刀记录列表: GET /auditor_record/list
# 4. 导出领刀记录: GET /auditor_record/export
# 5. 获取公共暂存记录列表: GET /auditor_record/storage_list
# 6. 导出公共暂存记录: GET /auditor_record/export_storage
# 7. 获取告警预警列表: GET /auditor_record/alarm_list
# 8. 刀柜货道绑定/补货刀具: POST /auditor_record/cabinet/stock_bind_cutter
# 9. 获取个人暂存柜: GET /auditor_record/cabinet/personal_storage
# 10. 取刀柜库存告警值预设: GET /auditor_record/cabinet/make_alarm
# 11. 获取取刀柜库存告警值预设: GET /auditor_record/cabinet/get_make_alarm