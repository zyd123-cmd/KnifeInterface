from fastapi import APIRouter, Query, HTTPException, Response, Body
from typing import Optional, List
import sys
import os
import json

# 将项目根目录添加到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from teamleader.schemas.data_schemas import (
    CutterQueryParams, 
    CutterQueryResponse,
    CreateCutterRequest,
    CreateCutterResponse,
    UpdateCutterRequest,
    UpdateCutterResponse,
    DeleteCutterResponse,
    BrandQueryParams,
    BrandQueryResponse,
    SubmitBrandRequest,
    SubmitBrandResponse,
    DeleteBrandResponse,
    StockPutQueryParams,
    StockPutQueryResponse,
    StockOperationResponse,
    StockStatisticalQueryParams,
    StockStatisticalResponse,
    StockTakeQueryParams,
    StockTakeQueryResponse,
    PreBatchPlugResponse,
    OnPreBatchPlugResponse,
    LendRecordResponse,
    RestockRequest,
    RestockResponse,
    ReplenishRecordResponse,
    StorageRecordResponse,
    PersonalStorageResponse,
    MakeAlarmResponse,
    CabinetAlarmResponse
)
from teamleader.services.api_client import TeamLeaderAPIClient
from config.config import settings

# 创建路由器
router = APIRouter(
    prefix="/teamleader",
    tags=["TeamLeader-班组长"],
    responses={404: {"description": "Not found"}}
)

# 初始化API客户端
api_client = TeamLeaderAPIClient(base_url=settings.ORIGINAL_API_BASE_URL)


@router.get(
    "/cutters",
    response_model=CutterQueryResponse,
    summary="刀具耗材分页查询",
    description="""
    查询刀具耗材信息，支持多维度筛选和分页。
    
    **支持的查询条件：**
    - 品牌名称：模糊查询
    - 刀具柜名称：模糊查询
    - 创建时间：精确匹配
    - 创建人：精确匹配
    - 刀具类型：模糊查询
    - 刀具型号：模糊查询
    - 价格区间：最低价格和最高价格
    
    **注意：**
    - 所有查询条件均为可选，不传递任何条件时返回全部数据
    - 价格区间可以只传最低价或最高价，也可以同时传递
    - 支持分页，默认第1页，每页10条
    """
)
async def query_cutters(
    brandName: Optional[str] = Query(None, description="品牌名称"),
    cabinetName: Optional[str] = Query(None, description="刀具柜名称"),
    createTime: Optional[str] = Query(None, description="创建时间（格式：YYYY-MM-DD HH:mm:ss）"),
    createUser: Optional[int] = Query(None, description="创建人 ID"),
    cutterType: Optional[str] = Query(None, description="刀具类型"),
    cutterCode: Optional[str] = Query(None, description="刀具型号"),
    minPrice: Optional[float] = Query(None, description="最低价格", ge=0),
    maxPrice: Optional[float] = Query(None, description="最高价格", ge=0),
    current: int = Query(1, description="当前页码", ge=1),
    size: int = Query(10, description="每页数量", ge=1, le=100)
):
    """
    刀具耗材分页查询接口
    """
    # 验证价格区间
    if minPrice is not None and maxPrice is not None and minPrice > maxPrice:
        raise HTTPException(status_code=400, detail="最低价格不能大于最高价格")
    
    # 构建查询参数
    query_params = CutterQueryParams(
        brandName=brandName,
        cabinetName=cabinetName,
        createTime=createTime,
        createUser=createUser,
        cutterType=cutterType,
        cutterCode=cutterCode,
        minPrice=minPrice,
        maxPrice=maxPrice,
        current=current,
        size=size
    )
    
    # 调用原始API
    try:
        result = api_client.get_cutter_list(query_params.dict(exclude_none=False))
        
        # 检查响应状态
        if not result.get("success"):
            raise HTTPException(
                status_code=500,
                detail=result.get("msg", "查询失败")
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"服务器错误: {str(e)}")


@router.get(
    "/cutters/search",
    response_model=CutterQueryResponse,
    summary="刀具耗材搜索（同查询接口）",
    description="""
    搜索刀具耗材信息，功能与查询接口相同。
    根据规范，搜索和刷新功能通过同一个接口实现。
    """
)
async def search_cutters(
    brandName: Optional[str] = Query(None, description="品牌名称"),
    cabinetName: Optional[str] = Query(None, description="刀具柜名称"),
    createTime: Optional[str] = Query(None, description="创建时间（格式：YYYY-MM-DD HH:mm:ss）"),
    createUser: Optional[int] = Query(None, description="创建人 ID"),
    cutterType: Optional[str] = Query(None, description="刀具类型"),
    cutterCode: Optional[str] = Query(None, description="刀具型号"),
    minPrice: Optional[float] = Query(None, description="最低价格", ge=0),
    maxPrice: Optional[float] = Query(None, description="最高价格", ge=0),
    current: int = Query(1, description="当前页码", ge=1),
    size: int = Query(10, description="每页数量", ge=1, le=100)
):
    """
    刀具耗材搜索接口（复用查询逻辑）
    """
    # 直接调用查询接口
    return await query_cutters(
        brandName=brandName,
        cabinetName=cabinetName,
        createTime=createTime,
        createUser=createUser,
        cutterType=cutterType,
        cutterCode=cutterCode,
        minPrice=minPrice,
        maxPrice=maxPrice,
        current=current,
        size=size
    )


