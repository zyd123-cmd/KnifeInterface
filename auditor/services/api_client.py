import requests
import logging
from typing import Dict, Any, List

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

        # 添加模拟数据
        self.mock_return_info_data = [
            {
                "id": 1,
                "cabinetCode": "CABINET-001",
                "borrowTime": "2023-10-01 09:00:00",
                "borrowUser": "张三",
                "brandName": "品牌A",
                "cutterCode": "CT-001",
                "cutterType": "铣刀",
                "lendTime": "2023-10-01 09:15:00",
                "lendUser": "李四",
                "recordStatus": 1,
                "specification": "Φ10",
                "stockLoc": "A01",
                "borrowStatus": 2
            },
            {
                "id": 2,
                "cabinetCode": "CABINET-002",
                "borrowTime": "2023-10-02 10:00:00",
                "borrowUser": "王五",
                "brandName": "品牌B",
                "cutterCode": "CT-002",
                "cutterType": "钻头",
                "lendTime": "2023-10-02 10:20:00",
                "lendUser": "赵六",
                "recordStatus": 1,
                "specification": "Φ12",
                "stockLoc": "B01",
                "borrowStatus": 2
            }
        ]

        # 添加收刀信息模拟数据
        self.mock_collect_info_data = [
            {
                "id": 1,
                "cabinetCode": "CABINET-001",
                "location": "A01",
                "cutterCode": "CT-001",
                "cutterType": "铣刀",
                "brandName": "品牌A",
                "specification": "Φ10",
                "collectTime": "2023-10-01 10:00:00",
                "collectUser": "张三",
                "status": 1
            },
            {
                "id": 2,
                "cabinetCode": "CABINET-002",
                "location": "B01",
                "cutterCode": "CT-002",
                "cutterType": "钻头",
                "brandName": "品牌B",
                "specification": "Φ12",
                "collectTime": "2023-10-02 11:00:00",
                "collectUser": "王五",
                "status": 0
            }
        ]

        # 添加排名统计模拟数据
        self.mock_yearly_quantity_stats = [
            {"month": f"{i}月", "quantity": 100 + i * 10} for i in range(1, 13)
        ]
        
        self.mock_yearly_amount_stats = [
            {"month": f"{i}月", "amount": 5000.0 + i * 500.0} for i in range(1, 13)
        ]
        
        self.mock_yearly_usage_stats = [
            {"date": f"2023-10-{i:02d}", "usageCount": 20 + i} for i in range(1, 31)
        ]
        
        self.mock_employee_ranking_stats = [
            {"employeeName": f"员工{i}", "count": 50 - i} for i in range(1, 11)
        ]
        
        self.mock_equipment_ranking_stats = [
            {"equipmentName": f"设备{i}", "count": 30 - i} for i in range(1, 11)
        ]
        
        self.mock_cutter_model_ranking_stats = [
            {"modelName": f"型号{i}", "count": 40 - i} for i in range(1, 11)
        ]
        
        self.mock_work_order_ranking_stats = [
            {"workOrder": f"工单{i:03d}", "count": 25 - i} for i in range(1, 11)
        ]
        
        self.mock_abnormal_return_ranking_stats = [
            {"reason": f"异常原因{i}", "count": 10 - i} for i in range(1, 6)
        ]
        
        # 添加总库存统计模拟数据
        self.mock_inventory_stats_data = [
            {
                "id": 1,
                "itemName": "铣刀",
                "itemType": "刀具",
                "brand": "品牌A",
                "currentStock": 50,
                "minStock": 10,
                "maxStock": 100,
                "unit": "把"
            },
            {
                "id": 2,
                "itemName": "钻头",
                "itemType": "刀具",
                "brand": "品牌B",
                "currentStock": 30,
                "minStock": 5,
                "maxStock": 50,
                "unit": "支"
            },
            {
                "id": 3,
                "itemName": "刀柄",
                "itemType": "刀柄",
                "brand": "品牌C",
                "currentStock": 20,
                "minStock": 5,
                "maxStock": 30,
                "unit": "个"
            }
        ]
        
        # 添加品牌列表模拟数据
        self.mock_brands = [
            {"id": 1, "name": "品牌A"},
            {"id": 2, "name": "品牌B"},
            {"id": 3, "name": "品牌C"}
        ]
        
        # 添加刀具类型列表模拟数据
        self.mock_cutter_types = [
            {"id": 1, "name": "铣刀"},
            {"id": 2, "name": "钻头"},
            {"id": 3, "name": "车刀"}
        ]
        
        # 添加刀柄类型列表模拟数据
        self.mock_handle_types = [
            {"id": 1, "name": "BT型"},
            {"id": 2, "name": "HSK型"},
            {"id": 3, "name": "CAT型"}
        ]
        
        # 添加刀柜列表模拟数据
        self.mock_cabinets = [
            {"id": 1, "code": "CABINET-001", "name": "一号刀柜"},
            {"id": 2, "code": "CABINET-002", "name": "二号刀柜"},
            {"id": 3, "code": "CABINET-003", "name": "三号刀柜"}
        ]
        
        # 添加未还信息模拟数据
        self.mock_unreturned_info_data = [
            {
                "id": 1,
                "borrower": "李四",
                "borrowTime": "2023-10-01 09:00:00",
                "cutterCode": "CT-001",
                "cutterType": "铣刀",
                "brandName": "品牌A",
                "specification": "Φ10",
                "expectedReturnTime": "2023-10-10 09:00:00",
                "overdueDays": 0,
                "status": 0
            },
            {
                "id": 2,
                "borrower": "王五",
                "borrowTime": "2023-10-02 10:00:00",
                "cutterCode": "CT-002",
                "cutterType": "钻头",
                "brandName": "品牌B",
                "specification": "Φ12",
                "expectedReturnTime": "2023-10-05 10:00:00",
                "overdueDays": 2,
                "status": 1
            }
        ]
        
        # 添加数据字典模拟数据
        # 刀具类型模拟数据
        self.mock_cutter_types_data = [
            {
                "id": 1,
                "name": "铣刀",
                "category": "加工刀具",
                "parentId": None,
                "description": "用于铣削加工的刀具",
                "status": 1
            },
            {
                "id": 2,
                "name": "钻头",
                "category": "加工刀具",
                "parentId": None,
                "description": "用于钻孔加工的刀具",
                "status": 1
            },
            {
                "id": 3,
                "name": "车刀",
                "category": "加工刀具",
                "parentId": None,
                "description": "用于车削加工的刀具",
                "status": 1
            }
        ]
        
        # 字典集合模拟数据
        self.mock_dict_collection_data = [
            {
                "id": 1,
                "code": "STATUS",
                "name": "状态字典",
                "type": "system",
                "parentId": None,
                "description": "系统状态字典",
                "status": 1
            },
            {
                "id": 2,
                "code": "USER_TYPE",
                "name": "用户类型",
                "type": "system",
                "parentId": None,
                "description": "用户类型字典",
                "status": 1
            }
        ]
        
        # 个性化设置模拟数据
        self.mock_personalized_settings_data = [
            {
                "id": 1,
                "name": "系统名称",
                "code": "SYSTEM_NAME",
                "type": "system",
                "group": "基础配置",
                "value": "刀具管理系统",
                "description": "系统名称设置",
                "status": 1
            },
            {
                "id": 2,
                "name": "默认语言",
                "code": "DEFAULT_LANGUAGE",
                "type": "system",
                "group": "基础配置",
                "value": "zh-CN",
                "description": "系统默认语言",
                "status": 1
            }
        ]
        
        # 历史记录模拟数据
        # 操作日志模拟数据
        self.mock_operation_log_data = [
            {
                "id": 1,
                "operator": "张三",
                "operationTime": "2023-10-01 09:00:00",
                "operationType": "查询",
                "moduleName": "刀具管理",
                "description": "查询刀具列表",
                "ipAddress": "192.168.1.100",
                "status": 1
            },
            {
                "id": 2,
                "operator": "李四",
                "operationTime": "2023-10-01 10:30:00",
                "operationType": "新增",
                "moduleName": "用户管理",
                "description": "新增用户信息",
                "ipAddress": "192.168.1.101",
                "status": 1
            }
        ]
        
        # 公共暂存记录模拟数据
        self.mock_public_storage_data = [
            {
                "id": 1,
                "storageCode": "PS20231001001",
                "cutterCode": "CT-001",
                "cutterType": "铣刀",
                "brandName": "品牌A",
                "specification": "Φ10",
                "quantity": 5,
                "storageTime": "2023-10-01 09:15:00",
                "operator": "张三",
                "status": 1
            },
            {
                "id": 2,
                "storageCode": "PS20231001002",
                "cutterCode": "CT-002",
                "cutterType": "钻头",
                "brandName": "品牌B",
                "specification": "Φ12",
                "quantity": 3,
                "storageTime": "2023-10-01 10:30:00",
                "operator": "李四",
                "status": 0
            }
        ]
        
        # 补货记录模拟数据
        self.mock_restock_data = [
            {
                "id": 1,
                "restockCode": "RS20231001001",
                "cutterCode": "CT-001",
                "cutterType": "铣刀",
                "brandName": "品牌A",
                "specification": "Φ10",
                "quantity": 10,
                "restockTime": "2023-10-01 09:00:00",
                "operator": "王五",
                "status": 1
            },
            {
                "id": 2,
                "restockCode": "RS20231001002",
                "cutterCode": "CT-002",
                "cutterType": "钻头",
                "brandName": "品牌B",
                "specification": "Φ12",
                "quantity": 5,
                "restockTime": "2023-10-01 10:00:00",
                "operator": "赵六",
                "status": 1
            }
        ]
        
        # 出入库记录模拟数据
        self.mock_stock_record_data = [
            {
                "id": 1,
                "recordCode": "IN20231001001",
                "cutterCode": "CT-001",
                "cutterType": "铣刀",
                "brandName": "品牌A",
                "specification": "Φ10",
                "quantity": 20,
                "recordType": "入库",
                "recordTime": "2023-10-01 08:00:00",
                "operator": "管理员A",
                "status": 1
            },
            {
                "id": 2,
                "recordCode": "OUT20231001001",
                "cutterCode": "CT-002",
                "cutterType": "钻头",
                "brandName": "品牌B",
                "specification": "Φ12",
                "quantity": 5,
                "recordType": "出库",
                "recordTime": "2023-10-01 14:00:00",
                "operator": "操作员B",
                "status": 1
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

    def get_return_info(self, info_id: int) -> Dict[str, Any]:
        """查询还刀信息详情"""
        #模拟数据
        if self.base_url =="mock":
            for item in self.mock_return_info_data:
                if item["id"] == info_id:
                    return item
            raise Exception(f"未找到id为{info_id}的还刀信息")
        #真实api
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

        #模拟数据测试
        if self.base_url =="mock":
            page = params.get("page", 1) if params else 1
            size = params.get("size", 10) if params else 10
            start = (page - 1) * size
            end = start + size
            paginated_data = self.mock_return_info_data[start:end]

            return {
                "list": paginated_data,
                "total": len(self.mock_return_info_data)
            }

        #真实api
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

    # 收刀信息相关方法
    def get_collect_info_list(self, params=None):
        """获取收刀信息列表"""
        # 模拟数据测试
        if self.base_url == "mock":
            page = params.get("page", 1) if params else 1
            size = params.get("size", 10) if params else 10
            start = (page - 1) * size
            end = start + size
            paginated_data = self.mock_collect_info_data[start:end]

            return {
                "list": paginated_data,
                "total": len(self.mock_collect_info_data)
            }

        # 真实API
        url = f"{self.base_url}/api/v1/collect_info"
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"获取收刀信息列表失败: {e}")
            raise

    def get_collect_info(self, info_id: int) -> Dict[str, Any]:
        """查询收刀信息详情"""
        # 模拟数据
        if self.base_url == "mock":
            for item in self.mock_collect_info_data:
                if item["id"] == info_id:
                    return item
            raise Exception(f"未找到ID为{info_id}的收刀信息")

        # 真实API
        url = f"{self.base_url}/api/v1/collect_info/{info_id}"
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"查询收刀信息详情失败: {e}")
            raise

    def confirm_collect(self, data):
        """确认收刀操作"""
        # 模拟数据
        if self.base_url == "mock":
            info_id = data.get("id")
            for item in self.mock_collect_info_data:
                if item["id"] == info_id:
                    item["status"] = 1  # 设置为已确认状态
                    return {"message": "确认收刀成功"}
            raise Exception(f"未找到ID为{info_id}的收刀信息")

        # 真实API
        url = f"{self.base_url}/api/v1/collect_info/confirm"
        try:
            response = self.session.post(url, json=data, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"确认收刀操作失败: {e}")
            raise

    def create_collect_info(self, data):
        """新增收刀信息"""
        # 模拟数据
        if self.base_url == "mock":
            new_id = max([item["id"] for item in self.mock_collect_info_data]) + 1 if self.mock_collect_info_data else 1
            new_info = {
                "id": new_id,
                "cabinetCode": data["cabinetCode"],
                "location": data["location"],
                "cutterCode": data["cutterCode"],
                "cutterType": data["cutterType"],
                "brandName": data["brandName"],
                "specification": data["specification"],
                "collectTime": data["collectTime"],
                "collectUser": data["collectUser"],
                "status": 0  # 默认待确认
            }
            self.mock_collect_info_data.append(new_info)
            return new_info

        # 真实API
        url = f"{self.base_url}/api/v1/collect_info"
        try:
            response = self.session.post(url, json=data, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"新增收刀信息失败: {e}")
            raise

    def update_collect_info(self, data):
        """修改收刀信息"""
        # 模拟数据
        if self.base_url == "mock":
            info_id = data.get("id")
            for item in self.mock_collect_info_data:
                if item["id"] == info_id:
                    # 更新字段
                    for key, value in data.items():
                        if key != "id" and value is not None:
                            item[key] = value
                    return item
            raise Exception(f"未找到ID为{info_id}的收刀信息")

        # 真实API
        url = f"{self.base_url}/api/v1/collect_info"
        try:
            response = self.session.put(url, json=data, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"修改收刀信息失败: {e}")
            raise

    def delete_collect_info(self, info_id):
        """删除收刀信息"""
        # 模拟数据
        if self.base_url == "mock":
            for i, item in enumerate(self.mock_collect_info_data):
                if item["id"] == info_id:
                    del self.mock_collect_info_data[i]
                    return {"message": "删除成功"}
            raise Exception(f"未找到ID为{info_id}的收刀信息")

        # 真实API
        url = f"{self.base_url}/api/v1/collect_info/{info_id}"
        try:
            response = self.session.delete(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"删除收刀信息失败: {e}")
            raise

    def batch_delete_collect_info(self, ids):
        """批量删除收刀信息"""
        # 模拟数据
        if self.base_url == "mock":
            original_length = len(self.mock_collect_info_data)
            self.mock_collect_info_data = [item for item in self.mock_collect_info_data if item["id"] not in ids]
            deleted_count = original_length - len(self.mock_collect_info_data)
            return {"message": f"成功删除{deleted_count}条记录"}

        # 真实API
        url = f"{self.base_url}/api/v1/collect_info/batch"
        try:
            response = self.session.delete(url, json=ids, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"批量删除收刀信息失败: {e}")
            raise

    def export_collect_info(self, params=None):
        """导出收刀信息"""
        # 模拟数据
        if self.base_url == "mock":
            return {
                "message": "导出成功",
                "data": self.mock_collect_info_data
            }

        # 真实API
        url = f"{self.base_url}/api/v1/collect_info/export"
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"导出收刀信息失败: {e}")
            raise

    def get_cabinet_code_list(self):
        """获取刀柜编码列表"""
        # 模拟数据
        if self.base_url == "mock":
            cabinet_codes = list(set([info["cabinetCode"] for info in self.mock_collect_info_data if info["cabinetCode"]]))
            return {"list": [{"code": code, "name": f"{code}号刀柜"} for code in cabinet_codes]}

        # 真实API
        url = f"{self.base_url}/api/v1/collect_info/cabinetCodes"
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"获取刀柜编码列表失败: {e}")
            raise

    def get_location_list(self, cabinet_code=None):
        """获取库位列表"""
        # 模拟数据
        if self.base_url == "mock":
            # 如果提供了cabinetCode参数，则筛选对应刀柜的库位
            if cabinet_code:
                locations = list(set([info["location"] for info in self.mock_collect_info_data 
                                    if info["location"] and info["cabinetCode"] == cabinet_code]))
            else:
                locations = list(set([info["location"] for info in self.mock_collect_info_data if info["location"]]))
            return {"list": [{"code": loc, "name": loc} for loc in locations]}

        # 真实API
        url = f"{self.base_url}/api/v1/collect_info/locations"
        try:
            params = {"cabinetCode": cabinet_code} if cabinet_code else None
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"获取库位列表失败: {e}")
            raise

    # 借还排名统计相关方法
    def get_yearly_quantity_statistics(self, params=None):
        """查询全年取刀数量统计"""
        # 模拟数据
        if self.base_url == "mock":
            return {"list": self.mock_yearly_quantity_stats}

        # 真实API
        url = f"{self.base_url}/api/v1/rankingStatistics/yearlyQuantity"
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"查询全年取刀数量统计失败: {e}")
            raise

    def get_yearly_amount_statistics(self, params=None):
        """查询全年取刀金额统计"""
        # 模拟数据
        if self.base_url == "mock":
            return {"list": self.mock_yearly_amount_stats}

        # 真实API
        url = f"{self.base_url}/api/v1/rankingStatistics/yearlyAmount"
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"查询全年取刀金额统计失败: {e}")
            raise

    def get_yearly_usage_statistics(self, params=None):
        """查询今年累计使用统计"""
        # 模拟数据
        if self.base_url == "mock":
            return {"list": self.mock_yearly_usage_stats}

        # 真实API
        url = f"{self.base_url}/api/v1/rankingStatistics/yearlyUsage"
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"查询今年累计使用统计失败: {e}")
            raise

    def get_employee_ranking_statistics(self, params=None):
        """查询员工领刀排行"""
        # 模拟数据
        if self.base_url == "mock":
            return {"list": self.mock_employee_ranking_stats}

        # 真实API
        url = f"{self.base_url}/api/v1/rankingStatistics/employeeRanking"
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"查询员工领刀排行失败: {e}")
            raise

    def get_equipment_ranking_statistics(self, params=None):
        """查询设备用刀排行"""
        # 模拟数据
        if self.base_url == "mock":
            return {"list": self.mock_equipment_ranking_stats}

        # 真实API
        url = f"{self.base_url}/api/v1/rankingStatistics/equipmentRanking"
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"查询设备用刀排行失败: {e}")
            raise

    def get_cutter_model_ranking_statistics(self, params=None):
        """查询刀具型号排行"""
        # 模拟数据
        if self.base_url == "mock":
            return {"list": self.mock_cutter_model_ranking_stats}

        # 真实API
        url = f"{self.base_url}/api/v1/rankingStatistics/cutterModelRanking"
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"查询刀具型号排行失败: {e}")
            raise

    def get_work_order_ranking_statistics(self, params=None):
        """查询工单排行"""
        # 模拟数据
        if self.base_url == "mock":
            return {"list": self.mock_work_order_ranking_stats}

        # 真实API
        url = f"{self.base_url}/api/v1/rankingStatistics/workOrderRanking"
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"查询工单排行失败: {e}")
            raise

    def get_abnormal_return_ranking_statistics(self, params=None):
        """查询异常还刀排行"""
        # 模拟数据
        if self.base_url == "mock":
            return {"list": self.mock_abnormal_return_ranking_stats}

        # 真实API
        url = f"{self.base_url}/api/v1/rankingStatistics/abnormalReturnRanking"
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"查询异常还刀排行失败: {e}")
            raise

    # 总库存统计相关方法
    def get_total_inventory_stats_list(self, params=None):
        """查询总库存统计列表"""
        # 模拟数据
        if self.base_url == "mock":
            page = params.get("page", 1) if params else 1
            size = params.get("size", 10) if params else 10
            start = (page - 1) * size
            end = start + size
            paginated_data = self.mock_inventory_stats_data[start:end]

            return {
                "list": paginated_data,
                "total": len(self.mock_inventory_stats_data)
            }

        # 真实API
        url = f"{self.base_url}/api/v1/totalInventoryStats/list"
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"查询总库存统计列表失败: {e}")
            raise

    def get_cutter_inventory_stats(self, params=None):
        """查询刀具库存统计"""
        # 模拟数据
        if self.base_url == "mock":
            cutter_stats = [item for item in self.mock_inventory_stats_data if item["itemType"] == "刀具"]
            return {"list": cutter_stats}

        # 真实API
        url = f"{self.base_url}/api/v1/totalInventoryStats/cutter"
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"查询刀具库存统计失败: {e}")
            raise

    def get_handle_inventory_stats(self, params=None):
        """查询刀柄库存统计"""
        # 模拟数据
        if self.base_url == "mock":
            handle_stats = [item for item in self.mock_inventory_stats_data if item["itemType"] == "刀柄"]
            return {"list": handle_stats}

        # 真实API
        url = f"{self.base_url}/api/v1/totalInventoryStats/handle"
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"查询刀柄库存统计失败: {e}")
            raise

    def get_inventory_summary(self, type_param=None):
        """获取库存汇总数据"""
        # 模拟数据
        if self.base_url == "mock":
            total_items = len(self.mock_inventory_stats_data)
            total_value = sum([item["currentStock"] * 100 for item in self.mock_inventory_stats_data])  # 假设单价100
            low_stock_items = len([item for item in self.mock_inventory_stats_data if item["currentStock"] <= item["minStock"]])
            out_of_stock_items = len([item for item in self.mock_inventory_stats_data if item["currentStock"] == 0])
            
            return {
                "totalItems": total_items,
                "totalValue": total_value,
                "lowStockItems": low_stock_items,
                "outOfStockItems": out_of_stock_items
            }

        # 真实API
        url = f"{self.base_url}/api/v1/totalInventoryStats/summary"
        try:
            params = {"type": type_param} if type_param else None
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"获取库存汇总数据失败: {e}")
            raise

    def export_inventory_stats(self, params=None):
        """导出库存统计"""
        # 模拟数据
        if self.base_url == "mock":
            return {
                "message": "导出成功",
                "data": self.mock_inventory_stats_data
            }

        # 真实API
        url = f"{self.base_url}/api/v1/totalInventoryStats/export"
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"导出库存统计失败: {e}")
            raise

    def get_brand_list(self):
        """获取品牌列表"""
        # 模拟数据
        if self.base_url == "mock":
            return {"list": self.mock_brands}

        # 真实API
        url = f"{self.base_url}/api/v1/totalInventoryStats/brands"
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"获取品牌列表失败: {e}")
            raise

    def get_cutter_type_list(self):
        """获取刀具类型列表"""
        # 模拟数据
        if self.base_url == "mock":
            return {"list": self.mock_cutter_types}

        # 真实API
        url = f"{self.base_url}/api/v1/totalInventoryStats/cutterTypes"
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"获取刀具类型列表失败: {e}")
            raise

    def get_handle_type_list(self):
        """获取刀柄类型列表"""
        # 模拟数据
        if self.base_url == "mock":
            return {"list": self.mock_handle_types}

        # 真实API
        url = f"{self.base_url}/api/v1/totalInventoryStats/handleTypes"
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"获取刀柄类型列表失败: {e}")
            raise

    def get_cabinet_list(self):
        """获取刀柜列表"""
        # 模拟数据
        if self.base_url == "mock":
            return {"list": self.mock_cabinets}

        # 真实API
        url = f"{self.base_url}/api/v1/totalInventoryStats/cabinets"
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"获取刀柜列表失败: {e}")
            raise

    # 未还信息相关方法
    def get_unreturned_info_list(self, params=None):
        """获取未还信息列表"""
        # 模拟数据测试
        if self.base_url == "mock":
            page = params.get("page", 1) if params else 1
            size = params.get("size", 10) if params else 10
            start = (page - 1) * size
            end = start + size
            paginated_data = self.mock_unreturned_info_data[start:end]

            return {
                "list": paginated_data,
                "total": len(self.mock_unreturned_info_data)
            }

        # 真实API
        url = f"{self.base_url}/api/v1/unreturned_info"
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"获取未还信息列表失败: {e}")
            raise

    def get_unreturned_info(self, info_id: int) -> Dict[str, Any]:
        """查询未还信息详情"""
        # 模拟数据
        if self.base_url == "mock":
            for item in self.mock_unreturned_info_data:
                if item["id"] == info_id:
                    return item
            raise Exception(f"未找到ID为{info_id}的未还信息")

        # 真实API
        url = f"{self.base_url}/api/v1/unreturned_info/{info_id}"
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"查询未还信息详情失败: {e}")
            raise

    def create_unreturned_info(self, data):
        """新增未还信息"""
        # 模拟数据
        if self.base_url == "mock":
            new_id = max([item["id"] for item in self.mock_unreturned_info_data]) + 1 if self.mock_unreturned_info_data else 1
            new_info = data.copy()
            new_info["id"] = new_id
            new_info["status"] = 0  # 默认未还状态
            new_info["overdueDays"] = 0  # 默认未逾期
            self.mock_unreturned_info_data.append(new_info)
            return new_info

        # 真实API
        url = f"{self.base_url}/api/v1/unreturned_info"
        try:
            response = self.session.post(url, json=data, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"新增未还信息失败: {e}")
            raise

    def update_unreturned_info(self, data):
        """修改未还信息"""
        # 模拟数据
        if self.base_url == "mock":
            for info in self.mock_unreturned_info_data:
                if info["id"] == data["id"]:
                    # 更新字段
                    for key, value in data.items():
                        if key != "id" and value is not None:
                            info[key] = value
                    return info
            raise Exception(f"未找到ID为{data['id']}的未还信息")

        # 真实API
        url = f"{self.base_url}/api/v1/unreturned_info"
        try:
            response = self.session.put(url, json=data, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"修改未还信息失败: {e}")
            raise

    def delete_unreturned_info(self, info_id):
        """删除未还信息"""
        # 模拟数据
        if self.base_url == "mock":
            for i, info in enumerate(self.mock_unreturned_info_data):
                if info["id"] == info_id:
                    del self.mock_unreturned_info_data[i]
                    return {"message": "删除成功"}
            raise Exception(f"未找到ID为{info_id}的未还信息")

        # 真实API
        url = f"{self.base_url}/api/v1/unreturned_info/{info_id}"
        try:
            response = self.session.delete(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"删除未还信息失败: {e}")
            raise

    def export_unreturned_info(self, params=None):
        """导出未还信息"""
        # 模拟数据
        if self.base_url == "mock":
            return {
                "message": "导出成功",
                "data": self.mock_unreturned_info_data
            }

        # 真实API
        url = f"{self.base_url}/api/v1/unreturned_info/export"
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"导出未还信息失败: {e}")
            raise

    def statistics_unreturned_info(self, params=None):
        """统计未还信息"""
        # 模拟数据
        if self.base_url == "mock":
            total_unreturned = len(self.mock_unreturned_info_data)
            overdue_count = len([item for item in self.mock_unreturned_info_data if item["overdueDays"] > 0])
            nearing_due_date = len([item for item in self.mock_unreturned_info_data if item["overdueDays"] == 0 and item["expectedReturnTime"]])
            
            return {
                "totalUnreturned": total_unreturned,
                "overdueCount": overdue_count,
                "nearingDueDate": nearing_due_date
            }

        # 真实API
        url = f"{self.base_url}/api/v1/unreturned_info/statistics"
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"统计未还信息失败: {e}")
            raise

    # 数据字典相关方法
    # 刀具类型相关方法
    def get_cutter_type_list(self, params=None):
        """查询刀具类型列表"""
        # 模拟数据
        if self.base_url == "mock":
            page = params.get("page", 1) if params else 1
            size = params.get("size", 10) if params else 10
            start = (page - 1) * size
            end = start + size
            paginated_data = self.mock_cutter_types_data[start:end]

            return {
                "list": paginated_data,
                "total": len(self.mock_cutter_types_data)
            }

        # 真实API
        url = f"{self.base_url}/api/v1/dataDictionary/cutterType/list"
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"查询刀具类型列表失败: {e}")
            raise

    def get_cutter_type(self, type_id: int) -> Dict[str, Any]:
        """查询刀具类型详细"""
        # 模拟数据
        if self.base_url == "mock":
            for item in self.mock_cutter_types_data:
                if item["id"] == type_id:
                    return item
            raise Exception(f"未找到ID为{type_id}的刀具类型")

        # 真实API
        url = f"{self.base_url}/api/v1/dataDictionary/cutterType/{type_id}"
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"查询刀具类型详情失败: {e}")
            raise

    def create_cutter_type(self, data):
        """新增刀具类型"""
        # 模拟数据
        if self.base_url == "mock":
            new_id = max([item["id"] for item in self.mock_cutter_types_data]) + 1 if self.mock_cutter_types_data else 1
            new_type = {
                "id": new_id,
                "name": data["name"],
                "category": data["category"],
                "parentId": data.get("parentId"),
                "description": data.get("description"),
                "status": 1  # 默认启用状态
            }
            self.mock_cutter_types_data.append(new_type)
            return new_type

        # 真实API
        url = f"{self.base_url}/api/v1/dataDictionary/cutterType"
        try:
            response = self.session.post(url, json=data, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"新增刀具类型失败: {e}")
            raise

    def update_cutter_type(self, data):
        """修改刀具类型"""
        # 模拟数据
        if self.base_url == "mock":
            for item in self.mock_cutter_types_data:
                if item["id"] == data["id"]:
                    # 更新字段
                    for key, value in data.items():
                        if key != "id" and value is not None:
                            item[key] = value
                    return item
            raise Exception(f"未找到ID为{data['id']}的刀具类型")

        # 真实API
        url = f"{self.base_url}/api/v1/dataDictionary/cutterType"
        try:
            response = self.session.put(url, json=data, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"修改刀具类型失败: {e}")
            raise

    def delete_cutter_type(self, type_id):
        """删除刀具类型"""
        # 模拟数据
        if self.base_url == "mock":
            for i, item in enumerate(self.mock_cutter_types_data):
                if item["id"] == type_id:
                    del self.mock_cutter_types_data[i]
                    return {"message": "删除成功"}
            raise Exception(f"未找到ID为{type_id}的刀具类型")

        # 真实API
        url = f"{self.base_url}/api/v1/dataDictionary/cutterType/{type_id}"
        try:
            response = self.session.delete(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"删除刀具类型失败: {e}")
            raise

    def batch_delete_cutter_type(self, ids: List[int]):
        """批量删除刀具类型"""
        # 模拟数据
        if self.base_url == "mock":
            original_length = len(self.mock_cutter_types_data)
            self.mock_cutter_types_data = [item for item in self.mock_cutter_types_data if item["id"] not in ids]
            deleted_count = original_length - len(self.mock_cutter_types_data)
            return {"message": f"成功删除{deleted_count}条记录"}

        # 真实API
        url = f"{self.base_url}/api/v1/dataDictionary/cutterType/batch"
        try:
            response = self.session.delete(url, json=ids, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"批量删除刀具类型失败: {e}")
            raise

    def export_cutter_type(self, params=None):
        """导出刀具类型"""
        # 模拟数据
        if self.base_url == "mock":
            return {
                "message": "导出成功",
                "data": self.mock_cutter_types_data
            }

        # 真实API
        url = f"{self.base_url}/api/v1/dataDictionary/cutterType/export"
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"导出刀具类型失败: {e}")
            raise

    def get_cutter_category_list(self):
        """获取刀具分类列表"""
        # 模拟数据
        if self.base_url == "mock":
            categories = list(set([item["category"] for item in self.mock_cutter_types_data if item["category"]]))
            return {"list": [{"name": cat} for cat in categories]}

        # 真实API
        url = f"{self.base_url}/api/v1/dataDictionary/cutterType/categories"
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"获取刀具分类列表失败: {e}")
            raise

    def get_parent_cutter_type_list(self):
        """获取父级刀具类型列表"""
        # 模拟数据
        if self.base_url == "mock":
            # 筛选出没有父级的刀具类型作为父级选项
            parent_types = [item for item in self.mock_cutter_types_data if item["parentId"] is None]
            return {"list": parent_types}

        # 真实API
        url = f"{self.base_url}/api/v1/dataDictionary/cutterType/parents"
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"获取父级刀具类型列表失败: {e}")
            raise

    # 字典集合相关方法
    def get_dict_collection_list(self, params=None):
        """查询字典集合列表"""
        # 模拟数据
        if self.base_url == "mock":
            page = params.get("page", 1) if params else 1
            size = params.get("size", 10) if params else 10
            start = (page - 1) * size
            end = start + size
            paginated_data = self.mock_dict_collection_data[start:end]

            return {
                "list": paginated_data,
                "total": len(self.mock_dict_collection_data)
            }

        # 真实API
        url = f"{self.base_url}/api/v1/dataDictionary/dictCollection/list"
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"查询字典集合列表失败: {e}")
            raise

    def get_dict_collection(self, collection_id: int) -> Dict[str, Any]:
        """查询字典集合详细"""
        # 模拟数据
        if self.base_url == "mock":
            for item in self.mock_dict_collection_data:
                if item["id"] == collection_id:
                    return item
            raise Exception(f"未找到ID为{collection_id}的字典集合")

        # 真实API
        url = f"{self.base_url}/api/v1/dataDictionary/dictCollection/{collection_id}"
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"查询字典集合详情失败: {e}")
            raise

    def get_dict_collection_by_code(self, code: str) -> Dict[str, Any]:
        """根据编码查询字典集合"""
        # 模拟数据
        if self.base_url == "mock":
            for item in self.mock_dict_collection_data:
                if item["code"] == code:
                    return item
            raise Exception(f"未找到编码为{code}的字典集合")

        # 真实API
        url = f"{self.base_url}/api/v1/dataDictionary/dictCollection/code"
        try:
            response = self.session.get(url, params={"code": code}, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"根据编码查询字典集合失败: {e}")
            raise

    def create_dict_collection(self, data):
        """新增字典集合"""
        # 模拟数据
        if self.base_url == "mock":
            new_id = max([item["id"] for item in self.mock_dict_collection_data]) + 1 if self.mock_dict_collection_data else 1
            new_collection = {
                "id": new_id,
                "code": data["code"],
                "name": data["name"],
                "type": data["type"],
                "parentId": data.get("parentId"),
                "description": data.get("description"),
                "status": 1  # 默认启用状态
            }
            self.mock_dict_collection_data.append(new_collection)
            return new_collection

        # 真实API
        url = f"{self.base_url}/api/v1/dataDictionary/dictCollection"
        try:
            response = self.session.post(url, json=data, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"新增字典集合失败: {e}")
            raise

    def update_dict_collection(self, data):
        """修改字典集合"""
        # 模拟数据
        if self.base_url == "mock":
            for item in self.mock_dict_collection_data:
                if item["id"] == data["id"]:
                    # 更新字段
                    for key, value in data.items():
                        if key != "id" and value is not None:
                            item[key] = value
                    return item
            raise Exception(f"未找到ID为{data['id']}的字典集合")

        # 真实API
        url = f"{self.base_url}/api/v1/dataDictionary/dictCollection"
        try:
            response = self.session.put(url, json=data, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"修改字典集合失败: {e}")
            raise

    def delete_dict_collection(self, collection_id):
        """删除字典集合"""
        # 模拟数据
        if self.base_url == "mock":
            for i, item in enumerate(self.mock_dict_collection_data):
                if item["id"] == collection_id:
                    del self.mock_dict_collection_data[i]
                    return {"message": "删除成功"}
            raise Exception(f"未找到ID为{collection_id}的字典集合")

        # 真实API
        url = f"{self.base_url}/api/v1/dataDictionary/dictCollection/{collection_id}"
        try:
            response = self.session.delete(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"删除字典集合失败: {e}")
            raise

    def batch_delete_dict_collection(self, ids: List[int]):
        """批量删除字典集合"""
        # 模拟数据
        if self.base_url == "mock":
            original_length = len(self.mock_dict_collection_data)
            self.mock_dict_collection_data = [item for item in self.mock_dict_collection_data if item["id"] not in ids]
            deleted_count = original_length - len(self.mock_dict_collection_data)
            return {"message": f"成功删除{deleted_count}条记录"}

        # 真实API
        url = f"{self.base_url}/api/v1/dataDictionary/dictCollection/batch"
        try:
            response = self.session.delete(url, json=ids, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"批量删除字典集合失败: {e}")
            raise

    def export_dict_collection(self, params=None):
        """导出字典集合"""
        # 模拟数据
        if self.base_url == "mock":
            return {
                "message": "导出成功",
                "data": self.mock_dict_collection_data
            }

        # 真实API
        url = f"{self.base_url}/api/v1/dataDictionary/dictCollection/export"
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"导出字典集合失败: {e}")
            raise

    def get_dict_type_list(self):
        """获取字典类型列表"""
        # 模拟数据
        if self.base_url == "mock":
            types = list(set([item["type"] for item in self.mock_dict_collection_data if item["type"]]))
            return {"list": [{"name": t} for t in types]}

        # 真实API
        url = f"{self.base_url}/api/v1/dataDictionary/dictCollection/types"
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"获取字典类型列表失败: {e}")
            raise

    def get_parent_dict_list(self):
        """获取父级字典列表"""
        # 模拟数据
        if self.base_url == "mock":
            # 筛选出没有父级的字典集合作为父级选项
            parent_dicts = [item for item in self.mock_dict_collection_data if item["parentId"] is None]
            return {"list": parent_dicts}

        # 真实API
        url = f"{self.base_url}/api/v1/dataDictionary/dictCollection/parents"
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"获取父级字典列表失败: {e}")
            raise

    # 个性化设置相关方法
    def get_personalized_settings_list(self, params=None):
        """查询个性化设置列表"""
        # 模拟数据
        if self.base_url == "mock":
            page = params.get("page", 1) if params else 1
            size = params.get("size", 10) if params else 10
            start = (page - 1) * size
            end = start + size
            paginated_data = self.mock_personalized_settings_data[start:end]

            return {
                "list": paginated_data,
                "total": len(self.mock_personalized_settings_data)
            }

        # 真实API
        url = f"{self.base_url}/api/v1/dataDictionary/personalizedSettings/list"
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"查询个性化设置列表失败: {e}")
            raise

    def get_personalized_settings(self, settings_id: int) -> Dict[str, Any]:
        """查询个性化设置详细"""
        # 模拟数据
        if self.base_url == "mock":
            for item in self.mock_personalized_settings_data:
                if item["id"] == settings_id:
                    return item
            raise Exception(f"未找到ID为{settings_id}的个性化设置")

        # 真实API
        url = f"{self.base_url}/api/v1/dataDictionary/personalizedSettings/{settings_id}"
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"查询个性化设置详情失败: {e}")
            raise

    def create_personalized_settings(self, data):
        """新增个性化设置"""
        # 模拟数据
        if self.base_url == "mock":
            new_id = max([item["id"] for item in self.mock_personalized_settings_data]) + 1 if self.mock_personalized_settings_data else 1
            new_settings = {
                "id": new_id,
                "name": data["name"],
                "code": data["code"],
                "type": data["type"],
                "group": data["group"],
                "value": data["value"],
                "description": data.get("description"),
                "status": 1  # 默认启用状态
            }
            self.mock_personalized_settings_data.append(new_settings)
            return new_settings

        # 真实API
        url = f"{self.base_url}/api/v1/dataDictionary/personalizedSettings"
        try:
            response = self.session.post(url, json=data, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"新增个性化设置失败: {e}")
            raise

    def update_personalized_settings(self, data):
        """修改个性化设置"""
        # 模拟数据
        if self.base_url == "mock":
            for item in self.mock_personalized_settings_data:
                if item["id"] == data["id"]:
                    # 更新字段
                    for key, value in data.items():
                        if key != "id" and value is not None:
                            item[key] = value
                    return item
            raise Exception(f"未找到ID为{data['id']}的个性化设置")

        # 真实API
        url = f"{self.base_url}/api/v1/dataDictionary/personalizedSettings"
        try:
            response = self.session.put(url, json=data, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"修改个性化设置失败: {e}")
            raise

    def delete_personalized_settings(self, settings_id):
        """删除个性化设置"""
        # 模拟数据
        if self.base_url == "mock":
            for i, item in enumerate(self.mock_personalized_settings_data):
                if item["id"] == settings_id:
                    del self.mock_personalized_settings_data[i]
                    return {"message": "删除成功"}
            raise Exception(f"未找到ID为{settings_id}的个性化设置")

        # 真实API
        url = f"{self.base_url}/api/v1/dataDictionary/personalizedSettings/{settings_id}"
        try:
            response = self.session.delete(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"删除个性化设置失败: {e}")
            raise

    def batch_delete_personalized_settings(self, ids: List[int]):
        """批量删除个性化设置"""
        # 模拟数据
        if self.base_url == "mock":
            original_length = len(self.mock_personalized_settings_data)
            self.mock_personalized_settings_data = [item for item in self.mock_personalized_settings_data if item["id"] not in ids]
            deleted_count = original_length - len(self.mock_personalized_settings_data)
            return {"message": f"成功删除{deleted_count}条记录"}

        # 真实API
        url = f"{self.base_url}/api/v1/dataDictionary/personalizedSettings/batch"
        try:
            response = self.session.delete(url, json=ids, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"批量删除个性化设置失败: {e}")
            raise

    def export_personalized_settings(self, params=None):
        """导出个性化设置"""
        # 模拟数据
        if self.base_url == "mock":
            return {
                "message": "导出成功",
                "data": self.mock_personalized_settings_data
            }

        # 真实API
        url = f"{self.base_url}/api/v1/dataDictionary/personalizedSettings/export"
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"导出个性化设置失败: {e}")
            raise

    def get_setting_type_list(self):
        """获取设置类型列表"""
        # 模拟数据
        if self.base_url == "mock":
            types = list(set([item["type"] for item in self.mock_personalized_settings_data if item["type"]]))
            return {"list": [{"name": t} for t in types]}

        # 真实API
        url = f"{self.base_url}/api/v1/dataDictionary/personalizedSettings/types"
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"获取设置类型列表失败: {e}")
            raise

    def get_config_group_list(self):
        """获取配置分组列表"""
        # 模拟数据
        if self.base_url == "mock":
            groups = list(set([item["group"] for item in self.mock_personalized_settings_data if item["group"]]))
            return {"list": [{"name": g} for g in groups]}

        # 真实API
        url = f"{self.base_url}/api/v1/dataDictionary/personalizedSettings/groups"
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"获取配置分组列表失败: {e}")
            raise

    def get_config_group_list(self):
        """获取配置分组列表"""
        # 模拟数据
        if self.base_url == "mock":
            groups = list(set([item["group"] for item in self.mock_personalized_settings_data if item["group"]]))
            return {"list": [{"name": g} for g in groups]}

        # 真实API
        url = f"{self.base_url}/api/v1/dataDictionary/personalizedSettings/groups"
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"获取配置分组列表失败: {e}")
            raise

    # 历史记录相关方法
    # 操作日志相关方法
    def get_operation_log_list(self, params=None):
        """分页查询操作日志"""
        # 模拟数据
        if self.base_url == "mock":
            page = params.get("page", 1) if params else 1
            size = params.get("size", 10) if params else 10
            start = (page - 1) * size
            end = start + size
            paginated_data = self.mock_operation_log_data[start:end]

            return {
                "list": paginated_data,
                "total": len(self.mock_operation_log_data)
            }

        # 真实API
        url = f"{self.base_url}/api/v1/historyrecord/operationLog"
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"分页查询操作日志失败: {e}")
            raise

    def export_operation_log(self, params=None):
        """导出操作日志数据"""
        # 模拟数据
        if self.base_url == "mock":
            return {
                "message": "导出成功",
                "data": self.mock_operation_log_data
            }

        # 真实API
        url = f"{self.base_url}/api/v1/historyrecord/exportOperationLog"
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"导出操作日志数据失败: {e}")
            raise

    def get_operation_log_detail(self, log_id: int) -> Dict[str, Any]:
        """获取操作日志详情"""
        # 模拟数据
        if self.base_url == "mock":
            for item in self.mock_operation_log_data:
                if item["id"] == log_id:
                    return item
            raise Exception(f"未找到ID为{log_id}的操作日志")

        # 真实API
        url = f"{self.base_url}/api/v1/historyrecord/operationLog/{log_id}"
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"获取操作日志详情失败: {e}")
            raise

    def get_operation_log_stats(self, params=None):
        """查询操作日志统计信息"""
        # 模拟数据
        if self.base_url == "mock":
            total_logs = len(self.mock_operation_log_data)
            success_count = len([item for item in self.mock_operation_log_data if item["status"] == 1])
            failure_count = total_logs - success_count
            
            return {
                "totalLogs": total_logs,
                "successCount": success_count,
                "failureCount": failure_count
            }

        # 真实API
        url = f"{self.base_url}/api/v1/historyrecord/operationLog/stats"
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"查询操作日志统计信息失败: {e}")
            raise

    def delete_operation_logs(self, ids: List[int]):
        """批量删除操作日志"""
        # 模拟数据
        if self.base_url == "mock":
            original_length = len(self.mock_operation_log_data)
            self.mock_operation_log_data = [item for item in self.mock_operation_log_data if item["id"] not in ids]
            deleted_count = original_length - len(self.mock_operation_log_data)
            return {"message": f"成功删除{deleted_count}条记录"}

        # 真实API
        url = f"{self.base_url}/api/v1/historyrecord/operationLog"
        try:
            response = self.session.delete(url, json=ids, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"批量删除操作日志失败: {e}")
            raise

    def clean_expired_logs(self, days: int):
        """清理过期操作日志"""
        # 模拟数据
        if self.base_url == "mock":
            # 在模拟环境中，我们只是返回一个成功消息
            return {"message": f"成功清理{days}天前的日志"}

        # 真实API
        url = f"{self.base_url}/api/v1/historyrecord/operationLog/clean"
        try:
            response = self.session.post(url, params={"days": days}, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"清理过期操作日志失败: {e}")
            raise

    # 公共暂存记录相关方法
    def get_public_storage_list(self, params=None):
        """分页查询公共暂存记录"""
        # 模拟数据
        if self.base_url == "mock":
            page = params.get("page", 1) if params else 1
            size = params.get("size", 10) if params else 10
            start = (page - 1) * size
            end = start + size
            paginated_data = self.mock_public_storage_data[start:end]

            return {
                "list": paginated_data,
                "total": len(self.mock_public_storage_data)
            }

        # 真实API
        url = f"{self.base_url}/api/v1/historyrecord/publicStorage"
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"分页查询公共暂存记录失败: {e}")
            raise

    def export_public_storage(self, params=None):
        """导出公共暂存记录"""
        # 模拟数据
        if self.base_url == "mock":
            return {
                "message": "导出成功",
                "data": self.mock_public_storage_data
            }

        # 真实API
        url = f"{self.base_url}/api/v1/historyrecord/exportPublicStorage"
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"导出公共暂存记录失败: {e}")
            raise

    def get_public_storage_detail(self, record_id: int) -> Dict[str, Any]:
        """获取公共暂存记录详情"""
        # 模拟数据
        if self.base_url == "mock":
            for item in self.mock_public_storage_data:
                if item["id"] == record_id:
                    return item
            raise Exception(f"未找到ID为{record_id}的公共暂存记录")

        # 真实API
        url = f"{self.base_url}/api/v1/historyrecord/publicStorage/{record_id}"
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"获取公共暂存记录详情失败: {e}")
            raise

    def get_public_storage_stats(self, params=None):
        """查询公共暂存记录统计信息"""
        # 模拟数据
        if self.base_url == "mock":
            total_records = len(self.mock_public_storage_data)
            processed_count = len([item for item in self.mock_public_storage_data if item["status"] == 1])
            pending_count = total_records - processed_count
            
            return {
                "totalRecords": total_records,
                "processedCount": processed_count,
                "pendingCount": pending_count
            }

        # 真实API
        url = f"{self.base_url}/api/v1/historyrecord/publicStorage/stats"
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"查询公共暂存记录统计信息失败: {e}")
            raise

    def delete_public_storage_records(self, ids: List[int]):
        """批量删除公共暂存记录"""
        # 模拟数据
        if self.base_url == "mock":
            original_length = len(self.mock_public_storage_data)
            self.mock_public_storage_data = [item for item in self.mock_public_storage_data if item["id"] not in ids]
            deleted_count = original_length - len(self.mock_public_storage_data)
            return {"message": f"成功删除{deleted_count}条记录"}

        # 真实API
        url = f"{self.base_url}/api/v1/historyrecord/publicStorage"
        try:
            response = self.session.delete(url, json=ids, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"批量删除公共暂存记录失败: {e}")
            raise

    def create_public_storage_record(self, data):
        """创建公共暂存记录"""
        # 模拟数据
        if self.base_url == "mock":
            new_id = max([item["id"] for item in self.mock_public_storage_data]) + 1 if self.mock_public_storage_data else 1
            new_record = {
                "id": new_id,
                "storageCode": data["storageCode"],
                "cutterCode": data["cutterCode"],
                "cutterType": data["cutterType"],
                "brandName": data["brandName"],
                "specification": data["specification"],
                "quantity": data["quantity"],
                "storageTime": data["storageTime"],
                "operator": data["operator"],
                "status": 0  # 默认状态
            }
            self.mock_public_storage_data.append(new_record)
            return new_record

        # 真实API
        url = f"{self.base_url}/api/v1/historyrecord/publicStorage"
        try:
            response = self.session.post(url, json=data, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"创建公共暂存记录失败: {e}")
            raise

    def update_public_storage_record(self, data):
        """更新公共暂存记录"""
        # 模拟数据
        if self.base_url == "mock":
            for item in self.mock_public_storage_data:
                if item["id"] == data["id"]:
                    # 更新字段
                    for key, value in data.items():
                        if key != "id" and value is not None:
                            item[key] = value
                    return item
            raise Exception(f"未找到ID为{data['id']}的公共暂存记录")

        # 真实API
        url = f"{self.base_url}/api/v1/historyrecord/publicStorage"
        try:
            response = self.session.put(url, json=data, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"更新公共暂存记录失败: {e}")
            raise

    def batch_process_public_storage(self, data):
        """批量处理公共暂存记录"""
        # 模拟数据
        if self.base_url == "mock":
            # 在模拟环境中，我们只是返回一个成功消息
            return {"message": "批量处理成功"}

        # 真实API
        url = f"{self.base_url}/api/v1/historyrecord/publicStorage/batch"
        try:
            response = self.session.post(url, json=data, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"批量处理公共暂存记录失败: {e}")
            raise

    # 补货记录相关方法
    def get_restock_record_list(self, params=None):
        """分页查询补货记录"""
        # 模拟数据
        if self.base_url == "mock":
            page = params.get("page", 1) if params else 1
            size = params.get("size", 10) if params else 10
            start = (page - 1) * size
            end = start + size
            paginated_data = self.mock_restock_data[start:end]

            return {
                "list": paginated_data,
                "total": len(self.mock_restock_data)
            }

        # 真实API
        url = f"{self.base_url}/api/v1/historyrecord/restockRecord"
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"分页查询补货记录失败: {e}")
            raise

    def export_restock_record(self, params=None):
        """导出补货记录"""
        # 模拟数据
        if self.base_url == "mock":
            return {
                "message": "导出成功",
                "data": self.mock_restock_data
            }

        # 真实API
        url = f"{self.base_url}/api/v1/historyrecord/exportRestockRecord"
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"导出补货记录失败: {e}")
            raise

    def get_restock_record_detail(self, record_id: int) -> Dict[str, Any]:
        """获取补货记录详情"""
        # 模拟数据
        if self.base_url == "mock":
            for item in self.mock_restock_data:
                if item["id"] == record_id:
                    return item
            raise Exception(f"未找到ID为{record_id}的补货记录")

        # 真实API
        url = f"{self.base_url}/api/v1/historyrecord/restockRecord/{record_id}"
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"获取补货记录详情失败: {e}")
            raise

    def get_restock_record_stats(self, params=None):
        """查询补货记录统计信息"""
        # 模拟数据
        if self.base_url == "mock":
            total_records = len(self.mock_restock_data)
            completed_count = len([item for item in self.mock_restock_data if item["status"] == 1])
            pending_count = total_records - completed_count
            
            return {
                "totalRecords": total_records,
                "completedCount": completed_count,
                "pendingCount": pending_count
            }

        # 真实API
        url = f"{self.base_url}/api/v1/historyrecord/restockRecord/stats"
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"查询补货记录统计信息失败: {e}")
            raise

    def delete_restock_records(self, ids: List[int]):
        """批量删除补货记录"""
        # 模拟数据
        if self.base_url == "mock":
            original_length = len(self.mock_restock_data)
            self.mock_restock_data = [item for item in self.mock_restock_data if item["id"] not in ids]
            deleted_count = original_length - len(self.mock_restock_data)
            return {"message": f"成功删除{deleted_count}条记录"}

        # 真实API
        url = f"{self.base_url}/api/v1/historyrecord/restockRecord"
        try:
            response = self.session.delete(url, json=ids, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"批量删除补货记录失败: {e}")
            raise

    def create_restock_record(self, data):
        """创建补货记录"""
        # 模拟数据
        if self.base_url == "mock":
            new_id = max([item["id"] for item in self.mock_restock_data]) + 1 if self.mock_restock_data else 1
            new_record = {
                "id": new_id,
                "restockCode": data["restockCode"],
                "cutterCode": data["cutterCode"],
                "cutterType": data["cutterType"],
                "brandName": data["brandName"],
                "specification": data["specification"],
                "quantity": data["quantity"],
                "restockTime": data["restockTime"],
                "operator": data["operator"],
                "status": 1  # 默认已完成状态
            }
            self.mock_restock_data.append(new_record)
            return new_record

        # 真实API
        url = f"{self.base_url}/api/v1/historyrecord/restockRecord"
        try:
            response = self.session.post(url, json=data, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"创建补货记录失败: {e}")
            raise

    def update_restock_record(self, data):
        """更新补货记录"""
        # 模拟数据
        if self.base_url == "mock":
            for item in self.mock_restock_data:
                if item["id"] == data["id"]:
                    # 更新字段
                    for key, value in data.items():
                        if key != "id" and value is not None:
                            item[key] = value
                    return item
            raise Exception(f"未找到ID为{data['id']}的补货记录")

        # 真实API
        url = f"{self.base_url}/api/v1/historyrecord/restockRecord"
        try:
            response = self.session.put(url, json=data, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"更新补货记录失败: {e}")
            raise

    # 出入库记录相关方法
    def get_stock_record_list(self, params=None):
        """分页查询出入库记录"""
        # 模拟数据
        if self.base_url == "mock":
            page = params.get("page", 1) if params else 1
            size = params.get("size", 10) if params else 10
            start = (page - 1) * size
            end = start + size
            paginated_data = self.mock_stock_record_data[start:end]

            return {
                "list": paginated_data,
                "total": len(self.mock_stock_record_data)
            }

        # 真实API
        url = f"{self.base_url}/api/v1/historyrecord/stockRecord"
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"分页查询出入库记录失败: {e}")
            raise

    def export_stock_record(self, params=None):
        """导出出入库记录"""
        # 模拟数据
        if self.base_url == "mock":
            return {
                "message": "导出成功",
                "data": self.mock_stock_record_data
            }

        # 真实API
        url = f"{self.base_url}/api/v1/historyrecord/exportStockRecord"
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"导出出入库记录失败: {e}")
            raise

    def get_stock_record_detail(self, record_id: int) -> Dict[str, Any]:
        """获取出入库记录详情"""
        # 模拟数据
        if self.base_url == "mock":
            for item in self.mock_stock_record_data:
                if item["id"] == record_id:
                    return item
            raise Exception(f"未找到ID为{record_id}的出入库记录")

        # 真实API
        url = f"{self.base_url}/api/v1/historyrecord/stockRecord/{record_id}"
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"获取出入库记录详情失败: {e}")
            raise

    def get_stock_record_stats(self, params=None):
        """查询出入库记录统计信息"""
        # 模拟数据
        if self.base_url == "mock":
            total_records = len(self.mock_stock_record_data)
            inbound_count = len([item for item in self.mock_stock_record_data if item["recordType"] == "入库"])
            outbound_count = len([item for item in self.mock_stock_record_data if item["recordType"] == "出库"])
            
            return {
                "totalRecords": total_records,
                "inboundCount": inbound_count,
                "outboundCount": outbound_count
            }

        # 真实API
        url = f"{self.base_url}/api/v1/historyrecord/stockRecord/stats"
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"查询出入库记录统计信息失败: {e}")
            raise

    def delete_stock_records(self, ids: List[int]):
        """批量删除出入库记录"""
        # 模拟数据
        if self.base_url == "mock":
            original_length = len(self.mock_stock_record_data)
            self.mock_stock_record_data = [item for item in self.mock_stock_record_data if item["id"] not in ids]
            deleted_count = original_length - len(self.mock_stock_record_data)
            return {"message": f"成功删除{deleted_count}条记录"}

        # 真实API
        url = f"{self.base_url}/api/v1/historyrecord/stockRecord"
        try:
            response = self.session.delete(url, json=ids, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"批量删除出入库记录失败: {e}")
            raise

# 初始化API客户端（这里使用示例API，实际使用时请替换为你的真实API地址）
original_api_client = OriginalAPIClient(
    #模拟数据
    base_url="mock",
    api_key=None


    # #真实api
    # base_url="https://jsonplaceholder.typicode.com",
    # api_key=None  # 如果有API密钥，请在此处填写
)