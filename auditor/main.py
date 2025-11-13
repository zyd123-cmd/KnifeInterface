import sys
import os
import logging
from fastapi import FastAPI

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 将项目根目录添加到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from routers.auditor_router import router as auditor_router
from auditor.services.api_client import original_api_client

# 启动时检查Token配置
logger.info("========== 审计员服务启动 ==========")
logger.info(f"API Base URL: {original_api_client.base_url}")
auth_header = original_api_client.session.headers.get('Authorization')
if auth_header:
    logger.info(f"✅ Token已加载（前50字符）: {auth_header[:50]}...")
else:
    logger.warning("⚠️  未检测到Token，请检查token.txt文件")
logger.info("=====================================")

# 创建FastAPI应用实例
app = FastAPI(
    title="刀具管理系统 - 审计员接口",
    description="""
    ## 审计员接口服务
    
    提供审计员查看日志与状态的只读权限API接口。
    
    ### 主要功能模块：
    
    #### 1. 出入库统计
    - 出入库记录查询（分页）
    - 出入库记录导出
    - 支持时间范围、记录状态、排名类型等多维度筛选
    
    #### 2. 统计图表
    - 全年取刀数量统计
    - 全年取刀金额统计
    - 刀具消耗统计
    
    #### 3. 总库存统计
    - 库存列表查询（支持搜索和分页）
    - 单个库位详情查询
    
    #### 4. 废刀回收统计
    - 收刀柜还刀信息查询
    - 按还刀状态分类统计（修磨、报废、换线、错领）
    
    ### 接口规范：
    - 基础路径：`/api/v1/auditor`
    - 端口：`8003`
    - 数据格式：JSON
    - 字符编码：UTF-8
    - 权限：只读
    
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
            "name": "出入库统计",
            "description": "出入库记录查询和导出功能",
        },
        {
            "name": "统计图表",
            "description": "各类统计图表数据接口",
        },
        {
            "name": "总库存统计",
            "description": "库存统计和查询功能",
        },
        {
            "name": "废刀回收统计",
            "description": "废刀回收和还刀信息统计",
        },
        {
            "name": "系统接口",
            "description": "系统级别的接口，如健康检查等",
        },
    ]
)

# 包含路由
app.include_router(auditor_router, prefix="/api/v1/auditor")

# 根路径路由
@app.get("/", tags=["系统接口"], summary="服务根路径")
async def root():
    """
    服务根路径，用于验证服务是否正常运行
    
    **返回示例**:
    ```json
    {
        "message": "审计员接口服务已启动",
        "status": "success",
        "role": "auditor",
        "permissions": "只读权限"
    }
    ```
    """
    return {
        "message": "审计员接口服务已启动",
        "status": "success",
        "role": "auditor",
        "permissions": "只读权限"
    }

# 健康检查端点
@app.get("/health", tags=["系统接口"], summary="健康检查")
async def health_check():
    """
    服务健康检查接口
    
    **用途**: 用于监控系统、负载均衡器等检查服务状态
    
    **返回示例**:
    ```json
    {
        "status": "healthy",
        "service": "auditor"
    }
    ```
    """
    return {
        "status": "healthy",
        "service": "auditor"
    }

# 支持直接运行
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "auditor.main:app",
        host="0.0.0.0",
        port=8003,
        reload=True
    )
