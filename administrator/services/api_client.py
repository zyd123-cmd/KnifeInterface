import requests
import logging
from typing import Dict, Any
from config.config import settings

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

    def get_return_info(self, info_id: int) -> Dict[str, Any]:
        """查询还刀信息详情"""
        url = f"{self.base_url}/api/v1/return_info/{info_id}"
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"查询还刀信息详情失败: {e}")
            raise

    def get_return_info_list(self, params=None):
        """获取还刀列表"""
        url = f"{self.base_url}/api/v1/return_info"
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"获取还刀列表失败: {e}")
            raise

    def create_return_info(self, data):
        """创建还刀信息"""
        url = f"{self.base_url}/api/v1/return_info"
        try:
            response = self.session.post(url, json=data, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"创建还刀信息失败: {e}")
            raise

    def update_return_info(self, data):
        """更新还刀信息"""
        url = f"{self.base_url}/api/v1/return_info"
        try:
            response = self.session.put(url, json=data, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"更新还刀信息失败: {e}")
            raise

    def delete_return_info(self, info_id):
        """删除还刀信息"""
        url = f"{self.base_url}/api/v1/return_info/{info_id}"
        try:
            response = self.session.delete(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"删除还刀信息失败: {e}")
            raise

    def export_return_info(self, params=None):
        """导出还刀信息"""
        url = f"{self.base_url}/api/v1/return_info"
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"导出还刀信息失败: {e}")
            raise

# 初始化API客户端（这里使用示例API，实际使用时请替换为你的真实API地址）
original_api_client = OriginalAPIClient(
    base_url="https://jsonplaceholder.typicode.com",
    api_key=None  # 如果有API密钥，请在此处填写
)