@router.post(
    "/cutters",
    response_model=CreateCutterResponse,
    summary="新增刀具耗材",
    description="""
    新增刀具耗材信息。
    
    **必填字段：**
    - 品牌名称（brandName）
    - 刀具柜名称（cabinetName）
    - 刀具型号（cutterCode）
    - 单价（price）
    - 创建人（createUser）
    
    **可选字段：**
    - 刀头图片列表（imageUrlList）
    - 其他扩展字段（品牌编码、刀具类型、规格等）
    
    **注意：**
    - 单价必须大于0
    - 图片列表为数组格式，每个图片包含name、newFilename、url字段
    """
)
async def create_cutter(request: CreateCutterRequest):
    """
    新增刀具耗材接口
    """
    # 验证价格
    if request.price <= 0:
        raise HTTPException(status_code=400, detail="单价必须大于0")
    
    # 调用原始API
    try:
        result = api_client.create_cutter(request.dict())
        
        # 检查响应状态
        if not result.get("success"):
            raise HTTPException(
                status_code=500,
                detail=result.get("msg", "新增失败")
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"服务器错误: {str(e)}")


@router.put(
    "/cutters/{cutter_id}",
    response_model=UpdateCutterResponse,
    summary="修改刀具耗材",
    description="""
    修改指定刀具耗材的信息。
    
    **必填字段：**
    - 刀具ID（cutter_id，通过URL路径传递）
    
    **可修改字段：**
    - 品牌名称（brandName）
    - 刀具柜名称（cabinetName）
    - 刀具型号（cutterCode）
    - 单价（price）
    - 更新人（updateUser）
    - 刀头图片列表（imageUrlList）
    - 其他扩展字段
    
    **注意：**
    - 只传递需要修改的字段，未传递的字段将保持原值
    - 如果传递了price字段，必须大于0
    - 图片列表为数组格式，每个图片包含name、newFilename、url字段
    """
)
async def update_cutter(cutter_id: int, request: UpdateCutterRequest):
    """
    修改刀具耗材接口
    """
    # 验证价格（如果传递了价格字段）
    if request.price is not None and request.price <= 0:
        raise HTTPException(status_code=400, detail="单价必须大于0")
    
    # 将URL路径中的ID赋值给请求体
    request.id = cutter_id
    
    # 调用原始API
    try:
        # 只传递非空字段
        result = api_client.update_cutter(request.dict(exclude_none=True))
        
        # 检查响应状态
        if not result.get("success"):
            raise HTTPException(
                status_code=500,
                detail=result.get("msg", "修改失败")
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"服务器错误: {str(e)}")


@router.delete(
    "/cutters",
    response_model=DeleteCutterResponse,
    summary="批量删除刀具耗材",
    description="""
    批量删除刀具耗材记录。
    
    **参数说明：**
    - ids: 要删除的刀具ID集合，多个ID用逗号分割
    
    **使用场景：**
    - 删除单条记录：ids=123
    - 批量删除：ids=123,456,789
    
    **注意：**
    - 删除操作不可逆，请谨慎操作
    - 建议在删除前进行二次确认
    - ID不存在的记录将被忽略
    """
)
async def delete_cutters(
    ids: str = Query(..., description="要删除的刀具ID集合，多个ID用逗号分割（例如：1,2,3）")
):
    """
    批量删除刀具耗材接口
    """
    # 验证ids参数
    if not ids or ids.strip() == "":
        raise HTTPException(status_code=400, detail="删除ID不能为空")
    
    # 验证ids格式（应该是数字和逗号的组合）
    import re
    if not re.match(r'^\d+(,\d+)*$', ids.strip()):
        raise HTTPException(
            status_code=400, 
            detail="ID格式不正确，应为数字或用逗号分隔的数字（例如：1,2,3）"
        )
    
    # 调用原始API
    try:
        result = api_client.delete_cutters(ids)
        
        # 检查响应状态
        if not result.get("success"):
            raise HTTPException(
                status_code=500,
                detail=result.get("msg", "删除失败")
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"服务器错误: {str(e)}")


# ==================== 品牌管理接口 ====================

