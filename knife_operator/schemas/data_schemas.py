from datetime import datetime

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


# 借出单接口参数
class LendRecordQueryParams(BaseModel):
    lendCode: Optional[str] = None      # 借出单号
    lendUser: Optional[str] = None      # 借出人
    brandCode: Optional[str] = None     # 品牌
    cutterCode: Optional[str] = None    # 型号
    status: Optional[str] = None        # 状态
    startTime: Optional[str] = None     # 开始时间
    endTime: Optional[str] = None       # 结束时间
    page: int = 1                       # 页码
    size: int = 10                      # 每页数量

# 借出单接口的响应模型
class LendRecord(BaseModel):
    id: int
    lendCode: str
    lendUser: str
    lendUserName: str
    brandCode: str
    cutterCode: str
    specification: str
    lendTime: datetime
    returnTime: Optional[datetime] = None
    status: str

class LendRecordListResponse(BaseModel):
    list: List[LendRecord]
    total: int
    page: int
    size: int

# 新增借出记录请求模型 (匹配前端表单字段)
class CreateLendRecordRequest(BaseModel):
    borrowCode: str                         # 借出单号（系统自动生成）
    borrowerName: str                       # 借出人姓名（自动填充）
    borrowerCode: str                       # 借出人编号（自动填充）
    brandName: str                          # 刀头品牌（用户选择）
    cutterType: str                         # 刀头型号（用户选择）
    quantity: int                           # 借出数量（用户输入）
    expectedReturnDate: Optional[str] = None  # 预计归还时间（用户选择）
    borrowPurpose: Optional[str] = None     # 借出用途/备注（用户输入）
    borrowDate: Optional[str] = None        # 借出日期
    borrowStatus: str = "borrowed"          # 借出状态


# 批量归还相关模型
class ReturnItem(BaseModel):
    """单个归还项"""
    borrowId: int
    borrowCode: str
    borrowerName: str
    borrowerCode: str
    brandName: str
    cutterType: str
    quantity: int
    borrowDate: str
    expectedReturnDate: str
    actualReturnDate: str
    borrowPurpose: Optional[str]
    assignedLocation: str

class LocationDetail(BaseModel):
    """库位详情"""
    locationCode: str
    totalQuantity: int
    itemCount: int
    items: List[dict]

class BatchReturnRequest(BaseModel):
    """批量归还请求"""
    cabinetCode: str
    locList: List[str]
    returnList: List[ReturnItem]
    operationType: str
    operateTime: str
    operateUser: Optional[str]
    returnRemarks: str
    totalQuantity: int
    allocationStrategy: str
    locationDetails: List[LocationDetail]

class TempStoreBatchReturnRequest(BaseModel):
    """暂存刀头批量归还请求"""
    cabinetCode: str
    locList: List[str]
    returnList: List[ReturnItem]
    operationType: str
    operateTime: str
    operateUser: Optional[str]
    returnRemarks: str
    totalQuantity: int
    allocationStrategy: str
    locationDetails: List[LocationDetail]

class FailedItem(BaseModel):
    """失败项"""
    borrowId: int
    reason: str

class BatchReturnResponse(BaseModel):
    """批量归还响应"""
    code: int
    msg: str
    data: Optional[dict]

class BatchReturnResult(BaseModel):
    """批量归还结果"""
    successCount: int
    failedItems: List[FailedItem]


# 编辑借出记录相关模型
class UpdateBorrowRequest(BaseModel):
    """更新借出记录请求 (编辑按钮接口)"""
    borrowCode: str
    borrowerName: str
    borrowerCode: str
    brandName: str
    cutterType: str
    quantity: int
    expectedReturnDate: str
    borrowPurpose: Optional[str]

# 归还相关模型
class ReturnRequest(BaseModel):
    """归还请求 (归还按钮接口)"""
    borrowId: int
    cabinetCode: str
    locList: List[str]
    actualReturnDate: str
    returnRemarks: str
    operateUser: str

