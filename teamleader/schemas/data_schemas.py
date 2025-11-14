from pydantic import BaseModel
from typing import Optional, List


# ==================== 刀具管理相关模型 ====================

# 刀具查询参数模型
class CutterQueryParams(BaseModel):
    """刀具耗材分页查询参数"""
    brandName: Optional[str] = None              # 品牌名称
    cabinetName: Optional[str] = None            # 刀具柜名称
    createTime: Optional[str] = None             # 创建时间
    createUser: Optional[int] = None             # 创建人
    cutterType: Optional[str] = None             # 刀具类型
    cutterCode: Optional[str] = None             # 刀具型号
    minPrice: Optional[float] = None             # 最低价格
    maxPrice: Optional[float] = None             # 最高价格
    current: Optional[int] = 1                   # 当前页
    size: Optional[int] = 10                     # 每页数量


# 文件信息模型
class FileInfo(BaseModel):
    """文件信息"""
    name: Optional[str] = None                   # 文件名
    newFilename: Optional[str] = None            # 新文件名
    url: Optional[str] = None                    # 文件路径


# 刀柜耗材数量模型
class CabinetCutterInfo(BaseModel):
    """刀柜耗材数量"""
    cabinetCode: Optional[str] = None            # 刀柜编码
    cabinetName: Optional[str] = None            # 刀具柜名称
    cutterId: Optional[int] = None               # 耗材主键
    locSurplus: Optional[int] = None             # 库位产品剩余[货道库存]
    stockLoc: Optional[str] = None               # 库位号


# 刀具耗材详细信息模型
class CutterDetail(BaseModel):
    """刀具耗材详细信息"""
    id: Optional[int] = None                     # 主键id
    brandCode: Optional[str] = None              # 品牌编码
    brandName: Optional[str] = None              # 品牌名称
    cabinetList: Optional[List[CabinetCutterInfo]] = []  # 刀柜信息
    createDept: Optional[int] = None             # 创建部门
    createTime: Optional[str] = None             # 创建时间
    createUser: Optional[int] = None             # 创建人
    cutterCode: Optional[str] = None             # 刀具型号
    cutterType: Optional[str] = None             # 刀具类型
    imageUrl: Optional[str] = None               # 图片路径
    imageUrlList: Optional[List[FileInfo]] = []  # 耗材图片集合
    inventoryWarning: Optional[int] = None       # 库存警告
    isDeleted: Optional[int] = None              # 是否已删除
    isUniqueCode: Optional[int] = None           # 是否一刀一码(0:否 1:是)
    materialCode: Optional[str] = None           # 物料编码
    materialType: Optional[str] = None           # 物料类型
    numberLife: Optional[int] = None             # 寿命次数
    packQty: Optional[int] = None                # 最小包装数量
    packUnit: Optional[str] = None               # 最小包装单位
    price: Optional[float] = None                # 单价
    specification: Optional[str] = None          # 规格
    status: Optional[int] = None                 # 业务状态
    stockNum: Optional[int] = None               # 当前库存数
    tenantId: Optional[str] = None               # 租户ID
    timeLife: Optional[int] = None               # 寿命小时
    updateTime: Optional[str] = None             # 更新时间
    updateUser: Optional[int] = None             # 更新人
    version: Optional[int] = None                # 版本号


# 刀具分页数据模型
class CutterPageData(BaseModel):
    """刀具分页数据"""
    current: Optional[int] = None                # 当前页
    size: Optional[int] = None                   # 每页数量
    total: Optional[int] = None                  # 总记录数
    pages: Optional[int] = None                  # 总页数
    records: Optional[List[CutterDetail]] = []   # 记录列表
    searchCount: Optional[bool] = None           # 是否进行count查询
    hitCount: Optional[bool] = None              # 是否命中count缓存


