from fastapi import APIRouter, Depends, Query, Response
from typing import Optional
from lend_record.schemas.data_schemas import (
    LendRecordResponse, 
    LendRecordListRequest,
    ExportLendRecordRequest
)
from lend_record.services.api_client import api_client
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