from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


# 补货记录相关模型
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

    class Config:
        orm_mode = True

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
    
    class Config:
        orm_mode = True

class ReplenishRecordResponse(BaseModel):
    """
    补货记录响应模型
    """
    code: int
    data: ReplenishRecordData
    msg: str
    success: bool
    
    class Config:
        orm_mode = True

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
    
    class Config:
        orm_mode = True

class ExportReplenishRecordRequest(BaseModel):
    """
    导出补货记录请求参数
    """
    endTime: Optional[str] = None  # 结束时间
    order: Optional[int] = None  # 顺序 0: 从大到小 1：从小到大
    rankingType: Optional[int] = None  # 0: 数量 1: 金额
    recordStatus: Optional[int] = None  # 0: 取刀 1: 还刀 2: 收刀 3: 暂存 4: 完成 5：违规还刀
    startTime: Optional[str] = None  # 开始时间
    
    class Config:
        orm_mode = True


# 领刀记录相关模型
class LendRecord(BaseModel):
    """
    领刀记录模型
    """
    # 取刀人相关信息
    lendUser: int  # 取刀人ID
    lendUserName: str  # 取刀人
    borrowUserName: Optional[str]  # 还刀人
    
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
    borrowStock: Optional[str]  # 还刀库位号
    
    # 时间信息
    lendTime: str  # 借刀时间
    borrowTime: Optional[str]  # 还刀时间
    finalCollectTime: Optional[str]  # 最终确认时间
    
    # 状态信息
    recordStatus: int  # 记录状态 (0: 取刀 1: 还刀 2: 收刀 3: 暂存 4: 完成 5：违规还刀)
    borrowStatus: Optional[int]  # 还刀状态 (0: 修磨 1: 报废 2: 换线 3: 错领)
    finalCollectStatus: Optional[int]  # 最终确认状态 (0: 通过 1: 未通过)
    
    # 备注和结果
    borrowRemarks: Optional[str]  # 还刀备注
    finalCollectRemarks: Optional[str]  # 最终确认结果
    collectStatus: Optional[str]  # 管理员确认结果
    
    class Config:
        orm_mode = True

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
    
    class Config:
        orm_mode = True

class LendRecordResponse(BaseModel):
    """
    领刀记录响应模型
    """
    code: int
    data: LendRecordData
    msg: str
    success: bool
    
    class Config:
        orm_mode = True

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
    
    class Config:
        orm_mode = True

class ExportLendRecordRequest(BaseModel):
    """
    导出领刀记录请求参数
    """
    endTime: Optional[str] = None  # 结束时间
    order: Optional[int] = None  # 顺序 0: 从大到小 1：从小到大
    rankingType: Optional[int] = None  # 0: 数量 1: 金额
    recordStatus: Optional[int] = None  # 0: 取刀 1: 还刀 2: 收刀 3: 暂存 4: 完成 5：违规还刀
    startTime: Optional[str] = None  # 开始时间
    
    class Config:
        orm_mode = True


# 公共暂存记录相关模型
class StorageRecord(BaseModel):
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

    class Config:
        orm_mode = True

class StorageRecordData(BaseModel):
    """
    公共暂存记录分页数据
    """
    current: int
    hitCount: bool
    pages: int
    records: List[StorageRecord]
    searchCount: bool
    size: int
    total: int
    
    class Config:
        orm_mode = True

class StorageRecordResponse(BaseModel):
    """
    公共暂存记录响应模型
    """
    code: int
    data: StorageRecordData
    msg: str
    success: bool
    
    class Config:
        orm_mode = True

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
    
    class Config:
        orm_mode = True

class ExportStorageRecordRequest(BaseModel):
    """
    导出公共暂存记录请求参数
    """
    endTime: Optional[str] = None  # 结束时间
    order: Optional[int] = None  # 顺序 0: 从大到小 1：从小到大
    rankingType: Optional[int] = None  # 0: 数量 1: 金额
    recordStatus: Optional[int] = None  # 0: 取刀 1: 还刀 2: 收刀 3: 暂存 4: 完成 5：违规还刀
    startTime: Optional[str] = None  # 开始时间
    
    class Config:
        orm_mode = True


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

    class Config:
        orm_mode = True

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
    
    class Config:
        orm_mode = True

class AlarmWarningResponse(BaseModel):
    """
    告警预警响应模型
    """
    code: int
    data: AlarmWarningData
    msg: str
    success: bool
    
    class Config:
        orm_mode = True

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
    
    class Config:
        orm_mode = True

class ThresholdSetting(BaseModel):
    """
    阈值设置模型
    """
    locSurplus: int  # 货道
    alarmThreshold: int  # 预警阈值
    
    class Config:
        orm_mode = True

class ThresholdSettingRequest(BaseModel):
    """
    阈值设置请求参数
    """
    locSurplus: int  # 货道
    alarmThreshold: int  # 预警阈值
    
    class Config:
        orm_mode = True

class AlarmStatistics(BaseModel):
    """
    告警统计模型
    """
    level1Count: int  # 安全库存量预警数量
    level2Count: int  # 采集阈值存储量预警数量
    level3Count: int  # 紧急补货存储量报警数量
    unhandledCount: int  # 未处理预警总数
    
    class Config:
        orm_mode = True

class AlarmStatisticsResponse(BaseModel):
    """
    告警统计响应模型
    """
    code: int
    data: AlarmStatistics
    msg: str
    success: bool
    
    class Config:
        orm_mode = True