# 暂存相关模型
class TempStoreRequest(BaseModel):
    """暂存请求 (暂存按钮接口)"""
    borrowId: int
    borrowRemarks: str
    operateTime: str
    borrowerCode: str

class TempStoreItem(BaseModel):
    """暂存项"""
    borrowId: int
    cutterType: str
    brandName: str
    quantity: int
    borrowCode: str


# 详情相关模型
class BorrowDetail(BaseModel):
    """借出详情 (详情按钮接口)"""
    id: int
    borrowCode: str
    borrowerName: str
    borrowerCode: str
    brandName: str
    cutterType: str
    quantity: int
    borrowDate: str
    expectedReturnDate: str
    actualReturnDate: Optional[str]
    borrowStatus: str
    borrowPurpose: Optional[str]

class BorrowDetailResponse(BaseModel):
    """借出详情响应"""
    code: int
    msg: str
    data: Optional[BorrowDetail]


# 基础响应模型
class BaseResponse(BaseModel):
    """基础响应模型"""
    code: int
    msg: str
    data: Optional[dict]


# 刀柄相关模型
class HandleLendRecord(BaseModel):
    """刀柄借出记录"""
    id: int
    handleCode: str              # 刀柄编码
    handleName: str              # 刀柄名称
    borrowerName: str            # 借出人姓名
    borrowerCode: str            # 借出人工号
    brand: str                   # 品牌
    model: str                   # 型号
    quantity: int                # 数量
    lendDate: str                # 借出日期
    expectedReturnDate: str      # 预计归还日期
    actualReturnDate: Optional[str]  # 实际归还日期
    status: str                  # 状态
    purpose: Optional[str]       # 用途

class HandleLendRecordListResponse(BaseModel):
    """刀柄借出记录列表响应"""
    list: List[HandleLendRecord]
    total: int
    page: int
    size: int

class CreateHandleLendRecordRequest(BaseModel):
    """创建刀柄借出记录请求"""
    handleCode: str
    handleName: str
    borrowerName: str
    borrowerCode: str
    brand: str
    model: str
    quantity: int
    lendDate: str
    expectedReturnDate: str
    purpose: Optional[str]
    status: str = "borrowed"

class UpdateHandleLendRecordRequest(BaseModel):
    """更新刀柄借出记录请求"""
    handleCode: str
    handleName: str
    borrowerName: str
    borrowerCode: str
    brand: str
    model: str
    quantity: int
    lendDate: str
    expectedReturnDate: str
    purpose: Optional[str]

# 刀柄批量归还相关模型
class HandleReturnItem(BaseModel):
    """刀柄单个归还项"""
    handleId: int
    handleCode: str
    handleName: str
    borrowerName: str
    borrowerCode: str
    brand: str
    model: str
    quantity: int
    lendDate: str
    expectedReturnDate: str
    actualReturnDate: str
    purpose: Optional[str]
    assignedLocation: str

class HandleBatchReturnRequest(BaseModel):
    """刀柄批量归还请求"""
    cabinetCode: str
    locList: List[str]
    returnList: List[HandleReturnItem]
    operationType: str
    operateTime: str
    operateUser: Optional[str]
    returnRemarks: str
    totalQuantity: int
    allocationStrategy: str
    locationDetails: List[LocationDetail]

# 刀柄归还相关模型
class HandleReturnRequest(BaseModel):
    """刀柄归还请求"""
    handleId: int
    cabinetCode: str
    locList: List[str]
    actualReturnDate: str
    returnRemarks: str
    operateUser: str

# 刀柄暂存相关模型
class HandleTempStoreRequest(BaseModel):
    """刀柄暂存请求"""
    handleId: int
    cabinetCode: str
    itemList: List[dict]
    borrowQty: int
    borrowRemarks: str
    operationType: str
    operateTime: str