# 刀具查询响应模型
class CutterQueryResponse(BaseModel):
    """刀具耗材查询响应"""
    code: int
    msg: str
    success: bool
    data: Optional[CutterPageData] = None        # 分页数据


# ==================== 新增刀具耗材相关模型 ====================

# 新增刀具耗材请求模型
class CreateCutterRequest(BaseModel):
    """新增刀具耗材请求"""
    brandName: str                               # 品牌名称（必填）
    cabinetName: str                             # 刀具柜名称（必填）
    cutterCode: str                              # 刀具型号（必填）
    price: float                                 # 单价（必填）
    createUser: int                              # 创建人（必填）
    imageUrlList: Optional[List[FileInfo]] = []  # 刀头图片列表（可选）
    
    # 其他可选字段
    brandCode: Optional[str] = None              # 品牌编码
    cutterType: Optional[str] = None             # 刀具类型
    specification: Optional[str] = None          # 规格
    materialCode: Optional[str] = None           # 物料编码
    materialType: Optional[str] = None           # 物料类型
    packQty: Optional[int] = None                # 最小包装数量
    packUnit: Optional[str] = None               # 最小包装单位
    inventoryWarning: Optional[int] = None       # 库存警告
    numberLife: Optional[int] = None             # 寿命次数
    timeLife: Optional[int] = None               # 寿命小时
    isUniqueCode: Optional[int] = 0              # 是否一刀一码(0:否 1:是)


# 新增刀具耗材响应模型
class CreateCutterResponse(BaseModel):
    """新增刀具耗材响应"""
    code: int
    msg: str
    success: bool
    data: Optional[CutterDetail] = None          # 新增成功后返回的刀具详情


# 修改刀具耗材请求模型
class UpdateCutterRequest(BaseModel):
    """修改刀具耗材请求"""
    id: int                                      # 刀具ID（必填，用于标识要修改的记录）
    brandName: Optional[str] = None              # 品牌名称
    cabinetName: Optional[str] = None            # 刀具柜名称
    cutterCode: Optional[str] = None             # 刀具型号
    price: Optional[float] = None                # 单价
    updateUser: Optional[int] = None             # 更新人
    imageUrlList: Optional[List[FileInfo]] = []  # 刀头图片列表
    
    # 其他可选字段
    brandCode: Optional[str] = None              # 品牌编码
    cutterType: Optional[str] = None             # 刀具类型
    specification: Optional[str] = None          # 规格
    materialCode: Optional[str] = None           # 物料编码
    materialType: Optional[str] = None           # 物料类型
    packQty: Optional[int] = None                # 最小包装数量
    packUnit: Optional[str] = None               # 最小包装单位
    inventoryWarning: Optional[int] = None       # 库存警告
    numberLife: Optional[int] = None             # 寿命次数
    timeLife: Optional[int] = None               # 寿命小时
    isUniqueCode: Optional[int] = None           # 是否一刀一码(0:否 1:是)
    status: Optional[int] = None                 # 业务状态


# 修改刀具耗材响应模型
class UpdateCutterResponse(BaseModel):
    """修改刀具耗材响应"""
    code: int
    msg: str
    success: bool
    data: Optional[CutterDetail] = None          # 修改成功后返回的刀具详情


# ==================== 删除刀具耗材相关模型 ====================

# 删除刀具耗材响应模型
class DeleteCutterResponse(BaseModel):
    """删除刀具耗材响应"""
    code: int
    msg: str
    success: bool
    data: Optional[bool] = None                  # 删除是否成功


# ==================== 品牌管理相关模型 ====================

# 品牌信息查询参数模型
class BrandQueryParams(BaseModel):
    """品牌信息分页查询参数"""
    brandCode: Optional[str] = None              # 品牌编码
    brandName: Optional[str] = None              # 品牌名称
    corporateName: Optional[str] = None          # 公司名称
    supplierName: Optional[str] = None           # 供应商名称
    status: Optional[int] = None                 # 业务状态
    createUser: Optional[int] = None             # 创建人
    startTime: Optional[str] = None              # 创建开始时间
    endTime: Optional[str] = None                # 创建结束时间
    current: Optional[int] = 1                   # 当前页
    size: Optional[int] = 10                     # 每页数量


