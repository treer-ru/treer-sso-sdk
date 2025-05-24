#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Treer SSO SDK 基础使用示例

此示例展示如何使用SDK进行用户认证
"""

import asyncio
import os
from treer_sso_sdk import get_user_info_by_code, SSOError


async def basic_example():
    """基础使用示例：使用便捷函数"""
    
    # 从环境变量获取配置（推荐做法）
    client_id = os.getenv("SSO_CLIENT_ID", "your_client_id")
    client_secret = os.getenv("SSO_CLIENT_SECRET", "your_client_secret")
    
    # 模拟从OAuth回调获取的授权码
    authorization_code = "example_auth_code"
    
    try:
        print("正在通过授权码获取用户信息...")
        
        user_info = await get_user_info_by_code(
            authorization_code=authorization_code,
            client_id=client_id,
            client_secret=client_secret,
            # sso_base_url="https://sso-api.treer.ru",  # 可选，使用默认值
            timeout=30  # 可选，30秒超时
        )
        
        # 打印用户信息
        print("=" * 50)
        print("用户信息获取成功！")
        print("=" * 50)
        print(f"用户ID: {user_info.id}")
        print(f"用户名: {user_info.username}")
        print(f"邮箱: {user_info.email or '未设置'}")
        print(f"电话: {user_info.phone or '未设置'}")
        print(f"激活状态: {'激活' if user_info.is_active else '未激活'}")
        
        if user_info.profile:
            print(f"姓名: {user_info.profile.full_name or '未设置'}")
            print(f"语言: {user_info.profile.locale}")
            print(f"时区: {user_info.profile.timezone}")
            if user_info.profile.avatar_url:
                print(f"头像: {user_info.profile.avatar_url}")
        
        print("=" * 50)
        
    except SSOError as e:
        print(f"SSO错误: {e}")
        if e.error_code:
            print(f"错误代码: {e.error_code}")
        if e.details:
            print(f"详细信息: {e.details}")
            
    except Exception as e:
        print(f"未知错误: {e}")


if __name__ == "__main__":
    print("Treer SSO SDK 基础使用示例")
    print("请确保设置了正确的环境变量:")
    print("- SSO_CLIENT_ID")
    print("- SSO_CLIENT_SECRET")
    print()
    
    asyncio.run(basic_example()) 