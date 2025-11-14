from pydantic import BaseModel
from typing import Optional, List, Union

# 原有接口的响应模型
class OriginalUserResponse(BaseModel):
    id: int
    name: str
    email: str
    created_at: Optional[str] = None

# 二次封装后的响应模型
class EnhancedUserResponse(BaseModel):
    user_id: int
    user_name: str
    email_address: str
    account_status: str
    additional_data: dict
    processed_at: str


# 出入库统计查询参数
class StorageStatisticsQueryParams(BaseModel):
    """出入库统计查询参数"""
    current: Optional[int] = 1                   # 当前页
    size: Optional[int] = 10                     # 每页数量
    startTime: Optional[str] = None              # 开始时间（格式：YYYY-MM-DD HH:mm:ss）
    endTime: Optional[str] = None                # 结束时间（格式：YYYY-MM-DD HH:mm:ss）
    recordStatus: Optional[int] = None           # 记录状态：0-取刀，1-还刀，2-收刀，3-暂存，4-完成，5-违规还刀
    rankingType: Optional[int] = None            # 排名类型：0-按数量排序，1-按金额排序
    order: Optional[int] = None                  # 排序顺序：0-从大到小（降序），1-从小到大（升序）


# 出入库记录模型
class StorageRecord(BaseModel):
    """出入库记录"""
    account: Optional[str] = None                # 用户名
    brandCode: Optional[str] = None              # 品牌编码
    brandName: Optional[str] = None              # 品牌名称
    cabinetCode: Optional[str] = None            # 刀柜编码
    cabinetName: Optional[str] = None            # 刀具柜名称
    createTime: Optional[str] = None             # 创建时间
    cutterCode: Optional[str] = None             # 刀具型号
    cutterId: Optional[int] = None               # 耗材主键
    cutterType: Optional[str] = None             # 刀具类型
    detailsCode: Optional[str] = None            # 操作详情编码
    detailsName: Optional[str] = None            # 操作详情名称
    factoryName: Optional[str] = None            # 工厂名称
    id: Optional[int] = None                     # 主键id
    name: Optional[str] = None                   # 用户名称
    oldPrice: Optional[float] = None             # 历史单价
    operator: Optional[str] = None               # 操作人
    price: Optional[float] = None                # 单价
    quantity: Optional[int] = None               # 数量
    remake: Optional[str] = None                 # 备注
    specification: Optional[str] = None          # 规格
    status: Optional[int] = None                 # 业务状态
    stockLoc: Optional[str] = None               # 库位号
    stockType: Optional[int] = None              # 0:入库 1:出库
    updateTime: Optional[str] = None             # 更新时间
    workshopName: Optional[str] = None           # 车间名称


# 出入库统计响应（分页）
class StorageStatisticsResponse(BaseModel):
    """出入库统计响应"""
    code: int
    msg: str
    success: bool
    data: Optional[dict] = None                  # 包含分页数据


# 出入库统计列表数据
class StorageStatisticsListData(BaseModel):
    """出入库统计列表数据"""
    current: int                                 # 当前页
    size: int                                    # 每页数量
    total: int                                   # 总记录数
    pages: int                                   # 总页数
    records: List[StorageRecord]                 # 记录列表


# 统计图表返回值
class ChartsData(BaseModel):
    """统计图表数据（全年取刀数量，全年取刀金额，刀具消耗数据）"""
    titleList: List[str] = []                                    # 标题列表（如月份或刀具类型）
    dataList: List[Union[str, int, float]] = []                  # 数据列表（支持字符串、整数、浮点数）


# 统计图表响应
class ChartsResponse(BaseModel):
    """统计图表响应（全年取刀数量，全年取刀金额，刀具消耗响应）"""
    code: int
    msg: str
    success: bool
    data: Optional[ChartsData] = None


# 总库存统计查询参数
class TotalStockQueryParams(BaseModel):
    """总库存统计查询参数"""
    statisticsType: Optional[str] = None         # 统计类型
    brandName: Optional[str] = None              # 品牌名称
    cabinetCode: Optional[str] = None            # 刀柜编码
    cutterType: Optional[str] = None             # 刀具类型
    stockStatus: Optional[int] = None            # 库位状态
    current: Optional[int] = 1                   # 当前页
    size: Optional[int] = 10                     # 每页数量


