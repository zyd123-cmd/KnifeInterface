import requests
import logging
import os
from typing import Dict, Any, Optional, List, Union
from urllib.parse import urljoin
from datetime import datetime

# 导入数据模型
from auditor.schemas.data_schemas import (
    StorageStatisticsResponse,
    ChartsResponse,
    TotalStockResponse,
    WasteKnifeRecycleResponse,
    DeviceRankingResponse,
    KnifeModelRankingResponse,
    EmployeeRankingResponse,
    ErrorReturnRankingResponse,
    # 系统记录相关模型
    ReplenishRecordResponse,
    LendRecordResponse,
    StorageRecordModelResponse,
    AlarmWarningResponse,
    AlarmStatisticsResponse,
    # 请求参数模型
    ReplenishRecordListRequest,
    LendRecordListRequest,
    StorageRecordListRequest,
    AlarmWarningListRequest,
    ThresholdSettingRequest
)

logger = logging.getLogger(__name__)


class ImprovedAPIClient:
    """
    改进的API客户端 - 结合两个版本的优点
    """

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
            "User-Agent": "Improved-API-Client/1.0"
        })

        # 认证处理（保留原始版本的认证逻辑）
        if api_key:
            self.session.headers.update({"Authorization": f"Bearer {api_key}"})
        elif token_file or os.path.exists("token.txt"):
            token = self._load_token_from_file(token_file or "token.txt")
            if token:
                self.session.headers.update({"Authorization": f"Bearer {token}"})
                logger.info("已从文件加载Token")
            else:
                logger.warning("无法加载Token，将使用无认证模式")

    def _load_token_from_file(self, token_file: str) -> Optional[str]:
        """从文件读取Token（保留原始版本实现）"""
        try:
            if not os.path.isabs(token_file):
                current_dir = os.path.dirname(os.path.abspath(__file__))
                project_root = os.path.dirname(os.path.dirname(current_dir))
                token_file = os.path.join(project_root, token_file)

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
        """更新Token"""
        self.session.headers.update({"Authorization": f"Bearer {token}"})
        logger.info("Token已更新")

    def _build_params(self, local_vars: dict) -> Dict[str, Any]:
        """构建查询参数，过滤掉None值"""
        return {k: v for k, v in local_vars.items() if v is not None and k != 'self'}

    # ==================== 系统记录相关接口 ====================

    def get_replenish_records(self,
                              current: Optional[int] = None,
                              endTime: Optional[str] = None,
                              order: Optional[int] = None,
                              rankingType: Optional[int] = None,
                              recordStatus: Optional[int] = None,
                              size: Optional[int] = None,
                              startTime: Optional[str] = None) -> ReplenishRecordResponse:
        """
        获取补货记录列表 - 改进版本
        """
        try:
            url = urljoin(self.base_url, "/qw/knife/web/from/mes/record/replenishList")
            params = self._build_params(locals())

            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()
            return ReplenishRecordResponse(**data)

        except requests.exceptions.RequestException as e:
            logger.error(f"获取补货记录失败: {e}")
            return ReplenishRecordResponse(
                code=500,
                msg=f"获取补货记录失败: {str(e)}",
                success=False,
                data=None
            )

    def get_lend_records(self,
                         current: int = 1,
                         size: int = 20,
                         keyword: Optional[str] = None,
                         department: Optional[str] = None,
                         startTime: Optional[str] = None,
                         endTime: Optional[str] = None,
                         order: Optional[int] = None,
                         rankingType: Optional[int] = None,
                         recordStatus: Optional[int] = None) -> LendRecordResponse:
        """
        获取领刀记录列表 - 改进版本
        """
        try:
            url = urljoin(self.base_url, "/qw/knife/web/from/mes/record/lendList")
            params = self._build_params(locals())

            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()
            return LendRecordResponse(**data)

        except requests.exceptions.RequestException as e:
            logger.error(f"获取领刀记录失败: {e}")
            return LendRecordResponse(
                code=500,
                msg=f"获取领刀记录失败: {str(e)}",
                success=False,
                data=None
            )

    def get_storage_records(self,
                            current: Optional[int] = None,
                            endTime: Optional[str] = None,
                            order: Optional[int] = None,
                            rankingType: Optional[int] = None,
                            recordStatus: Optional[int] = None,
                            size: Optional[int] = None,
                            startTime: Optional[str] = None) -> StorageRecordModelResponse:
        """
        获取公共暂存记录列表 - 改进版本
        """
        try:
            url = urljoin(self.base_url, "/qw/knife/web/from/mes/record/storageList")
            params = self._build_params(locals())

            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()
            return StorageRecordModelResponse(**data)

        except requests.exceptions.RequestException as e:
            logger.error(f"获取公共暂存记录失败: {e}")
            return StorageRecordModelResponse(
                code=500,
                msg=f"获取公共暂存记录失败: {str(e)}",
                success=False,
                data=None
            )

    # ==================== 告警预警相关接口 ====================

    def list_alarm_warning(self,
                           locSurplus: Optional[int] = None,
                           alarmLevel: Optional[int] = None,
                           deviceType: Optional[str] = None,
                           cabinetCode: Optional[str] = None,
                           brandName: Optional[str] = None,
                           handleStatus: Optional[int] = None,
                           current: Optional[int] = None,
                           size: Optional[int] = None) -> AlarmWarningResponse:
        """
        获取告警预警列表 - 改进版本
        """
        try:
            url = urljoin(self.base_url, "/qw/knife/web/from/mes/alarm/warning/list")
            params = self._build_params(locals())

            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()
            return AlarmWarningResponse(**data)

        except requests.exceptions.RequestException as e:
            logger.error(f"获取告警预警列表失败: {e}")
            return AlarmWarningResponse(
                code=500,
                msg=f"获取告警预警列表失败: {str(e)}",
                success=False,
                data=None
            )

    def get_alarm_statistics(self) -> AlarmStatisticsResponse:
        """获取告警统计信息"""
        try:
            url = urljoin(self.base_url, "/qw/knife/web/from/mes/alarm/warning/statistics")

            response = self.session.get(url, timeout=10)
            response.raise_for_status()

            data = response.json()
            return AlarmStatisticsResponse(**data)

        except requests.exceptions.RequestException as e:
            logger.error(f"获取告警统计信息失败: {e}")
            return AlarmStatisticsResponse(
                code=500,
                msg=f"获取告警统计信息失败: {str(e)}",
                success=False,
                data=None
            )

    def update_alarm_threshold(self, request: ThresholdSettingRequest) -> Dict[str, Any]:
        """更新告警阈值"""
        try:
            url = urljoin(self.base_url, "/qw/knife/web/from/mes/alarm/warning/threshold")

            response = self.session.post(url, json=request.model_dump(), timeout=10)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f"更新告警阈值失败: {e}")
            return {
                "code": 500,
                "msg": f"更新告警阈值失败: {str(e)}",
                "data": None,
                "success": False
            }

    def handle_alarm_warning(self,
                             alarm_id: int,
                             handle_status: int,
                             handle_remark: Optional[str] = None) -> Dict[str, Any]:
        """处理告警预警"""
        try:
            url = urljoin(self.base_url, f"/qw/knife/web/from/mes/alarm/warning/{alarm_id}/handle")

            data = {"handleStatus": handle_status}
            if handle_remark:
                data["handleRemark"] = handle_remark

            response = self.session.post(url, json=data, timeout=10)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f"处理告警预警失败: {e}")
            return {
                "code": 500,
                "msg": f"处理告警预警失败: {str(e)}",
                "data": None,
                "success": False
            }

    def batch_handle_alarm_warning(self,
                                   ids: List[int],
                                   handle_status: int,
                                   handle_remark: Optional[str] = None) -> Dict[str, Any]:
        """批量处理告警预警"""
        try:
            url = urljoin(self.base_url, "/qw/knife/web/from/mes/alarm/warning/batch/handle")

            data = {
                "ids": ids,
                "handleStatus": handle_status
            }
            if handle_remark:
                data["handleRemark"] = handle_remark

            response = self.session.post(url, json=data, timeout=10)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f"批量处理告警预警失败: {e}")
            return {
                "code": 500,
                "msg": f"批量处理告警预警失败: {str(e)}",
                "data": None,
                "success": False
            }

    # ==================== 导出功能 ====================

    def export_replenish_records(self,
                                 endTime: Optional[str] = None,
                                 order: Optional[int] = None,
                                 rankingType: Optional[int] = None,
                                 recordStatus: Optional[int] = None,
                                 startTime: Optional[str] = None) -> bytes:
        """导出补货记录"""
        try:
            url = urljoin(self.base_url, "/qw/knife/web/from/mes/record/exportReplenishRecord")
            params = self._build_params(locals())

            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.content

        except requests.exceptions.RequestException as e:
            logger.error(f"导出补货记录失败: {e}")
            raise Exception(f"导出补货记录失败: {str(e)}")

    def export_lend_records(self,
                            endTime: Optional[str] = None,
                            order: Optional[int] = None,
                            rankingType: Optional[int] = None,
                            recordStatus: Optional[int] = None,
                            startTime: Optional[str] = None) -> bytes:
        """导出领刀记录"""
        try:
            url = urljoin(self.base_url, "/qw/knife/web/from/mes/record/exportLendRecord")
            params = self._build_params(locals())

            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.content

        except requests.exceptions.RequestException as e:
            logger.error(f"导出领刀记录失败: {e}")
            raise Exception(f"导出领刀记录失败: {str(e)}")

    def export_storage_records(self,
                               endTime: Optional[str] = None,
                               order: Optional[int] = None,
                               rankingType: Optional[int] = None,
                               recordStatus: Optional[int] = None,
                               startTime: Optional[str] = None) -> bytes:
        """导出公共暂存记录"""
        try:
            url = urljoin(self.base_url, "/qw/knife/web/from/mes/record/exportStorageRecord")
            params = self._build_params(locals())

            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.content

        except requests.exceptions.RequestException as e:
            logger.error(f"导出公共暂存记录失败: {e}")
            raise Exception(f"导出公共暂存记录失败: {str(e)}")

    def export_alarm_warning(self,
                             locSurplus: Optional[int] = None,
                             alarmLevel: Optional[int] = None,
                             deviceType: Optional[str] = None,
                             cabinetCode: Optional[str] = None,
                             brandName: Optional[str] = None,
                             handleStatus: Optional[int] = None) -> bytes:
        """导出告警预警"""
        try:
            url = urljoin(self.base_url, "/qw/knife/web/from/mes/alarm/warning/export")
            params = self._build_params(locals())

            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.content

        except requests.exceptions.RequestException as e:
            logger.error(f"导出告警预警失败: {e}")
            raise Exception(f"导出告警预警失败: {str(e)}")

    # ==================== 刀柜管理功能 ====================

    def stock_bind_cutter(self,
                          cutterId: Optional[int] = None,
                          isBan: Optional[int] = None,
                          locCapacity: Optional[int] = None,
                          locPackQty: Optional[int] = None,
                          locSurplus: Optional[int] = None,
                          stockId: Optional[int] = None,
                          warningNum: Optional[int] = None) -> Dict[str, Any]:
        """
        刀柜货道 绑定/补货 刀具 - 新增功能
        """
        try:
            url = urljoin(self.base_url, "/qw/knife/app/from/mes/cabinet/stockBindCutter")
            params = self._build_params(locals())

            response = self.session.post(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f"刀柜货道绑定刀具失败: {e}")
            return {
                "code": 500,
                "msg": f"刀柜货道绑定刀具失败: {str(e)}",
                "data": None,
                "success": False
            }

    def get_personal_storage(self, cabinetCode: Optional[str] = None) -> Dict[str, Any]:
        """获取个人暂存柜 - 新增功能"""
        try:
            url = urljoin(self.base_url, "/qw/knife/app/from/mes/cabinet/personalStorage")
            params = self._build_params(locals())

            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f"获取个人暂存柜失败: {e}")
            return {
                "code": 500,
                "msg": f"获取个人暂存柜失败: {str(e)}",
                "data": [],
                "success": False
            }

    def make_alarm(self,
                   cabinetCode: Optional[str] = None,
                   makeAlarm: Optional[int] = None) -> Dict[str, Any]:
        """取刀柜库存告警值预设 - 新增功能"""
        try:
            url = urljoin(self.base_url, "/qw/knife/web/from/mes/cabinet/makeAlarm")
            params = self._build_params(locals())

            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f"设置取刀柜库存告警值失败: {e}")
            return {
                "code": 500,
                "msg": f"设置取刀柜库存告警值失败: {str(e)}",
                "data": None,
                "success": False
            }

    def get_make_alarm(self, cabinetCode: Optional[str] = None) -> Dict[str, Any]:
        """获取取刀柜库存告警值预设 - 新增功能"""
        try:
            url = urljoin(self.base_url, "/qw/knife/web/from/mes/cabinet/getMakeAlarm")
            params = self._build_params(locals())

            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f"获取取刀柜库存告警值失败: {e}")
            return {
                "code": 500,
                "msg": f"获取取刀柜库存告警值失败: {str(e)}",
                "data": None,
                "success": False
            }

    # ==================== 出入库统计接口 ====================

    def get_storage_statistics(self, params: Dict[str, Any]) -> StorageStatisticsResponse:
        """获取出入库统计数据"""
        try:
            query_params = {k: v for k, v in params.items() if v is not None}

            response = self.session.get(
                f"{self.base_url}/qw/knife/web/from/mes/record/stockList",
                params=query_params,
                timeout=10
            )
            response.raise_for_status()

            data = response.json()
            return StorageStatisticsResponse(**data)

        except requests.exceptions.RequestException as e:
            logger.error(f"获取出入库统计数据失败: {e}")
            return StorageStatisticsResponse(
                code=500,
                msg=f"获取出入库统计数据失败: {str(e)}",
                success=False,
                data=None
            )

    def export_stock_record(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        导出刀具耗材数据（出入库记录）
        """
        try:
            query_params = {k: v for k, v in params.items() if v is not None}

            response = self.session.get(
                f"{self.base_url}/qw/knife/web/from/mes/record/exportStockRecord",
                params=query_params,
                timeout=30
            )
            response.raise_for_status()

            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f"导出出入库记录失败: {e}")
            return {
                "code": 500,
                "msg": f"调用外部导出接口失败: {str(e)}",
                "success": False,
                "data": None
            }

    # ==================== 统计图表接口 ====================

    def get_charts_lend_by_year(self) -> ChartsResponse:
        """获取全年取刀数量统计"""
        try:
            response = self.session.get(
                f"{self.base_url}/qw/knife/web/from/mes/statistics/chartsLendByYear",
                timeout=10
            )
            response.raise_for_status()

            data = response.json()
            return ChartsResponse(**data)

        except requests.exceptions.RequestException as e:
            logger.error(f"获取全年取刀数量统计失败: {e}")
            return ChartsResponse(
                code=500,
                msg=f"获取全年取刀数量统计失败: {str(e)}",
                success=False,
                data=None
            )

    def get_charts_lend_price_by_year(self) -> ChartsResponse:
        """获取全年取刀金额统计"""
        try:
            response = self.session.get(
                f"{self.base_url}/qw/knife/web/from/mes/statistics/chartsLendPriceByYear",
                timeout=10
            )
            response.raise_for_status()

            data = response.json()
            return ChartsResponse(**data)

        except requests.exceptions.RequestException as e:
            logger.error(f"获取全年取刀金额统计失败: {e}")
            return ChartsResponse(
                code=500,
                msg=f"获取全年取刀金额统计失败: {str(e)}",
                success=False,
                data=None
            )

    def get_charts_accumulated(self) -> ChartsResponse:
        """获取刀具消耗统计"""
        try:
            response = self.session.get(
                f"{self.base_url}/qw/knife/web/from/mes/statistics/chartsAccumulated",
                timeout=10
            )
            response.raise_for_status()

            data = response.json()
            return ChartsResponse(**data)

        except requests.exceptions.RequestException as e:
            logger.error(f"获取刀具消耗统计失败: {e}")
            return ChartsResponse(
                code=500,
                msg=f"获取刀具消耗统计失败: {str(e)}",
                success=False,
                data=None
            )

    # ==================== 总库存统计接口 ====================

    def get_total_stock_list(self, params: Dict[str, Any]) -> TotalStockResponse:
        """获取总库存统计列表"""
        try:
            query_params = {k: v for k, v in params.items() if v is not None}

            response = self.session.get(
                f"{self.base_url}/qw/knife/web/from/mes/cabinetStock/stockLocTakeInfoList",
                params=query_params,
                timeout=10
            )
            response.raise_for_status()

            data = response.json()
            return TotalStockResponse(**data)

        except requests.exceptions.RequestException as e:
            logger.error(f"获取总库存统计列表失败: {e}")
            return TotalStockResponse(
                code=500,
                msg=f"获取总库存统计列表失败: {str(e)}",
                success=False,
                data=None
            )

    def get_stock_location_by_id(self, stock_id: int) -> TotalStockResponse:
        """获取取刀柜库位详情（单个）"""
        try:
            response = self.session.get(
                f"{self.base_url}/qw/knife/web/from/mes/cabinetStock/stockLocTakeInfoById",
                params={"stockId": stock_id},
                timeout=10
            )
            response.raise_for_status()

            data = response.json()
            return TotalStockResponse(**data)

        except requests.exceptions.RequestException as e:
            logger.error(f"获取库位详情失败: {e}")
            return TotalStockResponse(
                code=500,
                msg=f"获取库位详情失败: {str(e)}",
                success=False,
                data=None
            )

    # ==================== 废刀回收统计接口 ====================

    def get_waste_knife_recycle_info(self, params: Dict[str, Any]) -> WasteKnifeRecycleResponse:
        """获取废刀回收统计信息"""
        try:
            query_params = {k: v for k, v in params.items() if v is not None}

            response = self.session.get(
                f"{self.base_url}/qw/knife/web/from/mes/lend/getLendByStock",
                params=query_params,
                timeout=10
            )
            response.raise_for_status()

            data = response.json()
            return WasteKnifeRecycleResponse(**data)

        except requests.exceptions.RequestException as e:
            logger.error(f"获取废刀回收统计信息失败: {e}")
            return WasteKnifeRecycleResponse(
                code=500,
                msg=f"获取废刀回收统计信息失败: {str(e)}",
                success=False,
                data=None
            )

    # ==================== 排行接口 ====================

    def get_device_ranking(self, params: Dict[str, Any]) -> DeviceRankingResponse:
        """设备用刀排行"""
        try:
            query_params = {k: v for k, v in params.items() if v is not None}

            logger.info(f"调用设备用刀排行接口: {self.base_url}/qw/knife/web/from/mes/statistics/chartsDeviceRanking")
            logger.info(f"请求参数: {query_params}")

            response = self.session.get(
                f"{self.base_url}/qw/knife/web/from/mes/statistics/chartsDeviceRanking",
                params=query_params,
                timeout=10
            )
            response.raise_for_status()

            data = response.json()
            return DeviceRankingResponse(**data)

        except requests.exceptions.RequestException as e:
            logger.error(f"获取设备用刀排行失败: {e}")
            return DeviceRankingResponse(
                code=500,
                msg=f"获取设备用刀排行失败: {str(e)}",
                success=False,
                data=None
            )

    def get_knife_model_ranking(self, params: Dict[str, Any]) -> KnifeModelRankingResponse:
        """刀具型号排行"""
        try:
            query_params = {k: v for k, v in params.items() if v is not None}

            response = self.session.get(
                f"{self.base_url}/qw/knife/web/from/mes/statistics/chartsCutterRanking",
                params=query_params,
                timeout=10
            )
            response.raise_for_status()

            data = response.json()
            return KnifeModelRankingResponse(**data)

        except requests.exceptions.RequestException as e:
            logger.error(f"获取刀具型号排行失败: {e}")
            return KnifeModelRankingResponse(
                code=500,
                msg=f"获取刀具型号排行失败: {str(e)}",
                success=False,
                data=None
            )

    def get_employee_ranking(self, params: Dict[str, Any]) -> EmployeeRankingResponse:
        """员工领刀排行"""
        try:
            query_params = {k: v for k, v in params.items() if v is not None}

            response = self.session.get(
                f"{self.base_url}/qw/knife/web/from/mes/statistics/chartsLendRanking",
                params=query_params,
                timeout=10
            )
            response.raise_for_status()

            data = response.json()
            return EmployeeRankingResponse(**data)

        except requests.exceptions.RequestException as e:
            logger.error(f"获取员工领刀排行失败: {e}")
            return EmployeeRankingResponse(
                code=500,
                msg=f"获取员工领刀排行失败: {str(e)}",
                success=False,
                data=None
            )

    def get_error_return_ranking(self, params: Dict[str, Any]) -> ErrorReturnRankingResponse:
        """异常还刀排行"""
        try:
            query_params = {k: v for k, v in params.items() if v is not None}

            response = self.session.get(
                f"{self.base_url}/qw/knife/web/from/mes/statistics/chartsErrorBorrow",
                params=query_params,
                timeout=10
            )
            response.raise_for_status()

            data = response.json()
            return ErrorReturnRankingResponse(**data)

        except requests.exceptions.RequestException as e:
            logger.error(f"获取异常还刀排行失败: {e}")
            return ErrorReturnRankingResponse(
                code=500,
                msg=f"获取异常还刀排行失败: {str(e)}",
                success=False,
                data=None
            )


# 初始化改进的API客户端
improved_api_client = ImprovedAPIClient(
    base_url="http://39.98.115.114:8983",
    api_key=None,
    token_file="token.txt"
)