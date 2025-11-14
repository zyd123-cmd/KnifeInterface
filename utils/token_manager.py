"""
Token管理工具
用于登录获取新Token并自动保存到token.txt文件
"""
import requests
import logging
import os
from typing import Dict, Any, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TokenManager:
    """Token管理器 - 负责登录和Token刷新"""
    
    def __init__(self):
        self.login_url = "https://www.weiliansmartcabinet.com/api/blade-auth/oauth/token"
        self.project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.token_file = os.path.join(self.project_root, "token.txt")
    
    def login(self, username: str, password: str) -> Optional[str]:
        """
        使用账号密码登录获取Token
        
        参数:
            username: 用户名
            password: MD5加密后的密码
        
        返回:
            Token字符串，失败返回None
        """
        # 请求参数
        data = {
            "username": username,
            "password": password,
            "grantTypeInfo": "web",  # 使用web方式登录，而不是applet
            "grant_type": "captcha"
        }
        
        # 请求头
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": "Basic c2FiZXI6c2FiZXJfc2VjcmV0"
        }
        
        try:
            logger.info(f"正在为用户 {username} 登录...")
            
            # 发送登录请求
            response = requests.post(
                self.login_url,
                data=data,
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            
            # 解析响应
            result = response.json()
            
            # 打印完整响应用于调试
            logger.info(f"响应状态码: {response.status_code}")
            logger.info(f"响应内容: {result}")
            
            # 检查响应格式：直接返回access_token，没有success字段
            token = result.get("access_token")
            if token:
                logger.info("✅ 登录成功！")
                logger.info(f"Token有效期: {result.get('expires_in')} 秒")
                return token
            else:
                # 如果没有access_token，尝试检查是否有错误信息
                error_msg = result.get('msg') or result.get('error_description') or '未知错误'
                logger.error(f"❌ 登录失败: {error_msg}")
                logger.error(f"完整响应: {result}")
                return None
                
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ 登录请求失败: {e}")
            return None
        except Exception as e:
            logger.error(f"❌ 登录过程出错: {e}")
            return None
    
    def save_token(self, token: str) -> bool:
        """
        保存Token到token.txt文件
        
        参数:
            token: Token字符串
        
        返回:
            True表示保存成功，False表示失败
        """
        try:
            with open(self.token_file, 'w', encoding='utf-8') as f:
                f.write(token)
            logger.info(f"✅ Token已保存到: {self.token_file}")
            return True
        except Exception as e:
            logger.error(f"❌ 保存Token失败: {e}")
            return False
    
    def refresh_token(self, username: str, password: str) -> bool:
        """
        刷新Token（登录并保存）
        
        参数:
            username: 用户名
            password: MD5加密后的密码
        
        返回:
            True表示刷新成功，False表示失败
        """
        logger.info("========== Token刷新开始 ==========")
        
        # 登录获取新Token
        token = self.login(username, password)
        if not token:
            logger.error("❌ Token刷新失败")
            return False
        
        # 保存Token
        if self.save_token(token):
            logger.info("✅ Token刷新成功！")
            logger.info("===================================")
            return True
        else:
            logger.error("❌ Token刷新失败")
            return False
    
    def get_current_token(self) -> Optional[str]:
        """
        读取当前保存的Token
        
        返回:
            Token字符串，失败返回None
        """
        try:
            if os.path.exists(self.token_file):
                with open(self.token_file, 'r', encoding='utf-8') as f:
                    token = f.read().strip()
                    return token if token else None
            else:
                logger.warning(f"Token文件不存在: {self.token_file}")
                return None
        except Exception as e:
            logger.error(f"读取Token失败: {e}")
            return None


# 便捷函数
def refresh_token(username: str = "李敖", password: str = "e52ca69c7b3f5c50483cf9c821e77157"):
    """
    快捷刷新Token函数
    
    参数:
        username: 用户名，默认"李敖"
        password: MD5密码，默认"e52ca69c7b3f5c50483cf9c821e77157"
    """
    manager = TokenManager()
    return manager.refresh_token(username, password)


# 主程序 - 可以直接运行此脚本刷新Token
if __name__ == "__main__":
    import sys
    
    print("\n" + "="*50)
    print("          Token 刷新工具")
    print("="*50 + "\n")
    
    # 检查是否提供了命令行参数
    if len(sys.argv) >= 3:
        username = sys.argv[1]
        password = sys.argv[2]
        print(f"使用提供的账号: {username}")
    else:
        # 使用默认账号
        username = "李敖"
        password = "e52ca69c7b3f5c50483cf9c821e77157"
        print(f"使用默认账号: {username}")
    
    print()
    
    # 执行刷新
    success = refresh_token(username, password)
    
    if success:
        print("\n✅ Token刷新完成！可以重启服务使用新Token。\n")
        sys.exit(0)
    else:
        print("\n❌ Token刷新失败！请检查账号密码或网络连接。\n")
        sys.exit(1)
