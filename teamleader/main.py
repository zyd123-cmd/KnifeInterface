import sys
import os
from fastapi import FastAPI

# 将项目根目录添加到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from routers.teamleader_router import router as teamleader_router

# 创建FastAPI应用实例
app = FastAPI(
    title="刀具管理系统 - 班组长接口",
    description="""
    ## 班组长接口服务
    
    提供班组长日常管理所需的刀具信息查询、统计等功能的API接口。
    
    ### 主要功能模块：
    
    #### 1. 刀具管理
    - 刀具耗材信息查询
    - 多维度筛选（品牌、型号、类型、价格区间等）
    - 分页查询支持
    
    #### 2. 数据统计
    - 刀具使用情况统计
    - 库存统计分析
    
    ### 接口规范：
    - 基础路径：`/api/v1`
    - 端口：`8002`
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
            "name": "TeamLeader-班组长",
            "description": "班组长刀具管理相关接口",
        },
        {
            "name": "系统接口",
            "description": "系统级别的接口，如健康检查等",
        },
    ]
)

# 包含路由
app.include_router(teamleader_router, prefix="/api/v1")

# 根路径路由
@app.get("/", tags=["系统接口"], summary="服务根路径")
async def root():
    """
    服务根路径，用于验证服务是否正常运行
    
    **返回示例**:
    ```json
    {
        "message": "班组长接口服务已启动",
        "status": "success"
    }
    ```
    """
    return {"message": "班组长接口服务已启动", "status": "success"}

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
        "teamleader.main:app",
        host="0.0.0.0",
        port=8002,
        reload=True
    )
