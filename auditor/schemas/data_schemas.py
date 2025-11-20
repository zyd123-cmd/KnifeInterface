from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Union, Any
from datetime import datetime
#ok

# ==================== 用户相关模型 ====================
class OriginalUserResponse(BaseModel):
    id: int
    name: str
    email: str
    created_at: Optional[str] = None


class EnhancedUserResponse(BaseModel):
    user_id: int
    user_name: str
    email_address: str
    account_status: str
    additional_data: dict
    processed_at: str


# ==================== 出入库统计相关模型 ====================
class StorageStatisticsQueryParams(BaseModel):
    """出入库统计查询参数"""
    current: Optional[int] = 1  # 当前页
    size: Optional[int] = 10  # 每页数量
    startTime: Optional[str] = None  # 开始时间（格式：YYYY-MM-DD HH:mm:ss）
    endTime: Optional[str] = None  # 结束时间（格式：YYYY-MM-DD HH:mm:ss）
    recordStatus: Optional[int] = None  # 记录状态：0-取刀，1-还刀，2-收刀，3-暂存，4-完成，5-违规还刀
    rankingType: Optional[int] = None  # 排名类型：0-按数量排序，1-按金额排序
    order: Optional[int] = None  # 排序顺序：0-从大到小（降序），1-从小到大（升序）


class StorageRecord(BaseModel):
    """出入库记录"""
    account: Optional[str] = None  # 用户名
    brandCode: Optional[str] = None  # 品牌编码
    brandName: Optional[str] = None  # 品牌名称
    cabinetCode: Optional[str] = None  # 刀柜编码
    cabinetName: Optional[str] = None  # 刀具柜名称
    createTime: Optional[str] = None  # 创建时间
    cutterCode: Optional[str] = None  # 刀具型号
    cutterId: Optional[int] = None  # 耗材主键
    cutterType: Optional[str] = None  # 刀具类型
    detailsCode: Optional[str] = None  # 操作详情编码
    detailsName: Optional[str] = None  # 操作详情名称
    factoryName: Optional[str] = None  # 工厂名称
    id: Optional[int] = None  # 主键id
    name: Optional[str] = None  # 用户名称
    oldPrice: Optional[float] = None  # 历史单价
    operator: Optional[str] = None  # 操作人
    price: Optional[float] = None  # 单价
    quantity: Optional[int] = None  # 数量
    remake: Optional[str] = None  # 备注
    specification: Optional[str] = None  # 规格
    status: Optional[int] = None  # 业务状态
    stockLoc: Optional[str] = None  # 库位号
    stockType: Optional[int] = None  # 0:入库 1:出库
    updateTime: Optional[str] = None  # 更新时间
    workshopName: Optional[str] = None  # 车间名称


class StorageStatisticsListData(BaseModel):
    """出入库统计列表数据"""
    current: int  # 当前页
    size: int  # 每页数量
    total: int  # 总记录数
    pages: int  # 总页数
    records: List[StorageRecord]  # 记录列表


class StorageStatisticsResponse(BaseModel):
    """出入库统计响应"""
    code: int
    msg: str
    success: bool
    data: Optional[dict] = None  # 包含分页数据


# ==================== 图表统计相关模型 ====================
class ChartsData(BaseModel):
    """统计图表数据（全年取刀数量，全年取刀金额，刀具消耗数据）"""
    titleList: List[str] = []  # 标题列表（如月份或刀具类型）
    dataList: List[Union[str, int, float]] = []  # 数据列表（支持字符串、整数、浮点数）


class ChartsResponse(BaseModel):
    """统计图表响应（全年取刀数量，全年取刀金额，刀具消耗响应）"""
    code: int
    msg: str
    success: bool
    data: Optional[ChartsData] = None