# 品牌信息详细模型
class BrandDetail(BaseModel):
    """品牌信息详细信息"""
    id: Optional[int] = None                     # 主键id
    brandCode: Optional[str] = None              # 品牌编码
    brandName: Optional[str] = None              # 品牌名称
    corporateName: Optional[str] = None          # 公司名称
    supplierName: Optional[str] = None           # 供应商名称
    supplierUser: Optional[str] = None           # 供应商联系人
    phone: Optional[str] = None                  # 联系方式
    status: Optional[int] = None                 # 业务状态
    createUser: Optional[int] = None             # 创建人
    createDept: Optional[int] = None             # 创建部门
    createTime: Optional[str] = None             # 创建时间
    updateUser: Optional[int] = None             # 更新人
    updateTime: Optional[str] = None             # 更新时间
    isDeleted: Optional[int] = None              # 是否已删除
    tenantId: Optional[str] = None               # 租户ID


# 品牌分页数据模型
class BrandPageData(BaseModel):
    """品牌分页数据"""
    current: Optional[int] = None                # 当前页
    size: Optional[int] = None                   # 每页数量
    total: Optional[int] = None                  # 总记录数
    pages: Optional[int] = None                  # 总页数
    records: Optional[List[BrandDetail]] = []    # 记录列表
    searchCount: Optional[bool] = None           # 是否进行count查询
    hitCount: Optional[bool] = None              # 是否命中count缓存


# 品牌查询响应模型
class BrandQueryResponse(BaseModel):
    """品牌信息查询响应"""
    code: int
    msg: str
    success: bool
    data: Optional[BrandPageData] = None         # 分页数据


# 新增或修改品牌信息请求模型
class SubmitBrandRequest(BaseModel):
    """新增或修改品牌信息请求"""
    id: Optional[int] = None                     # 主键id（修改时必填，新增时不填）
    brandCode: str                               # 品牌编码（必填）
    brandName: str                               # 品牌名称（必填）
    corporateName: str                           # 公司名称（必填）
    supplierName: str                            # 供应商名称（必填）
    supplierUser: str                            # 供应商联系人（必填）
    phone: str                                   # 联系方式（必填）
    createDept: Optional[int] = None             # 创建部门
    status: Optional[int] = None                 # 业务状态
    
    # 其他可选字段
    createUser: Optional[int] = None             # 创建人
    updateUser: Optional[int] = None             # 更新人
    tenantId: Optional[str] = None               # 租户ID


# 新增或修改品牌信息响应模型
class SubmitBrandResponse(BaseModel):
    """新增或修改品牌信息响应"""
    code: int
    msg: str
    success: bool
    data: Optional[bool] = None                  # 操作是否成功


# 删除品牌信息响应模型
class DeleteBrandResponse(BaseModel):
    """删除品牌信息响应"""
    code: int
    msg: str
    success: bool
    data: Optional[bool] = None                  # 删除是否成功


# ==================== 收刀柜管理相关模型 ====================

# 收刀柜查询参数模型
class StockPutQueryParams(BaseModel):
    """收刀柜信息查询参数"""
    cabinetCode: Optional[str] = None            # 刀柜编码
    stockLoc: Optional[str] = None               # 库位号
    locPrefix: Optional[str] = None              # 柜子ABCDE面
    stockStatus: Optional[int] = None            # 库位状态
    isBan: Optional[str] = None                  # 绑定状态（是否禁用 0:非禁用 1:禁用）
    borrowStatus: Optional[int] = None           # 还刀状态（0:修磨 1:报废 2:换线 3:错领）
    storageType: Optional[int] = None            # 暂存类型（0:公共暂存 1:个人暂存 2:扩展取刀）


