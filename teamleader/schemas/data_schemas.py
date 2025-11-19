from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Union, Any, Dict
from datetime import datetime


# ==================== 刀具管理相关模型 ====================

# 刀具查询参数模型
class CutterQueryParams(BaseModel):
    """刀具耗材分页查询参数"""
    brandName: Optional[str] = None  # 品牌名称
    cabinetName: Optional[str] = None  # 刀具柜名称
    createTime: Optional[str] = None  # 创建时间
    createUser: Optional[int] = None  # 创建人
    cutterType: Optional[str] = None  # 刀具类型
    cutterCode: Optional[str] = None  # 刀具型号
    minPrice: Optional[float] = None  # 最低价格
    maxPrice: Optional[float] = None  # 最高价格
    current: Optional[int] = 1  # 当前页
    size: Optional[int] = 10  # 每页数量


# 文件信息模型
class FileInfo(BaseModel):
    """文件信息"""
    name: Optional[str] = None  # 文件名
    newFilename: Optional[str] = None  # 新文件名
    url: Optional[str] = None  # 文件路径


# 刀柜耗材数量模型
class CabinetCutterInfo(BaseModel):
    """刀柜耗材数量"""
    cabinetCode: Optional[str] = None  # 刀柜编码
    cabinetName: Optional[str] = None  # 刀具柜名称
    cutterId: Optional[int] = None  # 耗材主键
    locSurplus: Optional[int] = None  # 库位产品剩余[货道库存]
    stockLoc: Optional[str] = None  # 库位号


# 刀具耗材详细信息模型
class CutterDetail(BaseModel):
    """刀具耗材详细信息"""
    id: Optional[int] = None  # 主键id
    brandCode: Optional[str] = None  # 品牌编码
    brandName: Optional[str] = None  # 品牌名称
    cabinetList: Optional[List[CabinetCutterInfo]] = []  # 刀柜信息
    createDept: Optional[int] = None  # 创建部门
    createTime: Optional[str] = None  # 创建时间
    createUser: Optional[int] = None  # 创建人
    cutterCode: Optional[str] = None  # 刀具型号
    cutterType: Optional[str] = None  # 刀具类型
    imageUrl: Optional[str] = None  # 图片路径
    imageUrlList: Optional[List[FileInfo]] = []  # 耗材图片集合
    inventoryWarning: Optional[int] = None  # 库存警告
    isDeleted: Optional[int] = None  # 是否已删除
    isUniqueCode: Optional[int] = None  # 是否一刀一码(0:否 1:是)
    materialCode: Optional[str] = None  # 物料编码
    materialType: Optional[str] = None  # 物料类型
    numberLife: Optional[int] = None  # 寿命次数
    packQty: Optional[int] = None  # 最小包装数量
    packUnit: Optional[str] = None  # 最小包装单位
    price: Optional[float] = None  # 单价
    specification: Optional[str] = None  # 规格
    status: Optional[int] = None  # 业务状态
    stockNum: Optional[int] = None  # 当前库存数
    tenantId: Optional[str] = None  # 租户ID
    timeLife: Optional[int] = None  # 寿命小时
    updateTime: Optional[str] = None  # 更新时间
    updateUser: Optional[int] = None  # 更新人
    version: Optional[int] = None  # 版本号


# 刀具分页数据模型
class CutterPageData(BaseModel):
    """刀具分页数据"""
    current: Optional[int] = None  # 当前页
    size: Optional[int] = None  # 每页数量
    total: Optional[int] = None  # 总记录数
    pages: Optional[int] = None  # 总页数
    records: Optional[List[CutterDetail]] = []  # 记录列表
    searchCount: Optional[bool] = None  # 是否进行count查询
    hitCount: Optional[bool] = None  # 是否命中count缓存


# 刀具查询响应模型
class CutterQueryResponse(BaseModel):
    """刀具耗材查询响应"""
    code: int
    msg: str
    success: bool
    data: Optional[CutterPageData] = None  # 分页数据


# ==================== 新增刀具耗材相关模型 ====================

