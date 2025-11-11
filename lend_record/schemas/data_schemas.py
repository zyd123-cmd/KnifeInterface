from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class LendRecord(BaseModel):
    """
    领刀记录模型
    """
    # 取刀人相关信息
    lendUser: int  # 取刀人ID
    lendUserName: str  # 取刀人
    
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
    borrowTime: Optional[str] # 还刀时间
    finalCollectTime: Optional[str]  # 最终确认时间
    
    # 状态信息
    recordStatus: int  # 记录状态 (0: 取刀 1: 还刀 2: 收刀 3: 暂存 4: 完成 5：违规还刀)
    borrowStatus: Optional[int] # 还刀状态 (0: 修磨 1: 报废 2: 换线 3: 错领)
    finalCollectStatus: Optional[int] # 最终确认状态 (0: 通过 1: 未通过)
    
    # 备注和结果
    borrowRemarks: Optional[str] # 还刀备注
    finalCollectRemarks: Optional[str] # 最终确认结果
    collectStatus: Optional[str] # 管理员确认结果
    
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
    page: int = 1
    page_size: int = 20
    keyword: Optional[str] = None # 关键字搜索
    department: Optional[str] = None # 部门筛选
    start_date: Optional[str] = None # 开始日期
    end_date: Optional[str] = None # 结束日期
    order: Optional[int] = None # 顺序 0: 从大到小 1：从小到大
    rankingType: Optional[int] = None # 0: 数量 1: 金额
    recordStatus: Optional[int] = None # 0: 取刀 1: 还刀 2: 收刀 3: 暂存 4: 完成 5：违规还刀
    
    class Config:
        orm_mode = True


class ExportLendRecordRequest(BaseModel):
    """
    导出领刀记录请求参数
    """
    endTime: Optional[str] = None # 结束时间
    order: Optional[int] = None # 顺序 0: 从大到小 1：从小到大
    rankingType: Optional[int] = None # 0: 数量 1: 金额
    recordStatus: Optional[int] = None # 0: 取刀 1: 还刀 2: 收刀 3: 暂存 4: 完成 5：违规还刀
    startTime: Optional[str] = None # 开始时间
    
    class Config:
        orm_mode = True


class ItemDto(BaseModel):
    """
    刀柜货道项模型
    """
    locSurplus: Optional[int]  # 货道刀具数量
    stockId: Optional[int]      # 刀柜编码（根据文档描述，实际是stockId）
    
    class Config:
        orm_mode = True


class RestockRequest(BaseModel):
    """
    补货请求模型
    """
    replenishDto: Optional[dict] = None  # replenishDto 对象
    cabinetCode: Optional[str] = None    # 刀柜编码
    itemDtoList: Optional[List[ItemDto]] = None  # 补货信息列表
    
    class Config:
        orm_mode = True


class RestockData(BaseModel):
    """
    补货响应数据模型（取刀信息）
    """
    # 根据响应说明，这里应该包含"取刀信息"，暂时保持为空，可根据实际API响应添加字段
    pass


class RestockResponse(BaseModel):
    """
    补货响应模型
    """
    code: int
    data: Optional[RestockData]
    dataSuccess: Optional[bool]
    msg: str
    success: bool
    
    class Config:
        orm_mode = True


class ReplenishRecord(BaseModel):
    """
    补货记录模型
    """
    brandName: Optional[str] = None  # 品牌名称
    cabinetCode: Optional[str] = None  # 刀柜编码
    createDept: Optional[int] = None  # 创建部门
    createTime: Optional[str] = None  # 创建时间
    createUser: Optional[int] = None  # 创建人
    cutterCode: Optional[str] = None  # 刀具型号
    cutterType: Optional[str] = None  # 电池类型
    detailsCode: Optional[str] = None  # 操作详情
    id: Optional[int] = None  # 主键id
    isDeleted: Optional[int] = None  # 是否已删除
    lendUserName: Optional[str] = None  # 取出人
    logStatus: Optional[int] = None  # 日志类型 0：操作日志 1：公共暂存 2：补货
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


class StorageRecord(ReplenishRecord):
    """
    公共暂存记录模型（与补货记录模型相同）
    """
    pass


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


class PersonalStorageInfo(BaseModel):
    """
    个人暂存柜信息
    """
    cabinetCode: Optional[str] = None  # 刀柜编码
    id: Optional[str] = None  # 通道号主键
    locPrefix: Optional[str] = None  # 柜子ABCDE面
    locType: Optional[int] = None  # 库位类型[收刀柜: 0 取刀柜: 1]
    name: Optional[str] = None  # 暂存用户名
    stockLoc: Optional[str] = None  # 库位号
    storageCode: Optional[str] = None  # 一次暂存编码
    storageType: Optional[int] = None  # 暂存类型 0: 公共暂存 1: 个人暂存
    storageUser: Optional[int] = None  # 暂存用户
    
    class Config:
        orm_mode = True


class PersonalStorageResponse(BaseModel):
    """
    个人暂存柜响应模型
    """
    code: int
    data: Optional[List[PersonalStorageInfo]]
    msg: str
    success: bool
    
    class Config:
        orm_mode = True