@router.get(
    "/brands",
    response_model=BrandQueryResponse,
    summary="品牌信息分页查询",
    description="""
    查询刀具品牌信息，支持多维度筛选和分页。
    
    **支持的查询条件：**
    - 品牌编码：模糊查询
    - 品牌名称：模糊查询
    - 公司名称：模糊查询
    - 供应商名称：模糊查询
    - 业务状态：精确匹配
    - 创建人：精确匹配
    - 创建时间范围：开始时间和结束时间
    
    **注意：**
    - 所有查询条件均为可选，不传递任何条件时返回全部数据
    - 时间范围可以只传开始时间或结束时间，也可以同时传递
    - 支持分页，默认第1页，每頕10条
    - 此接口同时支持搜索和刷新功能
    """
)
async def query_brands(
    brandCode: Optional[str] = Query(None, description="品牌编码"),
    brandName: Optional[str] = Query(None, description="品牌名称"),
    corporateName: Optional[str] = Query(None, description="公司名称"),
    supplierName: Optional[str] = Query(None, description="供应商名称"),
    status: Optional[int] = Query(None, description="业务状态"),
    createUser: Optional[int] = Query(None, description="创建人 ID"),
    startTime: Optional[str] = Query(None, description="创建开始时间（格式：YYYY-MM-DD HH:mm:ss）"),
    endTime: Optional[str] = Query(None, description="创建结束时间（格式：YYYY-MM-DD HH:mm:ss）"),
    current: int = Query(1, description="当前页码", ge=1),
    size: int = Query(10, description="每页数量", ge=1, le=100)
):
    """
    品牌信息分页查询接口
    """
    # 验证时间范围
    if startTime and endTime:
        # 简单验证：开始时间不能大于结束时间
        if startTime > endTime:
            raise HTTPException(status_code=400, detail="开始时间不能大于结束时间")
    
    # 构建查询参数
    query_params = BrandQueryParams(
        brandCode=brandCode,
        brandName=brandName,
        corporateName=corporateName,
        supplierName=supplierName,
        status=status,
        createUser=createUser,
        startTime=startTime,
        endTime=endTime,
        current=current,
        size=size
    )
    
    # 调用原始API
    try:
        result = api_client.get_brand_list(query_params.dict(exclude_none=False))
        
        # 检查响应状态
        if not result.get("success"):
            raise HTTPException(
                status_code=500,
                detail=result.get("msg", "查询失败")
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"服务器错误: {str(e)}")


@router.post(
    "/brands",
    response_model=SubmitBrandResponse,
    summary="新增品牌信息",
    description="""
    新增刀具品牌信息。
    
    **必填字段：**
    - 品牌编码（brandCode）
    - 品牌名称（brandName）
    - 公司名称（corporateName）
    - 供应商名称（supplierName）
    - 供应商联系人（supplierUser）
    - 联系方式（phone）
    
    **可选字段：**
    - 创建部门（createDept）
    - 业务状态（status）
    
    **注意：**
    - 新增时不需要传递id字段
    - 联系方式建议使用手机号码格式
    """
)
async def create_brand(request: SubmitBrandRequest):
    """
    新增品牌信息接口
    """
    # 验证联系方式格式（简单验证）
    if request.phone and len(request.phone.strip()) == 0:
        raise HTTPException(status_code=400, detail="联系方式不能为空")
    
    # 新增时不应该有id
    if request.id is not None:
        raise HTTPException(status_code=400, detail="新增品牌时不应该传递id字段")
    
    # 调用原始API
    try:
        result = api_client.submit_brand(request.dict())
        
        # 检查响应状态
        if not result.get("success"):
            raise HTTPException(
                status_code=500,
                detail=result.get("msg", "新增失败")
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"服务器错误: {str(e)}")


@router.put(
    "/brands/{brand_id}",
    response_model=SubmitBrandResponse,
    summary="修改品牌信息",
    description="""
    修改指定品牌的信息。
    
    **必填字段：**
    - 品牌 ID（brand_id，通过URL路径传递）
    - 品牌编码（brandCode）
    - 品牌名称（brandName）
    - 公司名称（corporateName）
    - 供应商名称（supplierName）
    - 供应商联系人（supplierUser）
    - 联系方式（phone）
    
    **可选字段：**
    - 创建部门（createDept）
    - 业务状态（status）
    
    **注意：**
    - 修改时必须提供品牌ID
    - 所有字段都需要传递，即使不修改也要传递原值
    """
)
async def update_brand(brand_id: int, request: SubmitBrandRequest):
    """
    修改品牌信息接口
    """
    # 验证联系方式格式（简单验证）
    if request.phone and len(request.phone.strip()) == 0:
        raise HTTPException(status_code=400, detail="联系方式不能为空")
    
    # 将URL路径中的ID赋值给请求体
    request.id = brand_id
    
    # 调用原始API
    try:
        result = api_client.submit_brand(request.dict())
        
        # 检查响应状态
        if not result.get("success"):
            raise HTTPException(
                status_code=500,
                detail=result.get("msg", "修改失败")
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"服务器错误: {str(e)}")