# 刀柄暂存搜索参数
class HandleTempStoreQueryParams(BaseModel):
    """刀柄暂存查询参数"""
    storageCode: Optional[str] = None       # 暂存单号
    borrowerName: Optional[str] = None      # 暂存人姓名
    storageUser: Optional[str] = None       # 暂存人编号
    brandName: Optional[str] = None         # 刀柄品牌
    handleSpec: Optional[str] = None        # 刀柄规格
    storageType: Optional[str] = None       # 暂存类型（0: 公共暂存, 1: 个人暂存）
    storageTime: Optional[str] = None       # 暂存时间
    pageNum: int = 1                        # 页码
    pageSize: int = 10                      # 每页大小

# 刀柄暂存记录模型
class HandleTempStoreRecord(BaseModel):
    """刀柄暂存记录"""
    id: int
    storageCode: str                        # 暂存单号
    borrowerName: str                       # 暂存人姓名
    storageUser: str                        # 暂存人编号
    brandName: str                          # 刀柄品牌
    handleSpec: str                         # 刀柄规格
    storageType: str                        # 暂存类型（0: 公共暂存, 1: 个人暂存）
    quantity: int                           # 数量
    storageTime: datetime                   # 暂存时间
    status: str                             # 状态
    purpose: Optional[str]                  # 用途/备注

class HandleTempStoreRecordListResponse(BaseModel):
    """刀柄暂存记录列表响应"""
    list: List[HandleTempStoreRecord]
    total: int
    pageNum: int
    pageSize: int

# 新增刀柄暂存记录请求模型 (匹配前端表单字段)
class CreateHandleTempStoreRequest(BaseModel):
    """创建刀柄暂存记录请求"""
    storageCode: str                        # 暂存单号（系统自动生成，BOR+日期+序号）
    borrowerName: str                       # 暂存人姓名（自动填充）
    storageUser: str                        # 暂存人编号（自动填充）
    brandName: str                          # 刀柄品牌（用户选择）
    handleType: str                         # 刀柄类型（用户选择）
    handleSpec: str                         # 刀柄规格（用户选择）
    quantity: int                           # 暂存数量（用户输入）
    expectedReturnDate: Optional[str] = None  # 预计归还时间（用户选择）
    borrowPurpose: Optional[str] = None     # 暂存用途/备注（用户输入）
    borrowDate: Optional[str] = None        # 暂存日期（系统自动）
    borrowStatus: str = "borrowed"          # 暂存状态（系统自动）

# 刀头暂存搜索参数
class TempStoreQueryParams(BaseModel):
    tempStoreCode: Optional[str] = None      # 暂存单号
    storePerson: Optional[str] = None        # 暂存人
    storePersonCode: Optional[str] = None    # 暂存人编号
    storeType: Optional[str] = None          # 暂存类型
    brandName: Optional[str] = None          # 刀头品牌
    cutterType: Optional[str] = None         # 刀头型号
    status: Optional[str] = None             # 暂存状态
    storeTime: Optional[str] = None          # 暂存时间
    page: int = 1                            # 页码
    size: int = 10                           # 每页数量

# 刀头暂存记录模型
class TempStoreRecord(BaseModel):
    id: int
    tempStoreCode: str                       # 暂存单号
    storePerson: str                         # 暂存人
    storePersonCode: str                     # 暂存人编号
    storeType: str                           # 暂存类型
    brandName: str                           # 刀头品牌
    cutterType: str                          # 刀头型号
    specification: str                       # 规格
    storeTime: datetime                      # 暂存时间
    status: str                              # 暂存状态

class TempStoreRecordListResponse(BaseModel):
    list: List[TempStoreRecord]
    total: int
    page: int
    size: int

