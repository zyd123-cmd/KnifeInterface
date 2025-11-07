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

    def export_stock_record(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        导出刀具耗材数据（出入库记录）
        调用外部接口：/qw/knife/web/from/mes/record/exportStockRecord
        请求方式：GET
        请求数据类型：application/x-www-form-urlencoded
        
        参数：
        - startTime: 开始时间
        - endTime: 结束时间
        - recordStatus: 记录状态（0:取刀 1:还刀 2:收刀 3:暂存 4:完成 5:违规还刀）
        - rankingType: 排名类型（0:数量 1:金额）
        - order: 排序顺序（0:从大到小 1:从小到大）
        """
        try:
            # 构建查询参数，过滤掉None值
            query_params = {k: v for k, v in params.items() if v is not None}
            
            # 调用外部导出接口
            response = self.session.get(
                f"{self.base_url}/qw/knife/web/from/mes/record/exportStockRecord",
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
            logger.error(f"导出出入库记录失败: {e}")
            return {
                "code": 500,
                "msg": f"调用外部导出接口失败: {str(e)}",
                "success": False,
                "data": None
            }

    def get_charts_lend_by_year(self) -> Dict[str, Any]:
        """
        获取全年取刀数量统计
        调用外部接口：/qw/knife/web/from/mes/statistics/chartsLendByYear
        请求方式：GET
        无需参数
        
        返回数据：
        - titleList: 月份标题列表（如：["1月", "2月", ..., "12月"]）
        - dataList: 对应的取刀数量列表
        """
        try:
            # 调用外部接口
            response = self.session.get(
                f"{self.base_url}/qw/knife/web/from/mes/statistics/chartsLendByYear",
                timeout=10
            )
            response.raise_for_status()
            
            # 获取外部接口返回的数据
            external_data = response.json()
            
            # 返回需要的字段
            return {
                "code": external_data.get("code"),
                "msg": external_data.get("msg"),
                "success": external_data.get("success"),
                "data": external_data.get("data")
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"获取全年取刀数量统计失败: {e}")
            return {
                "code": 500,
                "msg": f"调用外部接口失败: {str(e)}",
                "success": False,
                "data": None
            }

    def get_charts_lend_price_by_year(self) -> Dict[str, Any]:
        """
        获取全年取刀金额统计
        调用外部接口：/qw/knife/web/from/mes/statistics/chartsLendPriceByYear
        请求方式：GET
        无需参数
        
        返回数据：
        - titleList: 月份标题列表（如：["1月", "2月", ..., "12月"]）
        - dataList: 对应的取刀金额列表
        """
        try:
            # 调用外部接口
            response = self.session.get(
                f"{self.base_url}/qw/knife/web/from/mes/statistics/chartsLendPriceByYear",
                timeout=10
            )
            response.raise_for_status()
            
            # 获取外部接口返回的数据
            external_data = response.json()
            
            # 返回需要的字段
            return {
                "code": external_data.get("code"),
                "msg": external_data.get("msg"),
                "success": external_data.get("success"),
                "data": external_data.get("data")
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"获取全年取刀金额统计失败: {e}")
            return {
                "code": 500,
                "msg": f"调用外部接口失败: {str(e)}",
                "success": False,
                "data": None
            }

    def get_charts_accumulated(self) -> Dict[str, Any]:
        """
        获取刀具消耗统计
        调用外部接口：/qw/knife/web/from/mes/statistics/chartsAccumulated
        请求方式：GET
        无需参数
        
        返回数据：
        - titleList: 统计项标题列表（可能包含：累计使用次数、使用时长、平均寿命等）
        - dataList: 对应的数据列表
        """
        try:
            # 调用外部接口
            response = self.session.get(
                f"{self.base_url}/qw/knife/web/from/mes/statistics/chartsAccumulated",
                timeout=10
            )
            response.raise_for_status()
            
            # 获取外部接口返回的数据
            external_data = response.json()
            
            # 返回需要的字段
            return {
                "code": external_data.get("code"),
                "msg": external_data.get("msg"),
                "success": external_data.get("success"),
                "data": external_data.get("data")
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"获取刀具消耗统计失败: {e}")
            return {
                "code": 500,
                "msg": f"调用外部接口失败: {str(e)}",
                "success": False,
                "data": None
            }

    def get_total_stock_list(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        获取总库存统计列表（支持搜索和刷新）
        调用外部接口：/qw/knife/web/from/mes/cabinetStock/stockLocTakeInfoById
        请求方式：GET
        
        参数：
        - statisticsType: 统计类型
        - brandName: 品牌名称
        - cabinetCode: 刀柜编码
        - cutterType: 刀具类型
        - stockStatus: 库位状态
        - current: 当前页
        - size: 每页数量
        
        返回数据：
        - 库存列表数据，包含分页信息和详细记录
        
        注意：
        由于外部接口是单个库位查询，这里假设外部系统也有列表接口。
        如果外部接口路径不同，请调整 URL。
        """
        try:
            # 构建查询参数
            query_params = {k: v for k, v in params.items() if v is not None}
            
            # 调用外部接口（这里假设有列表查询接口）
            # 如果外部系统没有列表接口，需要跟外部系统确认正确的接口地址
            response = self.session.get(
                f"{self.base_url}/qw/knife/web/from/mes/cabinetStock/stockLocTakeInfoList",
                params=query_params,
                timeout=10
            )
            response.raise_for_status()
            
            # 获取外部接口返回的数据
            external_data = response.json()
            
            # 如果外部返回的是单个对象，需要封装成列表格式
            data = external_data.get("data")
            if data and not isinstance(data, list):
                # 如果是单个对象，转换为列表
                data = [data]
            
            # 计算库存价值（单价 * 剩余数量）
            if data and isinstance(data, list):
                for item in data:
                    if isinstance(item, dict):
                        price = item.get('price', 0) or 0
                        loc_surplus = item.get('locSurplus', 0) or 0
                        item['stockValue'] = round(price * loc_surplus, 2)
            
            # 返回需要的字段
            return {
                "code": external_data.get("code"),
                "msg": external_data.get("msg"),
                "success": external_data.get("success"),
                "data": data
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"获取总库存统计列表失败: {e}")
            return {
                "code": 500,
                "msg": f"调用外部接口失败: {str(e)}",
                "success": False,
                "data": None
            }

    def get_stock_location_by_id(self, stock_id: int) -> Dict[str, Any]:
        """
        获取取刀柜库位详情（单个）
        调用外部接口：/qw/knife/web/from/mes/cabinetStock/stockLocTakeInfoById
        请求方式：GET
        
        参数：
        - stockId: 刀柜货道主键
        
        返回数据：
        - 单个库位的详细信息
        """
        try:
            # 调用外部接口
            response = self.session.get(
                f"{self.base_url}/qw/knife/web/from/mes/cabinetStock/stockLocTakeInfoById",
                params={"stockId": stock_id},
                timeout=10
            )
            response.raise_for_status()
            
            # 获取外部接口返回的数据
            external_data = response.json()
            
            # 计算库存价值
            data = external_data.get("data")
            if data and isinstance(data, dict):
                price = data.get('price', 0) or 0
                loc_surplus = data.get('locSurplus', 0) or 0
                data['stockValue'] = round(price * loc_surplus, 2)
            
            # 返回需要的字段
            return {
                "code": external_data.get("code"),
                "msg": external_data.get("msg"),
                "success": external_data.get("success"),
                "data": data
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"获取库位详情失败: {e}")
            return {
                "code": 500,
                "msg": f"调用外部接口失败: {str(e)}",
                "success": False,
                "data": None
            }

    def get_waste_knife_recycle_info(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        获取废刀回收统计信息（收刀柜还刀信息）
        调用外部接口：/qw/knife/web/from/mes/lend/getLendByStock
        请求方式：GET
        
        参数：
        - borrowCode: 还刀码（可选）
        - cabinetCode: 刀柜编码（可选）
        - stockLoc: 刀柜库位号（可选）
        
        返回数据：
        - 还刀数据，包含：
          * borrowStatus: 还刀状态
          * cabinetCode: 刀柜编码
          * recordStatus: 记录状态
          * list: 还刀详情列表，包含：
            - 还刀状态：0-修磨，1-报废，2-换线，3-错领
            - 还刀人、借刀人
            - 刀具信息：品牌、型号、类型、规格
            - 时间信息：取刀时间、还刀时间
        
        业务场景：
        - 废刀回收统计：查看收刀柜中的还刀信息
        - 统计报废刀具数量和信息
        - 查询需要修磨的刀具
        - 追踪错领刀具情况
        """
        try:
            # 构建查询参数
            query_params = {k: v for k, v in params.items() if v is not None}
            
            # 调用外部接口
            response = self.session.get(
                f"{self.base_url}/qw/knife/web/from/mes/lend/getLendByStock",
                params=query_params,
                timeout=10
            )
            response.raise_for_status()
            
            # 获取外部接口返回的数据
            external_data = response.json()
            
            # 返回需要的字段
            return {
                "code": external_data.get("code"),
                "msg": external_data.get("msg"),
                "success": external_data.get("success"),
                "data": external_data.get("data")
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"获取废刀回收统计信息失败: {e}")
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