@router.delete(
    "/brands",
    response_model=DeleteBrandResponse,
    summary="批量删除品牌信息",
    description="""
    批量删除品牌信息记录。
    
    **参数说明：**
    - ids: 要删除的品牌ID集合，多个ID用逗号分割
    
    **使用场景：**
    - 删除单条记录：ids=123
    - 批量删除：ids=123,456,789
    
    **注意：**
    - 删除操作不可逆，请谨慎操作
    - 建议在删除前进行二次确认
    - ID不存在的记录将被忽略
    - 删除品牌前请确保该品牌下没有关联的刀具耗材
    """
)
async def delete_brands(
    ids: str = Query(..., description="要删除的品牌ID集合，多个ID用逗号分割（例如：1,2,3）")
):
    """
    批量删除品牌信息接口
    """
    # 验证ids参数
    if not ids or ids.strip() == "":
        raise HTTPException(status_code=400, detail="删除ID不能为空")
    
    # 验证ids格式（应该是数字和逗号的组合）
    import re
    if not re.match(r'^\d+(,\d+)*$', ids.strip()):
        raise HTTPException(
            status_code=400, 
            detail="ID格式不正确，应为数字或用逗号分隔的数字（例如：1,2,3）"
        )
    
    # 调用原始API
    try:
        result = api_client.delete_brands(ids)
        
        # 检查响应状态
        if not result.get("success"):
            raise HTTPException(
                status_code=500,
                detail=result.get("msg", "删除失败")
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"服务器错误: {str(e)}")


# ==================== 收刀柜管理接口 ====================

@router.get(
    "/stock-put-cabinets",
    response_model=StockPutQueryResponse,
    summary="收刀柜信息查询",
    description="""
    查询收刀柜货道信息，支持多维度筛选。
    
    **支持的查询条件：**
    - 刀柜编码：精确匹配
    - 库位号：精确匹配
    - 柜子面：ABCDE面
    - 库位状态：精确匹配
    - 绑定状态：0-非禁用 1-禁用
    
    **展示字段：**
    - 库位号（stockLoc）
    - 柜子面（locPrefix）
    - 刀柜编码（cabinetCode）
    - 货道容量（locCapacity）
    - 剩余数量（locSurplus）
    - 包装数量（packQty）
    - 库位状态（stockStatus）
    - 绑定状态（isBan）
    - 绑定刀具型号（cutterCode）
    - 最近更新时间（warehouseInTime）
    
    **注意：**
    - 所有查询条件均为可选，不传递任何条件时返回全部收刀柜数据
    - 此接口同时支持搜索和刷新功能
    """
)
async def query_stock_put_cabinets(
    cabinetCode: Optional[str] = Query(None, description="刀柜编码"),
    stockLoc: Optional[str] = Query(None, description="库位号"),
    locPrefix: Optional[str] = Query(None, description="柜子面（ABCDE）"),
    stockStatus: Optional[int] = Query(None, description="库位状态"),
    isBan: Optional[str] = Query(None, description="绑定状态（0:非禁用 1:禁用）"),
    borrowStatus: Optional[int] = Query(None, description="还刀状态（0:修磨 1:报废 2:换线 3:错领）"),
    storageType: Optional[int] = Query(None, description="暂存类型（0:公共暂存 1:个人暂存 2:扩展取刀）")
):
    """
    收刀柜信息查询接口
    """
    # 构建查询参数
    query_params = StockPutQueryParams(
        cabinetCode=cabinetCode,
        stockLoc=stockLoc,
        locPrefix=locPrefix,
        stockStatus=stockStatus,
        isBan=isBan,
        borrowStatus=borrowStatus,
        storageType=storageType
    )
    
    # 调用原始API
    try:
        result = api_client.get_stock_put_list(query_params.dict(exclude_none=False))
        
        # 检查响应状态
        if not result.get("success"):
            raise HTTPException(
                status_code=500,
                detail=result.get("msg", "查询失败")
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"服务器错误: {str(e)}")


@router.post(
    "/stock-put-cabinets/{stock_id}/unbind",
    response_model=StockOperationResponse,
    summary="货道解绑耗材（清空刀具数量）",
    description="""
    解绑指定货道的刀具耗材，清空刀具数量。
    
    **参数说明：**
    - stock_id: 刀柜货道主键（通过URL路径传递）
    
    **操作效果：**
    - 清空该货道的刀具绑定关系
    - 重置刀具数量为0
    
    **注意：**
    - 解绑操作不可逆，请谨慎操作
    - 建议在解绑前进行二次确认
    - 解绑后需要重新绑定刀具才能使用
    """
)
async def unbind_stock_cutter(stock_id: int):
    """
    货道解绑耗材接口
    """
    # 调用原始API
    try:
        result = api_client.unbind_stock_cutter(stock_id)
        
        # 检查响应状态
        if not result.get("success"):
            raise HTTPException(
                status_code=500,
                detail=result.get("msg", "解绑失败")
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"服务器错误: {str(e)}")


