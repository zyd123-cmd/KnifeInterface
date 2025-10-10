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


class ReturnInfo(BaseModel):
    id: Optional[int] = None
    cabinetCode: Optional[str] = None
    borrowTime: Optional[str] = None
    borrowUser: Optional[str] = None
    brandName: Optional[str] = None
    cutterCode: Optional[str] = None
    cutterType: Optional[str] = None
    lendTime: Optional[str] = None
    lendUser: Optional[str] = None
    recordStatus: Optional[int] = None
    specification: Optional[str] = None
    stockLoc: Optional[str] = None
    borrowStatus: Optional[int] = None


class ReturnInfoListResponse(BaseModel):
    list: List[ReturnInfo]
    total: int


class ReturnInfoCreate(BaseModel):
    cabinetCode: str
    borrowTime: str
    borrowUser: str
    brandName: str
    cutterCode: str
    cutterType: str
    lendTime: str
    lendUser: str
    recordStatus: int
    specification: str
    stockLoc: str
    borrowStatus: int


class ReturnInfoUpdate(BaseModel):
    id: int
    cabinetCode: Optional[str] = None
    borrowTime: Optional[str] = None
    borrowUser: Optional[str] = None
    brandName: Optional[str] = None
    cutterCode: Optional[str] = None
    cutterType: Optional[str] = None
    lendTime: Optional[str] = None
    lendUser: Optional[str] = None
    recordStatus: Optional[int] = None
    specification: Optional[str] = None
    stockLoc: Optional[str] = None
    borrowStatus: Optional[int] = None

# 收刀信息相关模型
class CollectInfo(BaseModel):
    id: Optional[int] = None
    cabinetCode: Optional[str] = None
    location: Optional[str] = None
    cutterCode: Optional[str] = None
    cutterType: Optional[str] = None
    brandName: Optional[str] = None
    specification: Optional[str] = None
    collectTime: Optional[str] = None
    collectUser: Optional[str] = None
    status: Optional[int] = None  # 0-待确认, 1-已确认


class CollectInfoCreate(BaseModel):
    cabinetCode: str
    location: str
    cutterCode: str
    cutterType: str
    brandName: str
    specification: str
    collectTime: str
    collectUser: str


class CollectInfoUpdate(BaseModel):
    id: int
    cabinetCode: Optional[str] = None
    location: Optional[str] = None
    cutterCode: Optional[str] = None
    cutterType: Optional[str] = None
    brandName: Optional[str] = None
    specification: Optional[str] = None
    collectTime: Optional[str] = None
    collectUser: Optional[str] = None
    status: Optional[int] = None


class CollectInfoListResponse(BaseModel):
    list: List[CollectInfo]
    total: int


# 借还排名统计相关模型
class YearlyQuantityStat(BaseModel):
    month: str
    quantity: int


class YearlyAmountStat(BaseModel):
    month: str
    amount: float


class YearlyUsageStat(BaseModel):
    date: str
    usageCount: int


class EmployeeRanking(BaseModel):
    employeeName: str
    count: int


class EquipmentRanking(BaseModel):
    equipmentName: str
    count: int


class CutterModelRanking(BaseModel):
    modelName: str
    count: int


class WorkOrderRanking(BaseModel):
    workOrder: str
    count: int


class AbnormalReturnRanking(BaseModel):
    reason: str
    count: int


# 总库存统计相关模型
class TotalInventoryStat(BaseModel):
    id: Optional[int] = None
    itemName: Optional[str] = None
    itemType: Optional[str] = None
    brand: Optional[str] = None
    currentStock: Optional[int] = None
    minStock: Optional[int] = None
    maxStock: Optional[int] = None
    unit: Optional[str] = None


class InventorySummary(BaseModel):
    totalItems: int
    totalValue: float
    lowStockItems: int
    outOfStockItems: int


class InventoryStatListResponse(BaseModel):
    list: List[TotalInventoryStat]
    total: int