# 收刀柜信息详细模型
class StockPutDetail(BaseModel):
    """收刀柜信息详细数据"""
    id: Optional[str] = None                     # 通道号主键
    stockLoc: Optional[str] = None               # 库位号
    locPrefix: Optional[str] = None              # 柜子ABCDE面
    cabinetCode: Optional[str] = None            # 刀柜编码
    locCapacity: Optional[int] = None            # 货道容量（库位容量）
    locSurplus: Optional[int] = None             # 剩余数量（库位产品剩余）
    packQty: Optional[int] = None                # 包装数量（最小包装数量）
    stockStatus: Optional[int] = None            # 库位状态
    isBan: Optional[str] = None                  # 绑定状态（是否禁用 0:非禁用 1:禁用）
    cutterCode: Optional[str] = None             # 绑定刀具型号
    warehouseInTime: Optional[str] = None        # 最近更新时间（入库时间）
    
    # 其他字段
    brandCode: Optional[str] = None              # 品牌编码
    brandName: Optional[str] = None              # 品牌名称
    cutterId: Optional[int] = None               # 耗材主键
    cutterType: Optional[str] = None             # 刀具类型
    materialCode: Optional[str] = None           # 物料编码
    materialType: Optional[str] = None           # 物料类型
    specification: Optional[str] = None          # 规格
    price: Optional[float] = None                # 单价
    locType: Optional[int] = None                # 库位类型（收刀柜:0 取刀柜:1）
    warningNum: Optional[int] = None             # 警报数量
    storageType: Optional[int] = None            # 暂存类型
    
    # 还刀相关信息
    borrowCode: Optional[str] = None             # 还刀编码
    borrowStatus: Optional[int] = None           # 还刀状态（0:修磨 1:报废 2:换线 3:错领）
    account: Optional[str] = None                # 还刀人账号
    name: Optional[str] = None                   # 还刀人名称


# 收刀柜查询响应模型
class StockPutQueryResponse(BaseModel):
    """收刀柜信息查询响应"""
    code: int
    msg: str
    success: bool
    data: Optional[List[StockPutDetail]] = []    # 收刀柜信息列表


# 货道操作响应模型（解绑、禁用/启用）
class StockOperationResponse(BaseModel):
    """货道操作响应（解绑、禁用/启用）"""
    code: int
    msg: str
    success: bool
    data: Optional[bool] = None                  # 操作是否成功


# 货道数量统计数据模型
class StockStatisticalData(BaseModel):
    """货道数量统计数据"""
    totalNum: Optional[int] = None               # 货道总数
    disableNum: Optional[int] = None             # 禁用数量
    freeNum: Optional[int] = None                # 空闲数量（未使用）
    workNum: Optional[int] = None                # 占用数量（已使用）
    makeAlarm: Optional[int] = None              # 库存告警值（取刀柜库存告警值）
    totalAmount: Optional[float] = None          # 总库存金额（扩展字段）


# 货道统计查询参数模型
class StockStatisticalQueryParams(BaseModel):
    """货道统计查询参数"""
    cabinetCode: Optional[str] = None            # 刀柜编码
    locPrefix: Optional[str] = None              # 柜子ABCDE面
    locType: Optional[int] = 0                   # 库位类型（收刀柜:0 取刀柜:1，默认0）


# 货道统计响应模型
class StockStatisticalResponse(BaseModel):
    """货道统计响应"""
    code: int
    msg: str
    success: bool
    data: Optional[StockStatisticalData] = None  # 货道统计数据


# ==================== 取刀柜管理相关模型 ====================

