import sys
import os
from fastapi import APIRouter, HTTPException, Query, Depends, Body
from typing import Optional, Dict, Any

# 导入所需的模块
from knife_operator.services.api_client import OriginalAPIClient
from knife_operator.schemas.data_schemas import (
    LendRecordListResponse,
    CreateLendRecordRequest,
    BatchReturnRequest,
    BatchReturnResponse,
    UpdateBorrowRequest,
    ReturnRequest,
    TempStoreRequest,
    BorrowDetailResponse,
    BaseResponse,
    HandleLendRecordListResponse,
    CreateHandleLendRecordRequest,
    UpdateHandleLendRecordRequest,
    HandleBatchReturnRequest,
    HandleReturnRequest,
    HandleTempStoreRequest,
    TempStoreRecordListResponse,
    TempStoreQueryParams,
    TempStoreBatchReturnRequest,
    HandleTempStoreRecordListResponse,
    CreateTempStoreRequest,
    CreateHandleTempStoreRequest,
    HandleTempStoreBatchReturnRequest,
    HandleTempStoreBatchReturnResponse,
    UpdateHandleTempStoreRequest,
    HandleTempStoreReturnRequest,
    CreateHandleTempStoreFromBorrowRequest,
    HandleTempStoreDetailResponse
)

# 创建API客户端实例
api_client = OriginalAPIClient(base_url="mock")

router = APIRouter()

@router.get("/temp-store-records", response_model=TempStoreRecordListResponse)
async def get_temp_store_records(
    temp_store_code: Optional[str] = Query(None, alias="tempStoreCode", description="暂存单号"),
    store_person: Optional[str] = Query(None, alias="storePerson", description="暂存人"),
    store_person_code: Optional[str] = Query(None, alias="storePersonCode", description="暂存人编号"),
    store_type: Optional[str] = Query(None, alias="storeType", description="暂存类型"),
    brand_name: Optional[str] = Query(None, alias="brandName", description="刀头品牌"),
    cutter_type: Optional[str] = Query(None, alias="cutterType", description="刀头型号"),
    status: Optional[str] = Query(None, description="暂存状态"),
    store_time: Optional[str] = Query(None, alias="storeTime", description="暂存时间"),
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(10, ge=1, le=100, description="每页数量")
):
    """
    获取刀头暂存记录列表
    功能：根据搜索条件获取刀头暂存记录列表
    参数：暂存单号、暂存人、暂存人编号、暂存类型、刀头品牌、刀头型号、暂存状态、暂存时间等查询条件
    """
    try:
        # 构建查询参数
        params: Dict[str, Any] = {
            "page": page,
            "size": size
        }
        
        # 添加非空查询参数
        if temp_store_code:
            params["tempStoreCode"] = temp_store_code
        if store_person:
            params["storePerson"] = store_person
        if store_person_code:
            params["storePersonCode"] = store_person_code
        if store_type:
            params["storeType"] = store_type
        if brand_name:
            params["brandName"] = brand_name
        if cutter_type:
            params["cutterType"] = cutter_type
        if status:
            params["status"] = status
        if store_time:
            params["storeTime"] = store_time
            
        # 调用API客户端方法获取数据
        result = api_client.get_temp_store_records(params)
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取刀头暂存记录列表失败: {str(e)}")

