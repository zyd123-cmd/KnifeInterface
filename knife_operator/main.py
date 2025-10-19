import sys
import os
from fastapi import FastAPI

# 将项目根目录添加到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from routers.operator_router import router as operator_router

# 创建FastAPI应用实例
app = FastAPI(
    title="刀具管理系统 - 操作员接口",
    description="""
    ## 操作员接口服务
    
    提供刀具借出、归还、暂存等操作员日常业务功能的API接口。
    
    ### 主要功能模块：
    
    #### 1. 刀头管理
    - 刀头借出记录管理
    - 刀头暂存记录管理
    - 刀头批量归还
    
    #### 2. 刀柄管理
    - 刀柄借出记录管理
    - 刀柄暂存记录管理（新建、查询、编辑、归还、详情）
    - 刀柄批量归还
    
    #### 3. 权限控制
    - 所有操作都需要验证操作人权限
    - 用户只能操作自己相关的记录
    
    ### 接口规范：
    - 基础路径：`/api/v1`
    - 端口：`8001`
    - 数据格式：JSON
    - 字符编码：UTF-8
    
    ### 作者信息：
    - 开发团队：刀具管理系统开发组
    - 联系方式：support@example.com
    """,
    version="1.0.0",
    contact={
        "name": "刀具管理系统开发团队",
        "email": "support@example.com",
    },
    license_info={
        "name": "内部使用",
    },
    openapi_tags=[
        {
            "name": "刀头借出管理",
            "description": "刀头借出记录的增删改查操作",
        },
        {
            "name": "刀头暂存管理",
            "description": "刀头暂存记录的管理和批量归还操作",
        },
        {
            "name": "刀柄借出管理",
            "description": "刀柄借出记录的增删改查操作",
        },
        {
            "name": "刀柄暂存管理",
            "description": "刀柄暂存记录的完整管理（新建、查询、编辑、归还、暂存、详情、批量归还）",
        },
        {
            "name": "系统接口",
            "description": "系统级别的接口，如健康检查等",
        },
    ]
)

# 包含路由（不再使用tags参数，因为每个路由已经在内部定义）
app.include_router(operator_router, prefix="/api/v1")

# 根路径路由
@app.get("/", tags=["系统接口"], summary="服务根路径")
async def root():
    """
    服务根路径，用于验证服务是否正常运行
    
    **返回示例**:
    ```json
    {
        "message": "操作员接口服务已启动",
        "status": "success"
    }
    ```
    """
    return {"message": "操作员接口服务已启动", "status": "success"}

# 健康检查端点
@app.get("/health", tags=["系统接口"], summary="健康检查")
async def health_check():
    """
    服务健康检查接口
    
    **用途**: 用于监控系统、负载均衡器等检查服务状态
    
    **返回示例**:
    ```json
    {
        "status": "healthy"
    }
    ```
    """
    return {"status": "healthy"}

# 支持直接运行
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "knife_operator.main:app",
        host="0.0.0.0",
        port=8001,
        reload=True
    )