# 未还信息管理相关模型
class UnreturnedInfo(BaseModel):
    id: Optional[int] = None
    borrower: Optional[str] = None
    borrowTime: Optional[str] = None
    cutterCode: Optional[str] = None
    cutterType: Optional[str] = None
    brandName: Optional[str] = None
    specification: Optional[str] = None
    expectedReturnTime: Optional[str] = None
    overdueDays: Optional[int] = None
    status: Optional[int] = None


class UnreturnedInfoCreate(BaseModel):
    borrower: str
    borrowTime: str
    cutterCode: str
    cutterType: str
    brandName: str
    specification: str
    expectedReturnTime: str


class UnreturnedInfoUpdate(BaseModel):
    id: int
    borrower: Optional[str] = None
    borrowTime: Optional[str] = None
    cutterCode: Optional[str] = None
    cutterType: Optional[str] = None
    brandName: Optional[str] = None
    specification: Optional[str] = None
    expectedReturnTime: Optional[str] = None
    overdueDays: Optional[int] = None
    status: Optional[int] = None


class UnreturnedInfoListResponse(BaseModel):
    list: List[UnreturnedInfo]
    total: int


class UnreturnedStatistics(BaseModel):
    totalUnreturned: int
    overdueCount: int
    nearingDueDate: int