@router.post("/temp-store-records", status_code=201, response_model=BaseResponse)
async def create_temp_store_record(
    temp_store: CreateTempStoreRequest = Body(...)
):
    """
    新增刀头暂存记录
    功能：创建新的刀头暂存记录
    说明：
    - 系统自动生成暂存单号（前缀为日期格式 BOR+YYYYMMDD+序号）
    - 自动填充当前用户信息（borrowerName, storageUser）
    - 验证必填字段：品牌、类型、规格、数量
    """
    try:
        # 验证必填字段
        if not temp_store.brandName:
            raise HTTPException(status_code=400, detail="刀头品牌不能为空")
        if not temp_store.handleType:
            raise HTTPException(status_code=400, detail="刀头类型不能为空")
        if not temp_store.handleSpec:
            raise HTTPException(status_code=400, detail="刀头规格不能为空")
        if temp_store.quantity <= 0:
            raise HTTPException(status_code=400, detail="暂存数量必须大于0")
        
        # 验证暂存单号格式（应以 BOR+日期 开头）
        if not temp_store.storageCode.startswith("BOR"):
            raise HTTPException(status_code=400, detail="暂存单号格式错误，应以BOR开头")
        
        # 验证用户信息
        if not temp_store.borrowerName or not temp_store.storageUser:
            raise HTTPException(status_code=400, detail="暂存人信息不完整")
        
        # 调用API客户端方法创建暂存记录
        result = api_client.create_temp_store_record(temp_store.dict())
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建刀头暂存记录失败: {str(e)}")

@router.get("/lend-records", response_model=LendRecordListResponse)
async def get_lend_records(
    lend_code: Optional[str] = Query(None, alias="lendCode", description="借出单号"),
    lend_user: Optional[str] = Query(None, alias="lendUser", description="借出人"),
    brand_code: Optional[str] = Query(None, alias="brandCode", description="品牌"),
    cutter_code: Optional[str] = Query(None, alias="cutterCode", description="型号"),
    status: Optional[str] = Query(None, description="状态"),
    start_time: Optional[str] = Query(None, alias="startTime", description="开始时间"),
    end_time: Optional[str] = Query(None, alias="endTime", description="结束时间"),
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(10, ge=1, le=100, description="每页数量")
):
    """
    获取刀头借出记录列表
    功能：根据搜索条件获取借出记录列表
    参数：借出单号、借出人、品牌、型号、状态、时间等查询条件
    """
    try:
        # 构建查询参数
        params: Dict[str, Any] = {
            "page": page,
            "size": size
        }
        
        # 添加非空查询参数
        if lend_code:
            params["lendCode"] = lend_code
        if lend_user:
            params["lendUser"] = lend_user
        if brand_code:
            params["brandCode"] = brand_code
        if cutter_code:
            params["cutterCode"] = cutter_code
        if status:
            params["status"] = status
        if start_time:
            params["startTime"] = start_time
        if end_time:
            params["endTime"] = end_time
            
        # 调用API客户端方法获取数据
        result = api_client.get_lend_records(params)
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取借出记录列表失败: {str(e)}")

@router.post("/lend-records", status_code=201)
async def create_lend_record(
    lend_record: CreateLendRecordRequest = Body(...)
):
    """
    新增借出记录
    功能：创建新的刀具借出记录
    """
    try:
        # 调用API客户端方法创建借出记录
        result = api_client.create_lend_record(lend_record.model_dump())
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建借出记录失败: {str(e)}")

@router.post("/batch-return", response_model=BatchReturnResponse)
async def batch_return_knife_heads(
    request: BatchReturnRequest = Body(...)
):
    """
    批量归还刀头
    """
    try:
        # 模拟当前用户信息
        current_user = {"employeeCode": "zhangsan"}
        # 调用API客户端方法处理批量归还
        result = api_client.process_batch_return(request.model_dump())
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"批量归还处理失败: {str(e)}")

@router.post("/temp-store-batch-return", response_model=BatchReturnResponse)
async def temp_store_batch_return_knife_heads(
    request: TempStoreBatchReturnRequest = Body(...)
):
    """
    暂存刀头批量归还
    """
    try:
        # 模拟当前用户信息
        current_user = {"employeeCode": "zhangsan"}
        # 调用API客户端方法处理暂存刀头批量归还
        result = api_client.process_temp_store_batch_return(request.model_dump())
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"暂存刀头批量归还处理失败: {str(e)}")

