import requests
import logging
import os
from typing import Dict, Any, Optional, List
from urllib.parse import urljoin

logger = logging.getLogger(__name__)


class TeamLeaderAPIClient:
    """封装班组长的原始API调用"""

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
            "User-Agent": "TeamLeader-API-Wrapper/1.0"
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
                # 获取项目根目录（假设teamleader文件夹在项目根目录下）
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

    def get_cutter_list(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        分页查询刀具耗材信息
        接口地址: /qw/knife/web/from/mes/cutter/list
        请求方式: GET

        参数：
            params: 查询参数，包括：
                - brandName: 品牌名称
                - cabinetName: 刀具柜名称
                - createTime: 创建时间
                - createUser: 创建人
                - cutterType: 刀具类型
                - cutterCode: 刀具型号
                - minPrice: 最低价格
                - maxPrice: 最高价格
                - current: 当前页
                - size: 每页数量
        返回：
            包含分页数据的响应
        """
        url = f"{self.base_url}/qw/knife/web/from/mes/cutter/list"

        try:
            # 构建请求参数，过滤掉None值
            request_params = {}

            if params:
                # 基本查询参数
                if params.get("brandName"):
                    request_params["brandName"] = params["brandName"]

                if params.get("cutterType"):
                    request_params["cutterType"] = params["cutterType"]

                if params.get("cutterCode"):
                    request_params["cutterCode"] = params["cutterCode"]

                if params.get("createTime"):
                    request_params["createTime"] = params["createTime"]

                if params.get("createUser") is not None:
                    request_params["createUser"] = params["createUser"]

                # 处理刀具柜名称：需要通过cabinetList传递
                if params.get("cabinetName"):
                    request_params["cabinetList[0].cabinetName"] = params["cabinetName"]

                # 价格区间筛选：前端的minPrice和maxPrice，后端通过price参数过滤
                # 注：这里可能需要根据实际接口调整，如果接口支持区间查询
                # 如果原始接口不支持价格区间，则需要在返回后进行过滤
                if params.get("minPrice") is not None or params.get("maxPrice") is not None:
                    # 标记需要进行价格过滤
                    pass

                # 分页参数
                request_params["current"] = params.get("current", 1)
                request_params["size"] = params.get("size", 10)
            else:
                # 默认分页参数
                request_params["current"] = 1
                request_params["size"] = 10

            logger.info(f"请求刀具列表，参数: {request_params}")

            # 发起GET请求
            response = self.session.get(url, params=request_params, timeout=10)
            response.raise_for_status()

            result = response.json()

            # 如果有价格区间筛选，对结果进行过滤
            if params and (params.get("minPrice") is not None or params.get("maxPrice") is not None):
                if result.get("success") and result.get("data") and result["data"].get("records"):
                    min_price = params.get("minPrice")
                    max_price = params.get("maxPrice")

                    # 过滤记录
                    filtered_records = []
                    for record in result["data"]["records"]:
                        price = record.get("price")
                        if price is not None:
                            # 检查价格是否在区间内
                            if min_price is not None and price < min_price:
                                continue
                            if max_price is not None and price > max_price:
                                continue
                        filtered_records.append(record)

                    # 更新结果
                    result["data"]["records"] = filtered_records
                    result["data"]["total"] = len(filtered_records)
                    # 重新计算总页数
                    size = result["data"].get("size", 10)
                    result["data"]["pages"] = (len(filtered_records) + size - 1) // size if size > 0 else 0

            return result

        except requests.exceptions.RequestException as e:
            logger.error(f"获取刀具列表失败: {e}")
            return {
                "code": 500,
                "msg": f"请求失败: {str(e)}",
                "success": False,
                "data": None
            }
        except Exception as e:
            logger.error(f"处理刀具列表数据失败: {e}")
            return {
                "code": 500,
                "msg": f"数据处理失败: {str(e)}",
                "success": False,
                "data": None
            }

    def create_cutter(self, cutter_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        新增刀具耗材
        接口地址: /qw/knife/web/from/mes/cutter/saveCutter
        请求方式: POST
        请求数据类型: application/json

        参数：
            cutter_data: 刀具耗材数据，包括：
                - brandName: 品牌名称（必填）
                - cabinetName: 刀具柜名称（必填）
                - cutterCode: 刀具型号（必填）
                - price: 单价（必填）
                - createUser: 创建人（必填）
                - imageUrlList: 刀头图片列表（可选）
                - 其他可选字段...
        返回：
            新增结果，包含新增成功后的刀具详情
        """
        url = f"{self.base_url}/qw/knife/web/from/mes/cutter/saveCutter"

        try:
            # 构建请求体，处理cabinetList字段
            request_body = {}

            # 必填字段
            if cutter_data.get("brandName"):
                request_body["brandName"] = cutter_data["brandName"]

            if cutter_data.get("cutterCode"):
                request_body["cutterCode"] = cutter_data["cutterCode"]

            if cutter_data.get("price") is not None:
                request_body["price"] = cutter_data["price"]

            if cutter_data.get("createUser") is not None:
                request_body["createUser"] = cutter_data["createUser"]

            # 处理刀具柜信息：将cabinetName转换为cabinetList数组
            if cutter_data.get("cabinetName"):
                request_body["cabinetList"] = [{
                    "cabinetName": cutter_data["cabinetName"],
                    # 可以添加其他默认值，根据需要调整
                    "cabinetCode": cutter_data.get("cabinetCode", ""),
                    "locSurplus": cutter_data.get("locSurplus", 0),
                    "stockLoc": cutter_data.get("stockLoc", "")
                }]

            # 处理图片列表
            if cutter_data.get("imageUrlList"):
                request_body["imageUrlList"] = cutter_data["imageUrlList"]

            # 其他可选字段
            optional_fields = [
                "brandCode", "cutterType", "specification", "materialCode",
                "materialType", "packQty", "packUnit", "inventoryWarning",
                "numberLife", "timeLife", "isUniqueCode", "imageUrl",
                "createDept", "status", "stockNum", "tenantId"
            ]

            for field in optional_fields:
                if cutter_data.get(field) is not None:
                    request_body[field] = cutter_data[field]

            logger.info(f"新增刀具耗材，请求体: {request_body}")

            # 发起POST请求，使用JSON格式
            response = self.session.post(url, json=request_body, timeout=10)
            response.raise_for_status()

            result = response.json()
            logger.info(f"新增刀具耗材成功: {result}")

            return result

        except requests.exceptions.RequestException as e:
            logger.error(f"新增刀具耗材失败: {e}")
            return {
                "code": 500,
                "msg": f"请求失败: {str(e)}",
                "success": False,
                "data": None
            }
        except Exception as e:
            logger.error(f"处理新增刀具耗材数据失败: {e}")
            return {
                "code": 500,
                "msg": f"数据处理失败: {str(e)}",
                "success": False,
                "data": None
            }

    def update_cutter(self, cutter_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        修改刀具耗材
        接口地址: /qw/knife/web/from/mes/cutter/updateCutter
        请求方式: POST
        请求数据类型: application/json

        参数：
            cutter_data: 刀具耗材数据，包括：
                - id: 刀具ID（必填，用于标识要修改的记录）
                - brandName: 品牌名称（可选）
                - cabinetName: 刀具柜名称（可选）
                - cutterCode: 刀具型号（可选）
                - price: 单价（可选）
                - updateUser: 更新人（可选）
                - imageUrlList: 刀头图片列表（可选）
                - 其他可选字段...
        返回：
            修改结果，包含修改成功后的刀具详情
        """
        url = f"{self.base_url}/qw/knife/web/from/mes/cutter/updateCutter"

        try:
            # 构建请求体
            request_body = {}

            # 必填字段：id
            if cutter_data.get("id") is None:
                return {
                    "code": 400,
                    "msg": "刀具ID不能为空",
                    "success": False,
                    "data": None
                }
            request_body["id"] = cutter_data["id"]

            # 可选字段 - 基本信息
            if cutter_data.get("brandName") is not None:
                request_body["brandName"] = cutter_data["brandName"]

            if cutter_data.get("cutterCode") is not None:
                request_body["cutterCode"] = cutter_data["cutterCode"]

            if cutter_data.get("price") is not None:
                request_body["price"] = cutter_data["price"]

            if cutter_data.get("updateUser") is not None:
                request_body["updateUser"] = cutter_data["updateUser"]

            # 处理刀具柜信息：将cabinetName转换为cabinetList数组
            if cutter_data.get("cabinetName") is not None:
                request_body["cabinetList"] = [{
                    "cabinetName": cutter_data["cabinetName"],
                    "cabinetCode": cutter_data.get("cabinetCode", ""),
                    "cutterId": cutter_data.get("id"),  # 使用当前刀具ID
                    "locSurplus": cutter_data.get("locSurplus"),
                    "stockLoc": cutter_data.get("stockLoc", "")
                }]

            # 处理图片列表
            if cutter_data.get("imageUrlList") is not None:
                request_body["imageUrlList"] = cutter_data["imageUrlList"]

            # 其他可选字段
            optional_fields = [
                "brandCode", "cutterType", "specification", "materialCode",
                "materialType", "packQty", "packUnit", "inventoryWarning",
                "numberLife", "timeLife", "isUniqueCode", "imageUrl",
                "createDept", "createUser", "createTime", "status",
                "stockNum", "tenantId", "version"
            ]

            for field in optional_fields:
                if cutter_data.get(field) is not None:
                    request_body[field] = cutter_data[field]

            logger.info(f"修改刀具耗材，请求体: {request_body}")

            # 发起POST请求，使用JSON格式
            response = self.session.post(url, json=request_body, timeout=10)
            response.raise_for_status()

            result = response.json()
            logger.info(f"修改刀具耗材成功: {result}")

            return result

        except requests.exceptions.RequestException as e:
            logger.error(f"修改刀具耗材失败: {e}")
            return {
                "code": 500,
                "msg": f"请求失败: {str(e)}",
                "success": False,
                "data": None
            }
        except Exception as e:
            logger.error(f"处理修改刀具耗材数据失败: {e}")
            return {
                "code": 500,
                "msg": f"数据处理失败: {str(e)}",
                "success": False,
                "data": None
            }

    def delete_cutters(self, ids: str) -> Dict[str, Any]:
        """
        批量删除刀具耗材
        接口地址: /qw/knife/web/from/mes/cutter/delete
        请求方式: POST
        请求数据类型: application/json

        参数：
            ids: 主键集合，逗号分割（例如："1,2,3" 或 "1"）
        返回：
            删除结果，成功返回true
        """
        url = f"{self.base_url}/qw/knife/web/from/mes/cutter/delete"

        try:
            # 验证ids参数
            if not ids or ids.strip() == "":
                return {
                    "code": 400,
                    "msg": "删除ID不能为空",
                    "success": False,
                    "data": False
                }

            # 构建请求参数（使用query参数）
            params = {
                "ids": ids
            }

            logger.info(f"删除刀具耗材，参数: {params}")

            # 发起POST请求，使用params传递query参数
            response = self.session.post(url, params=params, timeout=10)
            response.raise_for_status()

            result = response.json()
            logger.info(f"删除刀具耗材成功: {result}")

            return result

        except requests.exceptions.RequestException as e:
            logger.error(f"删除刀具耗材失败: {e}")
            return {
                "code": 500,
                "msg": f"请求失败: {str(e)}",
                "success": False,
                "data": False
            }
        except Exception as e:
            logger.error(f"处理删除刀具耗材数据失败: {e}")
            return {
                "code": 500,
                "msg": f"数据处理失败: {str(e)}",
                "success": False,
                "data": False
            }

    def get_brand_list(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        分页查询品牌信息
        接口地址: /qw/knife/web/from/mes/cutter/pageListBrand
        请求方式: GET

        参数：
            params: 查询参数，包括：
                - brandCode: 品牌编码
                - brandName: 品牌名称
                - corporateName: 公司名称
                - supplierName: 供应商名称
                - status: 业务状态
                - createUser: 创建人
                - startTime: 创建开始时间
                - endTime: 创建结束时间
                - current: 当前页
                - size: 每页数量
        返回：
            包含分页数据的响应
        """
        url = f"{self.base_url}/qw/knife/web/from/mes/cutter/pageListBrand"

        try:
            # 构建请求参数，过滤掉None值
            request_params = {}

            if params:
                # 基本查询参数
                if params.get("brandCode"):
                    request_params["brandCode"] = params["brandCode"]

                if params.get("brandName"):
                    request_params["brandName"] = params["brandName"]

                if params.get("corporateName"):
                    request_params["corporateName"] = params["corporateName"]

                if params.get("supplierName"):
                    request_params["supplierName"] = params["supplierName"]

                if params.get("status") is not None:
                    request_params["status"] = params["status"]

                if params.get("createUser") is not None:
                    request_params["createUser"] = params["createUser"]

                # 时间范围查询
                if params.get("startTime"):
                    request_params["startTime"] = params["startTime"]

                if params.get("endTime"):
                    request_params["endTime"] = params["endTime"]

                # 分页参数
                request_params["current"] = params.get("current", 1)
                request_params["size"] = params.get("size", 10)
            else:
                # 默认分页参数
                request_params["current"] = 1
                request_params["size"] = 10

            logger.info(f"请求品牌列表，参数: {request_params}")

            # 发起GET请求
            response = self.session.get(url, params=request_params, timeout=10)
            response.raise_for_status()

            result = response.json()

            return result

        except requests.exceptions.RequestException as e:
            logger.error(f"获取品牌列表失败: {e}")
            return {
                "code": 500,
                "msg": f"请求失败: {str(e)}",
                "success": False,
                "data": None
            }
        except Exception as e:
            logger.error(f"处理品牌列表数据失败: {e}")
            return {
                "code": 500,
                "msg": f"数据处理失败: {str(e)}",
                "success": False,
                "data": None
            }

    def submit_brand(self, brand_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        新增或修改品牌信息
        接口地址: /qw/knife/web/from/mes/cutter/submitBrand
        请求方式: POST
        请求数据类型: application/json

        参数：
            brand_data: 品牌信息数据，包括：
                - id: 主键id（修改时必填，新增时不填）
                - brandCode: 品牌编码（必填）
                - brandName: 品牌名称（必填）
                - corporateName: 公司名称（必填）
                - supplierName: 供应商名称（必填）
                - supplierUser: 供应商联系人（必填）
                - phone: 联系方式（必填）
                - createDept: 创建部门（可选）
                - status: 业务状态（可选）
        返回：
            操作结果，成功返回true
        """
        url = f"{self.base_url}/qw/knife/web/from/mes/cutter/submitBrand"

        try:
            # 构建请求体
            request_body = {}

            # 必填字段
            if brand_data.get("brandCode"):
                request_body["brandCode"] = brand_data["brandCode"]

            if brand_data.get("brandName"):
                request_body["brandName"] = brand_data["brandName"]

            if brand_data.get("corporateName"):
                request_body["corporateName"] = brand_data["corporateName"]

            if brand_data.get("supplierName"):
                request_body["supplierName"] = brand_data["supplierName"]

            if brand_data.get("supplierUser"):
                request_body["supplierUser"] = brand_data["supplierUser"]

            if brand_data.get("phone"):
                request_body["phone"] = brand_data["phone"]

            # 可选字段
            if brand_data.get("id") is not None:
                request_body["id"] = brand_data["id"]

            if brand_data.get("createDept") is not None:
                request_body["createDept"] = brand_data["createDept"]

            if brand_data.get("status") is not None:
                request_body["status"] = brand_data["status"]

            # 其他可选字段
            optional_fields = ["createUser", "updateUser", "tenantId"]
            for field in optional_fields:
                if brand_data.get(field) is not None:
                    request_body[field] = brand_data[field]

            # 判断是新增还是修改
            operation = "修改" if brand_data.get("id") else "新增"
            logger.info(f"{operation}品牌信息，请求体: {request_body}")

            # 发起POST请求，使用JSON格式
            response = self.session.post(url, json=request_body, timeout=10)
            response.raise_for_status()

            result = response.json()
            logger.info(f"{operation}品牌信息成功: {result}")

            return result

        except requests.exceptions.RequestException as e:
            logger.error(f"提交品牌信息失败: {e}")
            return {
                "code": 500,
                "msg": f"请求失败: {str(e)}",
                "success": False,
                "data": False
            }
        except Exception as e:
            logger.error(f"处理品牌信息数据失败: {e}")
            return {
                "code": 500,
                "msg": f"数据处理失败: {str(e)}",
                "success": False,
                "data": False
            }

    def delete_brands(self, ids: str) -> Dict[str, Any]:
        """
        批量删除品牌信息
        接口地址: /qw/knife/web/from/mes/cutter/delBrand
        请求方式: POST
        请求数据类型: application/json

        参数：
            ids: 主键集合，逗号分割（例如："1,2,3" 或 "1"）
        返回：
            删除结果，成功返回true
        """
        url = f"{self.base_url}/qw/knife/web/from/mes/cutter/delBrand"

        try:
            # 验证ids参数
            if not ids or ids.strip() == "":
                return {
                    "code": 400,
                    "msg": "删除ID不能为空",
                    "success": False,
                    "data": False
                }

            # 构建请求参数（使用query参数）
            params = {
                "ids": ids
            }

            logger.info(f"删除品牌信息，参数: {params}")

            # 发起POST请求，使用params传递query参数
            response = self.session.post(url, params=params, timeout=10)
            response.raise_for_status()

            result = response.json()
            logger.info(f"删除品牌信息成功: {result}")

            return result

        except requests.exceptions.RequestException as e:
            logger.error(f"删除品牌信息失败: {e}")
            return {
                "code": 500,
                "msg": f"请求失败: {str(e)}",
                "success": False,
                "data": False
            }
        except Exception as e:
            logger.error(f"处理删除品牌信息数据失败: {e}")
            return {
                "code": 500,
                "msg": f"数据处理失败: {str(e)}",
                "success": False,
                "data": False
            }

    def get_stock_put_list(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        获取收刀柜信息
        接口地址: /qw/knife/app/from/mes/cabinet/stockPutList
        请求方式: GET

        参数：
            params: 查询参数，包括：
                - cabinetCode: 刀柜编码
                - stockLoc: 库位号
                - locPrefix: 柜子ABCDE面
                - stockStatus: 库位状态
                - isBan: 绑定状态（是否禁用 0:非禁用 1:禁用）
                - borrowStatus: 还刀状态（0:修磨 1:报废 2:换线 3:错领）
                - storageType: 暂存类型（0:公共暂存 1:个人暂存 2:扩展取刀）
        返回：
            收刀柜信息列表
        """
        url = f"{self.base_url}/qw/knife/app/from/mes/cabinet/stockPutList"

        try:
            # 构建请求参数，过滤掉None值
            request_params = {}

            if params:
                # 基本查询参数
                if params.get("cabinetCode"):
                    request_params["cabinetCode"] = params["cabinetCode"]

                if params.get("stockLoc"):
                    request_params["stockLoc"] = params["stockLoc"]

                if params.get("locPrefix"):
                    request_params["locPrefix"] = params["locPrefix"]

                if params.get("stockStatus") is not None:
                    request_params["stockStatus"] = params["stockStatus"]

                if params.get("isBan") is not None:
                    request_params["isBan"] = params["isBan"]

                if params.get("borrowStatus") is not None:
                    request_params["borrowStatus"] = params["borrowStatus"]

                if params.get("storageType") is not None:
                    request_params["storageType"] = params["storageType"]

            logger.info(f"请求收刀柜信息列表，参数: {request_params}")

            # 发起GET请求
            response = self.session.get(url, params=request_params, timeout=10)
            response.raise_for_status()

            result = response.json()

            return result

        except requests.exceptions.RequestException as e:
            logger.error(f"获取收刀柜信息列表失败: {e}")
            return {
                "code": 500,
                "msg": f"请求失败: {str(e)}",
                "success": False,
                "data": []
            }
        except Exception as e:
            logger.error(f"处理收刀柜信息列表数据失败: {e}")
            return {
                "code": 500,
                "msg": f"数据处理失败: {str(e)}",
                "success": False,
                "data": []
            }

    def unbind_stock_cutter(self, stock_id: int) -> Dict[str, Any]:
        """
        货道解绑耗材（清空刀具数量）
        接口地址: /qw/knife/web/from/mes/cabinetStock/stockUnBindCutter
        请求方式: POST
        请求数据类型: application/json

        参数：
            stock_id: 刀柜货道主键
        返回：
            解绑结果，成功返回true
        """
        url = f"{self.base_url}/qw/knife/web/from/mes/cabinetStock/stockUnBindCutter"

        try:
            # 验证stock_id参数
            if stock_id is None:
                return {
                    "code": 400,
                    "msg": "货道ID不能为空",
                    "success": False,
                    "data": False
                }

            # 构建请求参数（使用query参数）
            params = {
                "stockId": stock_id
            }

            logger.info(f"解绑货道耗材，参数: {params}")

            # 发起POST请求，使用params传递query参数
            response = self.session.post(url, params=params, timeout=10)
            response.raise_for_status()

            result = response.json()
            logger.info(f"解绑货道耗材成功: {result}")

            return result

        except requests.exceptions.RequestException as e:
            logger.error(f"解绑货道耗材失败: {e}")
            return {
                "code": 500,
                "msg": f"请求失败: {str(e)}",
                "success": False,
                "data": False
            }
        except Exception as e:
            logger.error(f"处理解绑货道耗材数据失败: {e}")
            return {
                "code": 500,
                "msg": f"数据处理失败: {str(e)}",
                "success": False,
                "data": False
            }

    def change_stock_ban_status(self, stock_id: int, is_ban: int) -> Dict[str, Any]:
        """
        货道禁用/启用库位
        接口地址: /qw/knife/web/from/mes/cabinetStock/changeBan
        请求方式: POST
        请求数据类型: application/json

        参数：
            stock_id: 刀柜货道主键
            is_ban: 0-非禁用（启用） 1-禁用
        返回：
            操作结果，成功返回true
        """
        url = f"{self.base_url}/qw/knife/web/from/mes/cabinetStock/changeBan"

        try:
            # 验证参数
            if stock_id is None:
                return {
                    "code": 400,
                    "msg": "货道ID不能为空",
                    "success": False,
                    "data": False
                }

            if is_ban not in [0, 1]:
                return {
                    "code": 400,
                    "msg": "禁用状态参数错误，应为0或1",
                    "success": False,
                    "data": False
                }

            # 构建请求参数（使用query参数）
            params = {
                "stockId": stock_id,
                "isBan": is_ban
            }

            operation = "禁用" if is_ban == 1 else "启用"
            logger.info(f"{operation}货道库位，参数: {params}")

            # 发起POST请求，使用params传递query参数
            response = self.session.post(url, params=params, timeout=10)
            response.raise_for_status()

            result = response.json()
            logger.info(f"{operation}货道库位成功: {result}")

            return result

        except requests.exceptions.RequestException as e:
            logger.error(f"修改货道禁用状态失败: {e}")
            return {
                "code": 500,
                "msg": f"请求失败: {str(e)}",
                "success": False,
                "data": False
            }
        except Exception as e:
            logger.error(f"处理修改货道禁用状态数据失败: {e}")
            return {
                "code": 500,
                "msg": f"数据处理失败: {str(e)}",
                "success": False,
                "data": False
            }

    def get_stock_statistical_num(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        获取货道统计数据
        接口地址: /qw/knife/app/from/mes/cabinet/stockStatisticalNum
        请求方式: GET

        参数：
            params: 查询参数，包括：
                - cabinetCode: 刀柜编码
                - locPrefix: 柜子ABCDE面
                - locType: 库位类型（收刀柜:0 取刀柜:1，默认0）
        返回：
            货道统计数据，包括：
                - totalNum: 货道总数
                - disableNum: 禁用数量
                - freeNum: 空闲数量
                - workNum: 占用数量
                - makeAlarm: 库存告警值
        """
        url = f"{self.base_url}/qw/knife/app/from/mes/cabinet/stockStatisticalNum"

        try:
            # 构建请求参数，过滤掉None值
            request_params = {}

            if params:
                # 刀柜编码
                if params.get("cabinetCode"):
                    request_params["cabinetCode"] = params["cabinetCode"]

                # 柜子面
                if params.get("locPrefix"):
                    request_params["locPrefix"] = params["locPrefix"]

                # 库位类型（默认0-收刀柜）
                if params.get("locType") is not None:
                    request_params["locType"] = params["locType"]
                else:
                    # 默认为收刀柜
                    request_params["locType"] = 0
            else:
                # 如果没有传递参数，默认查询收刀柜
                request_params["locType"] = 0

            logger.info(f"请求货道统计数据，参数: {request_params}")

            # 发起GET请求
            response = self.session.get(url, params=request_params, timeout=10)
            response.raise_for_status()

            result = response.json()
            logger.info(f"获取货道统计数据成功: {result}")

            return result

        except requests.exceptions.RequestException as e:
            logger.error(f"获取货道统计数据失败: {e}")
            return {
                "code": 500,
                "msg": f"请求失败: {str(e)}",
                "success": False,
                "data": {
                    "totalNum": 0,
                    "disableNum": 0,
                    "freeNum": 0,
                    "workNum": 0,
                    "makeAlarm": 0
                }
            }
        except Exception as e:
            logger.error(f"处理货道统计数据失败: {e}")
            return {
                "code": 500,
                "msg": f"数据处理失败: {str(e)}",
                "success": False,
                "data": {
                    "totalNum": 0,
                    "disableNum": 0,
                    "freeNum": 0,
                    "workNum": 0,
                    "makeAlarm": 0
                }
            }

    def get_stock_take_list(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        获取取刀柜信息
        接口地址: /qw/knife/app/from/mes/cabinet/stockTakeList
        请求方式: GET

        参数：
            params: 查询参数，包括：
                - brandCode: 品牌编码
                - cabinetCode: 刀柜编码
                - cutterCode: 刀具型号
                - cutterType: 刀具类型
                - locPrefix: 柜子ABCDE面
                - stockLoc: 库位号
                - cutterOrBrand: 耗材型号或品牌
                - materialCode: 物料编码
                - specification: 规格
        返回：
            取刀柜信息列表
        """
        url = f"{self.base_url}/qw/knife/app/from/mes/cabinet/stockTakeList"

        try:
            # 构建请求参数，过滤掉None值
            request_params = {}

            if params:
                # 基本查询参数
                if params.get("brandCode"):
                    request_params["brandCode"] = params["brandCode"]

                if params.get("cabinetCode"):
                    request_params["cabinetCode"] = params["cabinetCode"]

                if params.get("cutterCode"):
                    request_params["cutterCode"] = params["cutterCode"]

                if params.get("cutterType"):
                    request_params["cutterType"] = params["cutterType"]

                if params.get("locPrefix"):
                    request_params["locPrefix"] = params["locPrefix"]

                if params.get("stockLoc"):
                    request_params["stockLoc"] = params["stockLoc"]

                if params.get("cutterOrBrand"):
                    request_params["cutterOrBrand"] = params["cutterOrBrand"]

                if params.get("materialCode"):
                    request_params["materialCode"] = params["materialCode"]

                if params.get("specification"):
                    request_params["specification"] = params["specification"]

            logger.info(f"请求取刀柜信息列表，参数: {request_params}")

            # 发起GET请求
            response = self.session.get(url, params=request_params, timeout=10)
            response.raise_for_status()

            result = response.json()

            return result

        except requests.exceptions.RequestException as e:
            logger.error(f"获取取刀柜信息列表失败: {e}")
            return {
                "code": 500,
                "msg": f"请求失败: {str(e)}",
                "success": False,
                "data": []
            }
        except Exception as e:
            logger.error(f"处理取刀柜信息列表数据失败: {e}")
            return {
                "code": 500,
                "msg": f"数据处理失败: {str(e)}",
                "success": False,
                "data": []
            }

    def pre_batch_plug(self, cabinet_code: str) -> Dict[str, Any]:
        """
        预补刀查询（获取耗材是否可以补刀）
        接口地址: /qw/knife/web/from/mes/cabinetStock/preBatchPlug
        请求方式: POST
        请求数据类型: application/json

        参数：
            cabinet_code: 刀柜编码
        返回：
            补刀检查结果，包括：
                - successStock: 可以补刀的货道列表
                - errorStock: 不能补刀的货道列表
        """
        url = f"{self.base_url}/qw/knife/web/from/mes/cabinetStock/preBatchPlug"

        try:
            # 验证cabinet_code参数
            if not cabinet_code or cabinet_code.strip() == "":
                return {
                    "code": 400,
                    "msg": "刀柜编码不能为空",
                    "success": False,
                    "data": {
                        "successStock": [],
                        "errorStock": []
                    }
                }

            # 构建请求参数（使用query参数）
            params = {
                "cabinetCode": cabinet_code
            }

            logger.info(f"预补刀查询，参数: {params}")

            # 发起POST请求，使用params传递query参数
            response = self.session.post(url, params=params, timeout=10)
            response.raise_for_status()

            result = response.json()
            logger.info(f"预补刀查询成功: {result}")

            return result

        except requests.exceptions.RequestException as e:
            logger.error(f"预补刀查询失败: {e}")
            return {
                "code": 500,
                "msg": f"请求失败: {str(e)}",
                "success": False,
                "data": {
                    "successStock": [],
                    "errorStock": []
                }
            }
        except Exception as e:
            logger.error(f"处理预补刀查询数据失败: {e}")
            return {
                "code": 500,
                "msg": f"数据处理失败: {str(e)}",
                "success": False,
                "data": {
                    "successStock": [],
                    "errorStock": []
                }
            }

    def on_pre_batch_plug(self, cabinet_code: str) -> Dict[str, Any]:
        """
        批量一键补刀
        接口地址: /qw/knife/web/from/mes/cabinetStock/onPreBatchPlug
        请求方式: POST
        请求数据类型: application/json

        参数：
            cabinet_code: 刀柜编码
        返回：
            补刀结果，成功返回true
        """
        url = f"{self.base_url}/qw/knife/web/from/mes/cabinetStock/onPreBatchPlug"

        try:
            # 验证cabinet_code参数
            if not cabinet_code or cabinet_code.strip() == "":
                return {
                    "code": 400,
                    "msg": "刀柜编码不能为空",
                    "success": False,
                    "data": False
                }

            # 构建请求参数（使用query参数）
            params = {
                "cabinetCode": cabinet_code
            }

            logger.info(f"批量补刀，参数: {params}")

            # 发起POST请求，使用params传递query参数
            response = self.session.post(url, params=params, timeout=10)
            response.raise_for_status()

            result = response.json()
            logger.info(f"批量补刀成功: {result}")

            return result

        except requests.exceptions.RequestException as e:
            logger.error(f"批量补刀失败: {e}")
            return {
                "code": 500,
                "msg": f"请求失败: {str(e)}",
                "success": False,
                "data": False
            }
        except Exception as e:
            logger.error(f"处理批量补刀数据失败: {e}")
            return {
                "code": 500,
                "msg": f"数据处理失败: {str(e)}",
                "success": False,
                "data": False
            }

    # ==================== 统计接口方法（修正版） ====================

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
        调用外部接口：/qw/knife/web/from/mes/cabinetStock/stockLocTakeInfoList
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
        """
        try:
            # 构建查询参数
            query_params = {k: v for k, v in params.items() if v is not None}

            # 调用外部接口
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

    # ==================== 合并自 系统记录 模块的API客户端 ====================
    # 合并日期: 2025-11-15
    # 来源: teamleader_record/api_client.py

    # 补货记录API客户端 (班组长)
    def get_replenish_records(self,
                              current: Optional[int] = None,
                              endTime: Optional[str] = None,
                              order: Optional[int] = None,
                              rankingType: Optional[int] = None,
                              recordStatus: Optional[int] = None,
                              size: Optional[int] = None,
                              startTime: Optional[str] = None) -> Dict[str, Any]:
        """
        获取补货记录列表 (班组长)

        Args:
            current: 当前页
            endTime: 结束时间
            order: 顺序 0: 从大到小 1：从小到大
            rankingType: 0: 数量 1: 金额
            recordStatus: 0: 取刀 1: 还刀 2: 收刀 3: 暂存 4: 完成 5：违规还刀
            size: 每页的数量
            startTime: 开始时间

        Returns:
            Dict: API响应结果，包含以下字段：
                - code: 响应码
                - msg: 响应消息
                - success: 是否成功
                - data: 补货记录数据，包含以下子字段：
                    - current: 当前页码
                    - pages: 总页数
                    - records: 记录列表，每条记录包含以下字段：
                        - lendUserName: 取出人
                        - storageUserName: 暂存人
                        - brandName: 品牌名称
                        - cutterType: 电池类型
                        - cutterCode: 刀具型号
                        - specification: 规格
                        - quantity: 数量
                        - oldPrice: 老单价
                        - newPrice: 新单价
                        - oldStockNum: 操作前库存数
                        - newStockNum: 操作后库存数
                        - stockLoc: 库位号
                        - logType: 补货类型
                        - status: 业务状态
                        - cabinetCode: 刀柜编码
                        - createTime: 创建时间
                        - operator: 操作人
                        - materialCode: 物料编码
                        - detailsCode: 操作详情
                        - remake: 备注
                        - createDept: 创建部门
                        - createUser: 创建人
                        - updateUser: 更新人
                        - tenantId: 租户ID
                        - isDeleted: 是否已删除
                    - size: 每页记录数
                    - total: 总记录数
        """
        url = urljoin(self.base_url, "/qw/knife/web/from/mes/record/replenishList/teamleader")

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
        导出补货记录 (班组长)

        Args:
            endTime: 结束时间
            order: 顺序 0: 从大到小 1：从小到大
            rankingType: 0: 数量 1: 金额
            recordStatus: 0: 取刀 1: 还刀 2: 收刀 3: 暂存 4: 完成 5：违规还刀
            startTime: 开始时间

        Returns:
            bytes: 导出的Excel文件内容，包含以下字段：
                - lendUserName: 取出人
                - storageUserName: 暂存人
                - brandName: 品牌名称
                - cutterType: 电池类型
                - cutterCode: 刀具型号
                - specification: 规格
                - quantity: 数量
                - oldPrice: 老单价
                - newPrice: 新单价
                - oldStockNum: 操作前库存数
                - newStockNum: 操作后库存数
                - stockLoc: 库位号
                - logType: 补货类型
                - status: 业务状态
                - cabinetCode: 刀柜编码
                - createTime: 创建时间
                - operator: 操作人
                - materialCode: 物料编码
                - detailsCode: 操作详情
                - remake: 备注
                - createDept: 创建部门
                - createUser: 创建人
                - updateUser: 更新人
                - tenantId: 租户ID
                - isDeleted: 是否已删除
        """
        url = urljoin(self.base_url, "/qw/knife/web/from/mes/record/exportReplenishRecord/teamleader")

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

    # 领刀记录API客户端 (班组长)
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
        获取领刀记录列表 (班组长)

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
        url = urljoin(self.base_url, "/qw/knife/web/from/mes/record/lendList/teamleader")

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
        导出领刀记录 (班组长)

        Args:
            endTime: 结束时间
            order: 顺序 0: 从大到小 1：从小到大
            rankingType: 0: 数量 1: 金额
            recordStatus: 0: 取刀 1: 还刀 2: 收刀 3: 暂存 4: 完成 5：违规还刀
            startTime: 开始时间

        Returns:
            bytes: 导出的文件内容
        """
        url = urljoin(self.base_url, "/qw/knife/web/from/mes/record/exportLendRecord/teamleader")

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

    # 告警预警API客户端 (班组长)
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
            Dict: API响应结果
        """
        url = urljoin(self.base_url, "/qw/knife/web/from/mes/alarm/warning/list/teamleader")

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
        获取告警统计信息 (班组长)

        Returns:
            Dict: API响应结果
        """
        url = urljoin(self.base_url, "/qw/knife/web/from/mes/alarm/warning/statistics/teamleader")

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
        更新告警阈值 (班组长)

        Args:
            locSurplus: 货道
            alarmThreshold: 告警阈值

        Returns:
            Dict: API响应结果
        """
        url = urljoin(self.base_url, "/qw/knife/web/from/mes/alarm/warning/threshold/teamleader")

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
        处理告警预警 (班组长)

        Args:
            id: 告警ID
            handleStatus: 处理状态 (0: 未处理, 1: 已处理, 2: 已忽略)
            handleRemark: 处理备注

        Returns:
            Dict: API响应结果
        """
        url = urljoin(self.base_url, f"/qw/knife/web/from/mes/alarm/warning/{id}/handle/teamleader")

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
        批量处理告警预警 (班组长)

        Args:
            ids: 告警ID列表
            handleStatus: 处理状态 (0: 未处理, 1: 已处理, 2: 已忽略)
            handleRemark: 处理备注

        Returns:
            Dict: API响应结果
        """
        url = urljoin(self.base_url, "/qw/knife/web/from/mes/alarm/warning/batch/handle/teamleader")

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
        导出告警预警 (班组长)

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
        url = urljoin(self.base_url, "/qw/knife/web/from/mes/alarm/warning/export/teamleader")

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

    # 公共暂存记录API客户端 (班组长)
    def get_storage_records(self,
                            current: Optional[int] = None,
                            endTime: Optional[str] = None,
                            order: Optional[int] = None,
                            rankingType: Optional[int] = None,
                            recordStatus: Optional[int] = None,
                            size: Optional[int] = None,
                            startTime: Optional[str] = None) -> Dict[str, Any]:
        """
        获取公共暂存记录列表 (班组长)

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
        url = urljoin(self.base_url, "/qw/knife/web/from/mes/record/storageList/teamleader")

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
        导出公共暂存记录 (班组长)

        Args:
            endTime: 结束时间
            order: 顺序 0: 从大到小 1：从小到大
            rankingType: 0: 数量 1: 金额
            recordStatus: 0: 取刀 1: 还刀 2: 收刀 3: 暂存 4: 完成 5：违规还刀
            startTime: 开始时间

        Returns:
            bytes: 导出的文件内容
        """
        url = urljoin(self.base_url, "/qw/knife/web/from/mes/record/exportStorageRecord/teamleader")

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


# 初始化API客户端
# 使用配置文件的设置
try:
    from config.config import settings

    # 优先使用环境变量ORIGINAL_API_KEY
    # 其次尝试从token.txt文件读取
    api_key = settings.ORIGINAL_API_KEY if settings.ORIGINAL_API_KEY else None

    teamleader_api_client = TeamLeaderAPIClient(
        base_url=settings.ORIGINAL_API_BASE_URL,
        api_key=api_key,
        token_file=settings.TOKEN_FILE_PATH
    )
except ImportError:
    # 如果无法导入配置，使用默认配置
    teamleader_api_client = TeamLeaderAPIClient(
        base_url="http://39.38.115.114:8983",  # 请替换为你的真实API地址
        api_key=None,
        token_file="token.txt"
    )