# 数据字典相关模型
# 刀具类型相关模型
class CutterType(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    category: Optional[str] = None
    parentId: Optional[int] = None
    description: Optional[str] = None
    status: Optional[int] = None


class CutterTypeCreate(BaseModel):
    name: str
    category: str
    parentId: Optional[int] = None
    description: Optional[str] = None


class CutterTypeUpdate(BaseModel):
    id: int
    name: Optional[str] = None
    category: Optional[str] = None
    parentId: Optional[int] = None
    description: Optional[str] = None
    status: Optional[int] = None


class CutterTypeListResponse(BaseModel):
    list: List[CutterType]
    total: int


# 字典集合相关模型
class DictCollection(BaseModel):
    id: Optional[int] = None
    code: Optional[str] = None
    name: Optional[str] = None
    type: Optional[str] = None
    parentId: Optional[int] = None
    description: Optional[str] = None
    status: Optional[int] = None


class DictCollectionCreate(BaseModel):
    code: str
    name: str
    type: str
    parentId: Optional[int] = None
    description: Optional[str] = None


class DictCollectionUpdate(BaseModel):
    id: int
    code: Optional[str] = None
    name: Optional[str] = None
    type: Optional[str] = None
    parentId: Optional[int] = None
    description: Optional[str] = None
    status: Optional[int] = None


class DictCollectionListResponse(BaseModel):
    list: List[DictCollection]
    total: int


# 个性化设置相关模型
class PersonalizedSettings(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    code: Optional[str] = None
    type: Optional[str] = None
    group: Optional[str] = None
    value: Optional[str] = None
    description: Optional[str] = None
    status: Optional[int] = None


class PersonalizedSettingsCreate(BaseModel):
    name: str
    code: str
    type: str
    group: str
    value: str
    description: Optional[str] = None


class PersonalizedSettingsUpdate(BaseModel):
    id: int
    name: Optional[str] = None
    code: Optional[str] = None
    type: Optional[str] = None
    group: Optional[str] = None
    value: Optional[str] = None
    description: Optional[str] = None
    status: Optional[int] = None


class PersonalizedSettingsListResponse(BaseModel):
    list: List[PersonalizedSettings]
    total: int


# 历史记录相关模型
# 操作日志相关模型
class OperationLog(BaseModel):
    id: Optional[int] = None
    operator: Optional[str] = None
    operationTime: Optional[str] = None
    operationType: Optional[str] = None
    moduleName: Optional[str] = None
    description: Optional[str] = None
    ipAddress: Optional[str] = None
    status: Optional[int] = None


class OperationLogCreate(BaseModel):
    operator: str
    operationTime: str
    operationType: str
    moduleName: str
    description: str
    ipAddress: str


class OperationLogUpdate(BaseModel):
    id: int
    operator: Optional[str] = None
    operationTime: Optional[str] = None
    operationType: Optional[str] = None
    moduleName: Optional[str] = None
    description: Optional[str] = None
    ipAddress: Optional[str] = None
    status: Optional[int] = None


class OperationLogListResponse(BaseModel):
    list: List[OperationLog]
    total: int


class OperationLogStats(BaseModel):
    totalLogs: int
    successCount: int
    failureCount: int


# 公共暂存记录相关模型
class PublicStorageRecord(BaseModel):
    id: Optional[int] = None
    storageCode: Optional[str] = None
    cutterCode: Optional[str] = None
    cutterType: Optional[str] = None
    brandName: Optional[str] = None
    specification: Optional[str] = None
    quantity: Optional[int] = None
    storageTime: Optional[str] = None
    operator: Optional[str] = None
    status: Optional[int] = None


class PublicStorageRecordCreate(BaseModel):
    storageCode: str
    cutterCode: str
    cutterType: str
    brandName: str
    specification: str
    quantity: int
    storageTime: str
    operator: str


class PublicStorageRecordUpdate(BaseModel):
    id: int
    storageCode: Optional[str] = None
    cutterCode: Optional[str] = None
    cutterType: Optional[str] = None
    brandName: Optional[str] = None
    specification: Optional[str] = None
    quantity: Optional[int] = None
    storageTime: Optional[str] = None
    operator: Optional[str] = None
    status: Optional[int] = None


class PublicStorageRecordListResponse(BaseModel):
    list: List[PublicStorageRecord]
    total: int


class PublicStorageRecordStats(BaseModel):
    totalRecords: int
    processedCount: int
    pendingCount: int


# 补货记录相关模型
class RestockRecord(BaseModel):
    id: Optional[int] = None
    restockCode: Optional[str] = None
    cutterCode: Optional[str] = None
    cutterType: Optional[str] = None
    brandName: Optional[str] = None
    specification: Optional[str] = None
    quantity: Optional[int] = None
    restockTime: Optional[str] = None
    operator: Optional[str] = None
    status: Optional[int] = None


class RestockRecordCreate(BaseModel):
    restockCode: str
    cutterCode: str
    cutterType: str
    brandName: str
    specification: str
    quantity: int
    restockTime: str
    operator: str


class RestockRecordUpdate(BaseModel):
    id: int
    restockCode: Optional[str] = None
    cutterCode: Optional[str] = None
    cutterType: Optional[str] = None
    brandName: Optional[str] = None
    specification: Optional[str] = None
    quantity: Optional[int] = None
    restockTime: Optional[str] = None
    operator: Optional[str] = None
    status: Optional[int] = None


class RestockRecordListResponse(BaseModel):
    list: List[RestockRecord]
    total: int


class RestockRecordStats(BaseModel):
    totalRecords: int
    completedCount: int
    pendingCount: int


# 出入库记录相关模型
class StockRecord(BaseModel):
    id: Optional[int] = None
    recordCode: Optional[str] = None
    cutterCode: Optional[str] = None
    cutterType: Optional[str] = None
    brandName: Optional[str] = None
    specification: Optional[str] = None
    quantity: Optional[int] = None
    recordType: Optional[str] = None  # 入库/出库
    recordTime: Optional[str] = None
    operator: Optional[str] = None
    status: Optional[int] = None


class StockRecordCreate(BaseModel):
    recordCode: str
    cutterCode: str
    cutterType: str
    brandName: str
    specification: str
    quantity: int
    recordType: str
    recordTime: str
    operator: str


class StockRecordUpdate(BaseModel):
    id: int
    recordCode: Optional[str] = None
    cutterCode: Optional[str] = None
    cutterType: Optional[str] = None
    brandName: Optional[str] = None
    specification: Optional[str] = None
    quantity: Optional[int] = None
    recordType: Optional[str] = None
    recordTime: Optional[str] = None
    operator: Optional[str] = None
    status: Optional[int] = None


class StockRecordListResponse(BaseModel):
    list: List[StockRecord]
    total: int


class StockRecordStats(BaseModel):
    totalRecords: int
    inboundCount: int
    outboundCount: int