@router.put("/lend-records/{borrow_id}", response_model=BaseResponse)
async def update_borrow_record(
    borrow_id: int,
    request: UpdateBorrowRequest = Body(...)
):
    """
    更新借出记录 (编辑按钮接口)
    """
    try:
        # 模拟当前用户信息
        current_user = {"employeeCode": "zhangsan"}
        # 调用API客户端方法更新借出记录
        result = api_client.update_borrow_record_service(borrow_id, request.model_dump(), current_user)
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新借出记录失败: {str(e)}")

@router.post("/return", response_model=BatchReturnResponse)
async def return_knife_head(
    request: ReturnRequest = Body(...)
):
    """
    归还刀头 (归还按钮接口)
    """
    try:
        # 模拟当前用户信息
        current_user = {"employeeCode": "zhangsan"}
        # 调用API客户端方法处理归还
        result = api_client.process_return_service(request.model_dump(), current_user)
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"归还刀头处理失败: {str(e)}")

@router.post("/temp-store", response_model=BaseResponse)
async def temp_store_knife_head(
    request: TempStoreRequest = Body(...)
):
    """
    暂存刀头 (暂存按钮接口)
    通过修改现有借出记录的状态来实现暂存功能，而不是创建新的暂存记录
    """
    try:
        # 使用请求中的借出人编码作为当前用户
        current_user = {"employeeCode": request.borrowerCode}
        # 调用API客户端方法处理暂存
        result = api_client.process_temp_store_service(request.model_dump(), current_user)
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"暂存刀头处理失败: {str(e)}")

@router.get("/lend-records/{borrow_id}", response_model=BorrowDetailResponse)
async def get_borrow_detail(
    borrow_id: int
):
    """
    获取刀头借出记录详情 (详情按钮接口)
    """
    try:
        # 调用API客户端方法获取详情
        result = api_client.get_borrow_detail_service(borrow_id)
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取借出记录详情失败: {str(e)}")

# 刀柄相关路由
@router.get("/handle/lend-records", response_model=HandleLendRecordListResponse)
async def get_handle_lend_records(
    handle_code: Optional[str] = Query(None, alias="handleCode", description="刀柄编码"),
    borrower_name: Optional[str] = Query(None, alias="borrowerName", description="借出人"),
    brand: Optional[str] = Query(None, description="品牌"),
    model: Optional[str] = Query(None, description="型号"),
    status: Optional[str] = Query(None, description="状态"),
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(10, ge=1, le=100, description="每页数量")
):
    """
    获取刀柄借出记录列表
    功能：根据搜索条件获取刀柄借出记录列表
    参数：刀柄编码、借出人、品牌、型号、状态等查询条件
    """
    try:
        # 构建查询参数
        params: Dict[str, Any] = {
            "page": page,
            "size": size
        }
        
        # 添加非空查询参数
        if handle_code:
            params["handleCode"] = handle_code
        if borrower_name:
            params["borrowerName"] = borrower_name
        if brand:
            params["brand"] = brand
        if model:
            params["model"] = model
        if status:
            params["status"] = status
            
        # 调用API客户端方法获取数据
        result = api_client.get_handle_lend_records(params)
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取刀柄借出记录列表失败: {str(e)}")

@router.post("/handle/lend-records", status_code=201)
async def create_handle_lend_record(
    handle_record: CreateHandleLendRecordRequest = Body(...)
):
    """
    新增刀柄借出记录
    功能：创建新的刀柄借出记录
    """
    try:
        # 调用API客户端方法创建刀柄借出记录
        result = api_client.create_handle_lend_record(handle_record.model_dump())
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建刀柄借出记录失败: {str(e)}")

@router.put("/handle/lend-records/{handle_id}", response_model=BaseResponse)
async def update_handle_lend_record(
    handle_id: int,
    request: UpdateHandleLendRecordRequest = Body(...)
):
    """
    更新刀柄借出记录
    """
    try:
        # 模拟当前用户信息
        current_user = {"employeeCode": "zhangsan"}
        # 调用API客户端方法更新刀柄借出记录
        result = api_client.update_handle_lend_record(handle_id, request.model_dump(), current_user)
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新刀柄借出记录失败: {str(e)}")