class ExtendedChartsData(BaseModel):
    """扩展的图表数据结构 - 包含详细字段"""
    dataList: List[Union[str, int, float]] = []  # 添加缺失的字段
    titleList: List[str] = []  # 添加缺失的字段
    # 扩展字段 - 使用 Optional 避免验证错误
    device_details: Optional[List['DeviceRankingDetail']] = None
    employee_details: Optional[List['EmployeeRankingDetail']] = None
    knife_model_details: Optional[List['KnifeModelRankingDetail']] = None
    error_return_details: Optional[List['ErrorReturnRankingDetail']] = None


# ==================== 总库存统计相关模型 ====================
class TotalStockQueryParams(BaseModel):
    """总库存统计查询参数"""
    statisticsType: Optional[str] = None  # 统计类型
    brandName: Optional[str] = None  # 品牌名称
    cabinetCode: Optional[str] = None  # 刀柜编码
    cutterType: Optional[str] = None  # 刀具类型
    stockStatus: Optional[int] = None  # 库位状态
    current: Optional[int] = 1  # 当前页
    size: Optional[int] = 10  # 每页数量


class StockLocationDetail(BaseModel):
    """取刀柜库位详情"""
    id: Optional[int] = None  # 主键id
    brandCode: Optional[str] = None  # 品牌编码
    brandName: Optional[str] = None  # 品牌名称
    cabinetCode: Optional[str] = None  # 刀柜编码
    cabinetName: Optional[str] = None  # 刀具柜名称
    cutterCode: Optional[str] = None  # 刀具型号
    cutterId: Optional[int] = None  # 物料编码主键
    cutterType: Optional[str] = None  # 刀具类型
    imageUrl: Optional[str] = None  # 图片路径
    locCapacity: Optional[int] = None  # 库位容量
    locPackQty: Optional[int] = None  # 货道包装数量
    locSurplus: Optional[int] = None  # 库位产品剩余[货道库存]
    locType: Optional[int] = None  # 库位类型[收刀柜: 0 取刀柜: 1]
    materialCode: Optional[str] = None  # 物料编码
    materialType: Optional[str] = None  # 物料类型
    packQty: Optional[int] = None  # 最小包装数量
    price: Optional[float] = None  # 单价
    specification: Optional[str] = None  # 规格
    stockLoc: Optional[str] = None  # 库位号
    stockNum: Optional[int] = None  # 当前库存数
    stockStatus: Optional[int] = None  # 库位状态
    warningNum: Optional[int] = None  # 警报数量
    warehouseInTime: Optional[str] = None  # 入库时间
    updateTime: Optional[str] = None  # 更新时间

    # 计算字段（前端展示用）
    stockValue: Optional[float] = None  # 库存价值（单价 * 剩余数量）
    cabinetSide: Optional[str] = None  # 柜子面


class TotalStockResponse(BaseModel):
    """总库存统计响应"""
    code: int
    msg: str
    success: bool
    data: Optional[dict] = None  # 包含分页数据或列表数据


# ==================== 废刀回收统计相关模型 ====================
class ReturnKnifeDetail(BaseModel):
    """还刀信息详情"""
    id: Optional[int] = None  # 取刀主键
    borrowStatus: Optional[int] = None  # 还刀状态：0-修磨，1-报废，2-换线，3-错领
    borrowTime: Optional[str] = None  # 还刀时间
    borrowUserName: Optional[str] = None  # 还刀人
    brandName: Optional[str] = None  # 品牌名称
    cutterCode: Optional[str] = None  # 刀具型号
    cutterType: Optional[str] = None  # 刀具类型
    lendTime: Optional[str] = None  # 取刀时间
    lendUserName: Optional[str] = None  # 借刀人
    recordStatus: Optional[int] = None  # 记录状态：0-取刀，1-还刀，2-收刀，3-暂存
    specification: Optional[str] = None  # 规格
    stockLoc: Optional[str] = None  # 库位号


class ReturnKnifeData(BaseModel):
    """收刀柜还刀数据"""
    borrowStatus: Optional[str] = None  # 还刀状态（字符串形式）
    cabinetCode: Optional[str] = None  # 刀柜编码
    recordStatus: Optional[int] = None  # 记录状态：0-取刀，1-还刀，2-收刀，3-暂存
    list: Optional[List[ReturnKnifeDetail]] = []  # 还刀详情列表