# 新增刀具耗材请求模型
class CreateCutterRequest(BaseModel):
    """新增刀具耗材请求"""
    brandName: str  # 品牌名称（必填）
    cabinetName: str  # 刀具柜名称（必填）
    cutterCode: str  # 刀具型号（必填）
    price: float  # 单价（必填）
    createUser: int  # 创建人（必填）
    imageUrlList: Optional[List[FileInfo]] = []  # 刀头图片列表（可选）

    # 其他可选字段
    brandCode: Optional[str] = None  # 品牌编码
    cutterType: Optional[str] = None  # 刀具类型
    specification: Optional[str] = None  # 规格
    materialCode: Optional[str] = None  # 物料编码
    materialType: Optional[str] = None  # 物料类型
    packQty: Optional[int] = None  # 最小包装数量
    packUnit: Optional[str] = None  # 最小包装单位
    inventoryWarning: Optional[int] = None  # 库存警告
    numberLife: Optional[int] = None  # 寿命次数
    timeLife: Optional[int] = None  # 寿命小时
    isUniqueCode: Optional[int] = 0  # 是否一刀一码(0:否 1:是)


# 新增刀具耗材响应模型
class CreateCutterResponse(BaseModel):
    """新增刀具耗材响应"""
    code: int
    msg: str
    success: bool
    data: Optional[CutterDetail] = None  # 新增成功后返回的刀具详情


# 修改刀具耗材请求模型
class UpdateCutterRequest(BaseModel):
    """修改刀具耗材请求"""
    id: int  # 刀具ID（必填，用于标识要修改的记录）
    brandName: Optional[str] = None  # 品牌名称
    cabinetName: Optional[str] = None  # 刀具柜名称
    cutterCode: Optional[str] = None  # 刀具型号
    price: Optional[float] = None  # 单价
    updateUser: Optional[int] = None  # 更新人
    imageUrlList: Optional[List[FileInfo]] = []  # 刀头图片列表

    # 其他可选字段
    brandCode: Optional[str] = None  # 品牌编码
    cutterType: Optional[str] = None  # 刀具类型
    specification: Optional[str] = None  # 规格
    materialCode: Optional[str] = None  # 物料编码
    materialType: Optional[str] = None  # 物料类型
    packQty: Optional[int] = None  # 最小包装数量
    packUnit: Optional[str] = None  # 最小包装单位
    inventoryWarning: Optional[int] = None  # 库存警告
    numberLife: Optional[int] = None  # 寿命次数
    timeLife: Optional[int] = None  # 寿命小时
    isUniqueCode: Optional[int] = None  # 是否一刀一码(0:否 1:是)
    status: Optional[int] = None  # 业务状态


# 修改刀具耗材响应模型
class UpdateCutterResponse(BaseModel):
    """修改刀具耗材响应"""
    code: int
    msg: str
    success: bool
    data: Optional[CutterDetail] = None  # 修改成功后返回的刀具详情


# ==================== 删除刀具耗材相关模型 ====================

# 删除刀具耗材响应模型
class DeleteCutterResponse(BaseModel):
    """删除刀具耗材响应"""
    code: int
    msg: str
    success: bool
    data: Optional[bool] = None  # 删除是否成功


# ==================== 品牌管理相关模型 ====================

# 品牌信息查询参数模型
class BrandQueryParams(BaseModel):
    """品牌信息分页查询参数"""
    brandCode: Optional[str] = None  # 品牌编码
    brandName: Optional[str] = None  # 品牌名称
    corporateName: Optional[str] = None  # 公司名称
    supplierName: Optional[str] = None  # 供应商名称
    status: Optional[int] = None  # 业务状态
    createUser: Optional[int] = None  # 创建人
    startTime: Optional[str] = None  # 创建开始时间
    endTime: Optional[str] = None  # 创建结束时间
    current: Optional[int] = 1  # 当前页
    size: Optional[int] = 10  # 每页数量


# 品牌信息详细模型
class BrandDetail(BaseModel):
    """品牌信息详细信息"""
    id: Optional[int] = None  # 主键id
    brandCode: Optional[str] = None  # 品牌编码
    brandName: Optional[str] = None  # 品牌名称
    corporateName: Optional[str] = None  # 公司名称
    supplierName: Optional[str] = None  # 供应商名称
    supplierUser: Optional[str] = None  # 供应商联系人
    phone: Optional[str] = None  # 联系方式
    status: Optional[int] = None  # 业务状态
    createUser: Optional[int] = None  # 创建人
    createDept: Optional[int] = None  # 创建部门
    createTime: Optional[str] = None  # 创建时间
    updateUser: Optional[int] = None  # 更新人
    updateTime: Optional[str] = None  # 更新时间
    isDeleted: Optional[int] = None  # 是否已删除
    tenantId: Optional[str] = None  # 租户ID