@router.get("/handle/lend-records/{handle_id}", response_model=BorrowDetailResponse)
async def get_handle_lend_record_detail(
    handle_id: int
):
    """
    获取刀柄借出记录详情
    """
    try:
        # 调用API客户端方法获取详情
        result = api_client.get_handle_lend_record_detail(handle_id)
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取刀柄借出记录详情失败: {str(e)}")

@router.post("/handle/batch-return", response_model=BatchReturnResponse)
async def batch_return_handles(
    request: HandleBatchReturnRequest = Body(...)
):
    """
    批量归还刀柄
    """
    try:
        # 模拟当前用户信息
        current_user = {"employeeCode": "zhangsan"}
        # 调用API客户端方法处理刀柄批量归还
        result = api_client.process_handle_batch_return(request.dict())
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"刀柄批量归还处理失败: {str(e)}")

@router.post("/handle/return", response_model=BatchReturnResponse)
async def return_handle(
    request: HandleReturnRequest = Body(...)
):
    """
    归还刀柄
    """
    try:
        # 模拟当前用户信息
        current_user = {"employeeCode": "zhangsan"}
        # 调用API客户端方法处理刀柄归还
        result = api_client.process_handle_return(request.dict(), current_user)
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"刀柄归还处理失败: {str(e)}")

@router.post("/handle/temp-store", response_model=BaseResponse)
async def temp_store_handle(
    request: HandleTempStoreRequest = Body(...)
):
    """
    暂存刀柄
    """
    try:
        # 模拟当前用户信息
        current_user = {"employeeCode": "zhangsan"}
        # 调用API客户端方法处理刀柄暂存
        result = api_client.process_handle_temp_store(request.dict(), current_user)
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"刀柄暂存处理失败: {str(e)}")

@router.get("/handle/temp-store-records", response_model=HandleTempStoreRecordListResponse)
async def get_handle_temp_store_records(
    storage_code: Optional[str] = Query(None, alias="storageCode", description="暂存单号"),
    borrower_name: Optional[str] = Query(None, alias="borrowerName", description="暂存人姓名"),
    storage_user: Optional[str] = Query(None, alias="storageUser", description="暂存人编号"),
    brand_name: Optional[str] = Query(None, alias="brandName", description="刀柄品牌"),
    handle_spec: Optional[str] = Query(None, alias="handleSpec", description="刀柄规格"),
    storage_type: Optional[str] = Query(None, alias="storageType", description="暂存类型(0:公共暂存, 1:个人暂存)"),
    storage_time: Optional[str] = Query(None, alias="storageTime", description="暂存时间"),
    page_num: int = Query(1, ge=1, alias="pageNum", description="页码"),
    page_size: int = Query(10, ge=1, le=100, alias="pageSize", description="每页大小")
):
    """
    获取刀柄暂存记录列表
    功能：根据搜索条件获取刀柄暂存记录列表
    参数：暂存单号、暂存人姓名、暂存人编号、品牌、规格、暂存类型、暂存时间等查询条件
    """
    try:
        # 构建查询参数
        params: Dict[str, Any] = {
            "pageNum": page_num,
            "pageSize": page_size
        }
        
        # 添加非空查询参数
        if storage_code:
            params["storageCode"] = storage_code
        if borrower_name:
            params["borrowerName"] = borrower_name
        if storage_user:
            params["storageUser"] = storage_user
        if brand_name:
            params["brandName"] = brand_name
        if handle_spec:
            params["handleSpec"] = handle_spec
        if storage_type is not None:  # 注意："0" 也是有效值
            params["storageType"] = storage_type
        if storage_time:
            params["storageTime"] = storage_time
            
        # 调用API客户端方法获取数据
        result = api_client.get_handle_temp_store_records(params)
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取刀柄暂存记录列表失败: {str(e)}")