class WasteKnifeRecycleResponse(BaseModel):
    """废刀回收统计响应"""
    code: int
    msg: str
    success: bool
    data: Optional[ReturnKnifeData] = None  # 还刀数据


# ==================== 排行接口模型 ====================
class RankingBaseRequest(BaseModel):
    """排行接口基础请求参数"""
    startTime: Optional[str] = None
    endTime: Optional[str] = None
    order: Optional[int] = None
    rankingType: Optional[int] = None
    recordStatus: Optional[int] = None


class DeviceRankingDetail(BaseModel):
    """设备用刀排行详细数据项"""
    rank: int  # 排名
    device_code: str  # 设备编码
    device_name: str  # 设备名称
    usage_count: int  # 用刀次数
    total_amount: float  # 总金额
    avg_usage_duration: float  # 平均使用时长（小时）
    usage_efficiency: float  # 使用效率（百分比）


class EmployeeRankingDetail(BaseModel):
    """员工领刀排行详细数据项 - 根据合并前版本修复"""
    rank: int  # 排名
    employee_name: str  # 员工姓名
    department: str  # 部门
    borrow_count: int  # 领刀次数
    total_amount: float  # 总金额
    avg_amount: float  # 平均金额
    last_borrow_time: str  # 最后领刀时间


class KnifeModelRankingDetail(BaseModel):
    """刀具型号排行详细数据项"""
    rank: int  # 排名
    model: str  # 刀具型号
    knife_type: str  # 刀具类型
    brand: str  # 品牌名称
    usage_count: int  # 使用次数
    total_amount: float  # 总金额
    avg_lifespan: float  # 平均寿命（小时）
    popularity: float  # 受欢迎度（百分比）


class ErrorReturnRankingDetail(BaseModel):
    """异常还刀排行详细数据项"""
    rank: int  # 排名
    employee_name: str  # 员工姓名
    department: str  # 部门
    error_count: int  # 异常次数
    error_type: str  # 异常类型
    total_loss: float  # 总损失
    last_error_time: str  # 最后异常时间


class RankingBaseResponse(BaseModel):
    """排行接口基础响应"""
    code: int
    msg: str
    success: bool
    data: Optional[dict] = None  # 修复：允许data为None或字典


class DeviceRankingResponse(RankingBaseResponse):
    """设备用刀排行响应"""
    pass


class KnifeModelRankingResponse(RankingBaseResponse):
    """刀具型号排行响应"""
    pass


class EmployeeRankingResponse(RankingBaseResponse):
    """员工领刀排行响应"""
    pass


class ErrorReturnRankingResponse(RankingBaseResponse):
    """异常还刀排行响应"""
    pass


# ==================== 系统记录相关模型 ====================

# 合并自 auditor_record 模块的系统记录模型
# 日期: 2025-11-15
# 来源: auditor_record/schemas/data_schemas.py

class ReplenishRecord(BaseModel):
    """
    补货记录模型
    """
    id: Optional[int] = None
    brandName: Optional[str] = None  # 品牌名称
    cabinetCode: Optional[str] = None  # 刀柜编码
    createDept: Optional[int] = None  # 创建部门
    createTime: Optional[str] = None  # 创建时间
    createUser: Optional[int] = None  # 创建人
    cutterCode: Optional[str] = None  # 刀具型号
    cutterType: Optional[str] = None  # 刀具类型
    detailsCode: Optional[str] = None  # 操作详情
    isDeleted: Optional[int] = None  # 是否已删除
    lendUserName: Optional[str] = None  # 取出人
    logStatus: Optional[int] = None  # 日志状态
    logType: Optional[str] = None  # 日志类型
    materialCode: Optional[str] = None  # 物料编码
    newPrice: Optional[float] = None  # 新单价
    newStockNum: Optional[int] = None  # 操作后库存数
    oldPrice: Optional[float] = None  # 老单价
    oldStockNum: Optional[int] = None  # 操作前库存数
    operator: Optional[str] = None  # 操作人
    quantity: Optional[int] = None  # 数量
    remake: Optional[str] = None  # 备注
    specification: Optional[str] = None  # 规格
    status: Optional[int] = None  # 业务状态
    stockLoc: Optional[str] = None  # 库位号
    storageUserName: Optional[str] = None  # 暂存人
    tenantId: Optional[str] = None  # 租户ID
    updateTime: Optional[str] = None  # 更新时间
    updateUser: Optional[int] = None  # 更新人

    model_config = ConfigDict(from_attributes=True)


