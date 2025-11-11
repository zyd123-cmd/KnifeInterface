import requests
import logging
from typing import Dict, Any, Optional, List
from urllib.parse import urljoin
import json

logger = logging.getLogger(__name__)


class OriginalAPIClient:
    """封装对原始API的调用"""

    def __init__(self, base_url: str, api_key: str = None):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "User-Agent": "Secondary-API-Wrapper/1.0"
        })

        if api_key:
            self.session.headers.update({"Authorization": f"Bearer {api_key}"})

    def get_user_data(self, user_id: int) -> Dict[str, Any]:
        """获取用户数据 from 原始接口"""
        try:
            response = self.session.get(f"{self.base_url}/users/{user_id}", timeout=10)
            response.raise_for_status()  # 如果HTTP请求返回不成功状态码则抛出异常
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"获取用户数据失败: {e}")
            raise

    def get_user_posts(self, user_id: int) -> Dict[str, Any]:
        """获取用户帖子列表 from 原始接口"""
        try:
            response = self.session.get(f"{self.base_url}/users/{user_id}/posts", timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"获取用户帖子失败: {e}")
            raise


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
    
    def restock_cabinet(self, 
                       cabinetCode: Optional[str] = None,
                       itemDtoList: Optional[List[Dict[str, Any]]] = None,
                       replenishDto: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        刀柜补货
        
        Args:
            replenishDto: replenishDto 对象
            cabinetCode: 刀柜编码
            itemDtoList: 补货信息列表
            
        Returns:
            Dict: API响应结果
        """
        url = urljoin(self.base_url, "/qw/knife/app/from/mes/cabinet/changeBan")
        
        # 构造请求数据
        data = {}
        if replenishDto is not None:
            data["replenishDto"] = replenishDto
        if cabinetCode is not None:
            data["cabinetCode"] = cabinetCode
        if itemDtoList is not None:
            data["itemDtoList"] = itemDtoList
            
        try:
            response = self.session.post(url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {
                "code": -1,
                "msg": f"补货失败: {str(e)}",
                "data": None,
                "success": False,
                "dataSuccess": False
            }
    
    def get_replenish_records(self,
                              current: Optional[int] = None,
                              endTime: Optional[str] = None,
                              order: Optional[int] = None,
                              rankingType: Optional[int] = None,
                              recordStatus: Optional[int] = None,
                              size: Optional[int] = None,
                              startTime: Optional[str] = None) -> Dict[str, Any]:
        """
        获取补货记录列表
        
        Args:
            current: 当前页
            endTime: 结束时间
            order: 顺序 0: 从大到小 1：从小到大
            rankingType: 0: 数量 1: 金额
            recordStatus: 0: 取刀 1: 还刀 2: 收刀 3: 暂存 4: 完成 5：违规还刀
            size: 每页的数量
            startTime: 开始时间
            
        Returns:
            Dict: API响应结果
        """
        url = urljoin(self.base_url, "/qw/knife/web/from/mes/record/replenishList")
        
        params = {}
        
        # 添加可选参数
        if current is not None:
            params["current"] = current
        if endTime is not None:
            params["endTime"] = endTime
        if order is not None:
            params["order"] = order
        if rankingType is not None:
            params["rankingType"] = rankingType
        if recordStatus is not None:
            params["recordStatus"] = recordStatus
        if size is not None:
            params["size"] = size
        if startTime is not None:
            params["startTime"] = startTime
            
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
    
    def get_storage_records(self,
                           current: Optional[int] = None,
                           endTime: Optional[str] = None,
                           order: Optional[int] = None,
                           rankingType: Optional[int] = None,
                           recordStatus: Optional[int] = None,
                           size: Optional[int] = None,
                           startTime: Optional[str] = None) -> Dict[str, Any]:
        """
        获取公共暂存记录列表
        
        Args:
            current: 当前页
            endTime: 结束时间
            order: 顺序 0: 从大到小 1：从小到大
            rankingType: 0: 数量 1: 金额
            recordStatus: 0: 取刀 1: 还刀 2: 收刀 3: 暂存 4: 完成 5：违规还刀
            size: 每页的数量
            startTime: 开始时间
            
        Returns:
            Dict: API响应结果
        """
        url = urljoin(self.base_url, "/qw/knife/web/from/mes/record/storageList")
        
        params = {}
        
        # 添加可选参数
        if current is not None:
            params["current"] = current
        if endTime is not None:
            params["endTime"] = endTime
        if order is not None:
            params["order"] = order
        if rankingType is not None:
            params["rankingType"] = rankingType
        if recordStatus is not None:
            params["recordStatus"] = recordStatus
        if size is not None:
            params["size"] = size
        if startTime is not None:
            params["startTime"] = startTime
            
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
    
    def get_personal_storage(self, cabinetCode: Optional[str] = None) -> Dict[str, Any]:
        """
        获取个人暂存柜信息
        
        Args:
            cabinetCode: 刀柜编码
            
        Returns:
            Dict: API响应结果
        """
        url = urljoin(self.base_url, "/qw/knife/app/from/mes/cabinet/personalStorage")
        
        params = {}
        if cabinetCode is not None:
            params["cabinetCode"] = cabinetCode
            
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {
                "code": -1,
                "msg": f"请求失败: {str(e)}",
                "data": None,
                "success": False
            }

    def set_make_alarm(self, cabinetCode: Optional[str] = None, alarmValue: Optional[int] = None) -> Dict[str, Any]:
        """
        设置取刀柜告警值
        
        Args:
            cabinetCode: 刀柜编码
            alarmValue: 告警值
            
        Returns:
            Dict: API响应结果
        """
        url = urljoin(self.base_url, "/qw/knife/web/from/mes/cabinet/makeAlarm")
        
        params = {}
        if cabinetCode is not None:
            params["cabinetCode"] = cabinetCode
        if alarmValue is not None:
            params["alarmValue"] = alarmValue
            
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {
                "code": -1,
                "msg": f"请求失败: {str(e)}",
                "data": False,
                "success": False
            }
    
    def get_make_alarm(self, cabinetCode: Optional[str] = None) -> Dict[str, Any]:
        """
        获取取刀柜告警值
        
        Args:
            cabinetCode: 刀柜编码
            
        Returns:
            Dict: API响应结果
        """
        url = urljoin(self.base_url, "/qw/knife/web/from/mes/cabinet/getMakeAlarm")
        
        params = {}
        if cabinetCode is not None:
            params["cabinetCode"] = cabinetCode
            
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {
                "code": -1,
                "msg": f"请求失败: {str(e)}",
                "data": None,
                "success": False
            }


# 初始化API客户端（这里使用示例API，实际使用时请替换为你的真实API地址）
original_api_client = OriginalAPIClient(
    base_url="https://jsonplaceholder.typicode.com",
    api_key=None  # 如果有API密钥，请在此处填写
)

# 初始化领刀记录API客户端
api_client = LendRecordAPIClient()