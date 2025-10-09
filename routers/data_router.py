from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
import time
from administrator.services.api_client import original_api_client
from administrator.schemas.data_schemas import OriginalUserResponse, EnhancedUserResponse
from administrator.schemas.data_schemas import ReturnInfo,ReturnInfoListResponse,ReturnInfoCreate,ReturnInfoUpdate
router = APIRouter()

@router.get("/users/{user_id}", response_model=EnhancedUserResponse)
async def get_enhanced_user_data(user_id: int):
    """
    获取增强后的用户数据
    - 从原始API获取基础用户信息
    - 从原始API获取用户的帖子数据
    - 进行数据整合和增强
    """
    try:
        # 并行获取用户数据和帖子数据（在实际应用中可以使用异步优化）
        user_data = original_api_client.get_user_data(user_id)
        user_posts = original_api_client.get_user_posts(user_id)

        # 在这里进行你的二次封装逻辑
        enhanced_data = {
            "user_id": user_data["id"],
            "user_name": user_data["name"],
            "email_address": user_data["email"],
            "account_status": "active" if user_data.get("id", 0) % 2 == 0 else "inactive",
            "additional_data": {
                "posts_count": len(user_posts),
                "last_post_title": user_posts[0]["title"] if user_posts else None,
                "processing_notes": "数据已成功封装和增强"
            },
            "processed_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }

        return enhanced_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"数据处理失败: {str(e)}")


@router.get("/users/{user_id}/basic", response_model=OriginalUserResponse)
async def get_original_user_data(user_id: int):
    """
    直接返回从原始API获取的用户数据（示例：直接透传）
    """
    try:
        user_data = original_api_client.get_user_data(user_id)
        return user_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取原始数据失败: {str(e)}")


@router.get("/status")
async def api_status():
    """获取API服务状态"""
    return {
        "status": "operational",
        "service": "secondary-api-wrapper",
        "version": "1.0.0",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }

@router.get("/borrowReturnInfo/returnInfo/list", response_model=ReturnInfoListResponse)
async def list_return_info(page: int = 1, size: int = 10, query: dict = {}):
    """
    获取还刀信息列表
    """
    try:
        result = original_api_client.get_return_info_list({
            "page": page,
            "size": size,
            "query": query
        })
        return ReturnInfoListResponse(
            list=[ReturnInfo(**item) for item in result.get("list", [])],
            total=result.get("total", 0)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取还刀信息列表失败: {str(e)}")

# 查询还刀信息详细
@router.get("/borrowReturnInfo/returnInfo/{id}", response_model=ReturnInfo)
async def get_return_info(id: int):
    """
    查询还刀信息详情
    """
    try:
        result = original_api_client.get_return_info(id)
        return ReturnInfo(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询还刀信息详情失败: {str(e)}")

# 新增还刀信息
@router.post("/borrowReturnInfo/returnInfo", response_model=ReturnInfo)
async def create_return_info(data: ReturnInfoCreate):
    """
    创建还刀信息
    """
    try:
        result = original_api_client.create_return_info(data)
        return ReturnInfo(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建还刀信息失败: {str(e)}")

# 修改还刀信息
@router.put("/borrowReturnInfo/returnInfo", response_model=ReturnInfo)
async def update_return_info(data: ReturnInfoUpdate):
    """
    更新还刀信息
    """
    try:
        result = original_api_client.update_return_info(data)
        return ReturnInfo(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新还刀信息失败: {str(e)}")

# 删除还刀信息
@router.delete("/borrowReturnInfo/returnInfo/{id}")
async def delete_return_info(id: int):
    """
    删除还刀信息
    """
    try:
        result = original_api_client.delete_return_info(id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除还刀信息失败: {str(e)}")

# 导出还刀信息
@router.get("/borrowReturnInfo/returnInfo/export")
async def export_return_info(query: dict = {}):
    """
    导出还刀信息
    """
    try:
        result = original_api_client.export_return_info(query)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"导出还刀信息失败: {str(e)}")