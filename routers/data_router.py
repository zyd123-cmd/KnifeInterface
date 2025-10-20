from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
import time

from administrator.services.api_client import original_api_client
from administrator.schemas.data_schemas import EnhancedUserResponse, OriginalUserResponse

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