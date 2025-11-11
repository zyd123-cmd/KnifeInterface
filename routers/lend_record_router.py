from fastapi import APIRouter, Depends, Query, Response, Body
from typing import Optional, List
from auditor.schemas.data_schemas import (
    LendRecordResponse, 
    LendRecordListRequest,
    ExportLendRecordRequest,
    RestockRequest,
    RestockResponse,
    ReplenishRecordResponse,
    ReplenishRecordListRequest,
    StorageRecordResponse,
    StorageRecordListRequest,
    PersonalStorageResponse,
    MakeAlarmResponse,
    CabinetAlarmResponse
)
from auditor.services.api_client import api_client
import json

router = APIRouter(prefix="/lend_record", tags=["领刀记录"])

@router.get("/list", response_model=LendRecordResponse)
async def get_lend_record_list(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    keyword: Optional[str] = Query(None, description="关键字搜索"),
    department: Optional[str] = Query(None, description="部门筛选"),
    start_date: Optional[str] = Query(None, description="开始时间"),
    end_date: Optional[str] = Query(None, description="结束时间"),
    order: Optional[int] = Query(None, description="顺序 0: 从大到小 1：从小到大"),
    ranking_type: Optional[int] = Query(None, description="0: 数量 1: 金额"),
    record_status: Optional[int] = Query(None, description="0: 取刀 1: 还刀 2: 收刀 3: 暂存 4: 完成 5：违规还刀")
):
    """
    获取领刀记录列表
    
    Args:
        page: 页码，默认为1
        page_size: 每页数量，默认为20，最大100
        keyword: 关键字搜索
        department: 部门筛选
        start_date: 开始时间
        end_date: 结束时间
        order: 顺序 0: 从大到小 1：从小到大
        ranking_type: 0: 数量 1: 金额
        record_status: 0: 取刀 1: 还刀 2: 收刀 3: 暂存 4: 完成 5：违规还刀
        
    Returns:
        LendRecordResponse: 领刀记录列表响应
    """
    result = api_client.get_lend_records(
        page=page,
        page_size=page_size,
        keyword=keyword,
        department=department,
        start_date=start_date,
        end_date=end_date,
        order=order,
        rankingType=ranking_type,
        recordStatus=record_status
    )
    
    return result

@router.get("/export")
async def export_lend_records(
    end_time: Optional[str] = Query(None, description="结束时间"),
    order: Optional[int] = Query(None, description="顺序 0: 从大到小 1：从小到大"),
    ranking_type: Optional[int] = Query(None, description="0: 数量 1: 金额"),
    record_status: Optional[int] = Query(None, description="0: 取刀 1: 还刀 2: 收刀 3: 暂存 4: 完成 5：违规还刀"),
    start_time: Optional[str] = Query(None, description="开始时间")
):
    """
    导出领刀记录
    
    Args:
        end_time: 结束时间
        order: 顺序 0: 从大到小 1：从小到大
        ranking_type: 0: 数量 1: 金额
        record_status: 0: 取刀 1: 还刀 2: 收刀 3: 暂存 4: 完成 5：违规还刀
        start_time: 开始时间
        
    Returns:
        Response: 包含导出文件的响应
    """
    try:
        file_content = api_client.export_lend_records(
            endTime=end_time,
            order=order,
            rankingType=ranking_type,
            recordStatus=record_status,
            startTime=start_time
        )
        
        return Response(
            content=file_content,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Content-Disposition": "attachment; filename=lend_records.xlsx"
            }
        )
    except Exception as e:
        return Response(
            content=json.dumps({
                "code": -1,
                "msg": f"导出失败: {str(e)}",
                "data": None,
                "success": False
            }, ensure_ascii=False),
            media_type="application/json"
        )

@router.post("/restock", response_model=RestockResponse)
async def restock_cabinet(
    request: RestockRequest = Body(None, description="补货请求参数")
):
    """
    刀柜补货接口
    
    Args:
        request: 补货请求参数
        
    Returns:
        RestockResponse: 补货结果响应
    """
    result = api_client.restock_cabinet(
        cabinetCode=request.cabinetCode,
        itemDtoList=[item.dict() for item in request.itemDtoList] if request.itemDtoList else None,
        replenishDto=request.replenishDto
    )
    
    return result

