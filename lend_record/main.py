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