# 新增刀头暂存记录请求模型 (匹配前端表单字段)
class CreateTempStoreRequest(BaseModel):
    """创建刀头暂存记录请求"""
    storageCode: str                        # 暂存单号（系统自动生成）
    borrowerName: str                       # 暂存人姓名（自动填充）
    storageUser: str                        # 暂存人编号（自动填充）
    brandName: str                          # 刀柄品牌（用户选择）
    handleType: str                         # 刀柄类型（用户选择）
    handleSpec: str                         # 刀柄规格（用户选择）
    quantity: int                           # 暂存数量（用户输入）
    expectedReturnDate: Optional[str] = None  # 预计归还时间（用户选择）
    borrowPurpose: Optional[str] = None     # 暂存用途/备注（用户输入）
    borrowDate: Optional[str] = None        # 暂存日期（系统自动）
    borrowStatus: str = "borrowed"          # 暂存状态（系统自动）

# 刀柄暂存批量归还相关模型
class HandleTempStoreReturnItem(BaseModel):
    """刀柄暂存单个归还项"""
    borrowId: int                           # 暂存记录主键
    storageCode: str                        # 暂存单号
    borrowerName: str                       # 暂存人姓名
    storageUser: str                        # 暂存人编码
    brandName: str                          # 刀柄品牌
    handleSpec: str                         # 刀柄型号
    quantity: int                           # 归还数量
    storageTime: str                        # 暂存日期时间
    expectedReturnDate: str                 # 预期归还日期
    actualReturnDate: str                   # 实际归还日期
    borrowPurpose: Optional[str]            # 暂存目的
    assignedLocation: str                   # 分配的库位号

class HandleTempStoreBatchReturnRequest(BaseModel):
    """刀柄暂存批量归还请求"""
    cabinetCode: str                        # 刀柜编码
    locList: List[str]                      # 收刀库位号集合
    returnList: List[HandleTempStoreReturnItem]  # 批量归还详情列表
    operationType: str = "batch_return"     # 操作类型
    operateTime: str                        # 操作时间
    operateUser: Optional[str] = None       # 操作人
    returnRemarks: str = ""                 # 归还备注
    totalQuantity: int                      # 总归还数量
    allocationStrategy: str = "polling"     # 分配策略（轮询分配）
    locationDetails: List[LocationDetail]   # 库位详情

class HandleTempStoreBatchReturnResponse(BaseModel):
    """刀柄暂存批量归还响应"""
    code: int
    msg: str
    data: Optional[dict]

# 刀柄暂存编辑相关模型
class UpdateHandleTempStoreRequest(BaseModel):
    """更新刀柄暂存记录请求"""
    brandName: str                          # 刀柄品牌
    handleType: str                         # 刀柄类型
    handleSpec: str                         # 刀柄规格
    quantity: int                           # 数量
    expectedReturnDate: Optional[str] = None  # 预计归还时间
    borrowPurpose: Optional[str] = None     # 暂存用途/备注

# 刀柄暂存归还相关模型（单个归还，非批量）
class HandleTempStoreReturnRequest(BaseModel):
    """刀柄暂存归还请求（单个）"""
    borrowId: int                           # 暂存记录主键
    cabinetCode: str                        # 刀柜编码
    locList: List[str]                      # 收刀库位号集合
    actualReturnDate: str                   # 实际归还日期
    returnRemarks: str                      # 归还备注
    operateUser: Optional[str] = None       # 操作人

# 刀柄暂存（从借出状态转为暂存）相关模型
class CreateHandleTempStoreFromBorrowRequest(BaseModel):
    """从借出记录创建刀柄暂存请求"""
    borrowId: int                           # 借出记录主键
    cabinetCode: str                        # 刀柜编码
    itemList: List[dict]                    # 暂存详情列表
    borrowQty: int                          # 暂存数量
    borrowRemarks: str                      # 暂存备注
    operationType: str = "temp_store"       # 操作类型
    operateTime: str                        # 操作时间
    operateUser: Optional[str] = None       # 操作人

# 刀柄暂存详情响应模型
class HandleTempStoreDetailResponse(BaseModel):
    """刀柄暂存详情响应"""
    code: int
    msg: str
    data: Optional[dict]                    # 包含完整的暂存记录详情