# 库位详情模型
class StockLocationDetail(BaseModel):
    """取刀柜库位详情"""
    id: Optional[int] = None                     # 主键id
    brandCode: Optional[str] = None              # 品牌编码
    brandName: Optional[str] = None              # 品牌名称
    cabinetCode: Optional[str] = None            # 刀柜编码
    cabinetName: Optional[str] = None            # 刀具柜名称
    cutterCode: Optional[str] = None             # 刀具型号
    cutterId: Optional[int] = None               # 物料编码主键
    cutterType: Optional[str] = None             # 刀具类型
    imageUrl: Optional[str] = None               # 图片路径
    locCapacity: Optional[int] = None            # 库位容量
    locPackQty: Optional[int] = None             # 货道包装数量
    locSurplus: Optional[int] = None             # 库位产品剩余[货道库存]
    locType: Optional[int] = None                # 库位类型[收刀柜: 0 取刀柜: 1]
    materialCode: Optional[str] = None           # 物料编码
    materialType: Optional[str] = None           # 物料类型
    packQty: Optional[int] = None                # 最小包装数量
    price: Optional[float] = None                # 单价
    specification: Optional[str] = None          # 规格
    stockLoc: Optional[str] = None               # 库位号
    stockNum: Optional[int] = None               # 当前库存数
    stockStatus: Optional[int] = None            # 库位状态
    warningNum: Optional[int] = None             # 警报数量
    warehouseInTime: Optional[str] = None        # 入库时间
    updateTime: Optional[str] = None             # 更新时间
    
    # 计算字段（前端展示用）
    stockValue: Optional[float] = None           # 库存价值（单价 * 剩余数量）
    cabinetSide: Optional[str] = None            # 柜子面


# 总库存统计响应
class TotalStockResponse(BaseModel):
    """总库存统计响应"""
    code: int
    msg: str
    success: bool
    data: Optional[dict] = None                  # 包含分页数据或列表数据


# 废刀回收统计 - 还刀信息详情
class ReturnKnifeDetail(BaseModel):
    """还刀信息详情"""
    id: Optional[int] = None                     # 取刀主键
    borrowStatus: Optional[int] = None           # 还刀状态：0-修磨，1-报废，2-换线，3-错领
    borrowTime: Optional[str] = None             # 还刀时间
    borrowUserName: Optional[str] = None         # 还刀人
    brandName: Optional[str] = None              # 品牌名称
    cutterCode: Optional[str] = None             # 刀具型号
    cutterType: Optional[str] = None             # 刀具类型
    lendTime: Optional[str] = None               # 取刀时间
    lendUserName: Optional[str] = None           # 借刀人
    recordStatus: Optional[int] = None           # 记录状态：0-取刀，1-还刀，2-收刀，3-暂存
    specification: Optional[str] = None          # 规格
    stockLoc: Optional[str] = None               # 库位号


# 废刀回收统计 - 还刀数据
class ReturnKnifeData(BaseModel):
    """收刀柜还刀数据"""
    borrowStatus: Optional[str] = None           # 还刀状态（字符串形式）
    cabinetCode: Optional[str] = None            # 刀柜编码
    recordStatus: Optional[int] = None           # 记录状态：0-取刀，1-还刀，2-收刀，3-暂存
    list: Optional[List[ReturnKnifeDetail]] = [] # 还刀详情列表


# 废刀回收统计响应
class WasteKnifeRecycleResponse(BaseModel):
    """废刀回收统计响应"""
    code: int
    msg: str
    success: bool
    data: Optional[ReturnKnifeData] = None       # 还刀数据


# ==================== 领刀记录相关模型 ====================

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


# ==================== 补货相关模型 ====================

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


# ==================== 公共暂存相关模型 ====================

class StorageRecord2(ReplenishRecord):
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
    records: List[StorageRecord2]
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


# ==================== 个人暂存和其他接口模型 ====================

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


class MakeAlarmResponse(BaseModel):
    """
    设置取刀柜告警值响应模型
    """
    code: int
    data: Optional[bool]
    msg: str
    success: bool
    
    class Config:
        orm_mode = True


class CabinetAlarmResponse(BaseModel):
    """
    获取取刀柜告警值响应模型
    """
    code: int
    data: Optional[int]
    msg: str
    success: bool
    
    class Config:
        orm_mode = True


class SelectorOption(BaseModel):
    """
    选择器选项模型
    """
    label: Optional[str] = None  # 标题
    value: Optional[str] = None  # 值
    
    class Config:
        orm_mode = True


class CabinetSelectResponse(BaseModel):
    """
    获取刀柜信息下拉响应模型
    """
    code: int
    data: Optional[List[SelectorOption]]
    msg: str
    success: bool
    
    class Config:
        orm_mode = True