# 品牌分页数据模型
class BrandPageData(BaseModel):
    """品牌分页数据"""
    current: Optional[int] = None  # 当前页
    size: Optional[int] = None  # 每页数量
    total: Optional[int] = None  # 总记录数
    pages: Optional[int] = None  # 总页数
    records: Optional[List[BrandDetail]] = []  # 记录列表
    searchCount: Optional[bool] = None  # 是否进行count查询
    hitCount: Optional[bool] = None  # 是否命中count缓存


# 品牌查询响应模型
class BrandQueryResponse(BaseModel):
    """品牌信息查询响应"""
    code: int
    msg: str
    success: bool
    data: Optional[BrandPageData] = None  # 分页数据


# 新增或修改品牌信息请求模型
class SubmitBrandRequest(BaseModel):
    """新增或修改品牌信息请求"""
    id: Optional[int] = None  # 主键id（修改时必填，新增时不填）
    brandCode: str  # 品牌编码（必填）
    brandName: str  # 品牌名称（必填）
    corporateName: str  # 公司名称（必填）
    supplierName: str  # 供应商名称（必填）
    supplierUser: str  # 供应商联系人（必填）
    phone: str  # 联系方式（必填）
    createDept: Optional[int] = None  # 创建部门
    status: Optional[int] = None  # 业务状态

    # 其他可选字段
    createUser: Optional[int] = None  # 创建人
    updateUser: Optional[int] = None  # 更新人
    tenantId: Optional[str] = None  # 租户ID


# 新增或修改品牌信息响应模型
class SubmitBrandResponse(BaseModel):
    """新增或修改品牌信息响应"""
    code: int
    msg: str
    success: bool
    data: Optional[bool] = None  # 操作是否成功


# 删除品牌信息响应模型
class DeleteBrandResponse(BaseModel):
    """删除品牌信息响应"""
    code: int
    msg: str
    success: bool
    data: Optional[bool] = None  # 删除是否成功


# ==================== 收刀柜管理相关模型 ====================

# 收刀柜查询参数模型
class StockPutQueryParams(BaseModel):
    """收刀柜信息查询参数"""
    cabinetCode: Optional[str] = None  # 刀柜编码
    stockLoc: Optional[str] = None  # 库位号
    locPrefix: Optional[str] = None  # 柜子ABCDE面
    stockStatus: Optional[int] = None  # 库位状态
    isBan: Optional[str] = None  # 绑定状态（是否禁用 0:非禁用 1:禁用）
    borrowStatus: Optional[int] = None  # 还刀状态（0:修磨 1:报废 2:换线 3:错领）
    storageType: Optional[int] = None  # 暂存类型（0:公共暂存 1:个人暂存 2:扩展取刀）


# 收刀柜信息详细模型
class StockPutDetail(BaseModel):
    """收刀柜信息详细数据"""
    id: Optional[str] = None  # 通道号主键
    stockLoc: Optional[str] = None  # 库位号
    locPrefix: Optional[str] = None  # 柜子ABCDE面
    cabinetCode: Optional[str] = None  # 刀柜编码
    locCapacity: Optional[int] = None  # 货道容量（库位容量）
    locSurplus: Optional[int] = None  # 剩余数量（库位产品剩余）
    packQty: Optional[int] = None  # 包装数量（最小包装数量）
    stockStatus: Optional[int] = None  # 库位状态
    isBan: Optional[str] = None  # 绑定状态（是否禁用 0:非禁用 1:禁用）
    cutterCode: Optional[str] = None  # 绑定刀具型号
    warehouseInTime: Optional[str] = None  # 最近更新时间（入库时间）

    # 其他字段
    brandCode: Optional[str] = None  # 品牌编码
    brandName: Optional[str] = None  # 品牌名称
    cutterId: Optional[int] = None  # 耗材主键
    cutterType: Optional[str] = None  # 刀具类型
    materialCode: Optional[str] = None  # 物料编码
    materialType: Optional[str] = None  # 物料类型
    specification: Optional[str] = None  # 规格
    price: Optional[float] = None  # 单价
    locType: Optional[int] = None  # 库位类型（收刀柜:0 取刀柜:1）
    warningNum: Optional[int] = None  # 警报数量
    storageType: Optional[int] = None  # 暂存类型

    # 还刀相关信息
    borrowCode: Optional[str] = None  # 还刀编码
    borrowStatus: Optional[int] = None  # 还刀状态（0:修磨 1:报废 2:换线 3:错领）
    account: Optional[str] = None  # 还刀人账号
    name: Optional[str] = None  # 还刀人名称