@router.post(
    "/stock-put-cabinets/{stock_id}/ban",
    response_model=StockOperationResponse,
    summary="货道禁用/启用库位",
    description="""
    禁用或启用指定货道的库位。
    
    **参数说明：**
    - stock_id: 刀柜货道主键（通过URL路径传递）
    - is_ban: 禁用状态（0-启用 1-禁用）
    
    **操作效果：**
    - 禁用：该货道不能进行取刀/还刀操作
    - 启用：恢复该货道的正常使用
    
    **注意：**
    - 禁用后不影响已有数据，只是暂时停用
    - 启用后可以继续使用
    - 维护期间建议禁用相关货道
    """
)
async def change_stock_ban_status(
    stock_id: int,
    is_ban: int = Query(..., description="禁用状态（0:启用 1:禁用）", ge=0, le=1)
):
    """
    货道禁用/启用接口
    """
    # 调用原始API
    try:
        result = api_client.change_stock_ban_status(stock_id, is_ban)
        
        # 检查响应状态
        if not result.get("success"):
            raise HTTPException(
                status_code=500,
                detail=result.get("msg", "操作失败")
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"服务器错误: {str(e)}")


@router.get(
    "/stock-put-cabinets/statistics",
    response_model=StockStatisticalResponse,
    summary="货道统计数据查询",
    description="""
    查询收刀柜货道的统计数据。
    
    **支持的查询条件：**
    - 刀柜编码：精确匹配
    - 柜子面：ABCDE面
    - 库位类型：收刀柜(0) 或 取刀柜(1)，默认0
    
    **返回统计数据：**
    - 货道总数（totalNum）
    - 禁用数量（disableNum）
    - 空闲数量（freeNum）
    - 占用数量（workNum）
    - 库存告警值（makeAlarm）
    - 总库存金额（totalAmount，扩展字段）
    
    **使用场景：**
    - 收刀柜货道管理页面的“货道统计”按钮
    - 可按刀柜编码和柜子面进行筛选
    - 默认查询收刀柜的统计数据
    
    **注意：**
    - 所有查询条件均为可选
    - 不传递任何条件时返回所有收刀柜的统计数据
    - locType默认为0（收刀柜）
    """
)
async def get_stock_statistics(
    cabinetCode: Optional[str] = Query(None, description="刀柜编码"),
    locPrefix: Optional[str] = Query(None, description="柜子面（ABCDE）"),
    locType: Optional[int] = Query(0, description="库位类型（收刀柜:0 取刀柜:1）")
):
    """
    货道统计数据查询接口
    """
    # 构建查询参数
    query_params = StockStatisticalQueryParams(
        cabinetCode=cabinetCode,
        locPrefix=locPrefix,
        locType=locType
    )
    
    # 调用原始API
    try:
        result = api_client.get_stock_statistical_num(query_params.dict(exclude_none=False))
        
        # 检查响应状态
        if not result.get("success"):
            raise HTTPException(
                status_code=500,
                detail=result.get("msg", "查询失败")
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"服务器错误: {str(e)}")


# ==================== 取刀柜管理接口 ====================

@router.get(
    "/stock-take-cabinets",
    response_model=StockTakeQueryResponse,
    summary="取刀柜信息查询",
    description="""
    查询取刀柜货道信息，支持多维度筛选。
    
    **支持的查询条件：**
    - 品牌编码：精确匹配
    - 刀柜编码：精确匹配
    - 刀具型号：精确匹配
    - 刀具类型：精确匹配
    - 柜子面：ABCDE面
    - 库位号：精确匹配
    
    **展示字段：**
    - 品牌名称（brandName）
    - 刀具型号（cutterCode）
    - 刀具类型（cutterType）
    - 库位号（stockLoc）
    - 柜子面（locPrefix）
    - 单价（price）
    - 货道容量（locCapacity）
    - 剩余数量（locSurplus）
    - 货道状态（stockStatus）
    - 暂存类型（storageType）
    - 绑定状态（isBan）
    - 刀柜编码（cabinetCode）
    
    **注意：**
    - 所有查询条件均为可选，不传递任何条件时返回全部取刀柜数据
    - 此接口同时支持搜索和刷新功能
    """
)
async def query_stock_take_cabinets(
    brandCode: Optional[str] = Query(None, description="品牌编码"),
    cabinetCode: Optional[str] = Query(None, description="刀柜编码"),
    cutterCode: Optional[str] = Query(None, description="刀具型号"),
    cutterType: Optional[str] = Query(None, description="刀具类型"),
    locPrefix: Optional[str] = Query(None, description="柜子面（ABCDE）"),
    stockLoc: Optional[str] = Query(None, description="库位号"),
    cutterOrBrand: Optional[str] = Query(None, description="耗材型号或品牌"),
    materialCode: Optional[str] = Query(None, description="物料编码"),
    specification: Optional[str] = Query(None, description="规格")
):
    """
    取刀柜信息查询接口
    """
    # 构建查询参数
    query_params = StockTakeQueryParams(
        brandCode=brandCode,
        cabinetCode=cabinetCode,
        cutterCode=cutterCode,
        cutterType=cutterType,
        locPrefix=locPrefix,
        stockLoc=stockLoc,
        cutterOrBrand=cutterOrBrand,
        materialCode=materialCode,
        specification=specification
    )
    
    # 调用原始API
    try:
        result = api_client.get_stock_take_list(query_params.dict(exclude_none=False))
        
        # 检查响应状态
        if not result.get("success"):
            raise HTTPException(
                status_code=500,
                detail=result.get("msg", "查询失败")
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"服务器错误: {str(e)}")


