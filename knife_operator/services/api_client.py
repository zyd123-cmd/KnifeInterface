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
        
        # 添加模拟刀柄借出记录数据
        self.mock_handle_lend_records = [
            {
                "id": 1,
                "handleCode": "HC2023001",
                "handleName": "刀柄A",
                "borrowerName": "张三",
                "borrowerCode": "zhangsan",
                "brand": "品牌A",
                "model": "型号X",
                "quantity": 5,
                "lendDate": "2023-01-01",
                "expectedReturnDate": "2023-01-10",
                "actualReturnDate": None,
                "status": "借用中",
                "purpose": "生产使用"
            },
            {
                "id": 2,
                "handleCode": "HC2023002",
                "handleName": "刀柄B",
                "borrowerName": "李四",
                "borrowerCode": "lisi",
                "brand": "品牌B",
                "model": "型号Y",
                "quantity": 3,
                "lendDate": "2023-01-02",
                "expectedReturnDate": "2023-01-12",
                "actualReturnDate": "2023-01-05",
                "status": "已归还",
                "purpose": "维修使用"
            }
        ]
        
        # 添加模拟刀头暂存记录数据
        self.mock_temp_store_records = [
            {
                "id": 1,
                "tempStoreCode": "TS2023001",
                "storePerson": "张三",
                "storePersonCode": "zhangsan",
                "storeType": "刀头暂存",
                "brandName": "BC001",
                "cutterType": "CC001",
                "specification": "Φ10",
                "storeTime": datetime.now().isoformat(),
                "status": "暂存中"
            },
            {
                "id": 2,
                "tempStoreCode": "TS2023002",
                "storePerson": "李四",
                "storePersonCode": "lisi",
                "storeType": "刀头暂存",
                "brandName": "BC002",
                "cutterType": "CC002",
                "specification": "Φ12",
                "storeTime": datetime.now().isoformat(),
                "status": "暂存中"
            }
        ]
        
        # 添加模拟刀柄暂存记录数据
        self.mock_handle_temp_store_records = [
            {
                "id": 1,
                "storageCode": "HTS2023001",
                "borrowerName": "张三",
                "storageUser": "zhangsan",
                "brandName": "品牌A",
                "handleSpec": "BT40-型号X",
                "storageType": "1",  # 个人暂存
                "quantity": 3,
                "storageTime": datetime.now().isoformat(),
                "status": "暂存中",
                "purpose": "临时不用"
            },
            {
                "id": 2,
                "storageCode": "HTS2023002",
                "borrowerName": "李四",
                "storageUser": "lisi",
                "brandName": "品牌B",
                "handleSpec": "BT50-型号Y",
                "storageType": "0",  # 公共暂存
                "quantity": 2,
                "storageTime": datetime.now().isoformat(),
                "status": "暂存中",
                "purpose": "公共区域暂存"
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

    def create_lend_record(self, lend_record_data: Dict) -> Dict[str, Any]:
        """
        创建新的借出记录
        """
        # 如果是模拟模式，使用模拟数据
        if self.base_url == "mock":
            # 生成新的ID
            new_id = max([r["id"] for r in self.mock_lend_records]) + 1 if self.mock_lend_records else 1
            
            # 处理时间格式
            lend_time = lend_record_data.get("borrowDate") or datetime.now().isoformat()
            
            # 创建新的借出记录 (映射前端字段到后端字段)
            new_record = {
                "id": new_id,
                "lendCode": lend_record_data.get("borrowCode"),
                "lendUser": lend_record_data.get("borrowerCode"),
                "lendUserName": lend_record_data.get("borrowerName"),
                "brandCode": lend_record_data.get("brandName"),
                "cutterCode": lend_record_data.get("cutterType"),
                "specification": f"{lend_record_data.get('brandName', '')} {lend_record_data.get('cutterType', '')}",
                "lendTime": lend_time,
                "returnTime": None,
                "status": lend_record_data.get("borrowStatus", "borrowed")
            }
            
            # 添加到模拟数据中
            self.mock_lend_records.append(new_record)
            
            return {
                "success": True,
                "data": new_record
            }
        
        # 真实API调用
        url = f"{self.base_url}/lend-records"
        try:
            # 映射前端字段到后端字段
            mapped_data = {
                "lendCode": lend_record_data.get("borrowCode"),
                "lendUser": lend_record_data.get("borrowerCode"),
                "lendUserName": lend_record_data.get("borrowerName"),
                "brandCode": lend_record_data.get("brandName"),
                "cutterCode": lend_record_data.get("cutterType"),
                "quantity": lend_record_data.get("quantity"),
                "expectedReturnTime": lend_record_data.get("expectedReturnDate"),
                "purpose": lend_record_data.get("borrowPurpose"),
                "lendTime": lend_record_data.get("borrowDate"),
                "status": lend_record_data.get("borrowStatus", "borrowed")
            }
            response = self.session.post(url, json=mapped_data, timeout=10)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f"创建借出记录失败: {e}")
            raise

    def process_batch_return(self, request_data: Dict) -> Dict[str, Any]:
        """
        处理批量归还请求
        """
        # 如果是模拟模式，使用模拟数据
        if self.base_url == "mock":
            success_count = 0
            failed_items = []
            
            # 模拟处理每条归还记录
            for return_item in request_data.get("returnList", []):
                try:
                    # 查找借出记录
                    borrow_record = None
                    for record in self.mock_lend_records:
                        if record["id"] == return_item["borrowId"]:
                            borrow_record = record
                            break
                    
                    if not borrow_record:
                        failed_items.append({
                            "borrowId": return_item["borrowId"],
                            "reason": "借出记录不存在"
                        })
                        continue
                        
                    # 验证操作权限（只能本人归还）
                    if borrow_record["lendUser"] != request_data.get("operateUser"):
                        failed_items.append({
                            "borrowId": return_item["borrowId"],
                            "reason": "只能归还本人借出的工具"
                        })
                        continue
                        
                    # 验证借出状态
                    if borrow_record["status"] not in ['借用中', ' overdue']:
                        failed_items.append({
                            "borrowId": return_item["borrowId"],
                            "reason": "当前状态不允许归还"
                        })
                        continue
                    
                    # 更新借出记录状态
                    borrow_record["status"] = '已归还'
                    borrow_record["returnTime"] = datetime.now().isoformat()
                    
                    success_count += 1
                    
                except Exception as e:
                    failed_items.append({
                        "borrowId": return_item["borrowId"],
                        "reason": str(e)
                    })
            
            # 返回结果
            return {
                "code": 200,
                "msg": f"批量归还完成，成功 {success_count} 条，失败 {len(failed_items)} 条",
                "data": {
                    "successCount": success_count,
                    "failedItems": failed_items
                }
            }
        
        # 真实API调用
        url = f"{self.base_url}/batch-return"
        try:
            response = self.session.post(url, json=request_data, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"批量归还处理失败: {e}")
            return {
                "code": 500,
                "msg": f"批量归还处理失败: {str(e)}",
                "data": None
            }

    def process_temp_store_batch_return(self, request_data: Dict) -> Dict[str, Any]:
        """
        处理暂存刀头批量归还请求
        """
        # 如果是模拟模式，使用模拟数据
        if self.base_url == "mock":
            success_count = 0
            failed_items = []
            
            # 模拟处理每条归还记录
            for return_item in request_data.get("returnList", []):
                try:
                    # 查找借出记录
                    borrow_record = None
                    for record in self.mock_lend_records:
                        if record["id"] == return_item["borrowId"]:
                            borrow_record = record
                            break
                    
                    if not borrow_record:
                        failed_items.append({
                            "borrowId": return_item["borrowId"],
                            "reason": "借出记录不存在"
                        })
                        continue
                        
                    # 验证操作权限（只能本人归还）
                    if borrow_record["lendUser"] != request_data.get("operateUser"):
                        failed_items.append({
                            "borrowId": return_item["borrowId"],
                            "reason": "只能归还本人暂存的刀头"
                        })
                        continue
                        
                    # 验证借出状态（只能对暂存状态的记录进行归还）
                    if borrow_record["status"] not in ['temp_stored']:
                        failed_items.append({
                            "borrowId": return_item["borrowId"],
                            "reason": "当前状态不允许归还，只有暂存状态的刀头可以归还"
                        })
                        continue
                    
                    # 更新借出记录状态为已归还
                    borrow_record["status"] = '已归还'
                    borrow_record["returnTime"] = datetime.now().isoformat()
                    # 清除暂存相关信息
                    if "tempStoreTime" in borrow_record:
                        del borrow_record["tempStoreTime"]
                    if "tempStoreRemarks" in borrow_record:
                        del borrow_record["tempStoreRemarks"]
                    
                    success_count += 1
                    
                except Exception as e:
                    failed_items.append({
                        "borrowId": return_item["borrowId"],
                        "reason": str(e)
                    })
            
            # 返回结果
            return {
                "code": 200,
                "msg": f"暂存刀头批量归还完成，成功 {success_count} 条，失败 {len(failed_items)} 条",
                "data": {
                    "successCount": success_count,
                    "failedItems": failed_items
                }
            }
        
        # 真实API调用
        url = f"{self.base_url}/temp-store-batch-return"
        try:
            response = self.session.post(url, json=request_data, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"暂存刀头批量归还处理失败: {e}")
            return {
                "code": 500,
                "msg": f"暂存刀头批量归还处理失败: {str(e)}",
                "data": None
            }

    def update_borrow_record_service(self, borrow_id: int, request_data: Dict, current_user: Dict) -> Dict[str, Any]:
        """
        更新借出记录服务 (编辑按钮接口)
        """
        # 如果是模拟模式，使用模拟数据
        if self.base_url == "mock":
            # 查找借出记录
            borrow_record = None
            for record in self.mock_lend_records:
                if record["id"] == borrow_id:
                    borrow_record = record
                    break
            
            if not borrow_record:
                return {
                    "code": 404,
                    "msg": "借出记录不存在",
                    "data": None
                }
                
            # 验证权限（只能本人编辑）
            if borrow_record["lendUser"] != current_user.get("employeeCode"):
                return {
                    "code": 403,
                    "msg": "只能编辑本人的借出记录",
                    "data": None
                }
            
            # 更新记录，保持状态不变
            borrow_record.update({
                "lendCode": request_data.get("borrowCode"),
                "lendUser": request_data.get("borrowerCode"),
                "lendUserName": request_data.get("borrowerName"),
                "brandCode": request_data.get("brandName"),
                "cutterCode": request_data.get("cutterType"),
                "specification": f"{request_data.get('brandName', '')} {request_data.get('cutterType', '')}",
                "quantity": request_data.get("quantity"),
                "expectedReturnTime": request_data.get("expectedReturnDate"),
                "purpose": request_data.get("borrowPurpose")
                # 保持原有状态不变
            })
            
            return {
                "code": 200,
                "msg": "更新成功",
                "data": None
            }
        
        # 真实API调用
        url = f"{self.base_url}/lend-records/{borrow_id}"
        try:
            # 映射前端字段到后端字段
            mapped_data = {
                "lendCode": request_data.get("borrowCode"),
                "lendUser": request_data.get("borrowerCode"),
                "lendUserName": request_data.get("borrowerName"),
                "brandCode": request_data.get("brandName"),
                "cutterCode": request_data.get("cutterType"),
                "quantity": request_data.get("quantity"),
                "expectedReturnTime": request_data.get("expectedReturnDate"),
                "purpose": request_data.get("borrowPurpose")
            }
            response = self.session.put(url, json=mapped_data, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"更新借出记录失败: {e}")
            return {
                "code": 500,
                "msg": f"更新借出记录失败: {str(e)}",
                "data": None
            }

    def process_return_service(self, request_data: Dict, current_user: Dict) -> Dict[str, Any]:
        """
        处理刀头归还服务 (归还按钮接口)
        """
        # 如果是模拟模式，使用模拟数据
        if self.base_url == "mock":
            borrow_id = request_data.get("borrowId")
            
            # 查找借出记录
            borrow_record = None
            for record in self.mock_lend_records:
                if record["id"] == borrow_id:
                    borrow_record = record
                    break
            
            if not borrow_record:
                return {
                    "code": 404,
                    "msg": "借出记录不存在",
                    "data": None
                }
                
            # 验证权限（只能本人归还）
            if borrow_record["lendUser"] != current_user.get("employeeCode"):
                return {
                    "code": 403,
                    "msg": "只能归还本人借出的工具",
                    "data": None
                }
                
            # 验证借出状态
            if borrow_record["status"] not in ['借用中', 'overdue']:
                return {
                    "code": 400,
                    "msg": "当前状态不允许归还",
                    "data": None
                }
            
            # 更新借出记录状态
            borrow_record["status"] = '已归还'
            borrow_record["returnTime"] = datetime.now().isoformat()
            
            return {
                "code": 200,
                "msg": "归还成功",
                "data": None
            }
        
        # 真实API调用
        url = f"{self.base_url}/return"
        try:
            response = self.session.post(url, json=request_data, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"处理刀头归还失败: {e}")
            return {
                "code": 500,
                "msg": f"处理刀头归还失败: {str(e)}",
                "data": None
            }

    def process_temp_store_service(self, request_data: Dict, current_user: Dict) -> Dict[str, Any]:
        """
        处理刀头暂存服务 (暂存按钮接口)
        """
        # 如果是模拟模式，使用模拟数据
        if self.base_url == "mock":
            borrow_id = request_data.get("borrowId")
            
            # 查找借出记录
            borrow_record = None
            for record in self.mock_lend_records:
                if record["id"] == borrow_id:
                    borrow_record = record
                    break
            
            if not borrow_record:
                return {
                    "code": 404,
                    "msg": "借出记录不存在",
                    "data": None
                }
                
            # 验证权限（只能本人操作）
            if borrow_record["lendUser"] != current_user.get("employeeCode"):
                return {
                    "code": 403,
                    "msg": "只能操作本人的借出记录",
                    "data": None
                }
            
            # 验证借出状态（只能对借用中或逾期的记录进行暂存）
            if borrow_record["status"] not in ['借用中', 'overdue']:
                return {
                    "code": 400,
                    "msg": "当前状态不允许暂存",
                    "data": None
                }
            
            # 更新借出记录状态为暂存
            borrow_record["status"] = 'temp_stored'  # 修改状态为temp_stored而不是"暂存中"
            
            # 添加暂存时间和备注
            borrow_record["tempStoreTime"] = request_data.get("operateTime")
            borrow_record["tempStoreRemarks"] = request_data.get("borrowRemarks")
            
            return {
                "code": 200,
                "msg": "暂存成功",
                "data": None
            }
        
        # 真实API调用
        url = f"{self.base_url}/temp-store"
        try:
            response = self.session.post(url, json=request_data, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"处理刀头暂存失败: {e}")
            return {
                "code": 500,
                "msg": f"处理刀头暂存失败: {str(e)}",
                "data": None
            }

    def get_borrow_detail_service(self, borrow_id: int) -> Dict[str, Any]:
        """
        获取借出记录详情服务 (详情按钮接口)
        """
        # 如果是模拟模式，使用模拟数据
        if self.base_url == "mock":
            # 查找借出记录
            borrow_record = None
            for record in self.mock_lend_records:
                if record["id"] == borrow_id:
                    borrow_record = record
                    break
            
            if not borrow_record:
                return {
                    "code": 404,
                    "msg": "借出记录不存在",
                    "data": None
                }
            
            # 构造详情数据
            detail_data = {
                "id": borrow_record["id"],
                "borrowCode": borrow_record["lendCode"],
                "borrowerName": borrow_record["lendUserName"],
                "borrowerCode": borrow_record["lendUser"],
                "brandName": borrow_record["brandCode"],
                "cutterType": borrow_record["cutterCode"],
                "quantity": borrow_record.get("quantity", 1),
                "borrowDate": borrow_record["lendTime"].split("T")[0],  # 只取日期部分
                "expectedReturnDate": borrow_record.get("expectedReturnTime", ""),
                "actualReturnDate": borrow_record["returnTime"].split("T")[0] if borrow_record["returnTime"] else None,
                "borrowStatus": borrow_record["status"],
                "borrowPurpose": borrow_record.get("purpose", "")
            }
            
            return {
                "code": 200,
                "msg": "获取成功",
                "data": detail_data
            }
        
        # 真实API调用
        url = f"{self.base_url}/lend-records/{borrow_id}"
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            return {
                "code": 200,
                "msg": "获取成功",
                "data": data
            }
        except requests.exceptions.RequestException as e:
            logger.error(f"获取借出记录详情失败: {e}")
            return {
                "code": 500,
                "msg": f"获取借出记录详情失败: {str(e)}",
                "data": None
            }

    # 刀柄相关方法
    def get_handle_lend_records(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        获取刀柄借出记录列表
        """
        # 如果是模拟模式，使用模拟数据
        if self.base_url == "mock":
            # 获取分页参数
            page = params.get("page", 1) if params else 1
            size = params.get("size", 10) if params else 10
            
            # 筛选数据
            filtered_records = self.mock_handle_lend_records.copy()
            
            # 根据查询参数过滤数据
            if params:
                if params.get("handleCode"):
                    filtered_records = [r for r in filtered_records if params["handleCode"] in r["handleCode"]]
                if params.get("borrowerName"):
                    filtered_records = [r for r in filtered_records if params["borrowerName"] in r["borrowerName"]]
                if params.get("brand"):
                    filtered_records = [r for r in filtered_records if params["brand"] in r["brand"]]
                if params.get("model"):
                    filtered_records = [r for r in filtered_records if params["model"] in r["model"]]
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
        url = f"{self.base_url}/handle-lend-records"
        try:
            response = self.session.get(url, params=params or {}, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"获取刀柄借出记录列表失败: {e}")
            raise

    def create_handle_lend_record(self, handle_record_data: Dict) -> Dict[str, Any]:
        """
        创建新的刀柄借出记录
        """
        # 如果是模拟模式，使用模拟数据
        if self.base_url == "mock":
            # 生成新的ID
            new_id = max([r["id"] for r in self.mock_handle_lend_records]) + 1 if self.mock_handle_lend_records else 1
            
            # 创建新的刀柄借出记录
            new_record = {
                "id": new_id,
                "handleCode": handle_record_data.get("handleCode"),
                "handleName": handle_record_data.get("handleName"),
                "borrowerName": handle_record_data.get("borrowerName"),
                "borrowerCode": handle_record_data.get("borrowerCode"),
                "brand": handle_record_data.get("brand"),
                "model": handle_record_data.get("model"),
                "quantity": handle_record_data.get("quantity"),
                "lendDate": handle_record_data.get("lendDate"),
                "expectedReturnDate": handle_record_data.get("expectedReturnDate"),
                "actualReturnDate": None,
                "status": handle_record_data.get("status", "borrowed"),
                "purpose": handle_record_data.get("purpose")
            }
            
            # 添加到模拟数据中
            self.mock_handle_lend_records.append(new_record)
            
            return {
                "success": True,
                "data": new_record
            }
        
        # 真实API调用
        url = f"{self.base_url}/handle-lend-records"
        try:
            response = self.session.post(url, json=handle_record_data, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"创建刀柄借出记录失败: {e}")
            raise

    def update_handle_lend_record(self, handle_id: int, handle_record_data: Dict, current_user: Dict) -> Dict[str, Any]:
        """
        更新刀柄借出记录
        """
        # 如果是模拟模式，使用模拟数据
        if self.base_url == "mock":
            # 查找刀柄借出记录
            handle_record = None
            for record in self.mock_handle_lend_records:
                if record["id"] == handle_id:
                    handle_record = record
                    break
            
            if not handle_record:
                return {
                    "code": 404,
                    "msg": "刀柄借出记录不存在",
                    "data": None
                }
                
            # 验证权限（只能本人编辑）
            if handle_record["borrowerCode"] != current_user.get("employeeCode"):
                return {
                    "code": 403,
                    "msg": "只能编辑本人的刀柄借出记录",
                    "data": None
                }
            
            # 更新记录
            handle_record.update({
                "handleCode": handle_record_data.get("handleCode"),
                "handleName": handle_record_data.get("handleName"),
                "borrowerName": handle_record_data.get("borrowerName"),
                "borrowerCode": handle_record_data.get("borrowerCode"),
                "brand": handle_record_data.get("brand"),
                "model": handle_record_data.get("model"),
                "quantity": handle_record_data.get("quantity"),
                "lendDate": handle_record_data.get("lendDate"),
                "expectedReturnDate": handle_record_data.get("expectedReturnDate"),
                "status": handle_record["status"],  # 保持原有状态
                "purpose": handle_record_data.get("purpose")
            })
            
            return {
                "code": 200,
                "msg": "更新成功",
                "data": None
            }
        
        # 真实API调用
        url = f"{self.base_url}/handle-lend-records/{handle_id}"
        try:
            response = self.session.put(url, json=handle_record_data, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"更新刀柄借出记录失败: {e}")
            return {
                "code": 500,
                "msg": f"更新刀柄借出记录失败: {str(e)}",
                "data": None
            }

    def get_handle_lend_record_detail(self, handle_id: int) -> Dict[str, Any]:
        """
        获取刀柄借出记录详情
        """
        # 如果是模拟模式，使用模拟数据
        if self.base_url == "mock":
            # 查找刀柄借出记录
            handle_record = None
            for record in self.mock_handle_lend_records:
                if record["id"] == handle_id:
                    handle_record = record
                    break
            
            if not handle_record:
                return {
                    "code": 404,
                    "msg": "刀柄借出记录不存在",
                    "data": None
                }
            
            return {
                "code": 200,
                "msg": "获取成功",
                "data": handle_record
            }
        
        # 真实API调用
        url = f"{self.base_url}/handle-lend-records/{handle_id}"
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            return {
                "code": 200,
                "msg": "获取成功",
                "data": data
            }
        except requests.exceptions.RequestException as e:
            logger.error(f"获取刀柄借出记录详情失败: {e}")
            return {
                "code": 500,
                "msg": f"获取刀柄借出记录详情失败: {str(e)}",
                "data": None
            }

    def process_handle_batch_return(self, request_data: Dict) -> Dict[str, Any]:
        """
        处理刀柄批量归还请求
        """
        # 如果是模拟模式，使用模拟数据
        if self.base_url == "mock":
            success_count = 0
            failed_items = []
            
            # 模拟处理每条归还记录
            for return_item in request_data.get("returnList", []):
                try:
                    # 查找刀柄借出记录
                    handle_record = None
                    for record in self.mock_handle_lend_records:
                        if record["id"] == return_item["handleId"]:
                            handle_record = record
                            break
                    
                    if not handle_record:
                        failed_items.append({
                            "handleId": return_item["handleId"],
                            "reason": "刀柄借出记录不存在"
                        })
                        continue
                        
                    # 验证操作权限（只能本人归还）
                    if handle_record["borrowerCode"] != request_data.get("operateUser"):
                        failed_items.append({
                            "handleId": return_item["handleId"],
                            "reason": "只能归还本人借出的刀柄"
                        })
                        continue
                        
                    # 验证借出状态
                    if handle_record["status"] not in ['借用中', 'overdue']:
                        failed_items.append({
                            "handleId": return_item["handleId"],
                            "reason": "当前状态不允许归还"
                        })
                        continue
                    
                    # 更新刀柄借出记录状态
                    handle_record["status"] = '已归还'
                    handle_record["actualReturnDate"] = return_item["actualReturnDate"]
                    
                    success_count += 1
                    
                except Exception as e:
                    failed_items.append({
                        "handleId": return_item["handleId"],
                        "reason": str(e)
                    })
            
            # 返回结果
            return {
                "code": 200,
                "msg": f"刀柄批量归还完成，成功 {success_count} 条，失败 {len(failed_items)} 条",
                "data": {
                    "successCount": success_count,
                    "failedItems": failed_items
                }
            }
        
        # 真实API调用
        url = f"{self.base_url}/handle-batch-return"
        try:
            response = self.session.post(url, json=request_data, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"刀柄批量归还处理失败: {e}")
            return {
                "code": 500,
                "msg": f"刀柄批量归还处理失败: {str(e)}",
                "data": None
            }

    def process_handle_return(self, request_data: Dict, current_user: Dict) -> Dict[str, Any]:
        """
        处理刀柄归还服务
        """
        # 如果是模拟模式，使用模拟数据
        if self.base_url == "mock":
            handle_id = request_data.get("handleId")
            
            # 查找刀柄借出记录
            handle_record = None
            for record in self.mock_handle_lend_records:
                if record["id"] == handle_id:
                    handle_record = record
                    break
            
            if not handle_record:
                return {
                    "code": 404,
                    "msg": "刀柄借出记录不存在",
                    "data": None
                }
                
            # 验证权限（只能本人归还）
            if handle_record["borrowerCode"] != current_user.get("employeeCode"):
                return {
                    "code": 403,
                    "msg": "只能归还本人借出的刀柄",
                    "data": None
                }
                
            # 验证借出状态
            if handle_record["status"] not in ['借用中', 'overdue']:
                return {
                    "code": 400,
                    "msg": "当前状态不允许归还",
                    "data": None
                }
            
            # 更新刀柄借出记录状态
            handle_record["status"] = '已归还'
            handle_record["actualReturnDate"] = request_data.get("actualReturnDate")
            
            return {
                "code": 200,
                "msg": "刀柄归还成功",
                "data": None
            }
        
        # 真实API调用
        url = f"{self.base_url}/handle-return"
        try:
            response = self.session.post(url, json=request_data, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"处理刀柄归还失败: {e}")
            return {
                "code": 500,
                "msg": f"处理刀柄归还失败: {str(e)}",
                "data": None
            }

    def process_handle_temp_store(self, request_data: Dict, current_user: Dict) -> Dict[str, Any]:
        """
        处理刀柄暂存服务
        """
        # 如果是模拟模式，使用模拟数据
        if self.base_url == "mock":
            handle_id = request_data.get("handleId")
            
            # 查找刀柄借出记录
            handle_record = None
            for record in self.mock_handle_lend_records:
                if record["id"] == handle_id:
                    handle_record = record
                    break
            
            if not handle_record:
                return {
                    "code": 404,
                    "msg": "刀柄借出记录不存在",
                    "data": None
                }
                
            # 验证权限（只能本人操作）
            if handle_record["borrowerCode"] != current_user.get("employeeCode"):
                return {
                    "code": 403,
                    "msg": "只能操作本人的刀柄借出记录",
                    "data": None
                }
            
            # 更新刀柄借出记录状态为暂存
            handle_record["status"] = '暂存中'
            
            return {
                "code": 200,
                "msg": "刀柄暂存成功",
                "data": None
            }
        
        # 真实API调用
        url = f"{self.base_url}/handle-temp-store"
        try:
            response = self.session.post(url, json=request_data, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"处理刀柄暂存失败: {e}")
            return {
                "code": 500,
                "msg": f"处理刀柄暂存失败: {str(e)}",
                "data": None
            }

    def get_temp_store_records(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        获取刀头暂存记录列表
        参数：暂存单号、暂存人、暂存人编号、暂存类型、刀头品牌、刀头型号、暂存状态、暂存时间等查询条件
        """
        # 如果是模拟模式，使用模拟数据
        if self.base_url == "mock":
            # 获取分页参数
            page = params.get("page", 1) if params else 1
            size = params.get("size", 10) if params else 10
            
            # 筛选数据
            filtered_records = self.mock_temp_store_records.copy()
            
            # 根据查询参数过滤数据
            if params:
                if params.get("tempStoreCode"):
                    filtered_records = [r for r in filtered_records if params["tempStoreCode"] in r["tempStoreCode"]]
                if params.get("storePerson"):
                    filtered_records = [r for r in filtered_records if params["storePerson"] in r["storePerson"]]
                if params.get("storePersonCode"):
                    filtered_records = [r for r in filtered_records if params["storePersonCode"] in r["storePersonCode"]]
                if params.get("storeType"):
                    filtered_records = [r for r in filtered_records if params["storeType"] in r["storeType"]]
                if params.get("brandName"):
                    filtered_records = [r for r in filtered_records if params["brandName"] in r["brandName"]]
                if params.get("cutterType"):
                    filtered_records = [r for r in filtered_records if params["cutterType"] in r["cutterType"]]
                if params.get("status"):
                    filtered_records = [r for r in filtered_records if params["status"] == r["status"]]
                if params.get("storeTime"):
                    # 简化处理，实际应用中可能需要更复杂的日期比较
                    filtered_records = [r for r in filtered_records if params["storeTime"] in r["storeTime"]]
            
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
        url = f"{self.base_url}/temp-store-records"
        try:
            response = self.session.get(url, params=params or {}, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"获取刀头暂存记录列表失败: {e}")
            raise

    def create_temp_store_record(self, temp_store_data: Dict) -> Dict[str, Any]:
        """
        创建新的刀柄暂存记录
        """
        # 如果是模拟模式，使用模拟数据
        if self.base_url == "mock":
            # 生成新的ID
            new_id = max([r["id"] for r in self.mock_temp_store_records]) + 1 if self.mock_temp_store_records else 1
            
            # 处理时间格式
            store_time = temp_store_data.get("borrowDate") or datetime.now().isoformat()
            
            # 创建新的暂存记录 (映射前端字段到后端字段)
            new_record = {
                "id": new_id,
                "tempStoreCode": temp_store_data.get("storageCode"),
                "storePerson": temp_store_data.get("borrowerName"),
                "storePersonCode": temp_store_data.get("storageUser"),
                "storeType": "刀头暂存",
                "brandName": temp_store_data.get("brandName"),
                "cutterType": temp_store_data.get("handleType"),
                "specification": temp_store_data.get("handleSpec", ""),
                "storeTime": store_time,
                "status": temp_store_data.get("borrowStatus", "borrowed"),
                "quantity": temp_store_data.get("quantity", 1),
                "expectedReturnDate": temp_store_data.get("expectedReturnDate"),
                "purpose": temp_store_data.get("borrowPurpose")
            }
            
            # 添加到模拟数据中
            self.mock_temp_store_records.append(new_record)
            
            return {
                "code": 200,
                "msg": "暂存记录创建成功",
                "data": new_record
            }
        
        # 真实API调用
        url = f"{self.base_url}/temp-store-records"
        try:
            # 映射前端字段到后端字段
            mapped_data = {
                "tempStoreCode": temp_store_data.get("storageCode"),
                "storePerson": temp_store_data.get("borrowerName"),
                "storePersonCode": temp_store_data.get("storageUser"),
                "storeType": "刀头暂存",
                "brandName": temp_store_data.get("brandName"),
                "cutterType": temp_store_data.get("handleType"),
                "specification": temp_store_data.get("handleSpec"),
                "quantity": temp_store_data.get("quantity"),
                "expectedReturnDate": temp_store_data.get("expectedReturnDate"),
                "purpose": temp_store_data.get("borrowPurpose"),
                "storeTime": temp_store_data.get("borrowDate"),
                "status": temp_store_data.get("borrowStatus", "borrowed")
            }
            response = self.session.post(url, json=mapped_data, timeout=10)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f"创建暂存记录失败: {e}")
            raise

    def get_handle_temp_store_records(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        获取刀柄暂存记录列表
        参数：暂存单号、暂存人姓名、暂存人编号、品牌、规格、暂存类型、暂存时间等查询条件
        """
        # 如果是模拟模式，使用模拟数据
        if self.base_url == "mock":
            # 获取分页参数（支持前端的 pageNum 和 pageSize）
            page = params.get("pageNum", params.get("page", 1)) if params else 1
            size = params.get("pageSize", params.get("size", 10)) if params else 10
            
            # 筛选数据
            filtered_records = self.mock_handle_temp_store_records.copy()
            
            # 根据查询参数过滤数据
            if params:
                if params.get("storageCode"):
                    filtered_records = [r for r in filtered_records if params["storageCode"] in r["storageCode"]]
                if params.get("borrowerName"):
                    filtered_records = [r for r in filtered_records if params["borrowerName"] in r["borrowerName"]]
                if params.get("storageUser"):
                    filtered_records = [r for r in filtered_records if params["storageUser"] in r["storageUser"]]
                if params.get("brandName"):
                    filtered_records = [r for r in filtered_records if params["brandName"] in r["brandName"]]
                if params.get("handleSpec"):
                    filtered_records = [r for r in filtered_records if params["handleSpec"] in r["handleSpec"]]
                if params.get("storageType") is not None:  # 注意：0 也是有效值
                    filtered_records = [r for r in filtered_records if r["storageType"] == params["storageType"]]
                if params.get("storageTime"):
                    filtered_records = [r for r in filtered_records if params["storageTime"] in r["storageTime"]]
            
            # 分页处理
            start_index = (page - 1) * size
            end_index = start_index + size
            paginated_records = filtered_records[start_index:end_index]
            
            return {
                "list": paginated_records,
                "total": len(filtered_records),
                "pageNum": page,
                "pageSize": size
            }
        
        # 真实API调用
        url = f"{self.base_url}/handle/temp-store-records"
        try:
            response = self.session.get(url, params=params or {}, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"获取刀柄暂存记录列表失败: {e}")
            raise

    def create_handle_temp_store_record(self, handle_temp_store_data: Dict) -> Dict[str, Any]:
        """
        创建新的刀柄暂存记录
        """
        # 如果是模拟模式，使用模拟数据
        if self.base_url == "mock":
            # 生成新的ID
            new_id = max([r["id"] for r in self.mock_handle_temp_store_records]) + 1 if self.mock_handle_temp_store_records else 1
            
            # 处理时间格式
            storage_time = handle_temp_store_data.get("borrowDate") or datetime.now().isoformat()
            
            # 创建新的暂存记录
            new_record = {
                "id": new_id,
                "storageCode": handle_temp_store_data.get("storageCode"),
                "borrowerName": handle_temp_store_data.get("borrowerName"),
                "storageUser": handle_temp_store_data.get("storageUser"),
                "brandName": handle_temp_store_data.get("brandName"),
                "handleSpec": f"{handle_temp_store_data.get('handleType', '')}-{handle_temp_store_data.get('handleSpec', '')}",
                "storageType": "1",  # 默认个人暂存
                "quantity": handle_temp_store_data.get("quantity"),
                "storageTime": storage_time,
                "status": handle_temp_store_data.get("borrowStatus", "borrowed"),
                "purpose": handle_temp_store_data.get("borrowPurpose"),
                "expectedReturnDate": handle_temp_store_data.get("expectedReturnDate")
            }
            
            # 添加到模拟数据中
            self.mock_handle_temp_store_records.append(new_record)
            
            return {
                "code": 200,
                "msg": "刀柄暂存记录创建成功",
                "data": new_record
            }
        
        # 真实API调用
        url = f"{self.base_url}/handle/temp-store-records"
        try:
            # 构建请求数据
            mapped_data = {
                "storageCode": handle_temp_store_data.get("storageCode"),
                "borrowerName": handle_temp_store_data.get("borrowerName"),
                "storageUser": handle_temp_store_data.get("storageUser"),
                "brandName": handle_temp_store_data.get("brandName"),
                "handleType": handle_temp_store_data.get("handleType"),
                "handleSpec": handle_temp_store_data.get("handleSpec"),
                "quantity": handle_temp_store_data.get("quantity"),
                "expectedReturnDate": handle_temp_store_data.get("expectedReturnDate"),
                "purpose": handle_temp_store_data.get("borrowPurpose"),
                "storageTime": handle_temp_store_data.get("borrowDate"),
                "status": handle_temp_store_data.get("borrowStatus", "borrowed")
            }
            response = self.session.post(url, json=mapped_data, timeout=10)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f"创建刀柄暂存记录失败: {e}")
            raise

    def process_handle_temp_store_batch_return(self, request_data: Dict) -> Dict[str, Any]:
        """
        处理刀柄暂存批量归还请求
        支持多个暂存记录同时归还，自动分配库位策略（轮询分配）
        验证操作人权限（只能归还本人暂存的刀柄）
        记录操作时间和操作人信息
        """
        # 如果是模拟模式，使用模拟数据
        if self.base_url == "mock":
            success_count = 0
            failed_items = []
            location_details = []  # 库位详情
            
            # 获取库位列表和分配策略
            loc_list = request_data.get("locList", [])
            allocation_strategy = request_data.get("allocationStrategy", "polling")
            operate_user = request_data.get("operateUser")
            
            if not loc_list:
                return {
                    "code": 400,
                    "msg": "库位列表不能为空",
                    "data": None
                }
            
            # 初始化库位详情（轮询分配）
            location_map = {loc: {"locationCode": loc, "totalQuantity": 0, "itemCount": 0, "items": []} for loc in loc_list}
            current_location_index = 0
            
            # 模拟处理每条归还记录
            for return_item in request_data.get("returnList", []):
                try:
                    # 查找暂存记录
                    temp_store_record = None
                    for record in self.mock_handle_temp_store_records:
                        if record["id"] == return_item["borrowId"]:
                            temp_store_record = record
                            break
                    
                    if not temp_store_record:
                        failed_items.append({
                            "borrowId": return_item["borrowId"],
                            "reason": "暂存记录不存在"
                        })
                        continue
                    
                    # 验证操作权限（只能本人归还）
                    if operate_user and temp_store_record["storageUser"] != operate_user:
                        failed_items.append({
                            "borrowId": return_item["borrowId"],
                            "reason": "只能归还本人暂存的刀柄"
                        })
                        continue
                    
                    # 验证暂存状态（只能对暂存中的记录进行归还）
                    if temp_store_record["status"] not in ['borrowed', 'temp_stored', '暂存中']:
                        failed_items.append({
                            "borrowId": return_item["borrowId"],
                            "reason": f"当前状态[{temp_store_record['status']}]不允许归还，只有暂存状态的刀柄可以归还"
                        })
                        continue
                    
                    # 轮询分配库位
                    assigned_location = loc_list[current_location_index % len(loc_list)]
                    current_location_index += 1
                    
                    # 更新暂存记录状态为已归还
                    temp_store_record["status"] = '已归还'
                    temp_store_record["actualReturnDate"] = return_item.get("actualReturnDate", datetime.now().isoformat())
                    temp_store_record["assignedLocation"] = assigned_location
                    
                    # 记录库位详情
                    location_map[assigned_location]["totalQuantity"] += return_item.get("quantity", 1)
                    location_map[assigned_location]["itemCount"] += 1
                    location_map[assigned_location]["items"].append({
                        "borrowId": return_item["borrowId"],
                        "storageCode": return_item["storageCode"],
                        "brandName": return_item["brandName"],
                        "handleSpec": return_item["handleSpec"],
                        "quantity": return_item.get("quantity", 1)
                    })
                    
                    success_count += 1
                    
                except Exception as e:
                    failed_items.append({
                        "borrowId": return_item.get("borrowId", 0),
                        "reason": str(e)
                    })
            
            # 构建库位详情列表
            location_details = [details for details in location_map.values() if details["itemCount"] > 0]
            
            # 返回结果
            result_data = {
                "successCount": success_count,
                "failedCount": len(failed_items),
                "failedItems": failed_items,
                "locationDetails": location_details,
                "totalQuantity": request_data.get("totalQuantity", 0),
                "operateTime": request_data.get("operateTime"),
                "operateUser": operate_user,
                "cabinetCode": request_data.get("cabinetCode"),
                "returnRemarks": request_data.get("returnRemarks", "")
            }
            
            if success_count > 0 and len(failed_items) == 0:
                msg = f"批量归还成功！成功归还 {success_count} 条记录"
                code = 200
            elif success_count > 0 and len(failed_items) > 0:
                msg = f"批量归还部分成功，成功 {success_count} 条，失败 {len(failed_items)} 条"
                code = 200
            else:
                msg = f"批量归还失败，所有记录均未能归还"
                code = 400
            
            return {
                "code": code,
                "msg": msg,
                "data": result_data
            }
        
        # 真实API调用
        url = f"{self.base_url}/handle/temp-store-batch-return"
        try:
            response = self.session.post(url, json=request_data, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"刀柄暂存批量归还处理失败: {e}")
            return {
                "code": 500,
                "msg": f"刀柄暂存批量归还处理失败: {str(e)}",
                "data": None
            }

    def update_handle_temp_store_record(self, record_id: int, update_data: Dict, current_user: Dict) -> Dict[str, Any]:
        """
        更新刀柄暂存记录（编辑功能）
        只能编辑本人的暂存记录
        """
        # 如果是模拟模式，使用模拟数据
        if self.base_url == "mock":
            # 查找暂存记录
            temp_store_record = None
            for record in self.mock_handle_temp_store_records:
                if record["id"] == record_id:
                    temp_store_record = record
                    break
            
            if not temp_store_record:
                return {
                    "code": 404,
                    "msg": "刀柄暂存记录不存在",
                    "data": None
                }
            
            # 验证权限（只能编辑本人的记录）
            if temp_store_record["storageUser"] != current_user.get("employeeCode"):
                return {
                    "code": 403,
                    "msg": "只能编辑本人的暂存记录",
                    "data": None
                }
            
            # 验证状态（只能编辑暂存中的记录）
            if temp_store_record["status"] not in ['borrowed', 'temp_stored', '暂存中']:
                return {
                    "code": 400,
                    "msg": f"当前状态[{temp_store_record['status']}]不允许编辑",
                    "data": None
                }
            
            # 更新记录
            temp_store_record["brandName"] = update_data.get("brandName")
            temp_store_record["handleSpec"] = f"{update_data.get('handleType', '')}-{update_data.get('handleSpec', '')}"
            temp_store_record["quantity"] = update_data.get("quantity")
            temp_store_record["expectedReturnDate"] = update_data.get("expectedReturnDate")
            temp_store_record["purpose"] = update_data.get("borrowPurpose")
            
            return {
                "code": 200,
                "msg": "更新成功",
                "data": None
            }
        
        # 真实API调用
        url = f"{self.base_url}/handle/temp-store/{record_id}"
        try:
            mapped_data = {
                "brandName": update_data.get("brandName"),
                "handleType": update_data.get("handleType"),
                "handleSpec": update_data.get("handleSpec"),
                "quantity": update_data.get("quantity"),
                "expectedReturnDate": update_data.get("expectedReturnDate"),
                "borrowPurpose": update_data.get("borrowPurpose")
            }
            response = self.session.put(url, json=mapped_data, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"更新刀柄暂存记录失败: {e}")
            return {
                "code": 500,
                "msg": f"更新刀柄暂存记录失败: {str(e)}",
                "data": None
            }

    def return_handle_temp_store_record(self, request_data: Dict, current_user: Dict) -> Dict[str, Any]:
        """
        单个刀柄暂存记录归还（归还功能）
        只能归还本人的暂存记录
        """
        # 如果是模拟模式，使用模拟数据
        if self.base_url == "mock":
            borrow_id = request_data.get("borrowId")
            
            # 查找暂存记录
            temp_store_record = None
            for record in self.mock_handle_temp_store_records:
                if record["id"] == borrow_id:
                    temp_store_record = record
                    break
            
            if not temp_store_record:
                return {
                    "code": 404,
                    "msg": "刀柄暂存记录不存在",
                    "data": None
                }
            
            # 验证权限（只能归还本人的记录）
            operate_user = request_data.get("operateUser") or current_user.get("employeeCode")
            if temp_store_record["storageUser"] != operate_user:
                return {
                    "code": 403,
                    "msg": "只能归还本人的暂存记录",
                    "data": None
                }
            
            # 验证状态
            if temp_store_record["status"] not in ['borrowed', 'temp_stored', '暂存中']:
                return {
                    "code": 400,
                    "msg": f"当前状态[{temp_store_record['status']}]不允许归还",
                    "data": None
                }
            
            # 更新记录状态
            temp_store_record["status"] = '已归还'
            temp_store_record["actualReturnDate"] = request_data.get("actualReturnDate", datetime.now().isoformat())
            
            # 记录归还信息
            temp_store_record["returnRemarks"] = request_data.get("returnRemarks", "")
            temp_store_record["cabinetCode"] = request_data.get("cabinetCode")
            temp_store_record["locList"] = request_data.get("locList", [])
            
            return {
                "code": 200,
                "msg": "归还成功",
                "data": None
            }
        
        # 真实API调用
        url = f"{self.base_url}/handle/return"
        try:
            response = self.session.post(url, json=request_data, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"刀柄暂存归还失败: {e}")
            return {
                "code": 500,
                "msg": f"刀柄暂存归还失败: {str(e)}",
                "data": None
            }

    def create_temp_store_from_borrow(self, request_data: Dict, current_user: Dict) -> Dict[str, Any]:
        """
        从借出记录创建暂存（暂存功能）
        将已借出的刀柄转为暂存状态
        """
        # 如果是模拟模式，使用模拟数据
        if self.base_url == "mock":
            borrow_id = request_data.get("borrowId")
            
            # 这里假设我们从 handle_lend_records 中查找借出记录
            # 然后转换为暂存记录
            borrow_record = None
            for record in self.mock_handle_lend_records:
                if record["id"] == borrow_id:
                    borrow_record = record
                    break
            
            if not borrow_record:
                return {
                    "code": 404,
                    "msg": "借出记录不存在",
                    "data": None
                }
            
            # 验证权限
            operate_user = request_data.get("operateUser") or current_user.get("employeeCode")
            if borrow_record["borrowerCode"] != operate_user:
                return {
                    "code": 403,
                    "msg": "只能暂存本人的借出记录",
                    "data": None
                }
            
            # 验证状态（只能对借用中的记录进行暂存）
            if borrow_record["status"] not in ['借用中', 'overdue']:
                return {
                    "code": 400,
                    "msg": f"当前状态[{borrow_record['status']}]不允许暂存",
                    "data": None
                }
            
            # 生成暂存单号
            now = datetime.now()
            today = now.strftime("%Y%m%d")
            existing_codes = [r["storageCode"] for r in self.mock_handle_temp_store_records if r["storageCode"].startswith(f"BOR{today}")]
            next_number = len(existing_codes) + 1
            storage_code = f"BOR{today}{str(next_number).zfill(3)}"
            
            # 创建暂存记录
            new_id = max([r["id"] for r in self.mock_handle_temp_store_records]) + 1 if self.mock_handle_temp_store_records else 1
            
            new_temp_store = {
                "id": new_id,
                "storageCode": storage_code,
                "borrowerName": borrow_record["borrowerName"],
                "storageUser": borrow_record["borrowerCode"],
                "brandName": borrow_record["brand"],
                "handleSpec": borrow_record["model"],
                "storageType": "1",  # 个人暂存
                "quantity": request_data.get("borrowQty", borrow_record["quantity"]),
                "storageTime": request_data.get("operateTime", datetime.now().isoformat()),
                "status": "temp_stored",  # 暂存状态
                "purpose": request_data.get("borrowRemarks", ""),
                "expectedReturnDate": borrow_record.get("expectedReturnDate"),
                "cabinetCode": request_data.get("cabinetCode"),
                "itemList": request_data.get("itemList", [])
            }
            
            # 添加到暂存记录
            self.mock_handle_temp_store_records.append(new_temp_store)
            
            # 更新借出记录状态
            borrow_record["status"] = "temp_stored"
            
            return {
                "code": 200,
                "msg": "暂存成功",
                "data": {
                    "storageCode": storage_code,
                    "tempStoreId": new_id
                }
            }
        
        # 真实API调用
        url = f"{self.base_url}/handle/temp-store"
        try:
            response = self.session.post(url, json=request_data, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"创建刀柄暂存失败: {e}")
            return {
                "code": 500,
                "msg": f"创建刀柄暂存失败: {str(e)}",
                "data": None
            }

    def get_handle_temp_store_detail(self, record_id: int) -> Dict[str, Any]:
        """
        获取刀柄暂存记录详情（详情功能）
        """
        # 如果是模拟模式，使用模拟数据
        if self.base_url == "mock":
            # 查找暂存记录
            temp_store_record = None
            for record in self.mock_handle_temp_store_records:
                if record["id"] == record_id:
                    temp_store_record = record
                    break
            
            if not temp_store_record:
                return {
                    "code": 404,
                    "msg": "刀柄暂存记录不存在",
                    "data": None
                }
            
            # 返回完整详情
            return {
                "code": 200,
                "msg": "获取成功",
                "data": temp_store_record
            }
        
        # 真实API调用
        url = f"{self.base_url}/handle/temp-store/{record_id}"
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            return {
                "code": 200,
                "msg": "获取成功",
                "data": data
            }
        except requests.exceptions.RequestException as e:
            logger.error(f"获取刀柄暂存记录详情失败: {e}")
            return {
                "code": 500,
                "msg": f"获取刀柄暂存记录详情失败: {str(e)}",
                "data": None
            }

# 初始化API客户端（这里使用示例API，实际使用时请替换为你的真实API地址）
original_api_client = OriginalAPIClient(
    base_url="mock",  # 使用模拟数据
    #    base_url="https://jsonplaceholder.typicode.com",
    api_key=None  # 如果有API密钥，请在此处填写
)