# 收刀柜查询响应模型
class StockPutQueryResponse(BaseModel):
    """收刀柜信息查询响应"""
    code: int
    msg: str
    success: bool
    data: Optional[List[StockPutDetail]] = []  # 收刀柜信息列表


# 货道操作响应模型（解绑、禁用/启用）
class StockOperationResponse(BaseModel):
    """货道操作响应（解绑、禁用/启用）"""
    code: int
    msg: str
    success: bool
    data: Optional[bool] = None  # 操作是否成功


# 货道数量统计数据模型
class StockStatisticalData(BaseModel):
    """货道数量统计数据"""
    totalNum: Optional[int] = None  # 货道总数
    disableNum: Optional[int] = None  # 禁用数量
    freeNum: Optional[int] = None  # 空闲数量（未使用）
    workNum: Optional[int] = None  # 占用数量（已使用）
    makeAlarm: Optional[int] = None  # 库存告警值（取刀柜库存告警值）
    totalAmount: Optional[float] = None  # 总库存金额（扩展字段）


# 货道统计查询参数模型
class StockStatisticalQueryParams(BaseModel):
    """货道统计查询参数"""
    cabinetCode: Optional[str] = None  # 刀柜编码
    locPrefix: Optional[str] = None  # 柜子ABCDE面
    locType: Optional[int] = 0  # 库位类型（收刀柜:0 取刀柜:1，默认0）


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
    brandCode: Optional[str] = None  # 品牌编码
    cabinetCode: Optional[str] = None  # 刀柜编码
    cutterCode: Optional[str] = None  # 刀具型号
    cutterType: Optional[str] = None  # 刀具类型
    locPrefix: Optional[str] = None  # 柜子ABCDE面
    stockLoc: Optional[str] = None  # 库位号
    cutterOrBrand: Optional[str] = None  # 耗材型号或品牌
    materialCode: Optional[str] = None  # 物料编码
    specification: Optional[str] = None  # 规格


# 取刀柜信息详细模型
class StockTakeDetail(BaseModel):
    """取刀柜信息详细数据"""
    id: Optional[str] = None  # 通道号主键
    brandName: Optional[str] = None  # 品牌名称
    brandCode: Optional[str] = None  # 品牌编码
    cutterCode: Optional[str] = None  # 刀具型号
    cutterType: Optional[str] = None  # 刀具类型
    stockLoc: Optional[str] = None  # 库位号
    locPrefix: Optional[str] = None  # 柜子ABCDE面
    price: Optional[float] = None  # 单价(元)
    locCapacity: Optional[int] = None  # 货道容量
    locSurplus: Optional[int] = None  # 剩余数量（库位产品剩余）
    stockStatus: Optional[int] = None  # 货道状态（库位状态）
    storageType: Optional[int] = None  # 暂存类型（扩展字段）
    isBan: Optional[str] = None  # 绑定状态（是否禁用 0:非禁用 1:禁用）
    cabinetCode: Optional[str] = None  # 刀柜编码

    # 其他字段
    cabinetName: Optional[str] = None  # 刀具柜名称
    cutterId: Optional[int] = None  # 物料编码主键
    materialCode: Optional[str] = None  # 物料编码
    materialType: Optional[str] = None  # 物料类型
    specification: Optional[str] = None  # 规格
    imageUrl: Optional[str] = None  # 图片路径
    locType: Optional[int] = None  # 库位类型（收刀柜:0 取刀柜:1）
    packQty: Optional[int] = None  # 最小包装数量
    stockNum: Optional[int] = None  # 当前库存数
    warningNum: Optional[int] = None  # 警报数量
    inventoryWarning: Optional[int] = None  # 库存警告
    warehouseInTime: Optional[str] = None  # 入库时间
    awayQty: Optional[int] = None  # 磨损数量
    numberLife: Optional[int] = None  # 寿命次数
    timeLife: Optional[int] = None  # 寿命小时