@router.post(
    "/stock-take-cabinets/{stock_id}/unbind",
    response_model=StockOperationResponse,
    summary="取刀柜货道解绑耗材",
    description="""
    解绑指定取刀柜货道的刀具耗材，清空刀具数量。
    
    **参数说明：**
    - stock_id: 刀柜货道主键（通过URL路径传递）
    
    **操作效果：**
    - 清空该货道的刀具绑定关系
    - 重置刀具数量为0
    
    **注意：**
    - 解绑操作不可逆，请谨慎操作
    - 建议在解绑前进行二次确认
    - 解绑后需要重新绑定刀具才能使用
    - 与收刀柜解绑接口使用相同的后端API
    """
)
async def unbind_stock_take_cutter(stock_id: int):
    """
    取刀柜货道解绑耗材接口（复用收刀柜解绑接口）
    """
    # 调用原始API（与收刀柜使用相同API）
    try:
        result = api_client.unbind_stock_cutter(stock_id)
        
        # 检查响应状态
        if not result.get("success"):
            raise HTTPException(
                status_code=500,
                detail=result.get("msg", "解绑失败")
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"服务器错误: {str(e)}")


@router.post(
    "/stock-take-cabinets/{stock_id}/ban",
    response_model=StockOperationResponse,
    summary="取刀柜货道禁用/启用库位",
    description="""
    禁用或启用指定取刀柜货道的库位。
    
    **参数说明：**
    - stock_id: 刀柜货道主键（通过URL路径传递）
    - is_ban: 禁用状态（0-启用 1-禁用）
    
    **操作效果：**
    - 禁用：该货道不能进行取刀/还刀操作
    - 启用：恢复该货道的正常使用
    
    **注意：**
    - 禁用后不影响已有数据，只是暂时停用
    - 启用后可以继续使用
    - 维护期间建议禁用相关货道
    - 与收刀柜禁用/启用接口使用相同的后端API
    """
)
async def change_stock_take_ban_status(
    stock_id: int,
    is_ban: int = Query(..., description="禁用状态（0:启用 1:禁用）", ge=0, le=1)
):
    """
    取刀柜货道禁用/启用接口（复用收刀柜禁用/启用接口）
    """
    # 调用原始API（与收刀柜使用相同API）
    try:
        result = api_client.change_stock_ban_status(stock_id, is_ban)
        
        # 检查响应状态
        if not result.get("success"):
            raise HTTPException(
                status_code=500,
                detail=result.get("msg", "操作失败")
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"服务器错误: {str(e)}")


# ==================== 补刀管理接口 ====================

@router.post(
    "/cabinets/{cabinet_code}/pre-batch-plug",
    response_model=PreBatchPlugResponse,
    summary="预补刀查询（检查是否可以补刀）",
    description="""
    批量预补刀查询，获取指定刀柜中哪些货道可以补刀。
    
    **参数说明：**
    - cabinet_code: 刀柜编码（通过URL路径传递）
    
    **返回数据：**
    - successStock: 可以补刀的货道列表
      - 包含：刀柜编码、库位号、货道容量、补货前数量、补货后数量
    - errorStock: 不能补刀的货道列表
      - 包含：刀柜编码、库位号、失败原因
    
    **使用场景：**
    - 点击“预补刀”按钮时调用
    - 在实际补刀前检查哪些货道需要补充
    - 展示补刀预览信息给用户确认
    
    **注意：**
    - 此接口仅查询，不会实际补刀
    - 需要用户确认后再调用补刀接口
    - 返回的数据可用于展示补刀计划
    """
)
async def pre_batch_plug(cabinet_code: str):
    """
    预补刀查询接口
    """
    # 调用原始API
    try:
        result = api_client.pre_batch_plug(cabinet_code)
        
        # 检查响应状态
        if not result.get("success"):
            raise HTTPException(
                status_code=500,
                detail=result.get("msg", "查询失败")
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"服务器错误: {str(e)}")