class ReplenishRecordData(BaseModel):
    """
    补货记录分页数据
    """
    current: int
    hitCount: bool
    pages: int
    records: List[ReplenishRecord]
    searchCount: bool
    size: int
    total: int

    model_config = ConfigDict(from_attributes=True)


class ReplenishRecordResponse(BaseModel):
    """
    补货记录响应模型
    """
    code: int
    data: ReplenishRecordData
    msg: str
    success: bool

    model_config = ConfigDict(from_attributes=True)


class ReplenishRecordListRequest(BaseModel):
    """
    补货记录列表请求参数
    """
    current: Optional[int] = None  # 当前页
    endTime: Optional[str] = None  # 结束时间
    order: Optional[int] = None  # 顺序 0: 从大到小 1：从小到大
    rankingType: Optional[int] = None  # 0: 数量 1: 金额
    recordStatus: Optional[int] = None  # 0: 取刀 1: 还刀 2: 收刀 3: 暂存 4: 完成 5：违规还刀
    size: Optional[int] = None  # 每页的数量
    startTime: Optional[str] = None  # 开始时间

    model_config = ConfigDict(from_attributes=True)


class ExportReplenishRecordRequest(BaseModel):
    """
    导出补货记录请求参数
    """
    endTime: Optional[str] = None  # 结束时间
    order: Optional[int] = None  # 顺序 0: 从大到小 1：从小到大
    rankingType: Optional[int] = None  # 0: 数量 1: 金额
    recordStatus: Optional[int] = None  # 0: 取刀 1: 还刀 2: 收刀 3: 暂存 4: 完成 5：违规还刀
    startTime: Optional[str] = None  # 开始时间

    model_config = ConfigDict(from_attributes=True)


# 领刀记录相关模型
class LendRecord(BaseModel):
    """
    领刀记录模型
    """
    # 取刀人相关信息
    lendUser: int  # 取刀人ID
    lendUserName: str  # 取刀人
    borrowUserName: Optional[str] = None  # 还刀人

    # 品牌信息
    brandName: str  # 品牌名称
    brandCode: str  # 品牌编码

    # 刀具信息
    cutterType: str  # 刀具类型
    cutterCode: str  # 刀具型号
    specification: str  # 规格
    materialCode: str  # 物料编码
    price: float  # 单价

    # 位置信息
    cabinetCode: str  # 刀柜编码
    lendStock: str  # 借刀库位号
    borrowStock: Optional[str] = None  # 还刀库位号

    # 时间信息
    lendTime: str  # 借刀时间
    borrowTime: Optional[str] = None  # 还刀时间
    finalCollectTime: Optional[str] = None  # 最终确认时间

    # 状态信息
    recordStatus: int  # 记录状态 (0: 取刀 1: 还刀 2: 收刀 3: 暂存 4: 完成 5：违规还刀)
    borrowStatus: Optional[int] = None  # 还刀状态 (0: 修磨 1: 报废 2: 换线 3: 错领)
    finalCollectStatus: Optional[int] = None  # 最终确认状态 (0: 通过 1: 未通过)

    # 备注和结果
    borrowRemarks: Optional[str] = None  # 还刀备注
    finalCollectRemarks: Optional[str] = None  # 最终确认结果
    collectStatus: Optional[str] = None  # 管理员确认结果

    model_config = ConfigDict(from_attributes=True)


