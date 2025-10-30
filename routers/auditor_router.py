from fastapi import APIRouter, HTTPException, Query
from typing import Optional

# 导入所需的模块
from auditor.services.api_client import OriginalAPIClient
from auditor.schemas.data_schemas import StorageStatisticsResponse

# 创建API客户端实例（需要配置实际的外部API地址）
api_client = OriginalAPIClient(
    base_url="http://your-external-api-base-url",  # 请替换为实际的外部API基础地址
    api_key=None  # 如果需要API密钥，请在此处配置
)

router = APIRouter()


@router.get("/storage-statistics", response_model=StorageStatisticsResponse, tags=["出入库统计"])
async def get_storage_statistics(
    current: Optional[int] = Query(1, ge=1, description="当前页"),
    size: Optional[int] = Query(10, ge=1, le=100, description="每页数量"),
    start_time: Optional[str] = Query(None, alias="startTime", description="开始时间（YYYY-MM-DD HH:mm:ss）"),
    end_time: Optional[str] = Query(None, alias="endTime", description="结束时间（YYYY-MM-DD HH:mm:ss）"),
    record_status: Optional[int] = Query(None, alias="recordStatus", description="记录状态：0-取刀，1-还刀，2-收刀，3-暂存，4-完成，5-违规还刀"),
    ranking_type: Optional[int] = Query(None, alias="rankingType", description="排名类型：0-按数量排序，1-按金额排序"),
    order: Optional[int] = Query(None, description="排序顺序：0-从大到小（降序），1-从小到大（升序）")
):
    """
    获取出入库统计数据
    
    功能：查询刀具的出入库记录统计信息
    
    参数说明：
    - current: 当前页码，默认1
    - size: 每页数量，默认10
    - startTime: 开始时间
    - endTime: 结束时间
    - recordStatus: 记录状态
      * 0: 取刀
      * 1: 还刀
      * 2: 收刀
      * 3: 暂存
      * 4: 完成
      * 5: 违规还刀
    - rankingType: 排名类型
      * 0: 按数量排序
      * 1: 按金额排序
    - order: 排序顺序
      * 0: 从大到小（降序）
      * 1: 从小到大（升序）
    
    返回数据：
    - code: 状态码
    - msg: 返回消息
    - success: 是否成功
    - data: 分页数据
      * current: 当前页
      * size: 每页数量
      * total: 总记录数
      * pages: 总页数
      * records: 记录列表（仅包含必要字段）
    """
    try:
        # 构建查询参数
        params = {
            "current": current,
            "size": size,
            "startTime": start_time,
            "endTime": end_time,
            "recordStatus": record_status,
            "rankingType": ranking_type,
            "order": order
        }
        
        # 调用API客户端方法获取数据
        result = api_client.get_storage_statistics(params)
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取出入库统计数据失败: {str(e)}")
