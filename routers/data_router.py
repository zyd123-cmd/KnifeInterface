from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
import time
from auditor.services.api_client import original_api_client
from auditor.schemas.data_schemas import OriginalUserResponse, EnhancedUserResponse
from auditor.schemas.data_schemas import ReturnInfo,ReturnInfoListResponse,ReturnInfoCreate,ReturnInfoUpdate
from auditor.schemas.data_schemas import CollectInfo, CollectInfoListResponse, CollectInfoCreate, CollectInfoUpdate
from auditor.schemas.data_schemas import TotalInventoryStat, InventorySummary, InventoryStatListResponse
from auditor.schemas.data_schemas import UnreturnedInfo, UnreturnedInfoListResponse, UnreturnedInfoCreate, UnreturnedInfoUpdate, UnreturnedStatistics
from auditor.schemas.data_schemas import CutterType, CutterTypeListResponse, CutterTypeCreate, CutterTypeUpdate
from auditor.schemas.data_schemas import DictCollection, DictCollectionListResponse, DictCollectionCreate, DictCollectionUpdate
from auditor.schemas.data_schemas import PersonalizedSettings, PersonalizedSettingsListResponse, PersonalizedSettingsCreate, PersonalizedSettingsUpdate
from auditor.schemas.data_schemas import OperationLog, OperationLogListResponse, OperationLogCreate, OperationLogUpdate, OperationLogStats
from auditor.schemas.data_schemas import PublicStorageRecord, PublicStorageRecordListResponse, PublicStorageRecordCreate, PublicStorageRecordUpdate, PublicStorageRecordStats
from auditor.schemas.data_schemas import RestockRecord, RestockRecordListResponse, RestockRecordCreate, RestockRecordUpdate, RestockRecordStats
from auditor.schemas.data_schemas import StockRecord, StockRecordListResponse, StockRecordCreate, StockRecordUpdate, StockRecordStats
router = APIRouter()

@router.get("/users/{user_id}", response_model=EnhancedUserResponse)
async def get_enhanced_user_data(user_id: int):
    """
    获取增强后的用户数据
    - 从原始API获取基础用户信息
    - 从原始API获取用户的帖子数据
    - 进行数据整合和增强
    """
    try:
        # 并行获取用户数据和帖子数据（在实际应用中可以使用异步优化）
        user_data = original_api_client.get_user_data(user_id)
        user_posts = original_api_client.get_user_posts(user_id)

        # 在这里进行你的二次封装逻辑
        enhanced_data = {
            "user_id": user_data["id"],
            "user_name": user_data["name"],
            "email_address": user_data["email"],
            "account_status": "active" if user_data.get("id", 0) % 2 == 0 else "inactive",
            "additional_data": {
                "posts_count": len(user_posts),
                "last_post_title": user_posts[0]["title"] if user_posts else None,
                "processing_notes": "数据已成功封装和增强"
            },
            "processed_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }

        return enhanced_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"数据处理失败: {str(e)}")


@router.get("/users/{user_id}/basic", response_model=OriginalUserResponse)
async def get_original_user_data(user_id: int):
    """
    直接返回从原始API获取的用户数据（示例：直接透传）
    """
    try:
        user_data = original_api_client.get_user_data(user_id)
        return user_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取原始数据失败: {str(e)}")


@router.get("/status")
async def api_status():
    """获取API服务状态"""
    return {
        "status": "operational",
        "service": "secondary-api-wrapper",
        "version": "1.0.0",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }

@router.get("/borrowReturnInfo/returnInfo/list", response_model=ReturnInfoListResponse)
async def list_return_info(page: int = 1, size: int = 10, query: dict = {}):
    """
    获取还刀信息列表
    """
    try:
        result = original_api_client.get_return_info_list({
            "page": page,
            "size": size,
            "query": query
        })
        return ReturnInfoListResponse(
            list=[ReturnInfo(**item) for item in result.get("list", [])],
            total=result.get("total", 0)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取还刀信息列表失败: {str(e)}")

# 查询还刀信息详细
@router.get("/borrowReturnInfo/returnInfo/{id}", response_model=ReturnInfo)
async def get_return_info(id: int):
    """
    查询还刀信息详情
    """
    try:
        result = original_api_client.get_return_info(id)
        return ReturnInfo(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询还刀信息详情失败: {str(e)}")

# 新增还刀信息
@router.post("/borrowReturnInfo/returnInfo", response_model=ReturnInfo)
async def create_return_info(data: ReturnInfoCreate):
    """
    创建还刀信息
    """
    try:
        result = original_api_client.create_return_info(data)
        return ReturnInfo(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建还刀信息失败: {str(e)}")

# 修改还刀信息
@router.put("/borrowReturnInfo/returnInfo", response_model=ReturnInfo)
async def update_return_info(data: ReturnInfoUpdate):
    """
    更新还刀信息
    """
    try:
        result = original_api_client.update_return_info(data)
        return ReturnInfo(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新还刀信息失败: {str(e)}")

# 删除还刀信息
@router.delete("/borrowReturnInfo/returnInfo/{id}")
async def delete_return_info(id: int):
    """
    删除还刀信息
    """
    try:
        result = original_api_client.delete_return_info(id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除还刀信息失败: {str(e)}")

# 导出还刀信息
@router.get("/borrowReturnInfo/returnInfo/export")
async def export_return_info(query: dict = {}):
    """
    导出还刀信息
    """
    try:
        result = original_api_client.export_return_info(query)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"导出还刀信息失败: {str(e)}")

# 收刀信息管理相关接口
# 查询收刀信息列表
@router.get("/borrowReturnInfo/collectInfo/list", response_model=CollectInfoListResponse)
async def list_collect_info(page: int = 1, size: int = 10):
    """
    查询收刀信息列表
    """
    try:
        result = original_api_client.get_collect_info_list({
            "page": page,
            "size": size
        })
        return CollectInfoListResponse(
            list=[CollectInfo(**item) for item in result.get("list", [])],
            total=result.get("total", 0)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询收刀信息列表失败: {str(e)}")

# 查询收刀信息详细
@router.get("/borrowReturnInfo/collectInfo/{id}", response_model=CollectInfo)
async def get_collect_info(id: int):
    """
    查询收刀信息详情
    """
    try:
        result = original_api_client.get_collect_info(id)
        return CollectInfo(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询收刀信息详情失败: {str(e)}")

# 确认收刀操作
@router.post("/borrowReturnInfo/collectInfo/confirm")
async def confirm_collect(data: dict):
    """
    确认收刀操作
    """
    try:
        result = original_api_client.confirm_collect(data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"确认收刀操作失败: {str(e)}")

# 新增收刀信息
@router.post("/borrowReturnInfo/collectInfo", response_model=CollectInfo)
async def add_collect_info(data: CollectInfoCreate):
    """
    新增收刀信息
    """
    try:
        result = original_api_client.create_collect_info(data.dict())
        return CollectInfo(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"新增收刀信息失败: {str(e)}")

# 修改收刀信息
@router.put("/borrowReturnInfo/collectInfo", response_model=CollectInfo)
async def update_collect_info(data: CollectInfoUpdate):
    """
    修改收刀信息
    """
    try:
        result = original_api_client.update_collect_info(data.dict())
        return CollectInfo(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"修改收刀信息失败: {str(e)}")

# 删除收刀信息
@router.delete("/borrowReturnInfo/collectInfo/{id}")
async def del_collect_info(id: int):
    """
    删除收刀信息
    """
    try:
        result = original_api_client.delete_collect_info(id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除收刀信息失败: {str(e)}")

# 批量删除收刀信息
@router.delete("/borrowReturnInfo/collectInfo/batch")
async def batch_del_collect_info(ids: List[int]):
    """
    批量删除收刀信息
    """
    try:
        result = original_api_client.batch_delete_collect_info(ids)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"批量删除收刀信息失败: {str(e)}")

# 导出收刀信息
@router.get("/borrowReturnInfo/collectInfo/export")
async def export_collect_info():
    """
    导出收刀信息
    """
    try:
        result = original_api_client.export_collect_info()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"导出收刀信息失败: {str(e)}")

# 获取刀柜编码列表
@router.get("/borrowReturnInfo/collectInfo/cabinetCodes")
async def get_cabinet_code_list():
    """
    获取刀柜编码列表
    """
    try:
        result = original_api_client.get_cabinet_code_list()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取刀柜编码列表失败: {str(e)}")

# 获取库位列表
@router.get("/borrowReturnInfo/collectInfo/locations")
async def get_location_list(cabinetCode: Optional[str] = None):
    """
    获取库位列表
    """
    try:
        result = original_api_client.get_location_list(cabinetCode)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取库位列表失败: {str(e)}")

# 借还排名统计相关接口
# 查询全年取刀数量统计
@router.get("/borrowReturnInfo/rankingStatistics/yearlyQuantity", response_model=dict)
async def get_yearly_quantity_statistics(query: dict = {}):
    """
    查询全年取刀数量统计
    """
    try:
        result = original_api_client.get_yearly_quantity_statistics(query)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询全年取刀数量统计失败: {str(e)}")

# 查询全年取刀金额统计
@router.get("/borrowReturnInfo/rankingStatistics/yearlyAmount", response_model=dict)
async def get_yearly_amount_statistics(query: dict = {}):
    """
    查询全年取刀金额统计
    """
    try:
        result = original_api_client.get_yearly_amount_statistics(query)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询全年取刀金额统计失败: {str(e)}")

# 查询今年累计使用统计
@router.get("/borrowReturnInfo/rankingStatistics/yearlyUsage", response_model=dict)
async def get_yearly_usage_statistics(query: dict = {}):
    """
    查询今年累计使用统计
    """
    try:
        result = original_api_client.get_yearly_usage_statistics(query)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询今年累计使用统计失败: {str(e)}")

# 查询员工领刀排行
@router.get("/borrowReturnInfo/rankingStatistics/employeeRanking", response_model=dict)
async def get_employee_ranking_statistics(query: dict = {}):
    """
    查询员工领刀排行
    """
    try:
        result = original_api_client.get_employee_ranking_statistics(query)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询员工领刀排行失败: {str(e)}")

# 查询设备用刀排行
@router.get("/borrowReturnInfo/rankingStatistics/equipmentRanking", response_model=dict)
async def get_equipment_ranking_statistics(query: dict = {}):
    """
    查询设备用刀排行
    """
    try:
        result = original_api_client.get_equipment_ranking_statistics(query)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询设备用刀排行失败: {str(e)}")

# 查询刀具型号排行
@router.get("/borrowReturnInfo/rankingStatistics/cutterModelRanking", response_model=dict)
async def get_cutter_model_ranking_statistics(query: dict = {}):
    """
    查询刀具型号排行
    """
    try:
        result = original_api_client.get_cutter_model_ranking_statistics(query)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询刀具型号排行失败: {str(e)}")

# 查询工单排行
@router.get("/borrowReturnInfo/rankingStatistics/workOrderRanking", response_model=dict)
async def get_work_order_ranking_statistics(query: dict = {}):
    """
    查询工单排行
    """
    try:
        result = original_api_client.get_work_order_ranking_statistics(query)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询工单排行失败: {str(e)}")

# 查询异常还刀排行
@router.get("/borrowReturnInfo/rankingStatistics/abnormalReturnRanking", response_model=dict)
async def get_abnormal_return_ranking_statistics(query: dict = {}):
    """
    查询异常还刀排行
    """
    try:
        result = original_api_client.get_abnormal_return_ranking_statistics(query)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询异常还刀排行失败: {str(e)}")

# 总库存统计相关接口
# 查询总库存统计列表
@router.get("/borrowReturnInfo/totalInventoryStats/list", response_model=InventoryStatListResponse)
async def list_total_inventory_stats(page: int = 1, size: int = 10, query: dict = {}):
    """
    查询总库存统计列表
    """
    try:
        result = original_api_client.get_total_inventory_stats_list({
            "page": page,
            "size": size,
            "query": query
        })
        return InventoryStatListResponse(
            list=[TotalInventoryStat(**item) for item in result.get("list", [])],
            total=result.get("total", 0)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询总库存统计列表失败: {str(e)}")

# 查询刀具库存统计
@router.get("/borrowReturnInfo/totalInventoryStats/cutter")
async def get_cutter_inventory_stats(query: dict = {}):
    """
    查询刀具库存统计
    """
    try:
        result = original_api_client.get_cutter_inventory_stats(query)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询刀具库存统计失败: {str(e)}")

# 查询刀柄库存统计
@router.get("/borrowReturnInfo/totalInventoryStats/handle")
async def get_handle_inventory_stats(query: dict = {}):
    """
    查询刀柄库存统计
    """
    try:
        result = original_api_client.get_handle_inventory_stats(query)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询刀柄库存统计失败: {str(e)}")

# 获取库存汇总数据
@router.get("/borrowReturnInfo/totalInventoryStats/summary", response_model=InventorySummary)
async def get_inventory_summary(type: Optional[str] = None):
    """
    获取库存汇总数据
    """
    try:
        result = original_api_client.get_inventory_summary(type)
        return InventorySummary(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取库存汇总数据失败: {str(e)}")

# 导出库存统计
@router.get("/borrowReturnInfo/totalInventoryStats/export")
async def export_inventory_stats(query: dict = {}):
    """
    导出库存统计
    """
    try:
        result = original_api_client.export_inventory_stats(query)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"导出库存统计失败: {str(e)}")

# 获取品牌列表
@router.get("/borrowReturnInfo/totalInventoryStats/brands")
async def get_brand_list():
    """
    获取品牌列表
    """
    try:
        result = original_api_client.get_brand_list()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取品牌列表失败: {str(e)}")

# 获取刀具类型列表
@router.get("/borrowReturnInfo/totalInventoryStats/cutterTypes")
async def get_cutter_type_list():
    """
    获取刀具类型列表
    """
    try:
        result = original_api_client.get_cutter_type_list()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取刀具类型列表失败: {str(e)}")

# 获取刀柄类型列表
@router.get("/borrowReturnInfo/totalInventoryStats/handleTypes")
async def get_handle_type_list():
    """
    获取刀柄类型列表
    """
    try:
        result = original_api_client.get_handle_type_list()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取刀柄类型列表失败: {str(e)}")

# 获取刀柜列表
@router.get("/borrowReturnInfo/totalInventoryStats/cabinets")
async def get_cabinet_list():
    """
    获取刀柜列表
    """
    try:
        result = original_api_client.get_cabinet_list()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取刀柜列表失败: {str(e)}")

# 未还信息管理相关接口
# 查询未还信息列表
@router.get("/borrowReturnInfo/unreturnedInfo/list", response_model=UnreturnedInfoListResponse)
async def list_unreturned_info(page: int = 1, size: int = 10, query: dict = {}):
    """
    查询未还信息列表
    """
    try:
        result = original_api_client.get_unreturned_info_list({
            "page": page,
            "size": size,
            "query": query
        })
        return UnreturnedInfoListResponse(
            list=[UnreturnedInfo(**item) for item in result.get("list", [])],
            total=result.get("total", 0)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询未还信息列表失败: {str(e)}")

# 查询未还信息详细
@router.get("/borrowReturnInfo/unreturnedInfo/{id}", response_model=UnreturnedInfo)
async def get_unreturned_info(id: int):
    """
    查询未还信息详情
    """
    try:
        result = original_api_client.get_unreturned_info(id)
        return UnreturnedInfo(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询未还信息详情失败: {str(e)}")

# 新增未还信息
@router.post("/borrowReturnInfo/unreturnedInfo", response_model=UnreturnedInfo)
async def add_unreturned_info(data: UnreturnedInfoCreate):
    """
    新增未还信息
    """
    try:
        result = original_api_client.create_unreturned_info(data.dict())
        return UnreturnedInfo(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"新增未还信息失败: {str(e)}")

# 修改未还信息
@router.put("/borrowReturnInfo/unreturnedInfo", response_model=UnreturnedInfo)
async def update_unreturned_info(data: UnreturnedInfoUpdate):
    """
    修改未还信息
    """
    try:
        result = original_api_client.update_unreturned_info(data.dict())
        return UnreturnedInfo(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"修改未还信息失败: {str(e)}")

# 删除未还信息
@router.delete("/borrowReturnInfo/unreturnedInfo/{id}")
async def del_unreturned_info(id: int):
    """
    删除未还信息
    """
    try:
        result = original_api_client.delete_unreturned_info(id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除未还信息失败: {str(e)}")

# 导出未还信息
@router.get("/borrowReturnInfo/unreturnedInfo/export")
async def export_unreturned_info(query: dict = {}):
    """
    导出未还信息
    """
    try:
        result = original_api_client.export_unreturned_info(query)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"导出未还信息失败: {str(e)}")

# 统计未还信息
@router.get("/borrowReturnInfo/unreturnedInfo/statistics", response_model=UnreturnedStatistics)
async def statistics_unreturned_info(query: dict = {}):
    """
    统计未还信息
    """
    try:
        result = original_api_client.statistics_unreturned_info(query)
        return UnreturnedStatistics(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"统计未还信息失败: {str(e)}")


# 数据字典相关接口
# 刀具类型相关接口
# 查询刀具类型列表
@router.get("/dataDictionary/cutterType/list", response_model=CutterTypeListResponse)
async def list_cutter_type(page: int = 1, size: int = 10, query: dict = {}):
    """
    查询刀具类型列表
    """
    try:
        result = original_api_client.get_cutter_type_list({
            "page": page,
            "size": size,
            "query": query
        })
        return CutterTypeListResponse(
            list=[CutterType(**item) for item in result.get("list", [])],
            total=result.get("total", 0)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询刀具类型列表失败: {str(e)}")

# 查询刀具类型详细
@router.get("/dataDictionary/cutterType/{id}", response_model=CutterType)
async def get_cutter_type(id: int):
    """
    查询刀具类型详情
    """
    try:
        result = original_api_client.get_cutter_type(id)
        return CutterType(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询刀具类型详情失败: {str(e)}")

# 新增刀具类型
@router.post("/dataDictionary/cutterType", response_model=CutterType)
async def add_cutter_type(data: CutterTypeCreate):
    """
    新增刀具类型
    """
    try:
        result = original_api_client.create_cutter_type(data.dict())
        return CutterType(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"新增刀具类型失败: {str(e)}")

# 修改刀具类型
@router.put("/dataDictionary/cutterType", response_model=CutterType)
async def update_cutter_type(data: CutterTypeUpdate):
    """
    修改刀具类型
    """
    try:
        result = original_api_client.update_cutter_type(data.dict())
        return CutterType(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"修改刀具类型失败: {str(e)}")

# 删除刀具类型
@router.delete("/dataDictionary/cutterType/{id}")
async def del_cutter_type(id: int):
    """
    删除刀具类型
    """
    try:
        result = original_api_client.delete_cutter_type(id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除刀具类型失败: {str(e)}")

# 批量删除刀具类型
@router.delete("/dataDictionary/cutterType/batch")
async def batch_del_cutter_type(ids: List[int]):
    """
    批量删除刀具类型
    """
    try:
        result = original_api_client.batch_delete_cutter_type(ids)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"批量删除刀具类型失败: {str(e)}")

# 导出刀具类型
@router.get("/dataDictionary/cutterType/export")
async def export_cutter_type(query: dict = {}):
    """
    导出刀具类型
    """
    try:
        result = original_api_client.export_cutter_type(query)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"导出刀具类型失败: {str(e)}")

# 获取刀具分类列表
@router.get("/dataDictionary/cutterType/categories")
async def get_cutter_category_list():
    """
    获取刀具分类列表
    """
    try:
        result = original_api_client.get_cutter_category_list()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取刀具分类列表失败: {str(e)}")

# 获取父级刀具类型列表
@router.get("/dataDictionary/cutterType/parents")
async def get_parent_cutter_type_list():
    """
    获取父级刀具类型列表
    """
    try:
        result = original_api_client.get_parent_cutter_type_list()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取父级刀具类型列表失败: {str(e)}")


# 字典集合相关接口
# 查询字典集合列表
@router.get("/dataDictionary/dictCollection/list", response_model=DictCollectionListResponse)
async def list_dict_collection(page: int = 1, size: int = 10, query: dict = {}):
    """
    查询字典集合列表
    """
    try:
        result = original_api_client.get_dict_collection_list({
            "page": page,
            "size": size,
            "query": query
        })
        return DictCollectionListResponse(
            list=[DictCollection(**item) for item in result.get("list", [])],
            total=result.get("total", 0)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询字典集合列表失败: {str(e)}")

# 查询字典集合详细
@router.get("/dataDictionary/dictCollection/{id}", response_model=DictCollection)
async def get_dict_collection(id: int):
    """
    查询字典集合详情
    """
    try:
        result = original_api_client.get_dict_collection(id)
        return DictCollection(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询字典集合详情失败: {str(e)}")

# 根据主键集合查询字典集合
@router.get("/dataDictionary/dictCollection/code", response_model=DictCollection)
async def get_dict_collection_by_code(code: str):
    """
    根据编码查询字典集合
    """
    try:
        result = original_api_client.get_dict_collection_by_code(code)
        return DictCollection(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"根据编码查询字典集合失败: {str(e)}")

# 新增字典集合
@router.post("/dataDictionary/dictCollection", response_model=DictCollection)
async def add_dict_collection(data: DictCollectionCreate):
    """
    新增字典集合
    """
    try:
        result = original_api_client.create_dict_collection(data.dict())
        return DictCollection(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"新增字典集合失败: {str(e)}")

# 修改字典集合
@router.put("/dataDictionary/dictCollection", response_model=DictCollection)
async def update_dict_collection(data: DictCollectionUpdate):
    """
    修改字典集合
    """
    try:
        result = original_api_client.update_dict_collection(data.dict())
        return DictCollection(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"修改字典集合失败: {str(e)}")

# 删除字典集合
@router.delete("/dataDictionary/dictCollection/{id}")
async def del_dict_collection(id: int):
    """
    删除字典集合
    """
    try:
        result = original_api_client.delete_dict_collection(id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除字典集合失败: {str(e)}")

# 批量删除字典集合
@router.delete("/dataDictionary/dictCollection/batch")
async def batch_del_dict_collection(ids: List[int]):
    """
    批量删除字典集合
    """
    try:
        result = original_api_client.batch_delete_dict_collection(ids)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"批量删除字典集合失败: {str(e)}")

# 导出字典集合
@router.get("/dataDictionary/dictCollection/export")
async def export_dict_collection(query: dict = {}):
    """
    导出字典集合
    """
    try:
        result = original_api_client.export_dict_collection(query)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"导出字典集合失败: {str(e)}")

# 获取字典类型列表
@router.get("/dataDictionary/dictCollection/types")
async def get_dict_type_list():
    """
    获取字典类型列表
    """
    try:
        result = original_api_client.get_dict_type_list()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取字典类型列表失败: {str(e)}")

# 获取父级字典列表
@router.get("/dataDictionary/dictCollection/parents")
async def get_parent_dict_list():
    """
    获取父级字典列表
    """
    try:
        result = original_api_client.get_parent_dict_list()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取父级字典列表失败: {str(e)}")


# 个性化设置相关接口
# 查询个性化设置列表
@router.get("/dataDictionary/personalizedSettings/list", response_model=PersonalizedSettingsListResponse)
async def list_personalized_settings(page: int = 1, size: int = 10, query: dict = {}):
    """
    查询个性化设置列表
    """
    try:
        result = original_api_client.get_personalized_settings_list({
            "page": page,
            "size": size,
            "query": query
        })
        return PersonalizedSettingsListResponse(
            list=[PersonalizedSettings(**item) for item in result.get("list", [])],
            total=result.get("total", 0)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询个性化设置列表失败: {str(e)}")

# 查询个性化设置详细
@router.get("/dataDictionary/personalizedSettings/{id}", response_model=PersonalizedSettings)
async def get_personalized_settings(id: int):
    """
    查询个性化设置详情
    """
    try:
        result = original_api_client.get_personalized_settings(id)
        return PersonalizedSettings(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询个性化设置详情失败: {str(e)}")

# 新增个性化设置
@router.post("/dataDictionary/personalizedSettings", response_model=PersonalizedSettings)
async def add_personalized_settings(data: PersonalizedSettingsCreate):
    """
    新增个性化设置
    """
    try:
        result = original_api_client.create_personalized_settings(data.dict())
        return PersonalizedSettings(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"新增个性化设置失败: {str(e)}")

# 修改个性化设置
@router.put("/dataDictionary/personalizedSettings", response_model=PersonalizedSettings)
async def update_personalized_settings(data: PersonalizedSettingsUpdate):
    """
    修改个性化设置
    """
    try:
        result = original_api_client.update_personalized_settings(data.dict())
        return PersonalizedSettings(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"修改个性化设置失败: {str(e)}")

# 删除个性化设置
@router.delete("/dataDictionary/personalizedSettings/{id}")
async def del_personalized_settings(id: int):
    """
    删除个性化设置
    """
    try:
        result = original_api_client.delete_personalized_settings(id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除个性化设置失败: {str(e)}")

# 批量删除个性化设置
@router.delete("/dataDictionary/personalizedSettings/batch")
async def batch_del_personalized_settings(ids: List[int]):
    """
    批量删除个性化设置
    """
    try:
        result = original_api_client.batch_delete_personalized_settings(ids)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"批量删除个性化设置失败: {str(e)}")

# 导出个性化设置
@router.get("/dataDictionary/personalizedSettings/export")
async def export_personalized_settings(query: dict = {}):
    """
    导出个性化设置
    """
    try:
        result = original_api_client.export_personalized_settings(query)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"导出个性化设置失败: {str(e)}")

# 获取设置类型列表
@router.get("/dataDictionary/personalizedSettings/types")
async def get_setting_type_list():
    """
    获取设置类型列表
    """
    try:
        result = original_api_client.get_setting_type_list()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取设置类型列表失败: {str(e)}")

# 获取配置分组列表
@router.get("/dataDictionary/personalizedSettings/groups")
async def get_config_group_list():
    """
    获取配置分组列表
    """
    try:
        result = original_api_client.get_config_group_list()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取配置分组列表失败: {str(e)}")


# 历史记录相关接口
# 操作日志相关接口
# 分页查询操作日志
@router.get("/qw/knife/web/from/mes/record/operationLog", response_model=OperationLogListResponse)
async def get_operation_log_list(page: int = 1, size: int = 10, query: dict = {}):
    """
    分页查询操作日志
    """
    try:
        result = original_api_client.get_operation_log_list({
            "page": page,
            "size": size,
            "query": query
        })
        return OperationLogListResponse(
            list=[OperationLog(**item) for item in result.get("list", [])],
            total=result.get("total", 0)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"分页查询操作日志失败: {str(e)}")

# 导出操作日志数据
@router.get("/qw/knife/web/from/mes/record/exportOperationLog")
async def export_operation_log(query: dict = {}):
    """
    导出操作日志数据
    """
    try:
        result = original_api_client.export_operation_log(query)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"导出操作日志数据失败: {str(e)}")

# 获取操作日志详情
@router.get("/qw/knife/web/from/mes/record/operationLog/{id}", response_model=OperationLog)
async def get_operation_log_detail(id: int):
    """
    获取操作日志详情
    """
    try:
        result = original_api_client.get_operation_log_detail(id)
        return OperationLog(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取操作日志详情失败: {str(e)}")

# 查询操作日志统计信息
@router.get("/qw/knife/web/from/mes/record/operationLog/stats", response_model=OperationLogStats)
async def get_operation_log_stats(query: dict = {}):
    """
    查询操作日志统计信息
    """
    try:
        result = original_api_client.get_operation_log_stats(query)
        return OperationLogStats(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询操作日志统计信息失败: {str(e)}")

# 批量删除操作日志
@router.delete("/qw/knife/web/from/mes/record/operationLog")
async def delete_operation_logs(ids: List[int]):
    """
    批量删除操作日志
    """
    try:
        result = original_api_client.delete_operation_logs(ids)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"批量删除操作日志失败: {str(e)}")

# 清理过期操作日志
@router.post("/qw/knife/web/from/mes/record/operationLog/clean")
async def clean_expired_logs(days: int):
    """
    清理过期操作日志
    """
    try:
        result = original_api_client.clean_expired_logs(days)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"清理过期操作日志失败: {str(e)}")


# 公共暂存记录相关接口
# 分页查询公共暂存记录
@router.get("/qw/knife/web/from/mes/record/publicStorage", response_model=PublicStorageRecordListResponse)
async def get_public_storage_list(page: int = 1, size: int = 10, query: dict = {}):
    """
    分页查询公共暂存记录
    """
    try:
        result = original_api_client.get_public_storage_list({
            "page": page,
            "size": size,
            "query": query
        })
        return PublicStorageRecordListResponse(
            list=[PublicStorageRecord(**item) for item in result.get("list", [])],
            total=result.get("total", 0)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"分页查询公共暂存记录失败: {str(e)}")

# 导出公共暂存记录
@router.get("/qw/knife/web/from/mes/record/exportPublicStorage")
async def export_public_storage(query: dict = {}):
    """
    导出公共暂存记录
    """
    try:
        result = original_api_client.export_public_storage(query)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"导出公共暂存记录失败: {str(e)}")

# 获取公共暂存记录详情
@router.get("/qw/knife/web/from/mes/record/publicStorage/{id}", response_model=PublicStorageRecord)
async def get_public_storage_detail(id: int):
    """
    获取公共暂存记录详情
    """
    try:
        result = original_api_client.get_public_storage_detail(id)
        return PublicStorageRecord(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取公共暂存记录详情失败: {str(e)}")

# 查询公共暂存记录统计信息
@router.get("/qw/knife/web/from/mes/record/publicStorage/stats", response_model=PublicStorageRecordStats)
async def get_public_storage_stats(query: dict = {}):
    """
    查询公共暂存记录统计信息
    """
    try:
        result = original_api_client.get_public_storage_stats(query)
        return PublicStorageRecordStats(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询公共暂存记录统计信息失败: {str(e)}")

# 批量删除公共暂存记录
@router.delete("/qw/knife/web/from/mes/record/publicStorage")
async def delete_public_storage_records(ids: List[int]):
    """
    批量删除公共暂存记录
    """
    try:
        result = original_api_client.delete_public_storage_records(ids)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"批量删除公共暂存记录失败: {str(e)}")

# 创建公共暂存记录
@router.post("/qw/knife/web/from/mes/record/publicStorage", response_model=PublicStorageRecord)
async def create_public_storage_record(data: PublicStorageRecordCreate):
    """
    创建公共暂存记录
    """
    try:
        result = original_api_client.create_public_storage_record(data.dict())
        return PublicStorageRecord(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建公共暂存记录失败: {str(e)}")

# 更新公共暂存记录
@router.put("/qw/knife/web/from/mes/record/publicStorage", response_model=PublicStorageRecord)
async def update_public_storage_record(data: PublicStorageRecordUpdate):
    """
    更新公共暂存记录
    """
    try:
        result = original_api_client.update_public_storage_record(data.dict())
        return PublicStorageRecord(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新公共暂存记录失败: {str(e)}")

# 批量处理公共暂存记录
@router.post("/qw/knife/web/from/mes/record/publicStorage/batch")
async def batch_process_public_storage(data: dict):
    """
    批量处理公共暂存记录
    """
    try:
        result = original_api_client.batch_process_public_storage(data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"批量处理公共暂存记录失败: {str(e)}")


# 补货记录相关接口
# 分页查询补货记录
@router.get("/qw/knife/web/from/mes/record/restockRecord", response_model=RestockRecordListResponse)
async def get_restock_record_list(page: int = 1, size: int = 10, query: dict = {}):
    """
    分页查询补货记录
    """
    try:
        result = original_api_client.get_restock_record_list({
            "page": page,
            "size": size,
            "query": query
        })
        return RestockRecordListResponse(
            list=[RestockRecord(**item) for item in result.get("list", [])],
            total=result.get("total", 0)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"分页查询补货记录失败: {str(e)}")

# 导出补货记录
@router.get("/qw/knife/web/from/mes/record/exportRestockRecord")
async def export_restock_record(query: dict = {}):
    """
    导出补货记录
    """
    try:
        result = original_api_client.export_restock_record(query)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"导出补货记录失败: {str(e)}")

# 获取补货记录详情
@router.get("/qw/knife/web/from/mes/record/restockRecord/{id}", response_model=RestockRecord)
async def get_restock_record_detail(id: int):
    """
    获取补货记录详情
    """
    try:
        result = original_api_client.get_restock_record_detail(id)
        return RestockRecord(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取补货记录详情失败: {str(e)}")

# 查询补货记录统计信息
@router.get("/qw/knife/web/from/mes/record/restockRecord/stats", response_model=RestockRecordStats)
async def get_restock_record_stats(query: dict = {}):
    """
    查询补货记录统计信息
    """
    try:
        result = original_api_client.get_restock_record_stats(query)
        return RestockRecordStats(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询补货记录统计信息失败: {str(e)}")

# 批量删除补货记录
@router.delete("/qw/knife/web/from/mes/record/restockRecord")
async def delete_restock_records(ids: List[int]):
    """
    批量删除补货记录
    """
    try:
        result = original_api_client.delete_restock_records(ids)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"批量删除补货记录失败: {str(e)}")

# 创建补货记录
@router.post("/qw/knife/web/from/mes/record/restockRecord", response_model=RestockRecord)
async def create_restock_record(data: RestockRecordCreate):
    """
    创建补货记录
    """
    try:
        result = original_api_client.create_restock_record(data.dict())
        return RestockRecord(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建补货记录失败: {str(e)}")

# 更新补货记录
@router.put("/qw/knife/web/from/mes/record/restockRecord", response_model=RestockRecord)
async def update_restock_record(data: RestockRecordUpdate):
    """
    更新补货记录
    """
    try:
        result = original_api_client.update_restock_record(data.dict())
        return RestockRecord(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新补货记录失败: {str(e)}")


# 出入库记录相关接口
# 分页查询出入库记录
@router.get("/qw/knife/web/from/mes/record/stockRecord", response_model=StockRecordListResponse)
async def get_stock_record_list(page: int = 1, size: int = 10, query: dict = {}):
    """
    分页查询出入库记录
    """
    try:
        result = original_api_client.get_stock_record_list({
            "page": page,
            "size": size,
            "query": query
        })
        return StockRecordListResponse(
            list=[StockRecord(**item) for item in result.get("list", [])],
            total=result.get("total", 0)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"分页查询出入库记录失败: {str(e)}")

# 导出出入库记录
@router.get("/qw/knife/web/from/mes/record/exportStockRecord")
async def export_stock_record(query: dict = {}):
    """
    导出出入库记录
    """
    try:
        result = original_api_client.export_stock_record(query)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"导出出入库记录失败: {str(e)}")

# 获取出入库记录详情
@router.get("/qw/knife/web/from/mes/record/stockRecord/{id}", response_model=StockRecord)
async def get_stock_record_detail(id: int):
    """
    获取出入库记录详情
    """
    try:
        result = original_api_client.get_stock_record_detail(id)
        return StockRecord(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取出入库记录详情失败: {str(e)}")

# 查询出入库记录统计信息
@router.get("/qw/knife/web/from/mes/record/stockRecord/stats", response_model=StockRecordStats)
async def get_stock_record_stats(query: dict = {}):
    """
    查询出入库记录统计信息
    """
    try:
        result = original_api_client.get_stock_record_stats(query)
        return StockRecordStats(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询出入库记录统计信息失败: {str(e)}")

# 批量删除出入库记录
@router.delete("/qw/knife/web/from/mes/record/stockRecord")
async def delete_stock_records(ids: List[int]):
    """
    批量删除出入库记录
    """
    try:
        result = original_api_client.delete_stock_records(ids)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"批量删除出入库记录失败: {str(e)}")