# 取刀柜查询响应模型
class StockTakeQueryResponse(BaseModel):
    """取刀柜信息查询响应"""
    code: int
    msg: str
    success: bool
    data: Optional[List[StockTakeDetail]] = []  # 取刀柜信息列表


# ==================== 补刀相关模型 ====================

# 货道补货信息模型
class StockPlugInfo(BaseModel):
    """货道补货信息"""
    cabinetCode: Optional[str] = None  # 刀柜编码
    stockLoc: Optional[str] = None  # 库位号
    locCapacity: Optional[int] = None  # 货道容量
    locSurplus: Optional[int] = None  # 补货前数量
    plugNum: Optional[int] = None  # 补货后数量
    massage: Optional[str] = None  # 原因（错误原因或成功信息）


# 预补刀查询结果数据模型
class PreBatchPlugData(BaseModel):
    """预补刀查询结果数据"""
    successStock: Optional[List[StockPlugInfo]] = []  # 补刀成功的货道列表
    errorStock: Optional[List[StockPlugInfo]] = []  # 补刀失败的货道列表


# 预补刀查询响应模型
class PreBatchPlugResponse(BaseModel):
    """预补刀查询响应"""
    code: int
    msg: str
    success: bool
    data: Optional[PreBatchPlugData] = None  # 预补刀查询结果


# 批量补刀响应模型
class OnPreBatchPlugResponse(BaseModel):
    """批量补刀响应"""
    code: int
    msg: str
    success: bool
    data: Optional[bool] = None  # 补刀是否成功


# ==================== 统计接口模型（修正版） ====================

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


class ExportStockRecordQueryParams(BaseModel):
    """出入库记录导出查询参数"""
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


class StockLocationDetailResponse(BaseModel):
    """库位详情响应"""
    code: int
    msg: str
    success: bool
    data: Optional[StockLocationDetail] = None  # 库位详情数据


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


# ==================== 合并自 系统记录 模块的模型 ====================
# 合并日期: 2025-11-15
# 来源: teamleader_record/data_schemas.py

# 补货记录相关模型 (班组长)
class ReplenishRecord(BaseModel):
    """
    补货记录模型 (班组长)
    """
    model_config = ConfigDict(from_attributes=True)

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


class ReplenishRecordData(BaseModel):
    """
    补货记录分页数据 (班组长)
    """
    model_config = ConfigDict(from_attributes=True)

    current: int
    hitCount: bool
    pages: int
    records: List[ReplenishRecord]
    searchCount: bool
    size: int
    total: int


class ReplenishRecordResponse(BaseModel):
    """
    补货记录响应模型 (班组长)
    """
    model_config = ConfigDict(from_attributes=True)

    code: int
    data: ReplenishRecordData
    msg: str
    success: bool


class ReplenishRecordListRequest(BaseModel):
    """
    补货记录列表请求参数 (班组长)
    """
    model_config = ConfigDict(from_attributes=True)

    current: Optional[int] = None  # 当前页
    endTime: Optional[str] = None  # 结束时间
    order: Optional[int] = None  # 顺序 0: 从大到小 1：从小到大
    rankingType: Optional[int] = None  # 0: 数量 1: 金额
    recordStatus: Optional[int] = None  # 0: 取刀 1: 还刀 2: 收刀 3: 暂存 4: 完成 5：违规还刀
    size: Optional[int] = None  # 每页的数量
    startTime: Optional[str] = None  # 开始时间


