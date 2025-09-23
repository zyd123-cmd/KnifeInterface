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


# 还刀信息模型
class ReturnInfo(BaseModel):
    """还刀信息模型"""
    id: Optional[int] = None
    borrowStatus: Optional[int] = None  # 还刀状态 (0-修磨, 1-报废, 2-换线, 3-错领)
    cabinetCode: Optional[str] = None  # 刀柜编码
    borrowTime: Optional[str] = None  # 还刀时间
    borrowUserName: Optional[str] = None  # 还刀人
    brandName: Optional[str] = None  # 品牌名称
    cutterCode: Optional[str] = None  # 刀具型号
    cutterType: Optional[str] = None  # 刀具类型
    lendTime: Optional[str] = None  # 取刀时间
    lendUserName: Optional[str] = None  # 借刀人
    recordStatus: Optional[int] = None  # 记录状态 (0-取刀, 1-还刀, 2-收刀, 3-暂存)
    specification: Optional[str] = None  # 规格
    stockLoc: Optional[str] = None  # 库位号

class ReturnInfoCreate(BaseModel):
    """创建还刀信息请求模型"""
    borrowStatus: int  # 还刀状态 (0-修磨, 1-报废, 2-换线, 3-错领)
    cabinetCode: str  # 刀柜编码
    borrowTime: str  # 还刀时间
    borrowUserName: str  # 还刀人
    brandName: str  # 品牌名称
    cutterCode: str  # 刀具型号
    cutterType: str  # 刀具类型
    lendTime: str  # 取刀时间
    lendUserName: str  # 借刀人
    recordStatus: int  # 记录状态 (0-取刀, 1-还刀, 2-收刀, 3-暂存)
    specification: str  # 规格
    stockLoc: str  # 库位号

class ReturnInfoUpdate(BaseModel):
    """更新还刀信息请求模型"""
    id: int
    borrowStatus: Optional[int] = None  # 还刀状态 (0-修磨, 1-报废, 2-换线, 3-错领)
    cabinetCode: Optional[str] = None  # 刀柜编码
    borrowTime: Optional[str] = None  # 还刀时间
    borrowUserName: Optional[str] = None  # 还刀人
    brandName: Optional[str] = None  # 品牌名称
    cutterCode: Optional[str] = None  # 刀具型号
    cutterType: Optional[str] = None  # 刀具类型
    lendTime: Optional[str] = None  # 取刀时间
    lendUserName: Optional[str] = None  # 借刀人
    recordStatus: Optional[int] = None  # 记录状态 (0-取刀, 1-还刀, 2-收刀, 3-暂存)
    specification: Optional[str] = None  # 规格
    stockLoc: Optional[str] = None  # 库位号


class ReturnInfoListResponse(BaseModel):
    """还刀信息列表响应"""
    list: List[ReturnInfo]
    total: int