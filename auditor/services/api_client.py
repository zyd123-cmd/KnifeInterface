import requests
import logging
from typing import Dict, Any, Optional

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

    def get_storage_statistics(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        获取出入库统计数据
        调用外部接口：/qw/knife/web/from/mes/record/stockList
        请求类型：application/x-www-form-urlencoded
        
        参数：
        - current: 当前页
        - size: 每页数量
        - startTime: 开始时间
        - endTime: 结束时间
        - recordStatus: 记录状态（0:取刀 1:还刀 2:收刀 3:暂存 4:完成 5:违规还刀）
        - rankingType: 排名类型（0:数量 1:金额）
        - order: 排序顺序（0:从大到小 1:从小到大）
        """
        try:
            # 构建查询参数，过滤掉None值
            query_params = {k: v for k, v in params.items() if v is not None}
            
            # 调用外部接口，使用 params 传递查询参数
            response = self.session.get(
                f"{self.base_url}/qw/knife/web/from/mes/record/stockList",
                params=query_params,
                timeout=10
            )
            response.raise_for_status()
            
            # 获取外部接口返回的完整数据
            external_data = response.json()
            
            # 提取需要的字段并返回
            return {
                "code": external_data.get("code"),
                "msg": external_data.get("msg"),
                "success": external_data.get("success"),
                "data": external_data.get("data")
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"获取出入库统计数据失败: {e}")
            return {
                "code": 500,
                "msg": f"调用外部接口失败: {str(e)}",
                "success": False,
                "data": None
            }


# 初始化API客户端（这里使用示例API，实际使用时请替换为你的真实API地址）
original_api_client = OriginalAPIClient(
    base_url="https://jsonplaceholder.typicode.com",
    api_key=None  # 如果有API密钥，请在此处填写
)