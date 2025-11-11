from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

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


# 借出记录查询参数
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


# 借出记录模型
class LendRecordItem(BaseModel):
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


# 借出记录列表响应模型
class LendRecordListResponse(BaseModel):
    list: List[LendRecordItem]
    total: int
    page: int
    size: int