@router.get("/replenish_list", response_model=ReplenishRecordResponse)
async def get_replenish_record_list(
    current: Optional[int] = Query(None, description="当前页"),
    end_time: Optional[str] = Query(None, description="结束时间"),
    order: Optional[int] = Query(None, description="顺序 0: 从大到小 1：从小到大"),
    ranking_type: Optional[int] = Query(None, description="0: 数量 1: 金额"),
    record_status: Optional[int] = Query(None, description="0: 取刀 1: 还刀 2: 收刀 3: 暂存 4: 完成 5：违规还刀"),
    size: Optional[int] = Query(None, description="每页的数量"),
    start_time: Optional[str] = Query(None, description="开始时间")
):
    """
    获取补货记录列表
    
    Args:
        current: 当前页
        end_time: 结束时间
        order: 顺序 0: 从大到小 1：从小到大
        ranking_type: 0: 数量 1: 金额
        record_status: 0: 取刀 1: 还刀 2: 收刀 3: 暂存 4: 完成 5：违规还刀
        size: 每页的数量
        start_time: 开始时间
        
    Returns:
        ReplenishRecordResponse: 补货记录列表响应
    """
    result = api_client.get_replenish_records(
        current=current,
        endTime=end_time,
        order=order,
        rankingType=ranking_type,
        recordStatus=record_status,
        size=size,
        startTime=start_time
    )
    
    return result

@router.get("/storage_list", response_model=StorageRecordResponse)
async def get_storage_record_list(
    current: Optional[int] = Query(None, description="当前页"),
    end_time: Optional[str] = Query(None, description="结束时间"),
    order: Optional[int] = Query(None, description="顺序 0: 从大到小 1：从小到大"),
    ranking_type: Optional[int] = Query(None, description="0: 数量 1: 金额"),
    record_status: Optional[int] = Query(None, description="0: 取刀 1: 还刀 2: 收刀 3: 暂存 4: 完成 5：违规还刀"),
    size: Optional[int] = Query(None, description="每页的数量"),
    start_time: Optional[str] = Query(None, description="开始时间")
):
    """
    获取公共暂存记录列表
    
    Args:
        current: 当前页
        end_time: 结束时间
        order: 顺序 0: 从大到小 1：从小到大
        ranking_type: 0: 数量 1: 金额
        record_status: 0: 取刀 1: 还刀 2: 收刀 3: 暂存 4: 完成 5：违规还刀
        size: 每页的数量
        start_time: 开始时间
        
    Returns:
        StorageRecordResponse: 公共暂存记录列表响应
    """
    result = api_client.get_storage_records(
        current=current,
        endTime=end_time,
        order=order,
        rankingType=ranking_type,
        recordStatus=record_status,
        size=size,
        startTime=start_time
    )
    
    return result

@router.get("/personal_storage", response_model=PersonalStorageResponse)
async def get_personal_storage(
    cabinet_code: Optional[str] = Query(None, description="刀柜编码")
):
    """
    获取个人暂存柜信息
    
    Args:
        cabinet_code: 刀柜编码
        
    Returns:
        PersonalStorageResponse: 个人暂存柜信息响应
    """
    result = api_client.get_personal_storage(cabinetCode=cabinet_code)
    
    return result

@router.get("/make_alarm", response_model=MakeAlarmResponse)
async def set_make_alarm(
    cabinet_code: Optional[str] = Query(None, description="刀柜编码"),
    alarm_value: Optional[int] = Query(None, description="告警值")
):
    """
    设置取刀柜告警值
    
    Args:
        cabinet_code: 刀柜编码
        alarm_value: 告警值
        
    Returns:
        MakeAlarmResponse: 设置告警值响应
    """
    result = api_client.set_make_alarm(cabinetCode=cabinet_code, alarmValue=alarm_value)
    
    return result

@router.get("/get_make_alarm", response_model=CabinetAlarmResponse)
async def get_make_alarm(
    cabinet_code: Optional[str] = Query(None, description="刀柜编码")
):
    """
    获取取刀柜告警值
    
    Args:
        cabinet_code: 刀柜编码
        
    Returns:
        CabinetAlarmResponse: 获取告警值响应
    """
    result = api_client.get_make_alarm(cabinetCode=cabinet_code)
    
    return result