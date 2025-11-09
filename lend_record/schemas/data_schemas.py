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
    borrowStatus: Optional[int]  # 还刀状态 (0: 修磨 1: 报废 2: 换线 3: 错领)
    finalCollectStatus: Optional[int]  # 最终确认状态 (0: 通过 1: 未通过)
    
    # 备注和结果
    borrowRemarks: Optional[str]  # 还刀备注
    finalCollectRemarks: Optional[str]  # 最终确认结果
    collectStatus: Optional[str]  # 管理员确认结果
    
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
    keyword: Optional[str] = None  # 关键字搜索
    department: Optional[str] = None  # 部门筛选
    start_date: Optional[str] = None  # 开始日期
    end_date: Optional[str] = None  # 结束日期
    order: Optional[int] = None  # 顺序 0: 从大到小 1：从小到大
    rankingType: Optional[int] = None  # 0: 数量 1: 金额
    recordStatus: Optional[int] = None  # 0: 取刀 1: 还刀 2: 收刀 3: 暂存 4: 完成 5：违规还刀
    
    class Config:
        orm_mode = True


class ExportLendRecordRequest(BaseModel):
    """
    导出领刀记录请求参数
    """
    endTime: Optional[str] = None  # 结束时间
    order: Optional[int] = None  # 顺序 0: 从大到小 1：从小到大
    rankingType: Optional[int] = None  # 0: 数量 1: 金额
    recordStatus: Optional[int] = None  # 0: 取刀 1: 还刀 2: 收刀 3: 暂存 4: 完成 5：违规还刀
    startTime: Optional[str] = None  # 开始时间
    
    class Config:
        orm_mode = True