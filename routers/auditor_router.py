from fastapi import APIRouter, HTTPException, Query, Response, Body
from typing import Optional, List
import logging
import traceback
import json

# 配置日志
logger = logging.getLogger(__name__)

# 导入所需的模块
from auditor.services.api_client import original_api_client as api_client
from auditor.schemas.data_schemas import (
    StorageStatisticsResponse,
    ChartsResponse,
    TotalStockResponse,
    WasteKnifeRecycleResponse,
    DeviceRankingResponse,
    KnifeModelRankingResponse,
    EmployeeRankingResponse,
    ErrorReturnRankingResponse,
    # 系统记录相关模型
    LendRecordResponse,
    ExportLendRecordRequest,
    ReplenishRecordResponse,
    StorageRecordModelResponse,
    AlarmWarningResponse,
    AlarmStatisticsResponse,
    ThresholdSettingRequest,
    ExportReplenishRecordRequest,
    ExportStorageRecordRequest
)

router = APIRouter()


# 测试接口
@router.get("/test", tags=["测试"])
async def test_connection():
    """测试路由连接"""
    return {
        "message": "审计员接口连接正常",
        "status": "success",
        "timestamp": "2024-11-11"
    }


# ==================== 出入库统计接口 ====================
@router.get("/storage-statistics", response_model=StorageStatisticsResponse, tags=["出入库统计"])
async def get_storage_statistics(
        current: Optional[int] = Query(1, ge=1, description="当前页"),
        size: Optional[int] = Query(10, ge=1, le=100, description="每页数量"),
        start_time: Optional[str] = Query(None, alias="startTime", description="开始时间（YYYY-MM-DD HH:mm:ss）"),
        end_time: Optional[str] = Query(None, alias="endTime", description="结束时间（YYYY-MM-DD HH:mm:ss）"),
        record_status: Optional[int] = Query(None, alias="recordStatus",
                                             description="记录状态：0-取刀，1-还刀，2-收刀，3-暂存，4-完成，5-违规还刀"),
        ranking_type: Optional[int] = Query(None, alias="rankingType",
                                            description="排名类型：0-按数量排序，1-按金额排序"),
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
        logger.error(f"获取出入库统计数据失败: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"获取出入库统计数据失败: {str(e)}")


@router.get("/export-stock-record", response_model=StorageStatisticsResponse, tags=["出入库统计"])
async def export_stock_record(
        start_time: Optional[str] = Query(None, alias="startTime", description="开始时间（YYYY-MM-DD HH:mm:ss）"),
        end_time: Optional[str] = Query(None, alias="endTime", description="结束时间（YYYY-MM-DD HH:mm:ss）"),
        record_status: Optional[int] = Query(None, alias="recordStatus",
                                             description="记录状态：0-取刀，1-还刀，2-收刀，3-暂存，4-完成，5-违规还刀"),
        ranking_type: Optional[int] = Query(None, alias="rankingType",
                                            description="排名类型：0-按数量排序，1-按金额排序"),
        order: Optional[int] = Query(None, description="排序顺序：0-从大到小（降序），1-从小到大（升序）")
):
    """
    导出刀具耗材数据（出入库记录）

    功能：导出刀具的出入库记录数据，返回JSON格式
    封装外部接口：/qw/knife/web/from/mes/record/exportStockRecord

    参数说明：
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
    - data: 导出数据
      * current: 当前页
      * size: 每页数量
      * total: 总记录数
      * pages: 总页数
      * records: 记录列表（包含完整的出入库信息）
        - account: 用户名
        - name: 用户名称
        - brandName: 品牌名称
        - brandCode: 品牌编码
        - cutterType: 刀具类型
        - cutterCode: 刀具型号
        - specification: 规格
        - quantity: 数量
        - price: 单价
        - oldPrice: 历史单价
        - stockLoc: 库位号
        - stockType: 库存类型（0:入库 1:出库）
        - status: 业务状态
        - cabinetName: 刀具柜名称
        - cabinetCode: 刀具柜编码
        - factoryName: 工厂名称
        - workshopName: 车间名称
        - operator: 操作人
        - createTime: 创建时间
        - updateTime: 更新时间
        - detailsName: 操作详情
        - remake: 备注
        - 及其他字段...
    """
    try:
        # 构建查询参数
        params = {
            "startTime": start_time,
            "endTime": end_time,
            "recordStatus": record_status,
            "rankingType": ranking_type,
            "order": order
        }

        # 调用API客户端方法获取导出数据
        result = api_client.export_stock_record(params)

        return result

    except Exception as e:
        logger.error(f"导出出入库记录失败: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"导出出入库记录失败: {str(e)}")


# ==================== 统计图表接口 ====================
@router.get("/charts-lend-by-year", response_model=ChartsResponse, tags=["统计图表"])
async def get_charts_lend_by_year():
    """
    获取全年取刀数量统计

    功能：查询全年（12个月）的取刀数量统计数据
    封装外部接口：/qw/knife/web/from/mes/statistics/chartsLendByYear

    请求参数：
    - 无

    返回数据：
    - code: 状态码
    - msg: 返回消息
    - success: 是否成功
    - data: 统计数据
      * titleList: 月份标题列表 ["１月", "２月", ..., "１２月"]
      * dataList: 对应的取刀数量列表 [150, 200, 180, ...]

    使用场景：
    - 显示全年取刀数量趋势图
    - 查找取刀高峰月份（前端通过 Math.max(dataList) 计算）
    - 对比各月取刀数量

    示例响应：
    ```json
    {
      "code": 200,
      "msg": "查询成功",
      "success": true,
      "data": {
        "titleList": ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"],
        "dataList": [150, 200, 180, 220, 190, 210, 230, 250, 240, 260, 270, 280]
      }
    }
    ```
    """
    try:
        # 调用API客户端方法获取数据
        result = api_client.get_charts_lend_by_year()
        return result
    except Exception as e:
        logger.error(f"获取全年取刀数量统计失败: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"获取全年取刀数量统计失败: {str(e)}")


@router.get("/charts-lend-price-by-year", response_model=ChartsResponse, tags=["统计图表"])
async def get_charts_lend_price_by_year():
    """
    获取全年取刀金额统计

    功能：查询全年（12个月）的取刀金额统计数据
    封装外部接口：/qw/knife/web/from/mes/statistics/chartsLendPriceByYear

    请求参数：
    - 无

    返回数据：
    - code: 状态码
    - msg: 返回消息
    - success: 是否成功
    - data: 统计数据
      * titleList: 月份标题列表 ["1月", "2月", ..., "12月"]
      * dataList: 对应的取刀金额列表 [15000.50, 20000.00, ...]

    使用场景：
    - 显示全年取刀金额趋势图
    - 查找金额高峰月份（前端通过 Math.max(dataList) 计算）
    - 对比各月取刀成本
    - 计算全年总金额（前端通过 dataList.reduce((a,b)=>a+b) 计算）

    示例响应：
    ```json
    {
      "code": 200,
      "msg": "查询成功",
      "success": true,
      "data": {
        "titleList": ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"],
        "dataList": [15000.50, 20000.00, 18000.75, 22000.30, 19000.60, 21000.00, 23000.50, 25000.00, 24000.80, 26000.90, 27000.40, 28000.20]
      }
    }
    ```
    """
    try:
        # 调用API客户端方法获取数据
        result = api_client.get_charts_lend_price_by_year()
        return result
    except Exception as e:
        logger.error(f"获取全年取刀金额统计失败: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"获取全年取刀金额统计失败: {str(e)}")


@router.get("/charts-accumulated", response_model=ChartsResponse, tags=["统计图表"])
async def get_charts_accumulated():
    """
    获取刀具消耗统计

    功能：查询刀具的消耗统计数据，支持按刀具类型或统计指标展示
    封装外部接口：/qw/knife/web/from/mes/statistics/chartsAccumulated

    请求参数：
    - 无

    返回数据：
    - code: 状态码
    - msg: 返回消息
    - success: 是否成功
    - data: 统计数据
      * titleList: 统计项标题列表（刀具类型或统计指标）
      * dataList: 对应的数据列表

    数据展示方式：

    方式1 - 按刀具类型统计：
    - titleList 包含：车刀片、铣刀、钻头、镑刀等刀具类型
    - dataList 包含：各类刀具的累计消耗数量或使用次数

    方式2 - 按统计指标展示：
    - titleList 包含：
      * 累计使用次数：刀具被使用的总次数
      * 累计使用时长：刀具累计工作时间
      * 平均寿命：刀具平均使用寿命
      * 更换次数：刀具被更换的次数
      * 使用效率：刀具使用效率百分比
    - dataList 包含：各指标对应的数值

    使用场景：
    - 显示刀具消耗情况（按类型分类）
    - 统计刀具使用效率（按指标分类）
    - 分析刀具消耗趋势
    - 为刀具采购提供数据支持

    示例响应 1 - 按刀具类型统计：
    ```json
    {
      "code": 200,
      "msg": "查询成功",
      "success": true,
      "data": {
        "titleList": ["车刀片", "铣刀", "钻头", "镑刀", "丝锥"],
        "dataList": [1500, 2000, 1800, 1200, 950]
      }
    }
    ```

    示例响应 2 - 按统计指标展示：
    ```json
    {
      "code": 200,
      "msg": "查询成功",
      "success": true,
      "data": {
        "titleList": [
          "累计使用次数",
          "累计使用时长(h)",
          "平均寿命(h)",
          "更换次数",
          "使用效率(%)"
        ],
        "dataList": [1500, 3000, 120, 50, 85]
      }
    }
    ```

    注意：请先调用接口查看实际返回的数据结构，以确定 titleList 和 dataList 的具体内容和展示方式。
    """
    try:
        # 调用API客户端方法获取数据
        result = api_client.get_charts_accumulated()
        return result
    except Exception as e:
        logger.error(f"获取刀具消耗统计失败: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"获取刀具消耗统计失败: {str(e)}")


# ==================== 总库存统计接口 ====================
@router.get("/total-stock", response_model=TotalStockResponse, tags=["总库存统计"])
async def get_total_stock(
        statistics_type: Optional[str] = Query(None, alias="statisticsType", description="统计类型"),
        brand_name: Optional[str] = Query(None, alias="brandName", description="品牌名称"),
        cabinet_code: Optional[str] = Query(None, alias="cabinetCode", description="刀柜编码"),
        cutter_type: Optional[str] = Query(None, alias="cutterType", description="刀具类型"),
        stock_status: Optional[int] = Query(None, alias="stockStatus", description="库位状态"),
        current: Optional[int] = Query(1, ge=1, description="当前页"),
        size: Optional[int] = Query(10, ge=1, le=100, description="每页数量")
):
    """
    获取总库存统计列表（支持搜索和刷新）

    功能：查询刀柜库存统计数据，支持多条件搜索和列表刷新
    封装外部接口：/qw/knife/web/from/mes/cabinetStock/stockLocTakeInfoList

    请求参数：
    - statisticsType: 统计类型（可选）
    - brandName: 品牌名称（可选）
    - cabinetCode: 刀柜编码（可选）
    - cutterType: 刀具类型（可选）
    - stockStatus: 库位状态（可选）
    - current: 当前页，默认1
    - size: 每页数量，默认10

    返回数据：
    - code: 状态码
    - msg: 返回消息
    - success: 是否成功
    - data: 库存列表数据（数组格式）
      * id: 主键id
      * cabinetCode: 刀柜编码
      * stockLoc: 库位号
      * brandName: 品牌名称
      * cutterCode: 刀具型号
      * cutterType: 刀具类型
      * specification: 规格
      * locCapacity: 库位容量
      * locSurplus: 剩余数量（货道库存）
      * stockStatus: 库位状态
      * price: 单价
      * stockValue: 库存价值（后端计算：单价 * 剩余数量）
      * cabinetSide: 柜子面
      * warehouseInTime: 入库时间
      * updateTime: 更新时间
      * 及其他字段...

    使用场景：
    1. **搜索功能**：根据统计类型、品牌名称、刀柜编码、刀具类型、库位状态进行查询
    2. **刷新功能**：不带搜索条件，获取所有库存数据
    3. **分页显示**：支持分页查询，适合前端表格展示

    示例请求 1 - 搜索（根据品牌名称和刀具类型）：
    ```
    GET /api/v1/auditor/total-stock?brandName=三菱&cutterType=车刀片&current=1&size=10
    ```

    示例请求 2 - 刷新（获取所有数据）：
    ```
    GET /api/v1/auditor/total-stock?current=1&size=20
    ```

    示例响应：
    ```json
    {
      "code": 200,
      "msg": "查询成功",
      "success": true,
      "data": [
        {
          "id": 1,
          "cabinetCode": "CB001",
          "stockLoc": "A01-01",
          "brandName": "三菱",
          "cutterCode": "CNMG120408",
          "cutterType": "车刀片",
          "specification": "CNMG120408-MA",
          "locCapacity": 100,
          "locSurplus": 75,
          "stockStatus": 1,
          "price": 25.50,
          "stockValue": 1912.50,
          "warehouseInTime": "2024-01-15 10:30:00",
          "updateTime": "2024-11-04 14:20:00"
        },
        {
          "id": 2,
          "cabinetCode": "CB002",
          "stockLoc": "A02-05",
          "brandName": "京瓷",
          "cutterCode": "WNMG080408",
          "cutterType": "车刀片",
          "specification": "WNMG080408-PM",
          "locCapacity": 80,
          "locSurplus": 60,
          "stockStatus": 1,
          "price": 18.00,
          "stockValue": 1080.00,
          "warehouseInTime": "2024-02-20 09:15:00",
          "updateTime": "2024-11-04 14:25:00"
        }
      ]
    }
    ```

    注意：
    1. 库存价值 (stockValue) 由后端自动计算：price * locSurplus
    2. 如果外部接口路径不同，请联系外部系统提供正确的列表查询接口
    3. 前端可以直接展示返回的数据，不需要额外处理
    """
    try:
        # 构建查询参数
        params = {
            "statisticsType": statistics_type,
            "brandName": brand_name,
            "cabinetCode": cabinet_code,
            "cutterType": cutter_type,
            "stockStatus": stock_status,
            "current": current,
            "size": size
        }

        # 调用API客户端方法获取数据
        result = api_client.get_total_stock_list(params)

        return result

    except Exception as e:
        logger.error(f"获取总库存统计列表失败: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"获取总库存统计列表失败: {str(e)}")


@router.get("/stock-location/{stock_id}", response_model=TotalStockResponse, tags=["总库存统计"])
async def get_stock_location_detail(stock_id: int):
    """
    获取单个库位详情

    功能：根据库位主键查询单个库位的详细信息
    封装外部接口：/qw/knife/web/from/mes/cabinetStock/stockLocTakeInfoById

    请求参数：
    - stock_id: 刀柜货道主键（路径参数）

    返回数据：
    - code: 状态码
    - msg: 返回消息
    - success: 是否成功
    - data: 库位详细信息（包含所有字段）

    使用场景：
    - 查看单个库位的完整信息
    - 点击表格行查看详情

    示例请求：
    ```
    GET /api/v1/auditor/stock-location/123
    ```

    示例响应：
    ```json
    {
      "code": 200,
      "msg": "查询成功",
      "success": true,
      "data": {
        "id": 123,
        "cabinetCode": "CB001",
        "stockLoc": "A01-01",
        "brandName": "三菱",
        "brandCode": "MITSUBISHI",
        "cutterCode": "CNMG120408",
        "cutterType": "车刀片",
        "specification": "CNMG120408-MA",
        "locCapacity": 100,
        "locSurplus": 75,
        "stockNum": 75,
        "stockStatus": 1,
        "price": 25.50,
        "stockValue": 1912.50,
        "imageUrl": "https://example.com/images/cutter.jpg",
        "warehouseInTime": "2024-01-15 10:30:00",
        "updateTime": "2024-11-04 14:20:00",
        "warningNum": 20,
        "locType": 1,
        "materialCode": "MAT001",
        "materialType": "刀片",
        "packQty": 10
      }
    }
    ```
    """
    try:
        # 调用API客户端方法获取数据
        result = api_client.get_stock_location_by_id(stock_id)

        return result

    except Exception as e:
        logger.error(f"获取库位详情失败: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"获取库位详情失败: {str(e)}")


# ==================== 废刀回收统计接口 ====================
@router.get("/waste-knife-recycle", response_model=WasteKnifeRecycleResponse, tags=["废刀回收统计"])
async def get_waste_knife_recycle(
        borrow_code: Optional[str] = Query(None, alias="borrowCode", description="还刀码"),
        cabinet_code: Optional[str] = Query(None, alias="cabinetCode", description="刀柜编码"),
        stock_loc: Optional[str] = Query(None, alias="stockLoc", description="刀柜库位号")
):
    """
    获取废刀回收统计信息（收刀柜还刀信息）

    功能：查询收刀柜中的还刀信息，用于废刀回收统计和管理
    封装外部接口：/qw/knife/web/from/mes/lend/getLendByStock

    请求参数（全部可选）：
    - borrowCode: 还刀码
    - cabinetCode: 刀柜编码
    - stockLoc: 刀柜库位号

    返回数据：
    - code: 状态码
    - msg: 返回消息
    - success: 是否成功
    - data: 还刀数据
      * borrowStatus: 还刀状态（字符串）
      * cabinetCode: 刀柜编码
      * recordStatus: 记录状态：0-取刀，1-还刀，2-收刀，3-暂存
      * list: 还刀详情列表
        - id: 取刀主键
        - borrowStatus: 还刀状态：0-修磨，1-报废，2-换线，3-错领
        - borrowTime: 还刀时间
        - borrowUserName: 还刀人
        - brandName: 品牌名称
        - cutterCode: 刀具型号
        - cutterType: 刀具类型
        - lendTime: 取刀时间
        - lendUserName: 借刀人
        - recordStatus: 记录状态
        - specification: 规格
        - stockLoc: 库位号

    使用场景：
    1. **废刀回收统计**：查看所有报废刀具（borrowStatus=1）
    2. **修磨管理**：查看需要修磨的刀具（borrowStatus=0）
    3. **错领追踪**：查询错领刀具情况（borrowStatus=3）
    4. **换线管理**：统计需要换线的刀具（borrowStatus=2）

    示例请求 1 - 查询指定刀柜的还刀信息：
    ```
    GET /api/v1/auditor/waste-knife-recycle?cabinetCode=CB001
    ```

    示例请求 2 - 查询指定库位的还刀信息：
    ```
    GET /api/v1/auditor/waste-knife-recycle?cabinetCode=CB001&stockLoc=A01-01
    ```

    示例响应：
    ```json
    {
      "code": 200,
      "msg": "查询成功",
      "success": true,
      "data": {
        "borrowStatus": "",
        "cabinetCode": "CB001",
        "recordStatus": 2,
        "list": [
          {
            "id": 123,
            "borrowStatus": 1,
            "borrowTime": "2024-11-04 10:30:00",
            "borrowUserName": "张三",
            "brandName": "三菱",
            "cutterCode": "CNMG120408",
            "cutterType": "车刀片",
            "lendTime": "2024-11-01 08:00:00",
            "lendUserName": "李四",
            "recordStatus": 2,
            "specification": "CNMG120408-MA",
            "stockLoc": "A01-01"
          },
          {
            "id": 124,
            "borrowStatus": 0,
            "borrowTime": "2024-11-04 11:15:00",
            "borrowUserName": "王五",
            "brandName": "京瓷",
            "cutterCode": "WNMG080408",
            "cutterType": "车刀片",
            "lendTime": "2024-11-02 09:30:00",
            "lendUserName": "赵六",
            "recordStatus": 2,
            "specification": "WNMG080408-PM",
            "stockLoc": "A01-02"
          }
        ]
      }
    }
    ```

    前端处理建议：
    - 根据 borrowStatus 分类统计：
      * 0-修磨：需要修磨的刀具数量
      * 1-报废：废刀回收统计
      * 2-换线：需要换线的刀具
      * 3-错领：错领刀具追踪
    - 计算各类型刀具的数量和占比
    - 显示还刀时间、取刀时间以计算使用时长
    """
    try:
        # 构建查询参数
        params = {
            "borrowCode": borrow_code,
            "cabinetCode": cabinet_code,
            "stockLoc": stock_loc
        }

        # 调用API客户端方法获取数据
        result = api_client.get_waste_knife_recycle_info(params)

        return result

    except Exception as e:
        logger.error(f"获取废刀回收统计信息失败: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"获取废刀回收统计信息失败: {str(e)}")


# ==================== 排行接口 ====================
@router.get("/device-ranking", response_model=DeviceRankingResponse, tags=["设备排行"])
async def get_device_ranking(
        start_time: Optional[str] = Query(None, alias="startTime", description="开始时间"),
        end_time: Optional[str] = Query(None, alias="endTime", description="结束时间"),
        order: Optional[int] = Query(None, description="顺序 0:从大到小 1:从小到大"),
        ranking_type: Optional[int] = Query(None, alias="rankingType", description="0:批量 1:查错"),
        record_status: Optional[int] = Query(None, alias="recordStatus", description="记录状态")
):
    """
    设备用刀排行

    功能：获取设备用刀排行数据，按使用次数或金额排序
    封装外部接口：/ou/knife/web/from/ms/statistics/chartsDeviceSanking

    参数说明：
    - startTime: 开始时间（可选）
    - endTime: 结束时间（可选）
    - order: 排序顺序（0:从大到小 1:从小到大）
    - rankingType: 排行类型（0:批量 1:查错）
    - recordStatus: 记录状态（可选）

    返回数据：
    - code: 状态码
    - msg: 返回消息
    - success: 是否成功
    - data: 排行数据
      * titleList: 设备名称列表
      * dataList: 对应的排行数据
      * device_details: 设备详细信息（可选）
        - rank: 排名
        - device_code: 设备编码
        - device_name: 设备名称
        - usage_count: 用刀次数
        - total_amount: 总金额
        - avg_usage_duration: 平均使用时长
        - usage_efficiency: 使用效率
    """
    try:
        logger.info(f"调用设备用刀排行接口，参数: {locals()}")
        params = {
            "startTime": start_time,
            "endTime": end_time,
            "order": order,
            "rankingType": ranking_type,
            "recordStatus": record_status
        }

        result = api_client.get_device_ranking(params)
        logger.info(f"设备用刀排行返回结果: {result}")
        return result

    except Exception as e:
        logger.error(f"获取设备用刀排行失败: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"获取设备用刀排行失败: {str(e)}")


@router.get("/knife-model-ranking", response_model=KnifeModelRankingResponse, tags=["刀具排行"])
async def get_knife_model_ranking(
        start_time: Optional[str] = Query(None, alias="startTime", description="开始时间"),
        end_time: Optional[str] = Query(None, alias="endTime", description="结束时间"),
        order: Optional[int] = Query(None, description="顺序 0:从大到小 1:从小到大"),
        ranking_type: Optional[int] = Query(None, alias="rankingType", description="0:数量 1:金额"),
        record_status: Optional[int] = Query(None, alias="recordStatus", description="记录状态")
):
    """
    刀具型号排行

    功能：获取刀具型号排行数据，按使用数量或金额排序
    封装外部接口：/api/mifc/web/from/me/statistics/charts@tuttenbanking

    参数说明：
    - startTime: 开始时间（可选）
    - endTime: 结束时间（可选）
    - order: 排序顺序（0:从大到小 1:从小到大）
    - rankingType: 排行类型（0:数量 1:金额）
    - recordStatus: 记录状态（可选）

    返回数据：
    - code: 状态码
    - msg: 返回消息
    - success: 是否成功
    - data: 排行数据
      * titleList: 刀具型号列表
      * dataList: 对应的排行数据
      * knife_model_details: 刀具型号详细信息（可选）
        - rank: 排名
        - model: 刀具型号
        - knife_type: 刀具类型
        - brand: 品牌名称
        - usage_count: 使用次数
        - total_amount: 总金额
        - avg_lifespan: 平均寿命
        - popularity: 受欢迎度
    """
    try:
        params = {
            "startTime": start_time,
            "endTime": end_time,
            "order": order,
            "rankingType": ranking_type,
            "recordStatus": record_status
        }

        return api_client.get_knife_model_ranking(params)

    except Exception as e:
        logger.error(f"获取刀具型号排行失败: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"获取刀具型号排行失败: {str(e)}")


@router.get("/employee-ranking", response_model=EmployeeRankingResponse, tags=["员工排行"])
async def get_employee_ranking(
        start_time: Optional[str] = Query(None, alias="startTime", description="开始时间"),
        end_time: Optional[str] = Query(None, alias="endTime", description="结束时间"),
        order: Optional[int] = Query(None, description="顺序 0:从大到小 1:从小到大"),
        ranking_type: Optional[int] = Query(None, alias="rankingType", description="排行类型"),
        record_status: Optional[int] = Query(None, alias="recordStatus", description="记录状态")
):
    """
    员工领刀排行

    功能：获取员工领刀排行数据，按领刀次数或金额排序
    封装外部接口：/go/kaife/web/from/mss/statistics/chartslandHunting

    参数说明：
    - startTime: 开始时间（可选）
    - endTime: 结束时间（可选）
    - order: 排序顺序（0:从大到小 1:从小到大）
    - rankingType: 排行类型
    - recordStatus: 记录状态（可选）

    返回数据：
    - code: 状态码
    - msg: 返回消息
    - success: 是否成功
    - data: 排行数据
      * titleList: 员工姓名列表
      * dataList: 对应的排行数据
      * employee_details: 员工详细信息（可选）
        - rank: 排名
        - employee_name: 员工姓名
        - department: 部门
        - borrow_count: 领刀次数
        - total_amount: 总金额
        - avg_amount: 平均金额
        - last_borrow_time: 最后领刀时间
    """
    try:
        params = {
            "startTime": start_time,
            "endTime": end_time,
            "order": order,
            "rankingType": ranking_type,
            "recordStatus": record_status
        }

        return api_client.get_employee_ranking(params)

    except Exception as e:
        logger.error(f"获取员工领刀排行失败: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"获取员工领刀排行失败: {str(e)}")


@router.get("/error-return-ranking", response_model=ErrorReturnRankingResponse, tags=["异常排行"])
async def get_error_return_ranking(
        start_time: Optional[str] = Query(None, alias="startTime", description="开始时间"),
        end_time: Optional[str] = Query(None, alias="endTime", description="结束时间"),
        order: Optional[int] = Query(None, description="顺序 0:从大到小 1:从小到大"),
        ranking_type: Optional[int] = Query(None, alias="rankingType", description="0:批量 1:金额"),
        record_status: Optional[int] = Query(None, alias="recordStatus", description="记录状态")
):
    """
    异常还刀排行

    功能：获取异常还刀排行数据，按异常次数或损失金额排序
    封装外部接口：/ou/knife/web/from/news/statsstics/dhatsErrorBorrow

    参数说明：
    - startTime: 开始时间（可选）
    - endTime: 结束时间（可选）
    - order: 排序顺序（0:从大到小 1:从小到大）
    - rankingType: 排行类型（0:批量 1:金额）
    - recordStatus: 记录状态（可选）

    返回数据：
    - code: 状态码
    - msg: 返回消息
    - success: 是否成功
    - data: 排行数据
      * titleList: 异常类型或员工列表
      * dataList: 对应的排行数据
      * error_return_details: 异常还刀详细信息（可选）
        - rank: 排名
        - employee_name: 员工姓名
        - department: 部门
        - error_count: 异常次数
        - error_type: 异常类型
        - total_loss: 总损失
        - last_error_time: 最后异常时间
    """
    try:
        params = {
            "startTime": start_time,
            "endTime": end_time,
            "order": order,
            "rankingType": ranking_type,
            "recordStatus": record_status
        }

        return api_client.get_error_return_ranking(params)

    except Exception as e:
        logger.error(f"获取异常还刀排行失败: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"获取异常还刀排行失败: {str(e)}")


# ==================== 系统记录相关接口 ====================

# 合并自 auditor_record 模块的系统记录接口
# 日期: 2025-11-15

# 领刀记录相关路由
@router.get("/list", response_model=LendRecordResponse, tags=["领刀记录"])
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


@router.get("/export", tags=["领刀记录"])
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


# 告警预警相关路由
@router.get("/alarm_list", response_model=AlarmWarningResponse, tags=["告警预警"])
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


@router.get("/alarm_statistics", response_model=AlarmStatisticsResponse, tags=["告警预警"])
async def get_alarm_statistics():
    """
    获取告警统计信息

    Returns:
        AlarmStatisticsResponse: 告警统计信息响应
    """
    result = api_client.get_alarm_statistics()

    return result


@router.post("/alarm_threshold", tags=["告警预警"])
async def update_alarm_threshold(
        request: ThresholdSettingRequest = Body(..., description="阈值设置请求参数")
):
    """
    更新告警阈值

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


@router.post("/handle_alarm/{alarm_id}", tags=["告警预警"])
async def handle_alarm_warning(
        alarm_id: int,
        handle_status: int = Body(..., description="处理状态"),
        handle_remark: Optional[str] = Body(None, description="处理备注")
):
    """
    处理告警预警

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


@router.post("/batch_handle_alarm", tags=["告警预警"])
async def batch_handle_alarm_warning(
        ids: List[int] = Body(..., description="告警ID列表"),
        handle_status: int = Body(..., description="处理状态"),
        handle_remark: Optional[str] = Body(None, description="处理备注")
):
    """
    批量处理告警预警

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


@router.get("/export_alarm", tags=["告警预警"])
async def export_alarm_warning(
        loc_surplus: Optional[int] = Query(None, description="货道"),
        alarm_level: Optional[int] = Query(None, description="预警等级"),
        device_type: Optional[str] = Query(None, description="设备类型"),
        cabinet_code: Optional[str] = Query(None, description="刀柜编码"),
        brand_name: Optional[str] = Query(None, description="品牌名称"),
        handle_status: Optional[int] = Query(None, description="处理状态")
):
    """
    导出告警预警

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


# 补货记录相关路由
@router.get("/replenish_list", response_model=ReplenishRecordResponse, tags=["补货记录"])
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


@router.get("/export_replenish", tags=["补货记录"])
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


# 公共暂存记录相关路由
@router.get("/storage_list", response_model=StorageRecordModelResponse, tags=["公共暂存记录"])
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
        StorageRecordModelResponse: 公共暂存记录列表响应
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


@router.get("/export_storage", tags=["公共暂存记录"])
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