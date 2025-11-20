import requests
from typing import Dict, Any, Optional, List
from urllib.parse import urljoin
import json
from teamleader_record.data_schemas import (
    ReplenishRecordResponse, 
    LendRecordResponse, 
    StorageRecordResponse,
    AlarmWarningResponse,
    ReplenishRecordData,
    LendRecordData,
    StorageRecordData,
    AlarmWarningData,
    ReplenishRecord,
    LendRecord,
    StorageRecord,
    AlarmWarning
)


class APIClient:
    """
    班组长刀具管理系统API客户端
    """

    def __init__(self, base_url: str = "http://localhost:8080"):
        """
        初始化API客户端

        Args:
            base_url: API基础URL
        """
        self.base_url = base_url
        self.session = requests.Session()

    # 补货记录接口整合
    def get_replenish_records(self,
                              current: Optional[int] = None,
                              endTime: Optional[str] = None,
                              order: Optional[int] = None,
                              rankingType: Optional[int] = None,
                              recordStatus: Optional[int] = None,
                              size: Optional[int] = None,
                              startTime: Optional[str] = None) -> ReplenishRecordResponse:
        """
        分页查询补货记录数据 (班组长)

        Args:
            current: 当前页
            endTime: 结束时间
            order: 顺序（0:从大到小 1:从小到大）
            rankingType: 0:数量 1:金额
            recordStatus: 0:取刀 1:还刀 2:收刀 3:暂存 4:完成 5:违规还刀
            size: 每页的数量
            startTime: 开始时间

        Returns:
            ReplenishRecordResponse: 补货记录响应数据
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
            data = response.json()
            
            # 构造符合ReplenishRecordResponse格式的响应
            records = [
                ReplenishRecord(**record) for record in data.get("data", {}).get("records", [])
            ]
            
            replenish_data = ReplenishRecordData(
                current=data.get("data", {}).get("current", 0),
                hitCount=data.get("data", {}).get("hitCount", False),
                pages=data.get("data", {}).get("pages", 0),
                records=records,
                searchCount=data.get("data", {}).get("searchCount", False),
                size=data.get("data", {}).get("size", 0),
                total=data.get("data", {}).get("total", 0)
            )
            
            return ReplenishRecordResponse(
                code=data.get("code", 0),
                data=replenish_data,
                msg=data.get("msg", ""),
                success=data.get("success", True)
            )
        except requests.RequestException as e:
            # 出错时返回默认格式
            replenish_data = ReplenishRecordData(
                current=0,
                hitCount=False,
                pages=0,
                records=[],
                searchCount=False,
                size=0,
                total=0
            )
            
            return ReplenishRecordResponse(
                code=-1,
                data=replenish_data,
                msg=f"请求失败: {str(e)}",
                success=False
            )

    # 领刀记录接口整合
    def get_lend_records(self,
                         current: Optional[int] = None,
                         endTime: Optional[str] = None,
                         order: Optional[int] = None,
                         rankingType: Optional[int] = None,
                         recordStatus: Optional[int] = None,
                         size: Optional[int] = None,
                         startTime: Optional[str] = None) -> LendRecordResponse:
        """
        分页查询取刀数据 (班组长)

        Args:
            current: 当前页
            endTime: 结束时间
            order: 顺序（0:从大到小 1:从小到大）
            rankingType: 0:数量 1:金额
            recordStatus: 0:取刀 1:还刀 2:收刀 3:暂存 4:完成 5:违规还刀
            size: 每页的数量
            startTime: 开始时间

        Returns:
            LendRecordResponse: 领刀记录响应数据
        """
        url = urljoin(self.base_url, "/qw/knife/web/from/mes/record/lendList")

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
            data = response.json()
            
            # 构造符合LendRecordResponse格式的响应
            records = [
                LendRecord(**record) for record in data.get("data", {}).get("records", [])
            ]
            
            lend_data = LendRecordData(
                current=data.get("data", {}).get("current", 0),
                hitCount=data.get("data", {}).get("hitCount", False),
                pages=data.get("data", {}).get("pages", 0),
                records=records,
                searchCount=data.get("data", {}).get("searchCount", False),
                size=data.get("data", {}).get("size", 0),
                total=data.get("data", {}).get("total", 0)
            )
            
            return LendRecordResponse(
                code=data.get("code", 0),
                data=lend_data,
                msg=data.get("msg", ""),
                success=data.get("success", True)
            )
        except requests.RequestException as e:
            # 出错时返回默认格式
            lend_data = LendRecordData(
                current=0,
                hitCount=False,
                pages=0,
                records=[],
                searchCount=False,
                size=0,
                total=0
            )
            
            return LendRecordResponse(
                code=-1,
                data=lend_data,
                msg=f"请求失败: {str(e)}",
                success=False
            )

    # 公共暂存记录接口整合
    def get_storage_records(self,
                            current: Optional[int] = None,
                            endTime: Optional[str] = None,
                            order: Optional[int] = None,
                            rankingType: Optional[int] = None,
                            recordStatus: Optional[int] = None,
                            size: Optional[int] = None,
                            startTime: Optional[str] = None) -> StorageRecordResponse:
        """
        分页查询公共暂存数据 (班组长)

        Args:
            current: 当前页
            endTime: 结束时间
            order: 顺序（0:从大到小 1:从小到大）
            rankingType: 0:数量 1:金额
            recordStatus: 0:取刀 1:还刀 2:收刀 3:暂存 4:完成 5:违规还刀
            size: 每页的数量
            startTime: 开始时间

        Returns:
            StorageRecordResponse: 公共暂存记录响应数据
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
            data = response.json()
            
            # 构造符合StorageRecordResponse格式的响应
            records = [
                StorageRecord(**record) for record in data.get("data", {}).get("records", [])
            ]
            
            storage_data = StorageRecordData(
                current=data.get("data", {}).get("current", 0),
                hitCount=data.get("data", {}).get("hitCount", False),
                pages=data.get("data", {}).get("pages", 0),
                records=records,
                searchCount=data.get("data", {}).get("searchCount", False),
                size=data.get("data", {}).get("size", 0),
                total=data.get("data", {}).get("total", 0)
            )
            
            return StorageRecordResponse(
                code=data.get("code", 0),
                data=storage_data,
                msg=data.get("msg", ""),
                success=data.get("success", True)
            )
        except requests.RequestException as e:
            # 出错时返回默认格式
            storage_data = StorageRecordData(
                current=0,
                hitCount=False,
                pages=0,
                records=[],
                searchCount=False,
                size=0,
                total=0
            )
            
            return StorageRecordResponse(
                code=-1,
                data=storage_data,
                msg=f"请求失败: {str(e)}",
                success=False
            )

    # 告警预警接口整合
    def get_alarm_warnings(self,
                           locSurplus: Optional[int] = None,
                           alarmLevel: Optional[int] = None,
                           deviceType: Optional[str] = None,
                           cabinetCode: Optional[str] = None,
                           brandName: Optional[str] = None,
                           handleStatus: Optional[int] = None,
                           current: Optional[int] = None,
                           size: Optional[int] = None) -> AlarmWarningResponse:
        """
        获取告警预警列表 (班组长)

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
            AlarmWarningResponse: 告警预警响应数据
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
            data = response.json()
            
            # 构造符合AlarmWarningResponse格式的响应
            records = [
                AlarmWarning(**record) for record in data.get("data", {}).get("records", [])
            ]
            
            alarm_data = AlarmWarningData(
                current=data.get("data", {}).get("current", 0),
                hitCount=data.get("data", {}).get("hitCount", False),
                pages=data.get("data", {}).get("pages", 0),
                records=records,
                searchCount=data.get("data", {}).get("searchCount", False),
                size=data.get("data", {}).get("size", 0),
                total=data.get("data", {}).get("total", 0)
            )
            
            return AlarmWarningResponse(
                code=data.get("code", 0),
                data=alarm_data,
                msg=data.get("msg", ""),
                success=data.get("success", True)
            )
        except requests.RequestException as e:
            # 出错时返回默认格式
            alarm_data = AlarmWarningData(
                current=0,
                hitCount=False,
                pages=0,
                records=[],
                searchCount=False,
                size=0,
                total=0
            )
            
            return AlarmWarningResponse(
                code=-1,
                data=alarm_data,
                msg=f"请求失败: {str(e)}",
                success=False
            )

    # 其他接口保持不变
    def export_lend_records(self,
                            endTime: Optional[str] = None,
                            order: Optional[int] = None,
                            rankingType: Optional[int] = None,
                            recordStatus: Optional[int] = None,
                            startTime: Optional[str] = None) -> bytes:
        """
        导出刀具耗材数据（领刀记录） (班组长)

        Args:
            endTime: 结束时间
            order: 顺序（0:从大到小 1:从小到大）
            rankingType: 0:数量 1:金额
            recordStatus: 0:取刀 1:还刀 2:收刀 3:暂存 4:完成 5:违规还刀
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

    def stock_bind_cutter(self,
                          cutterId: Optional[int] = None,
                          isBan: Optional[int] = None,
                          locCapacity: Optional[int] = None,
                          locPackQty: Optional[int] = None,
                          locSurplus: Optional[int] = None,
                          stockId: Optional[int] = None,
                          warningNum: Optional[int] = None) -> Dict[str, Any]:
        """
        刀柜货道 绑定/补货 刀具 (班组长)

        Args:
            cutterId: 耗材主键
            isBan: 是否禁用（0:非禁用 1:禁用）
            locCapacity: 货道容量
            locPackQty: 货道包装数量
            locSurplus: 货道刀具数量
            stockId: 刀柜货道主键
            warningNum: 警报数量

        Returns:
            Dict: API响应结果
        """
        url = urljoin(self.base_url, "/qw/knife/app/from/mes/cabinet/stockBindCutter")

        params = {}

        # 添加可选参数
        if cutterId is not None:
            params["cutterId"] = cutterId
        if isBan is not None:
            params["isBan"] = isBan
        if locCapacity is not None:
            params["locCapacity"] = locCapacity
        if locPackQty is not None:
            params["locPackQty"] = locPackQty
        if locSurplus is not None:
            params["locSurplus"] = locSurplus
        if stockId is not None:
            params["stockId"] = stockId
        if warningNum is not None:
            params["warningNum"] = warningNum

        try:
            response = self.session.post(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {
                "code": -1,
                "msg": f"请求失败: {str(e)}",
                "data": None,
                "success": False
            }

    def export_replenish_records(self,
                                endTime: Optional[str] = None,
                                order: Optional[int] = None,
                                rankingType: Optional[int] = None,
                                recordStatus: Optional[int] = None,
                                startTime: Optional[str] = None) -> bytes:
        """
        导出补货记录 (班组长)

        Args:
            endTime: 结束时间
            order: 顺序（0:从大到小 1:从小到大）
            rankingType: 0:数量 1:金额
            recordStatus: 0:取刀 1:还刀 2:收刀 3:暂存 4:完成 5:违规还刀
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

    def export_storage_records(self,
                              endTime: Optional[str] = None,
                              order: Optional[int] = None,
                              rankingType: Optional[int] = None,
                              recordStatus: Optional[int] = None,
                              startTime: Optional[str] = None) -> bytes:
        """
        导出公共暂存记录 (班组长)

        Args:
            endTime: 结束时间
            order: 顺序（0:从大到小 1:从小到大）
            rankingType: 0:数量 1:金额
            recordStatus: 0:取刀 1:还刀 2:收刀 3:暂存 4:完成 5:违规还刀
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

    def get_personal_storage(self, cabinetCode: Optional[str] = None) -> Dict[str, Any]:
        """
        获取个人暂存柜 (班组长)

        Args:
            cabinetCode: 刀柜编码

        Returns:
            Dict: API响应结果
        """
        url = urljoin(self.base_url, "/qw/knife/app/from/mes/cabinet/personalStorage")

        params = {}

        # 添加可选参数
        if cabinetCode:
            params["cabinetCode"] = cabinetCode

        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {
                "code": -1,
                "msg": f"请求失败: {str(e)}",
                "data": [],
                "success": False
            }

    def make_alarm(self,
                   cabinetCode: Optional[str] = None,
                   makeAlarm: Optional[int] = None) -> Dict[str, Any]:
        """
        取刀柜库存告警值预设 (班组长)

        Args:
            cabinetCode: 刀柜编码
            makeAlarm: 警值预设

        Returns:
            Dict: API响应结果
        """
        url = urljoin(self.base_url, "/qw/knife/web/from/mes/cabinet/makeAlarm")

        params = {}

        # 添加可选参数
        if cabinetCode:
            params["cabinetCode"] = cabinetCode
        if makeAlarm is not None:
            params["makeAlarm"] = makeAlarm

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

    def get_make_alarm(self, cabinetCode: Optional[str] = None) -> Dict[str, Any]:
        """
        获取取刀柜库存告警值预设 (班组长)

        Args:
            cabinetCode: 刀柜编码

        Returns:
            Dict: API响应结果
        """
        url = urljoin(self.base_url, "/qw/knife/web/from/mes/cabinet/getMakeAlarm")

        params = {}

        # 添加可选参数
        if cabinetCode:
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


# 创建全局API客户端实例
api_client = APIClient()