class ExportReplenishRecordRequest(BaseModel):
    """
    导出补货记录请求参数 (班组长)
    """
    model_config = ConfigDict(from_attributes=True)

    endTime: Optional[str] = None  # 结束时间
    order: Optional[int] = None  # 顺序 0: 从大到小 1：从小到大
    rankingType: Optional[int] = None  # 0: 数量 1: 金额
    recordStatus: Optional[int] = None  # 0: 取刀 1: 还刀 2: 收刀 3: 暂存 4: 完成 5：违规还刀
    startTime: Optional[str] = None  # 开始时间


# 领刀记录相关模型 (班组长)
class LendRecord(BaseModel):
    """
    领刀记录模型 (班组长)
    """
    model_config = ConfigDict(from_attributes=True)

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


class LendRecordData(BaseModel):
    """
    领刀记录分页数据 (班组长)
    """
    model_config = ConfigDict(from_attributes=True)

    current: int
    hitCount: bool
    pages: int
    records: List[LendRecord]
    searchCount: bool
    size: int
    total: int


class LendRecordResponse(BaseModel):
    """
    领刀记录响应模型 (班组长)
    """
    model_config = ConfigDict(from_attributes=True)

    code: int
    data: LendRecordData
    msg: str
    success: bool


class LendRecordListRequest(BaseModel):
    """
    领刀记录列表请求参数 (班组长)
    """
    model_config = ConfigDict(from_attributes=True)

    current: int = 1
    size: int = 20
    keyword: Optional[str] = None  # 关键字搜索
    department: Optional[str] = None  # 部门筛选
    startTime: Optional[str] = None  # 开始时间
    endTime: Optional[str] = None  # 结束时间
    order: Optional[int] = None  # 顺序 0: 从大到小 1：从小到大
    rankingType: Optional[int] = None  # 0: 数量 1: 金额
    recordStatus: Optional[int] = None  # 0: 取刀 1: 还刀 2: 收刀 3: 暂存 4: 完成 5：违规还刀


class ExportLendRecordRequest(BaseModel):
    """
    导出领刀记录请求参数 (班组长)
    """
    model_config = ConfigDict(from_attributes=True)

    endTime: Optional[str] = None  # 结束时间
    order: Optional[int] = None  # 顺序 0: 从大到小 1：从小到大
    rankingType: Optional[int] = None  # 0: 数量 1: 金额
    recordStatus: Optional[int] = None  # 0: 取刀 1: 还刀 2: 收刀 3: 暂存 4: 完成 5：违规还刀
    startTime: Optional[str] = None  # 开始时间


# 公共暂存记录相关模型 (班组长)
class StorageRecord(BaseModel):
    """
    公共暂存记录模型 (班组长)
    """
    model_config = ConfigDict(from_attributes=True)

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


class StorageRecordData(BaseModel):
    """
    公共暂存记录分页数据 (班组长)
    """
    model_config = ConfigDict(from_attributes=True)

    current: int
    hitCount: bool
    pages: int
    records: List[StorageRecord]
    searchCount: bool
    size: int
    total: int


class StorageRecordResponse(BaseModel):
    """
    公共暂存记录响应模型 (班组长)
    """
    model_config = ConfigDict(from_attributes=True)

    code: int
    data: StorageRecordData
    msg: str
    success: bool


class StorageRecordListRequest(BaseModel):
    """
    公共暂存记录列表请求参数 (班组长)
    """
    model_config = ConfigDict(from_attributes=True)

    current: Optional[int] = None  # 当前页
    endTime: Optional[str] = None  # 结束时间
    order: Optional[int] = None  # 顺序 0: 从大到小 1：从小到大
    rankingType: Optional[int] = None  # 0: 数量 1: 金额
    recordStatus: Optional[int] = None  # 0: 取刀 1: 还刀 2: 收刀 3: 暂存 4: 完成 5：违规还刀
    size: Optional[int] = None  # 每页的数量
    startTime: Optional[str] = None  # 开始时间


class ExportStorageRecordRequest(BaseModel):
    """
    导出公共暂存记录请求参数 (班组长)
    """
    model_config = ConfigDict(from_attributes=True)

    endTime: Optional[str] = None  # 结束时间
    order: Optional[int] = None  # 顺序 0: 从大到小 1：从小到大
    rankingType: Optional[int] = None  # 0: 数量 1: 金额
    recordStatus: Optional[int] = None  # 0: 取刀 1: 还刀 2: 收刀 3: 暂存 4: 完成 5：违规还刀
    startTime: Optional[str] = None  # 开始时间


