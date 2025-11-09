import requests
from typing import Dict, Any, Optional
from urllib.parse import urljoin
import json


class LendRecordAPIClient:
    """
    领刀记录API客户端
    """
    
    def __init__(self, base_url: str = "http://localhost:8080"):
        """
        初始化API客户端
        
        Args:
            base_url: API基础URL
        """
        self.base_url = base_url
        self.session = requests.Session()
    
    def get_lend_records(self, 
                         page: int = 1,
                         page_size: int = 20,
                         keyword: Optional[str] = None,
                         department: Optional[str] = None,
                         start_date: Optional[str] = None,
                         end_date: Optional[str] = None,
                         order: Optional[int] = None,
                         rankingType: Optional[int] = None,
                         recordStatus: Optional[int] = None) -> Dict[str, Any]:
        """
        获取领刀记录列表
        
        Args:
            page: 页码
            page_size: 每页数量
            keyword: 关键字搜索
            department: 部门筛选
            start_date: 开始时间
            end_date: 结束时间
            order: 顺序 0: 从大到小 1：从小到大
            rankingType: 0: 数量 1: 金额
            recordStatus: 0: 取刀 1: 还刀 2: 收刀 3: 暂存 4: 完成 5：违规还刀
            
        Returns:
            Dict: API响应结果
        """
        url = urljoin(self.base_url, "/qw/knife/web/from/mes/record/lendList")
        
        params = {
            "current": page,
            "size": page_size
        }
        
        # 添加可选参数
        if keyword:
            params["keyword"] = keyword
        if department:
            params["department"] = department
        if start_date:
            params["startTime"] = start_date
        if end_date:
            params["endTime"] = end_date
        if order is not None:
            params["order"] = order
        if rankingType is not None:
            params["rankingType"] = rankingType
        if recordStatus is not None:
            params["recordStatus"] = recordStatus
            
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {
                "code": -1,
                "msg": f"请求失败: {str(e)}",
                "data": {
                    "current": 0,
                    "hitCount": False,
                    "pages": 0,
                    "records": [],
                    "searchCount": False,
                    "size": 0,
                    "total": 0
                },
                "success": False
            }
    
    def export_lend_records(self,
                            endTime: Optional[str] = None,
                            order: Optional[int] = None,
                            rankingType: Optional[int] = None,
                            recordStatus: Optional[int] = None,
                            startTime: Optional[str] = None) -> bytes:
        """
        导出领刀记录
        
        Args:
            endTime: 结束时间
            order: 顺序 0: 从大到小 1：从小到大
            rankingType: 0: 数量 1: 金额
            recordStatus: 0: 取刀 1: 还刀 2: 收刀 3: 暂存 4: 完成 5：违规还刀
            startTime: 开始时间
            
        Returns:
            bytes: 导出的文件内容
        """
        url = urljoin(self.base_url, "/qw/knife/web/from/mes/record/exportLendRecord")
        
        params = {}
        
        # 添加可选参数
        if endTime:
            params["endTime"] = endTime
        if order is not None:
            params["order"] = order
        if rankingType is not None:
            params["rankingType"] = rankingType
        if recordStatus is not None:
            params["recordStatus"] = recordStatus
        if startTime:
            params["startTime"] = startTime
            
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.content
        except requests.RequestException as e:
            raise Exception(f"导出失败: {str(e)}")


# 全局API客户端实例
api_client = LendRecordAPIClient()