class LendRecordData(BaseModel):
    """
    领刀记录分页数据
    """
    current: int
    hitCount: bool
    pages: int
    records: List[LendRecord]
    searchCount: bool
    size: int
    total: int

    model_config = ConfigDict(from_attributes=True)


class LendRecordResponse(BaseModel):
    """
    领刀记录响应模型
    """
    code: int
    data: LendRecordData
    msg: str
    success: bool

    model_config = ConfigDict(from_attributes=True)


class LendRecordListRequest(BaseModel):
    """
    领刀记录列表请求参数
    """
    current: int = 1
    size: int = 20
    keyword: Optional[str] = None  # 关键字搜索
    department: Optional[str] = None  # 部门筛选
    startTime: Optional[str] = None  # 开始时间
    endTime: Optional[str] = None  # 结束时间
    order: Optional[int] = None  # 顺序 0: 从大到小 1：从小到大
    rankingType: Optional[int] = None  # 0: 数量 1: 金额
    recordStatus: Optional[int] = None  # 0: 取刀 1: 还刀 2: 收刀 3: 暂存 4: 完成 5：违规还刀

    model_config = ConfigDict(from_attributes=True)


class ExportLendRecordRequest(BaseModel):
    """
    导出领刀记录请求参数
    """
    endTime: Optional[str] = None  # 结束时间
    order: Optional[int] = None  # 顺序 0: 从大到小 1：从小到大
    rankingType: Optional[int] = None  # 0: 数量 1: 金额
    recordStatus: Optional[int] = None  # 0: 取刀 1: 还刀 2: 收刀 3: 暂存 4: 完成 5：违规还刀
    startTime: Optional[str] = None  # 开始时间

    model_config = ConfigDict(from_attributes=True)


# 公共暂存记录相关模型
class StorageRecordModel(BaseModel):
    """
    公共暂存记录模型
    """
    id: Optional[int] = None  # 主键ID
    brandName: Optional[str] = None  # 品牌名称
    cabinetCode: Optional[str] = None  # 刀柜编码
    createDept: Optional[int] = None  # 创建部门
    createTime: Optional[str] = None  # 创建时间
    createUser: Optional[int] = None  # 创建人
    cutterCode: Optional[str] = None  # 刀具型号
    detailsCode: Optional[str] = None  # 操作详情
    isDeleted: Optional[int] = None  # 是否已删除
    lendUserName: Optional[str] = None  # 取出人
    logStatus: Optional[int] = None  # 日志状态
    materialCode: Optional[str] = None  # 物料编码
    newPrice: Optional[float] = None  # 新单价
    newStockNum: Optional[int] = None  # 操作后库存数
    oldPrice: Optional[float] = None  # 老单价
    oldStockNum: Optional[int] = None  # 操作前库存数
    operator: Optional[str] = None  # 操作人
    quantity: Optional[int] = None  # 数量
    remake: Optional[str] = None  # 备注
    specification: Optional[str] = None  # 规格
    status: Optional[int] = None  # 业务状态
    stockLoc: Optional[str] = None  # 库位号
    storageUserName: Optional[str] = None  # 暂存人
    tenantId: Optional[str] = None  # 租户ID
    updateTime: Optional[str] = None  # 更新时间
    updateUser: Optional[int] = None  # 更新人

    model_config = ConfigDict(from_attributes=True)


class StorageRecordModelData(BaseModel):
    """
    公共暂存记录分页数据
    """
    current: int
    hitCount: bool
    pages: int
    records: List[StorageRecordModel]
    searchCount: bool
    size: int
    total: int

    model_config = ConfigDict(from_attributes=True)


class StorageRecordModelResponse(BaseModel):
    """
    公共暂存记录响应模型
    """
    code: int
    data: StorageRecordModelData
    msg: str
    success: bool

    model_config = ConfigDict(from_attributes=True)