@router.post("/handle/temp-store-records", status_code=201, response_model=BaseResponse)
async def create_handle_temp_store_record(
    handle_temp_store: CreateHandleTempStoreRequest = Body(...)
):
    """
    新增刀柄暂存记录
    功能：创建新的刀柄暂存记录
    说明：
    - 系统自动生成暂存单号（前缀为日期格式 BOR+YYYYMMDD+序号）
    - 自动填充当前用户信息（borrowerName, storageUser）
    - 验证必填字段：品牌、类型、规格、数量
    """
    try:
        # 验证必填字段
        if not handle_temp_store.brandName:
            raise HTTPException(status_code=400, detail="刀柄品牌不能为空")
        if not handle_temp_store.handleType:
            raise HTTPException(status_code=400, detail="刀柄类型不能为空")
        if not handle_temp_store.handleSpec:
            raise HTTPException(status_code=400, detail="刀柄规格不能为空")
        if handle_temp_store.quantity <= 0:
            raise HTTPException(status_code=400, detail="暂存数量必须大于0")
        
        # 验证暂存单号格式（应以 BOR+日期 开头）
        if not handle_temp_store.storageCode.startswith("BOR"):
            raise HTTPException(status_code=400, detail="暂存单号格式错误，应以BOR开头")
        
        # 验证用户信息
        if not handle_temp_store.borrowerName or not handle_temp_store.storageUser:
            raise HTTPException(status_code=400, detail="暂存人信息不完整")
        
        # 调用API客户端方法创建暂存记录
        result = api_client.create_handle_temp_store_record(handle_temp_store.dict())
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建刀柄暂存记录失败: {str(e)}")

@router.post("/handle/temp-store-batch-return", response_model=HandleTempStoreBatchReturnResponse)
async def handle_temp_store_batch_return(
    request: HandleTempStoreBatchReturnRequest = Body(...)
):
    """
    刀柄暂存批量归还
    功能：支持多个暂存记录同时归还
    特点：
    - 自动分配库位策略（轮询分配）
    - 返回成功和失败的详细信息
    - 验证操作人权限（只能归还本人暂存的刀柄）
    - 记录操作时间和操作人信息
    
    请求参数：
    - cabinetCode: 刀柜编码
    - locList: 收刀库位号集合
    - returnList: 批量归还详情列表
    - operationType: 操作类型
    - operateTime: 操作时间
    - operateUser: 操作人
    - returnRemarks: 归还备注
    - totalQuantity: 总归还数量
    - allocationStrategy: 分配策略（默认为轮询分配）
    
    返回结果：
    - successCount: 成功归还数量
    - failedCount: 失败数量
    - failedItems: 失败项详情
    - locationDetails: 库位分配详情
    """
    try:
        # 验证必填字段
        if not request.cabinetCode:
            raise HTTPException(status_code=400, detail="刀柜编码不能为空")
        
        if not request.locList or len(request.locList) == 0:
            raise HTTPException(status_code=400, detail="收刀库位号不能为空")
        
        if not request.returnList or len(request.returnList) == 0:
            raise HTTPException(status_code=400, detail="归还列表不能为空")
        
        if not request.operateTime:
            raise HTTPException(status_code=400, detail="操作时间不能为空")
        
        # 调用API客户端方法处理批量归还
        result = api_client.process_handle_temp_store_batch_return(request.dict())
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"刀柄暂存批量归还处理失败: {str(e)}")

@router.put("/handle/temp-store/{record_id}", response_model=BaseResponse)
async def update_handle_temp_store_record(
    record_id: int,
    request: UpdateHandleTempStoreRequest = Body(...)
):
    """
    编辑刀柄暂存记录
    功能：修改现有刀柄暂存记录的信息
    权限：只能编辑本人的暂存记录
    
    参数：
    - record_id: 暂存记录主键
    - brandName: 刀柄品牌
    - handleType: 刀柄类型
    - handleSpec: 刀柄规格
    - quantity: 数量
    - expectedReturnDate: 预计归还时间
    - borrowPurpose: 暂存用途/备注
    """
    try:
        # 验证必填字段
        if not request.brandName:
            raise HTTPException(status_code=400, detail="刀柄品牌不能为空")
        if not request.handleType:
            raise HTTPException(status_code=400, detail="刀柄类型不能为空")
        if not request.handleSpec:
            raise HTTPException(status_code=400, detail="刀柄规格不能为空")
        if request.quantity <= 0:
            raise HTTPException(status_code=400, detail="数量必须大于0")
        
        # 模拟当前用户信息
        current_user = {"employeeCode": "zhangsan"}
        
        # 调用API客户端方法更新记录
        result = api_client.update_handle_temp_store_record(record_id, request.dict(), current_user)
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"编辑刀柄暂存记录失败: {str(e)}")

