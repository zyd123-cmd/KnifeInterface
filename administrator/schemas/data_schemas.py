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