# 告警预警相关模型 (班组长)
class AlarmWarning(BaseModel):
    """
    告警预警模型 (班组长)
    """
    model_config = ConfigDict(from_attributes=True)

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


class AlarmWarningData(BaseModel):
    """
    告警预警分页数据 (班组长)
    """
    model_config = ConfigDict(from_attributes=True)

    current: int
    hitCount: bool
    pages: int
    records: List[AlarmWarning]
    searchCount: bool
    size: int
    total: int


class AlarmWarningResponse(BaseModel):
    """
    告警预警响应模型 (班组长)
    """
    model_config = ConfigDict(from_attributes=True)

    code: int
    data: AlarmWarningData
    msg: str
    success: bool


class AlarmWarningListRequest(BaseModel):
    """
    告警预警列表请求参数 (班组长)
    """
    model_config = ConfigDict(from_attributes=True)

    locSurplus: Optional[int] = None  # 货道
    alarmLevel: Optional[int] = None  # 预警等级
    deviceType: Optional[str] = None  # 设备类型
    cabinetCode: Optional[str] = None  # 刀柜编码
    brandName: Optional[str] = None  # 品牌名称
    handleStatus: Optional[int] = None  # 处理状态
    current: Optional[int] = None  # 当前页
    size: Optional[int] = None  # 每页数量


class ThresholdSetting(BaseModel):
    """
    阈值设置模型 (班组长)
    """
    model_config = ConfigDict(from_attributes=True)

    locSurplus: int  # 货道
    alarmThreshold: int  # 预警阈值


class ThresholdSettingRequest(BaseModel):
    """
    阈值设置请求参数 (班组长)
    """
    model_config = ConfigDict(from_attributes=True)

    locSurplus: int  # 货道
    alarmThreshold: int  # 预警阈值


class AlarmStatistics(BaseModel):
    """
    告警统计模型 (班组长)
    """
    model_config = ConfigDict(from_attributes=True)

    level1Count: int  # 安全库存量预警数量
    level2Count: int  # 采集阈值存储量预警数量
    level3Count: int  # 紧急补货存储量报警数量
    unhandledCount: int  # 未处理预警总数


class AlarmStatisticsResponse(BaseModel):
    """
    告警统计响应模型 (班组长)
    """
    model_config = ConfigDict(from_attributes=True)

    code: int
    data: AlarmStatistics
    msg: str
    success: bool


# ==================== 批量上传刀具耗材相关模型 ====================

# 批量上传请求模型
class BatchCreateCutterRequest(BaseModel):
    """批量新增刀具耗材请求"""
    items: List[CreateCutterRequest]  # 刀具耗材列表
    batchConfig: Optional[Dict[str, Any]] = None  # 批量配置（可选）

    class Config:
        schema_extra = {
            "example": {
                "items": [
                    {
                        "brandName": "品牌A",
                        "cabinetName": "刀具柜A",
                        "cutterCode": "CODE001",
                        "price": 100.0,
                        "createUser": 1
                    },
                    {
                        "brandName": "品牌B",
                        "cabinetName": "刀具柜B",
                        "cutterCode": "CODE002",
                        "price": 150.0,
                        "createUser": 1
                    }
                ],
                "batchConfig": {
                    "stopOnError": False,  # 遇到错误是否停止
                    "maxConcurrent": 5  # 最大并发数
                }
            }
        }


# 批量上传响应项模型
class BatchCutterItemResponse(BaseModel):
    """批量上传单个项响应"""
    status: str  # success/error
    index: int  # 项索引
    cutterCode: str  # 刀具型号
    data: Optional[Dict[str, Any]] = None  # 成功时返回的数据
    error: Optional[str] = None  # 错误信息


# 批量上传响应模型
class BatchCreateCutterResponse(BaseModel):
    """批量新增刀具耗材响应"""
    code: int
    msg: str
    success: bool
    data: Optional[Dict[str, Any]] = None

    # 批量操作详情
    total: int  # 总数量
    success_count: int  # 成功数量
    error_count: int  # 失败数量
    details: List[BatchCutterItemResponse]  # 详细结果