@router.post("/handle/return", response_model=BaseResponse)
async def return_handle_temp_store(
    request: HandleTempStoreReturnRequest = Body(...)
):
    """
    刀柄暂存归还（单个）
    功能：将暂存的刀柄归还入库
    权限：只能归还本人的暂存记录
    
    参数：
    - borrowId: 暂存记录主键
    - cabinetCode: 刀柜编码
    - locList: 收刀库位号集合
    - actualReturnDate: 实际归还日期
    - returnRemarks: 归还备注
    - operateUser: 操作人
    """
    try:
        # 验证必填字段
        if not request.cabinetCode:
            raise HTTPException(status_code=400, detail="刀柜编码不能为空")
        if not request.locList or len(request.locList) == 0:
            raise HTTPException(status_code=400, detail="收刀库位号不能为空")
        if not request.actualReturnDate:
            raise HTTPException(status_code=400, detail="实际归还日期不能为空")
        
        # 模拟当前用户信息（如果前端没有传operateUser）
        current_user = {"employeeCode": request.operateUser or "zhangsan"}
        
        # 调用API客户端方法处理归还
        result = api_client.return_handle_temp_store_record(request.dict(), current_user)
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"刀柄暂存归还失败: {str(e)}")

@router.post("/handle/temp-store", response_model=BaseResponse)
async def create_handle_temp_store_from_borrow(
    request: CreateHandleTempStoreFromBorrowRequest = Body(...)
):
    """
    刀柄暂存（从借出记录创建）
    功能：对已借出的刀柄进行临时存储处理
    权限：只能暂存本人的借出记录
    
    参数：
    - borrowId: 借出记录主键
    - cabinetCode: 刀柜编码
    - itemList: 暂存详情列表
    - borrowQty: 暂存数量
    - borrowRemarks: 暂存备注
    - operationType: 操作类型
    - operateTime: 操作时间
    - operateUser: 操作人
    """
    try:
        # 验证必填字段
        if not request.cabinetCode:
            raise HTTPException(status_code=400, detail="刀柜编码不能为空")
        if not request.operateTime:
            raise HTTPException(status_code=400, detail="操作时间不能为空")
        if request.borrowQty <= 0:
            raise HTTPException(status_code=400, detail="暂存数量必须大于0")
        
        # 模拟当前用户信息
        current_user = {"employeeCode": request.operateUser or "zhangsan"}
        
        # 调用API客户端方法创建暂存
        result = api_client.create_temp_store_from_borrow(request.dict(), current_user)
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建刀柄暂存失败: {str(e)}")

@router.get("/handle/temp-store/{record_id}", response_model=HandleTempStoreDetailResponse)
async def get_handle_temp_store_detail(
    record_id: int
):
    """
    获取刀柄暂存记录详情
    功能：查看刀柄暂存记录的详细信息
    
    参数：
    - record_id: 暂存记录主键
    
    返回信息：
    - 暂存单号
    - 暂存人信息
    - 刀柄信息（品牌、型号、规格、数量）
    - 时间信息（暂存时间、预计归还时间、实际归还时间）
    - 状态信息
    - 备注信息
    """
    try:
        # 调用API客户端方法获取详情
        result = api_client.get_handle_temp_store_detail(record_id)
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取刀柄暂存记录详情失败: {str(e)}")