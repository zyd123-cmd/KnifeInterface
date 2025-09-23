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


@router.get("/return_info/list", response_model=ReturnInfoListResponse)
async def list_return_info(page: int = 1, size: int = 10):
    """
    获取还刀信息列表
    """
    try:
        # 调用API客户端获取数据
        result = original_api_client.get_return_info_list({
            "page": page,
            "size": size
        })
        return ReturnInfoListResponse(
            list=[ReturnInfo(**item) for item in result.get("list", [])],
            total=result.get("total", 0)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取还刀信息列表失败: {str(e)}")

@router.post("/return_info", response_model=ReturnInfo)
async def create_return_info(data: ReturnInfoCreate):
    """
    创建还刀信息
    """
    try:
        # 调用实际后端服务
        result = original_api_client.create_return_info(data)
        return ReturnInfo(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建还刀信息失败: {str(e)}")

@router.put("/return_info", response_model=ReturnInfo)
async def update_return_info(data: ReturnInfoUpdate):
    """
    更新还刀信息
    """
    try:
        result = original_api_client.update_return_info(data)
        return ReturnInfo(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新还刀信息失败: {str(e)}")

@router.delete("/return_info/{info_id}")
async def delete_return_info(info_id: int):
    """
    删除还刀信息
    """
    try:
        result = original_api_client.delete_return_info(info_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除还刀信息失败: {str(e)}")

@router.get("/return_info/export")
async def export_return_info():
    """
    导出还刀信息
    """
    try:
        result = original_api_client.export_return_info()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"导出还刀信息失败: {str(e)}")