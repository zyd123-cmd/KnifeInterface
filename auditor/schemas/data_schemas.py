from pydantic import BaseModel
from typing import Optional, List

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