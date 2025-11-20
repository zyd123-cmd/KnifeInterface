from fastapi import APIRouter, Depends, Query, Response, Body
from typing import Optional, List
from auditor_record.schemas.data_schemas import (
    ReplenishRecordResponse, 
    LendRecordResponse, 
    StorageRecordResponse,
    AlarmWarningResponse,
    ReplenishRecordListRequest,
    ExportReplenishRecordRequest,
    LendRecordListRequest,
    ExportLendRecordRequest,
    StorageRecordListRequest,
    ExportStorageRecordRequest,
    AlarmWarningListRequest
)
from auditor_record.services.api_client import api_client
import json

router = APIRouter(prefix="/auditor_record", tags=["刀具管理"])

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
        ReplenishRecordResponse: 补货记录响应数据
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

@router.get("/export_replenish")
async def export_replenish_records(
    end_time: Optional[str] = Query(None, description="结束时间"),
    order: Optional[int] = Query(None, description="顺序 0: 从大到小 1：从小到大"),
    ranking_type: Optional[int] = Query(None, description="0: 数量 1: 金额"),
    record_status: Optional[int] = Query(None, description="0: 取刀 1: 还刀 2: 收刀 3: 暂存 4: 完成 5：违规还刀"),
    start_time: Optional[str] = Query(None, description="开始时间")
):
    """
    导出补货记录
    
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
        file_content = api_client.export_replenish_records(
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
                "Content-Disposition": "attachment; filename=replenish_records.xlsx"
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

@router.get("/list", response_model=LendRecordResponse)
async def get_lend_record_list(
    current: int = Query(1, ge=1, description="页码"),
    size: int = Query(20, ge=1, le=100, description="每页数量"),
    keyword: Optional[str] = Query(None, description="关键字搜索"),
    department: Optional[str] = Query(None, description="部门筛选"),
    startTime: Optional[str] = Query(None, description="开始时间"),
    endTime: Optional[str] = Query(None, description="结束时间"),
    order: Optional[int] = Query(None, description="顺序 0: 从大到小 1：从小到大"),
    rankingType: Optional[int] = Query(None, description="0: 数量 1: 金额"),
    recordStatus: Optional[int] = Query(None, description="0: 取刀 1: 还刀 2: 收刀 3: 暂存 4: 完成 5：违规还刀")
):
    """
    获取领刀记录列表
    
    Args:
        current: 页码，默认为1
        size: 每页数量，默认为20，最大100
        keyword: 关键字搜索
        department: 部门筛选
        startTime: 开始时间
        endTime: 结束时间
        order: 顺序 0: 从大到小 1：从小到大
        rankingType: 0: 数量 1: 金额
        recordStatus: 0: 取刀 1: 还刀 2: 收刀 3: 暂存 4: 完成 5：违规还刀
        
    Returns:
        LendRecordResponse: 领刀记录响应数据
    """
    result = api_client.get_lend_records(
        current=current,
        size=size,
        keyword=keyword,
        department=department,
        startTime=startTime,
        endTime=endTime,
        order=order,
        rankingType=rankingType,
        recordStatus=recordStatus
    )
    
    return result

@router.get("/export")
async def export_lend_records(
    endTime: Optional[str] = Query(None, description="结束时间"),
    order: Optional[int] = Query(None, description="顺序 0: 从大到小 1：从小到大"),
    rankingType: Optional[int] = Query(None, description="0: 数量 1: 金额"),
    recordStatus: Optional[int] = Query(None, description="0: 取刀 1: 还刀 2: 收刀 3: 暂存 4: 完成 5：违规还刀"),
    startTime: Optional[str] = Query(None, description="开始时间")
):
    """
    导出领刀记录
    
    Args:
        endTime: 结束时间
        order: 顺序 0: 从大到小 1：从小到大
        rankingType: 0: 数量 1: 金额
        recordStatus: 0: 取刀 1: 还刀 2: 收刀 3: 暂存 4: 完成 5：违规还刀
        startTime: 开始时间
        
    Returns:
        Response: 包含导出文件的响应
    """
    try:
        file_content = api_client.export_lend_records(
            endTime=endTime,
            order=order,
            rankingType=rankingType,
            recordStatus=recordStatus,
            startTime=startTime
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
        StorageRecordResponse: 公共暂存记录响应数据
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

@router.get("/export_storage")
async def export_storage_records(
    end_time: Optional[str] = Query(None, description="结束时间"),
    order: Optional[int] = Query(None, description="顺序 0: 从大到小 1：从小到大"),
    ranking_type: Optional[int] = Query(None, description="0: 数量 1: 金额"),
    record_status: Optional[int] = Query(None, description="0: 取刀 1: 还刀 2: 收刀 3: 暂存 4: 完成 5：违规还刀"),
    start_time: Optional[str] = Query(None, description="开始时间")
):
    """
    导出公共暂存记录
    
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
        file_content = api_client.export_storage_records(
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
                "Content-Disposition": "attachment; filename=storage_records.xlsx"
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

@router.get("/alarm_list", response_model=AlarmWarningResponse)
async def list_alarm_warning(
    loc_surplus: Optional[int] = Query(None, description="货道"),
    alarm_level: Optional[int] = Query(None, description="预警等级"),
    device_type: Optional[str] = Query(None, description="设备类型"),
    cabinet_code: Optional[str] = Query(None, description="刀柜编码"),
    brand_name: Optional[str] = Query(None, description="品牌名称"),
    handle_status: Optional[int] = Query(None, description="处理状态"),
    current: Optional[int] = Query(None, description="当前页"),
    size: Optional[int] = Query(None, description="每页数量")
):
    """
    获取告警预警列表
    
    Args:
        loc_surplus: 货道
        alarm_level: 预警等级
        device_type: 设备类型
        cabinet_code: 刀柜编码
        brand_name: 品牌名称
        handle_status: 处理状态
        current: 当前页
        size: 每页数量
        
    Returns:
        AlarmWarningResponse: 告警预警响应数据
    """
    result = api_client.get_alarm_warnings(
        locSurplus=loc_surplus,
        alarmLevel=alarm_level,
        deviceType=device_type,
        cabinetCode=cabinet_code,
        brandName=brand_name,
        handleStatus=handle_status,
        current=current,
        size=size
    )
    
    return result

# 刀柜相关路由
@router.post("/cabinet/stock_bind_cutter")
async def stock_bind_cutter(
    cutter_id: Optional[int] = Query(None, description="耗材主键"),
    is_ban: Optional[int] = Query(None, description="是否禁用（0:非禁用 1:禁用）"),
    loc_capacity: Optional[int] = Query(None, description="货道容量"),
    loc_pack_qty: Optional[int] = Query(None, description="货道包装数量"),
    loc_surplus: Optional[int] = Query(None, description="货道刀具数量"),
    stock_id: Optional[int] = Query(None, description="刀柜货道主键"),
    warning_num: Optional[int] = Query(None, description="警报数量")
):
    """
    刀柜货道 绑定/补货 刀具
    
    Args:
        cutter_id: 耗材主键
        is_ban: 是否禁用（0:非禁用 1:禁用）
        loc_capacity: 货道容量
        loc_pack_qty: 货道包装数量
        loc_surplus: 货道刀具数量
        stock_id: 刀柜货道主键
        warning_num: 警报数量
        
    Returns:
        Response: 绑定/补货结果响应
    """
    result = api_client.stock_bind_cutter(
        cutterId=cutter_id,
        isBan=is_ban,
        locCapacity=loc_capacity,
        locPackQty=loc_pack_qty,
        locSurplus=loc_surplus,
        stockId=stock_id,
        warningNum=warning_num
    )
    
    return result

@router.get("/cabinet/personal_storage")
async def get_personal_storage(
    cabinet_code: Optional[str] = Query(None, description="刀柜编码")
):
    """
    获取个人暂存柜
    
    Args:
        cabinet_code: 刀柜编码
        
    Returns:
        Response: 个人暂存柜信息响应
    """
    result = api_client.get_personal_storage(
        cabinetCode=cabinet_code
    )
    
    return result

@router.get("/cabinet/make_alarm")
async def make_alarm(
    cabinet_code: Optional[str] = Query(None, description="刀柜编码"),
    make_alarm: Optional[int] = Query(None, description="警值预设")
):
    """
    取刀柜库存告警值预设
    
    Args:
        cabinet_code: 刀柜编码
        make_alarm: 警值预设
        
    Returns:
        Response: 设置结果响应
    """
    result = api_client.make_alarm(
        cabinetCode=cabinet_code,
        makeAlarm=make_alarm
    )
    
    return result

@router.get("/cabinet/get_make_alarm")
async def get_make_alarm(
    cabinet_code: Optional[str] = Query(None, description="刀柜编码")
):
    """
    获取取刀柜库存告警值预设
    
    Args:
        cabinet_code: 刀柜编码
        
    Returns:
        Response: 告警值预设信息响应
    """
    result = api_client.get_make_alarm(
        cabinetCode=cabinet_code
    )
    
    return result