import requests
import logging
from typing import Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class OriginalAPIClient:
    """封装对原始API的调用"""

    def __init__(self, base_url: str, api_key: Optional[str] = None):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "User-Agent": "Secondary-API-Wrapper/1.0"
        })
        
        # 添加模拟借出记录数据
        self.mock_lend_records = [
            {
                "id": 1,
                "lendCode": "LC2023001",
                "lendUser": "zhangsan",
                "lendUserName": "张三",
                "brandCode": "BC001",
                "cutterCode": "CC001",
                "specification": "Φ10",
                "lendTime": datetime.now().isoformat(),
                "returnTime": None,
                "status": "借用中"
            },
            {
                "id": 2,
                "lendCode": "LC2023002",
                "lendUser": "lisi",
                "lendUserName": "李四",
                "brandCode": "BC002",
                "cutterCode": "CC002",
                "specification": "Φ12",
                "lendTime": datetime.now().isoformat(),
                "returnTime": datetime.now().isoformat(),
                "status": "已归还"
            },
            {
                "id": 3,
                "lendCode": "LC2023003",
                "lendUser": "wangwu",
                "lendUserName": "王五",
                "brandCode": "BC001",
                "cutterCode": "CC003",
                "specification": "Φ14",
                "lendTime": datetime.now().isoformat(),
                "returnTime": None,
                "status": "借用中"
            }
        ]

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

    def get_lend_records(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        获取借出记录列表
        参数：借出单号、借出人、品牌、型号、状态、时间等查询条件
        """
        # 如果是模拟模式，使用模拟数据
        if self.base_url == "mock":
            # 获取分页参数
            page = params.get("page", 1) if params else 1
            size = params.get("size", 10) if params else 10
            
            # 筛选数据
            filtered_records = self.mock_lend_records.copy()
            
            # 根据查询参数过滤数据
            if params:
                if params.get("lendCode"):
                    filtered_records = [r for r in filtered_records if params["lendCode"] in r["lendCode"]]
                if params.get("lendUser"):
                    filtered_records = [r for r in filtered_records if params["lendUser"] in r["lendUser"]]
                if params.get("brandCode"):
                    filtered_records = [r for r in filtered_records if params["brandCode"] in r["brandCode"]]
                if params.get("cutterCode"):
                    filtered_records = [r for r in filtered_records if params["cutterCode"] in r["cutterCode"]]
                if params.get("status"):
                    filtered_records = [r for r in filtered_records if params["status"] == r["status"]]
            
            # 分页处理
            start_index = (page - 1) * size
            end_index = start_index + size
            paginated_records = filtered_records[start_index:end_index]
            
            return {
                "list": paginated_records,
                "total": len(filtered_records),
                "page": page,
                "size": size
            }
        
        # 真实API调用
        url = f"{self.base_url}/lend-records"
        try:
            response = self.session.get(url, params=params or {}, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"获取借出记录列表失败: {e}")
            raise


# 初始化API客户端（这里使用示例API，实际使用时请替换为你的真实API地址）
original_api_client = OriginalAPIClient(
    base_url="mock",  # 使用模拟数据
    #    base_url="https://jsonplaceholder.typicode.com",
    api_key=None  # 如果有API密钥，请在此处填写
)