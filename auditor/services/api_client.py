import requests
import logging
import os
from typing import Dict, Any, Optional, List
from urllib.parse import urljoin
#ok
logger = logging.getLogger(__name__)


class OriginalAPIClient:
    """封装对原始API的调用"""

    def __init__(self, base_url: str, api_key: Optional[str] = None, token_file: Optional[str] = None):
        """
        初始化API客户端

        参数：
            base_url: API基础URL
            api_key: API密钥（可选）
            token_file: Token文件路径（可选），默认为项目根目录下token.txt
        """
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "User-Agent": "Secondary-API-Wrapper/1.0"
        })

        # 优先使用api_key参数
        if api_key:
            self.session.headers.update({"Authorization": f"Bearer {api_key}"})
        # 其次尝试从文件读取token
        elif token_file or os.path.exists("token.txt"):
            token = self._load_token_from_file(token_file or "token.txt")
            if token:
                self.session.headers.update({"Authorization": f"Bearer {token}"})
                logger.info("已从文件加载Token")
            else:
                logger.warning("无法加载Token，将使用无认证模式")

    def _load_token_from_file(self, token_file: str) -> Optional[str]:
        """
        从文件读取Token

        参数：
            token_file: Token文件路径
        返回：
            Token字符串，如果读取失败则返回None
        """
        try:
            # 如果是相对路径，转换为绝对路径
            if not os.path.isabs(token_file):
                # 获取项目根目录
                current_dir = os.path.dirname(os.path.abspath(__file__))
                project_root = os.path.dirname(os.path.dirname(current_dir))
                token_file = os.path.join(project_root, token_file)

            # 读取token文件
            with open(token_file, 'r', encoding='utf-8') as f:
                token = f.read().strip()
                if token:
                    logger.info(f"成功从 {token_file} 读取Token")
                    return token
                else:
                    logger.warning(f"Token文件 {token_file} 为空")
                    return None
        except FileNotFoundError:
            logger.warning(f"Token文件 {token_file} 不存在")
            return None
        except Exception as e:
            logger.error(f"读取Token文件失败: {e}")
            return None

    def update_token(self, token: str):
        """
        更新Token

        参数：
            token: 新的Token字符串
        """
        self.session.headers.update({"Authorization": f"Bearer {token}"})
        logger.info("Token已更新")

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

    # ==================== 排行接口方法 ====================
    def get_ranking_data(self, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """通用排行数据获取方法"""
        try:
            # 过滤None值参数
            query_params = {k: v for k, v in params.items() if v is not None}

            logger.info(f"调用外部API: {self.base_url}{endpoint}")
            logger.info(f"请求参数: {query_params}")

            response = self.session.get(
                f"{self.base_url}{endpoint}",
                params=query_params,
                timeout=10
            )
            response.raise_for_status()

            result = response.json()
            logger.info(f"外部API响应: {result}")
            return result

        except requests.exceptions.RequestException as e:
            logger.error(f"获取排行数据失败 {endpoint}: {e}")
            logger.info("由于外部API连接失败，返回模拟数据")
            # 返回模拟数据用于测试
            return self._get_mock_ranking_data(endpoint, params)

    def _get_mock_ranking_data(self, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        生成模拟排行数据用于测试
        当外部API不可用时提供基础数据
        """
        # 基础响应结构
        mock_data = {
            "code": 200,
            "msg": "模拟数据（外部API不可用）",
            "success": True,
            "data": {
                "titleList": [],
                "dataList": []
            }
        }

        # 根据不同的端点提供不同的模拟数据
        if "chartsDeviceSanking" in endpoint:
            # 设备用刀排行模拟数据
            mock_data["data"]["titleList"] = ["设备A", "设备B", "设备C", "设备D", "设备E"]
            mock_data["data"]["dataList"] = [120, 95, 80, 65, 50]
        elif "charts@tuttenbanking" in endpoint:
            # 刀具型号排行模拟数据
            mock_data["data"]["titleList"] = ["型号A", "型号B", "型号C", "型号D", "型号E"]
            mock_data["data"]["dataList"] = [1500, 1200, 900, 750, 600]
        elif "chartslandHunting" in endpoint:
            # 员工领刀排行模拟数据
            mock_data["data"]["titleList"] = ["员工A", "员工B", "员工C", "员工D", "员工E"]
            mock_data["data"]["dataList"] = [45, 38, 32, 28, 25]
        elif "dhatsErrorBorrow" in endpoint:
            # 异常还刀排行模拟数据
            mock_data["data"]["titleList"] = ["异常类型A", "异常类型B", "异常类型C", "异常类型D"]
            mock_data["data"]["dataList"] = [12, 8, 5, 3]
        else:
            # 默认模拟数据
            mock_data["data"]["titleList"] = ["项目1", "项目2", "项目3", "项目4", "项目5"]
            mock_data["data"]["dataList"] = [100, 80, 60, 40, 20]

        return mock_data
    # ==================== 排行接口方法 ====================
    # 这些是新增的排行接口，在合并版本中缺失

    def get_device_ranking(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        设备用刀排行
        接口地址: /qw/knife/web/from/ms/statistics/chartsDeviceSanking
        rankingType: 0.批量 1 查错
        """
        try:
            # 构建查询参数，过滤掉None值
            query_params = {k: v for k, v in params.items() if v is not None}

            logger.info(f"调用设备用刀排行接口: {self.base_url}/qw/knife/web/from/ms/statistics/chartsDeviceSanking")
            logger.info(f"请求参数: {query_params}")

            response = self.session.get(
                f"{self.base_url}/qw/knife/web/from/ms/statistics/chartsDeviceSanking",
                params=query_params,
                timeout=10
            )
            response.raise_for_status()

            result = response.json()
            logger.info(f"设备用刀排行响应: {result}")
            return result

        except requests.exceptions.RequestException as e:
            logger.error(f"获取设备用刀排行失败: {e}")
            # 返回模拟数据用于测试
            return {
                "code": 200,
                "msg": "模拟数据（外部API不可用）",
                "success": True,
                "data": {
                    "titleList": ["设备A", "设备B", "设备C", "设备D", "设备E"],
                    "dataList": [120, 95, 80, 65, 50]
                }
            }

    def get_knife_model_ranking(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        刀具型号排行
        接口地址: /api/mifc/web/from/me/statistics/charts@tuttenbanking
        rankingType: 0:数量 1:金额
        """
        try:
            # 构建查询参数，过滤掉None值
            query_params = {k: v for k, v in params.items() if v is not None}

            logger.info(f"调用刀具型号排行接口: {self.base_url}/api/mifc/web/from/me/statistics/charts@tuttenbanking")
            logger.info(f"请求参数: {query_params}")

            response = self.session.get(
                f"{self.base_url}/api/mifc/web/from/me/statistics/charts@tuttenbanking",
                params=query_params,
                timeout=10
            )
            response.raise_for_status()

            result = response.json()
            logger.info(f"刀具型号排行响应: {result}")
            return result

        except requests.exceptions.RequestException as e:
            logger.error(f"获取刀具型号排行失败: {e}")
            # 返回模拟数据用于测试
            return {
                "code": 200,
                "msg": "模拟数据（外部API不可用）",
                "success": True,
                "data": {
                    "titleList": ["型号A", "型号B", "型号C", "型号D", "型号E"],
                    "dataList": [1500, 1200, 900, 750, 600]
                }
            }

    def get_employee_ranking(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        员工领刀排行
        接口地址: /go/kaife/web/from/mss/statistics/chartslandHunting
        rankingType: 0:批量下拉量 (根据文档推测含义)
        """
        try:
            # 构建查询参数，过滤掉None值
            query_params = {k: v for k, v in params.items() if v is not None}

            logger.info(f"调用员工领刀排行接口: {self.base_url}/go/kaife/web/from/mss/statistics/chartslandHunting")
            logger.info(f"请求参数: {query_params}")

            response = self.session.get(
                f"{self.base_url}/go/kaife/web/from/mss/statistics/chartslandHunting",
                params=query_params,
                timeout=10
            )
            response.raise_for_status()

            result = response.json()
            logger.info(f"员工领刀排行响应: {result}")
            return result

        except requests.exceptions.RequestException as e:
            logger.error(f"获取员工领刀排行失败: {e}")
            # 返回模拟数据用于测试
            return {
                "code": 200,
                "msg": "模拟数据（外部API不可用）",
                "success": True,
                "data": {
                    "titleList": ["员工A", "员工B", "员工C", "员工D", "员工E"],
                    "dataList": [45, 38, 32, 28, 25]
                }
            }

    def get_error_return_ranking(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        异常还刀排行
        接口地址: /qw/knife/web/from/news/statsstics/dhatsErrorBorrow
        rankingType: 0:批量 1:金额
        """
        try:
            # 构建查询参数，过滤掉None值
            query_params = {k: v for k, v in params.items() if v is not None}

            logger.info(f"调用异常还刀排行接口: {self.base_url}/qw/knife/web/from/news/statsstics/dhatsErrorBorrow")
            logger.info(f"请求参数: {query_params}")

            response = self.session.get(
                f"{self.base_url}/qw/knife/web/from/news/statsstics/dhatsErrorBorrow",
                params=query_params,
                timeout=10
            )
            response.raise_for_status()

            result = response.json()
            logger.info(f"异常还刀排行响应: {result}")
            return result

        except requests.exceptions.RequestException as e:
            logger.error(f"获取异常还刀排行失败: {e}")
            # 返回模拟数据用于测试
            return {
                "code": 200,
                "msg": "模拟数据（外部API不可用）",
                "success": True,
                "data": {
                    "titleList": ["异常类型A", "异常类型B", "异常类型C", "异常类型D"],
                    "dataList": [12, 8, 5, 3]
                }
            }

    # ==================== 系统记录相关接口 ====================

    # 合并自 auditor_record 模块的系统记录接口
    # 日期: 2025-11-15
    # 来源: auditor_record/services/api_client.py

    # 补货记录API客户端
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

    def export_replenish_records(self,
                                 endTime: Optional[str] = None,
                                 order: Optional[int] = None,
                                 rankingType: Optional[int] = None,
                                 recordStatus: Optional[int] = None,
                                 startTime: Optional[str] = None) -> bytes:
        """
        导出补货记录

        Args:
            endTime: 结束时间
            order: 顺序 0: 从大到小 1：从小到大
            rankingType: 0: 数量 1: 金额
            recordStatus: 0: 取刀 1: 还刀 2: 收刀 3: 暂存 4: 完成 5：违规还刀
            startTime: 开始时间

        Returns:
            bytes: 导出的Excel文件内容
        """
        url = urljoin(self.base_url, "/qw/knife/web/from/mes/record/exportReplenishRecord")

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

    # 领刀记录API客户端
    def get_lend_records(self,
                         current: int = 1,
                         size: int = 20,
                         keyword: Optional[str] = None,
                         department: Optional[str] = None,
                         startTime: Optional[str] = None,
                         endTime: Optional[str] = None,
                         order: Optional[int] = None,
                         rankingType: Optional[int] = None,
                         recordStatus: Optional[int] = None) -> Dict[str, Any]:
        """
        获取领刀记录列表

        Args:
            current: 当前页码
            size: 每页数量
            keyword: 关键字搜索
            department: 部门筛选
            startTime: 开始时间
            endTime: 结束时间
            order: 顺序 0: 从大到小 1：从小到大
            rankingType: 0: 数量 1: 金额
            recordStatus: 0: 取刀 1: 还刀 2: 收刀 3: 暂存 4: 完成 5：违规还刀

        Returns:
            Dict: API响应结果
        """
        url = urljoin(self.base_url, "/qw/knife/web/from/mes/record/lendList")

        params = {
            "current": current,
            "size": size
        }

        # 添加可选参数
        if keyword:
            params["keyword"] = keyword
        if department:
            params["department"] = department
        if startTime:
            params["startTime"] = startTime
        if endTime:
            params["endTime"] = endTime
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

    # 告警预警API客户端
    def list_alarm_warning(self,
                           locSurplus: Optional[int] = None,
                           alarmLevel: Optional[int] = None,
                           deviceType: Optional[str] = None,
                           cabinetCode: Optional[str] = None,
                           brandName: Optional[str] = None,
                           handleStatus: Optional[int] = None,
                           current: Optional[int] = None,
                           size: Optional[int] = None) -> Dict[str, Any]:
        """
        获取告警预警列表

        Args:
            locSurplus: 货道
            alarmLevel: 预警等级
            deviceType: 设备类型
            cabinetCode: 刀柜编码
            brandName: 品牌名称
            handleStatus: 处理状态
            current: 当前页
            size: 每页数量

        Returns:
            Dict: API响应结果
        """
        url = urljoin(self.base_url, "/qw/knife/web/from/mes/alarm/warning/list")

        params = {}

        # 添加可选参数
        if locSurplus is not None:
            params["locSurplus"] = locSurplus
        if alarmLevel is not None:
            params["alarmLevel"] = alarmLevel
        if deviceType is not None:
            params["deviceType"] = deviceType
        if cabinetCode is not None:
            params["cabinetCode"] = cabinetCode
        if brandName is not None:
            params["brandName"] = brandName
        if handleStatus is not None:
            params["handleStatus"] = handleStatus
        if current is not None:
            params["current"] = current
        if size is not None:
            params["size"] = size

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

    def get_alarm_statistics(self) -> Dict[str, Any]:
        """
        获取告警统计信息

        Returns:
            Dict: API响应结果
        """
        url = urljoin(self.base_url, "/qw/knife/web/from/mes/alarm/warning/statistics")

        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {
                "code": -1,
                "msg": f"请求失败: {str(e)}",
                "data": {
                    "level1Count": 0,
                    "level2Count": 0,
                    "level3Count": 0,
                    "unhandledCount": 0
                },
                "success": False
            }

    def update_alarm_threshold(self,
                               locSurplus: int,
                               alarmThreshold: int) -> Dict[str, Any]:
        """
        更新告警阈值

        Args:
            locSurplus: 货道
            alarmThreshold: 告警阈值

        Returns:
            Dict: API响应结果
        """
        url = urljoin(self.base_url, "/qw/knife/web/from/mes/alarm/warning/threshold")

        data = {
            "locSurplus": locSurplus,
            "alarmThreshold": alarmThreshold
        }

        try:
            response = self.session.post(url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {
                "code": -1,
                "msg": f"请求失败: {str(e)}",
                "data": None,
                "success": False
            }

    def handle_alarm_warning(self,
                             id: int,
                             handleStatus: int,
                             handleRemark: Optional[str] = None) -> Dict[str, Any]:
        """
        处理告警预警

        Args:
            id: 告警ID
            handleStatus: 处理状态 (0: 未处理, 1: 已处理, 2: 已忽略)
            handleRemark: 处理备注

        Returns:
            Dict: API响应结果
        """
        url = urljoin(self.base_url, f"/qw/knife/web/from/mes/alarm/warning/{id}/handle")

        data = {
            "handleStatus": handleStatus
        }

        if handleRemark is not None:
            data["handleRemark"] = handleRemark

        try:
            response = self.session.post(url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {
                "code": -1,
                "msg": f"请求失败: {str(e)}",
                "data": None,
                "success": False
            }

    def batch_handle_alarm_warning(self,
                                   ids: List[int],
                                   handleStatus: int,
                                   handleRemark: Optional[str] = None) -> Dict[str, Any]:
        """
        批量处理告警预警

        Args:
            ids: 告警ID列表
            handleStatus: 处理状态 (0: 未处理, 1: 已处理, 2: 已忽略)
            handleRemark: 处理备注

        Returns:
            Dict: API响应结果
        """
        url = urljoin(self.base_url, "/qw/knife/web/from/mes/alarm/warning/batch/handle")

        data = {
            "ids": ids,
            "handleStatus": handleStatus
        }

        if handleRemark is not None:
            data["handleRemark"] = handleRemark

        try:
            response = self.session.post(url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {
                "code": -1,
                "msg": f"请求失败: {str(e)}",
                "data": None,
                "success": False
            }

    def export_alarm_warning(self,
                             locSurplus: Optional[int] = None,
                             alarmLevel: Optional[int] = None,
                             deviceType: Optional[str] = None,
                             cabinetCode: Optional[str] = None,
                             brandName: Optional[str] = None,
                             handleStatus: Optional[int] = None) -> bytes:
        """
        导出告警预警

        Args:
            locSurplus: 货道
            alarmLevel: 预警等级
            deviceType: 设备类型
            cabinetCode: 刀柜编码
            brandName: 品牌名称
            handleStatus: 处理状态

        Returns:
            bytes: 导出的文件内容
        """
        url = urljoin(self.base_url, "/qw/knife/web/from/mes/alarm/warning/export")

        params = {}

        # 添加可选参数
        if locSurplus is not None:
            params["locSurplus"] = locSurplus
        if alarmLevel is not None:
            params["alarmLevel"] = alarmLevel
        if deviceType is not None:
            params["deviceType"] = deviceType
        if cabinetCode is not None:
            params["cabinetCode"] = cabinetCode
        if brandName is not None:
            params["brandName"] = brandName
        if handleStatus is not None:
            params["handleStatus"] = handleStatus

        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.content
        except requests.RequestException as e:
            raise Exception(f"导出失败: {str(e)}")

    # 公共暂存记录API客户端
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

    def export_storage_records(self,
                               endTime: Optional[str] = None,
                               order: Optional[int] = None,
                               rankingType: Optional[int] = None,
                               recordStatus: Optional[int] = None,
                               startTime: Optional[str] = None) -> bytes:
        """
        导出公共暂存记录

        Args:
            endTime: 结束时间
            order: 顺序 0: 从大到小 1：从小到大
            rankingType: 0: 数量 1: 金额
            recordStatus: 0: 取刀 1: 还刀 2: 收刀 3: 暂存 4: 完成 5：违规还刀
            startTime: 开始时间

        Returns:
            bytes: 导出的文件内容
        """
        url = urljoin(self.base_url, "/qw/knife/web/from/mes/record/exportStorageRecord")

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


# 初始化API客户端 - 使用 master 分支的配置，保留 token_file 支持
original_api_client = OriginalAPIClient(
    base_url="http://39.98.115.114:8983",
    api_key=None,
    token_file="token.txt"
)