class StorageRecordListRequest(BaseModel):
    """
    公共暂存记录列表请求参数
    """
    current: Optional[int] = None  # 当前页
    endTime: Optional[str] = None  # 结束时间
    order: Optional[int] = None  # 顺序 0: 从大到小 1：从小到大
    rankingType: Optional[int] = None  # 0: 数量 1: 金额
    recordStatus: Optional[int] = None  # 0: 取刀 1: 还刀 2: 收刀 3: 暂存 4: 完成 5：违规还刀
    size: Optional[int] = None  # 每页的数量
    startTime: Optional[str] = None  # 开始时间

    model_config = ConfigDict(from_attributes=True)


class ExportStorageRecordRequest(BaseModel):
    """
    导出公共暂存记录请求参数
    """
    endTime: Optional[str] = None  # 结束时间
    order: Optional[int] = None  # 顺序 0: 从大到小 1：从小到大
    rankingType: Optional[int] = None  # 0: 数量 1: 金额
    recordStatus: Optional[int] = None  # 0: 取刀 1: 还刀 2: 收刀 3: 暂存 4: 完成 5：违规还刀
    startTime: Optional[str] = None  # 开始时间

    model_config = ConfigDict(from_attributes=True)


# 告警预警相关模型
class AlarmWarning(BaseModel):
    """
    告警预警模型
    """
    id: int
    locSurplus: int  # 货道
    alarmLevel: int  # 预警等级
    deviceType: str  # 设备类型
    cabinetCode: str  # 刀柜编码
    stockLoc: str  # 库位号
    brandName: str  # 品牌名称
    itemCode: str  # 物品编码
    itemType: str  # 物品类型
    currentStock: int  # 当前库存
    thresholdValue: int  # 阈值
    alarmMessage: str  # 预警信息
    handleStatus: int  # 处理状态
    createTime: str  # 预警时间
    handleTime: Optional[str] = None  # 处理时间
    handleUser: Optional[str] = None  # 处理人
    handleRemark: Optional[str] = None  # 处理备注

    model_config = ConfigDict(from_attributes=True)


class AlarmWarningData(BaseModel):
    """
    告警预警分页数据
    """
    current: int
    hitCount: bool
    pages: int
    records: List[AlarmWarning]
    searchCount: bool
    size: int
    total: int

    model_config = ConfigDict(from_attributes=True)


class AlarmWarningResponse(BaseModel):
    """
    告警预警响应模型
    """
    code: int
    data: AlarmWarningData
    msg: str
    success: bool

    model_config = ConfigDict(from_attributes=True)


class AlarmWarningListRequest(BaseModel):
    """
    告警预警列表请求参数
    """
    locSurplus: Optional[int] = None  # 货道
    alarmLevel: Optional[int] = None  # 预警等级
    deviceType: Optional[str] = None  # 设备类型
    cabinetCode: Optional[str] = None  # 刀柜编码
    brandName: Optional[str] = None  # 品牌名称
    handleStatus: Optional[int] = None  # 处理状态
    current: Optional[int] = None  # 当前页
    size: Optional[int] = None  # 每页数量

    model_config = ConfigDict(from_attributes=True)


class ThresholdSetting(BaseModel):
    """
    阈值设置模型
    """
    locSurplus: int  # 货道
    alarmThreshold: int  # 预警阈值

    model_config = ConfigDict(from_attributes=True)


class ThresholdSettingRequest(BaseModel):
    """
    阈值设置请求参数
    """
    locSurplus: int  # 货道
    alarmThreshold: int  # 预警阈值

    model_config = ConfigDict(from_attributes=True)


class AlarmStatistics(BaseModel):
    """
    告警统计模型
    """
    level1Count: int  # 安全库存量预警数量
    level2Count: int  # 采集阈值存储量预警数量
    level3Count: int  # 紧急补货存储量报警数量
    unhandledCount: int  # 未处理预警总数

    model_config = ConfigDict(from_attributes=True)


class AlarmStatisticsResponse(BaseModel):
    """
    告警统计响应模型
    """
    code: int
    data: AlarmStatistics
    msg: str
    success: bool

    model_config = ConfigDict(from_attributes=True)