@router.post(
    "/cabinets/{cabinet_code}/batch-plug",
    response_model=OnPreBatchPlugResponse,
    summary="批量一键补刀",
    description="""
    执行批量一键补刀操作，对指定刀柜中需要补充的货道进行补刀。
    
    **参数说明：**
    - cabinet_code: 刀柜编码（通过URL路径传递）
    
    **操作效果：**
    - 对所有可补充的货道进行补刀
    - 补充到货道的最大容量
    - 自动更新库存数量
    
    **使用场景：**
    - 点击“补刀”按钮时调用
    - 在预补刀查询后用户确认执行
    - 定期维护时批量补充刀具
    
    **注意：**
    - 此操作不可逆，请谨慎操作
    - 建议先调用预补刀接口查看预览
    - 补刀后会自动更新库存
    - 如果部分货道补刀失败，整体操作可能仍然返回true
    """
)
async def on_pre_batch_plug(cabinet_code: str):
    """
    批量补刀接口
    """
    # 调用原始API
    try:
        result = api_client.on_pre_batch_plug(cabinet_code)
        
        # 检查响应状态
        if not result.get("success"):
            raise HTTPException(
                status_code=500,
                detail=result.get("msg", "补刀失败")
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"服务器错误: {str(e)}")





# ==================== 合并自 系统记录 模块的接口 ====================
# 合并日期: 2025-11-15
# 来源: teamleader_record/lend_record_router.py

# 领刀记录相关路由 (班组长)
@router.get("/list", response_model=LendRecordResponse, tags=["班组长记录"])
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
    获取领刀记录列表 (班组长)
    
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
        LendRecordResponse: 领刀记录列表响应
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