# 取刀柜查询参数模型
class StockTakeQueryParams(BaseModel):
    """取刀柜信息查询参数"""
    brandCode: Optional[str] = None              # 品牌编码
    cabinetCode: Optional[str] = None            # 刀柜编码
    cutterCode: Optional[str] = None             # 刀具型号
    cutterType: Optional[str] = None             # 刀具类型
    locPrefix: Optional[str] = None              # 柜子ABCDE面
    stockLoc: Optional[str] = None               # 库位号
    cutterOrBrand: Optional[str] = None          # 耗材型号或品牌
    materialCode: Optional[str] = None           # 物料编码
    specification: Optional[str] = None          # 规格


# 取刀柜信息详细模型
class StockTakeDetail(BaseModel):
    """取刀柜信息详细数据"""
    id: Optional[str] = None                     # 通道号主键
    brandName: Optional[str] = None              # 品牌名称
    brandCode: Optional[str] = None              # 品牌编码
    cutterCode: Optional[str] = None             # 刀具型号
    cutterType: Optional[str] = None             # 刀具类型
    stockLoc: Optional[str] = None               # 库位号
    locPrefix: Optional[str] = None              # 柜子ABCDE面
    price: Optional[float] = None                # 单价(元)
    locCapacity: Optional[int] = None            # 货道容量
    locSurplus: Optional[int] = None             # 剩余数量（库位产品剩余）
    stockStatus: Optional[int] = None            # 货道状态（库位状态）
    storageType: Optional[int] = None            # 暂存类型（扩展字段）
    isBan: Optional[str] = None                  # 绑定状态（是否禁用 0:非禁用 1:禁用）
    cabinetCode: Optional[str] = None            # 刀柜编码
    
    # 其他字段
    cabinetName: Optional[str] = None            # 刀具柜名称
    cutterId: Optional[int] = None               # 物料编码主键
    materialCode: Optional[str] = None           # 物料编码
    materialType: Optional[str] = None           # 物料类型
    specification: Optional[str] = None          # 规格
    imageUrl: Optional[str] = None               # 图片路径
    locType: Optional[int] = None                # 库位类型（收刀柜:0 取刀柜:1）
    packQty: Optional[int] = None                # 最小包装数量
    stockNum: Optional[int] = None               # 当前库存数
    warningNum: Optional[int] = None             # 警报数量
    inventoryWarning: Optional[int] = None       # 库存警告
    warehouseInTime: Optional[str] = None        # 入库时间
    awayQty: Optional[int] = None                # 磨损数量
    numberLife: Optional[int] = None             # 寿命次数
    timeLife: Optional[int] = None               # 寿命小时


# 取刀柜查询响应模型
class StockTakeQueryResponse(BaseModel):
    """取刀柜信息查询响应"""
    code: int
    msg: str
    success: bool
    data: Optional[List[StockTakeDetail]] = []   # 取刀柜信息列表


# ==================== 补刀相关模型 ====================

# 货道补货信息模型
class StockPlugInfo(BaseModel):
    """货道补货信息"""
    cabinetCode: Optional[str] = None            # 刀柜编码
    stockLoc: Optional[str] = None               # 库位号
    locCapacity: Optional[int] = None            # 货道容量
    locSurplus: Optional[int] = None             # 补货前数量
    plugNum: Optional[int] = None                # 补货后数量
    massage: Optional[str] = None                # 原因（错误原因或成功信息）


# 预补刀查询结果数据模型
class PreBatchPlugData(BaseModel):
    """预补刀查询结果数据"""
    successStock: Optional[List[StockPlugInfo]] = []   # 补刀成功的货道列表
    errorStock: Optional[List[StockPlugInfo]] = []     # 补刀失败的货道列表


# 预补刀查询响应模型
class PreBatchPlugResponse(BaseModel):
    """预补刀查询响应"""
    code: int
    msg: str
    success: bool
    data: Optional[PreBatchPlugData] = None      # 预补刀查询结果


# 批量补刀响应模型
class OnPreBatchPlugResponse(BaseModel):
    """批量补刀响应"""
    code: int
    msg: str
    success: bool
    data: Optional[bool] = None                  # 补刀是否成功


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