@router.get("/export", tags=["班组长记录"])
async def export_lend_records(
    endTime: Optional[str] = Query(None, description="结束时间"),
    order: Optional[int] = Query(None, description="顺序 0: 从大到小 1：从小到大"),
    rankingType: Optional[int] = Query(None, description="0: 数量 1: 金额"),
    recordStatus: Optional[int] = Query(None, description="0: 取刀 1: 还刀 2: 收刀 3: 暂存 4: 完成 5：违规还刀"),
    startTime: Optional[str] = Query(None, description="开始时间")
):
    """
    导出领刀记录 (班组长)
    
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

# 告警预警相关路由 (班组长)
@router.get("/alarm_list", response_model=AlarmWarningResponse, tags=["班组长记录"])
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
    获取告警预警列表 (班组长)
    
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
        AlarmWarningResponse: 告警预警列表响应
    """
    result = api_client.list_alarm_warning(
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

@router.get("/alarm_statistics", response_model=AlarmStatisticsResponse, tags=["班组长记录"])
async def get_alarm_statistics():
    """
    获取告警统计信息 (班组长)
    
    Returns:
        AlarmStatisticsResponse: 告警统计信息响应
    """
    result = api_client.get_alarm_statistics()
    
    return result

@router.post("/alarm_threshold", tags=["班组长记录"])
async def update_alarm_threshold(
    request: ThresholdSettingRequest = Body(..., description="阈值设置请求参数")
):
    """
    更新告警阈值 (班组长)
    
    Args:
        request: 阈值设置请求参数
        
    Returns:
        Response: 更新结果响应
    """
    result = api_client.update_alarm_threshold(
        locSurplus=request.locSurplus,
        alarmThreshold=request.alarmThreshold
    )
    
    return result

@router.post("/handle_alarm/{alarm_id}", tags=["班组长记录"])
async def handle_alarm_warning(
    alarm_id: int,
    handle_status: int = Body(..., description="处理状态"),
    handle_remark: Optional[str] = Body(None, description="处理备注")
):
    """
    处理告警预警 (班组长)
    
    Args:
        alarm_id: 告警ID
        handle_status: 处理状态 (0: 未处理, 1: 已处理, 2: 已忽略)
        handle_remark: 处理备注
        
    Returns:
        Response: 处理结果响应
    """
    result = api_client.handle_alarm_warning(
        id=alarm_id,
        handleStatus=handle_status,
        handleRemark=handle_remark
    )
    
    return result

@router.post("/batch_handle_alarm", tags=["班组长记录"])
async def batch_handle_alarm_warning(
    ids: List[int] = Body(..., description="告警ID列表"),
    handle_status: int = Body(..., description="处理状态"),
    handle_remark: Optional[str] = Body(None, description="处理备注")
):
    """
    批量处理告警预警 (班组长)
    
    Args:
        ids: 告警ID列表
        handle_status: 处理状态 (0: 未处理, 1: 已处理, 2: 已忽略)
        handle_remark: 处理备注
        
    Returns:
        Response: 处理结果响应
    """
    result = api_client.batch_handle_alarm_warning(
        ids=ids,
        handleStatus=handle_status,
        handleRemark=handle_remark
    )
    
    return result

@router.get("/export_alarm", tags=["班组长记录"])
async def export_alarm_warning(
    loc_surplus: Optional[int] = Query(None, description="货道"),
    alarm_level: Optional[int] = Query(None, description="预警等级"),
    device_type: Optional[str] = Query(None, description="设备类型"),
    cabinet_code: Optional[str] = Query(None, description="刀柜编码"),
    brand_name: Optional[str] = Query(None, description="品牌名称"),
    handle_status: Optional[int] = Query(None, description="处理状态")
):
    """
    导出告警预警 (班组长)
    
    Args:
        loc_surplus: 货道
        alarm_level: 预警等级
        device_type: 设备类型
        cabinet_code: 刀柜编码
        brand_name: 品牌名称
        handle_status: 处理状态
        
    Returns:
        Response: 包含导出文件的响应
    """
    try:
        file_content = api_client.export_alarm_warning(
            locSurplus=loc_surplus,
            alarmLevel=alarm_level,
            deviceType=device_type,
            cabinetCode=cabinet_code,
            brandName=brand_name,
            handleStatus=handle_status
        )
        
        return Response(
            content=file_content,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Content-Disposition": "attachment; filename=alarm_warnings.xlsx"
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

# 补货记录相关路由 (班组长)
@router.get("/replenish_list", response_model=ReplenishRecordResponse, tags=["班组长记录"])
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
    获取补货记录列表 (班组长)
    
    Args:
        current: 当前页
        end_time: 结束时间
        order: 顺序 0: 从大到小 1：从小到大
        ranking_type: 0: 数量 1: 金额
        record_status: 0: 取刀 1: 还刀 2: 收刀 3: 暂存 4: 完成 5：违规还刀
        size: 每页的数量
        start_time: 开始时间
        
    Returns:
        ReplenishRecordResponse: 补货记录列表响应，包含以下字段：
            - lendUserName: 取出人
            - storageUserName: 暂存人
            - brandName: 品牌名称
            - cutterType: 电池类型
            - cutterCode: 刀具型号
            - specification: 规格
            - quantity: 数量
            - oldPrice: 老单价
            - newPrice: 新单价
            - oldStockNum: 操作前库存数
            - newStockNum: 操作后库存数
            - stockLoc: 库位号
            - logType: 补货类型
            - status: 业务状态
            - cabinetCode: 刀柜编码
            - createTime: 创建时间
            - operator: 操作人
            - materialCode: 物料编码
            - detailsCode: 操作详情
            - remake: 备注
            - createDept: 创建部门
            - createUser: 创建人
            - updateUser: 更新人
            - tenantId: 租户ID
            - isDeleted: 是否已删除
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

@router.get("/export_replenish", tags=["班组长记录"])
async def export_replenish_records(
    end_time: Optional[str] = Query(None, description="结束时间"),
    order: Optional[int] = Query(None, description="顺序 0: 从大到小 1：从小到大"),
    ranking_type: Optional[int] = Query(None, description="0: 数量 1: 金额"),
    record_status: Optional[int] = Query(None, description="0: 取刀 1: 还刀 2: 收刀 3: 暂存 4: 完成 5：违规还刀"),
    start_time: Optional[str] = Query(None, description="开始时间")
):
    """
    导出补货记录 (班组长)
    
    Args:
        end_time: 结束时间
        order: 顺序 0: 从大到小 1：从小到大
        ranking_type: 0: 数量 1: 金额
        record_status: 0: 取刀 1: 还刀 2: 收刀 3: 暂存 4: 完成 5：违规还刀
        start_time: 开始时间
        
    Returns:
        Response: 包含导出文件的响应，Excel文件包含以下字段：
            - lendUserName: 取出人
            - storageUserName: 暂存人
            - brandName: 品牌名称
            - cutterType: 电池类型
            - cutterCode: 刀具型号
            - specification: 规格
            - quantity: 数量
            - oldPrice: 老单价
            - newPrice: 新单价
            - oldStockNum: 操作前库存数
            - newStockNum: 操作后库存数
            - stockLoc: 库位号
            - logType: 补货类型
            - status: 业务状态
            - cabinetCode: 刀柜编码
            - createTime: 创建时间
            - operator: 操作人
            - materialCode: 物料编码
            - detailsCode: 操作详情
            - remake: 备注
            - createDept: 创建部门
            - createUser: 创建人
            - updateUser: 更新人
            - tenantId: 租户ID
            - isDeleted: 是否已删除
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

# 公共暂存记录相关路由 (班组长)
@router.get("/storage_list", response_model=StorageRecordResponse, tags=["班组长记录"])
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
    获取公共暂存记录列表 (班组长)
    
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

@router.get("/export_storage", tags=["班组长记录"])
async def export_storage_records(
    end_time: Optional[str] = Query(None, description="结束时间"),
    order: Optional[int] = Query(None, description="顺序 0: 从大到小 1：从小到大"),
    ranking_type: Optional[int] = Query(None, description="0: 数量 1: 金额"),
    record_status: Optional[int] = Query(None, description="0: 取刀 1: 还刀 2: 收刀 3: 暂存 4: 完成 5：违规还刀"),
    start_time: Optional[str] = Query(None, description="开始时间")
):
    """
    导出公共暂存记录 (班组长)
    
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


