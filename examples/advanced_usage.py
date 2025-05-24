#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Treer SSO SDK 高级使用示例

此示例展示如何使用客户端类进行更复杂的操作
"""

import asyncio
import os
from treer_sso_sdk import TreerSSOClient, SSOConfig, SSOError


async def advanced_example():
    """高级使用示例：使用客户端类"""
    
    # 配置SSO客户端
    config = SSOConfig(
        client_id=os.getenv("SSO_CLIENT_ID", "your_client_id"),
        client_secret=os.getenv("SSO_CLIENT_SECRET", "your_client_secret"),
        sso_base_url="https://sso-api.treer.ru",  # 生产环境
        timeout=30,  # 30秒超时
        max_retries=3,  # 最大重试3次
        verify_ssl=True  # 验证SSL证书
    )
    
    print("配置信息:")
    print(f"- SSO服务地址: {config.sso_base_url}")
    print(f"- 超时时间: {config.timeout}秒")
    print(f"- 最大重试: {config.max_retries}次")
    print()
    
    # 模拟授权码
    authorization_code = "example_auth_code"
    redirect_uri = "https://yourapp.com/callback"
    
    # 使用异步上下文管理器
    async with TreerSSOClient(config) as client:
        try:
            print("方法1: 分步获取用户信息")
            print("-" * 30)
            
            # 步骤1: 获取访问令牌
            print("正在获取访问令牌...")
            token_response = await client.get_access_token(
                authorization_code=authorization_code,
                redirect_uri=redirect_uri
            )
            
            print(f"访问令牌: {token_response.access_token[:20]}...")
            print(f"令牌类型: {token_response.token_type}")
            if token_response.expires_in:
                print(f"有效期: {token_response.expires_in}秒")
            print()
            
            # 步骤2: 获取用户信息
            print("正在获取用户信息...")
            user_info = await client.get_user_info(token_response.access_token)
            
            print_user_info(user_info)
            
            print("\n" + "="*50 + "\n")
            
            print("方法2: 一步获取用户信息")
            print("-" * 30)
            
            # 一步到位获取用户信息
            user_info2 = await client.get_user_info_by_code(
                authorization_code=authorization_code,
                redirect_uri=redirect_uri
            )
            
            print_user_info(user_info2)
            
        except SSOError as e:
            print(f"SSO错误: {e}")
            print(f"错误类型: {type(e).__name__}")
            if e.error_code:
                print(f"错误代码: {e.error_code}")
            if e.details:
                print(f"详细信息: {e.details}")
                
        except Exception as e:
            print(f"未知错误: {e}")


def print_user_info(user_info):
    """打印用户信息的辅助函数"""
    print("用户信息:")
    print(f"  ID: {user_info.id}")
    print(f"  用户名: {user_info.username}")
    print(f"  邮箱: {user_info.email or '未设置'}")
    print(f"  电话: {user_info.phone or '未设置'}")
    print(f"  状态: {'激活' if user_info.is_active else '未激活'}")
    
    if user_info.profile:
        print(f"  档案信息:")
        print(f"    姓名: {user_info.profile.full_name or '未设置'}")
        print(f"    语言: {user_info.profile.locale}")
        print(f"    时区: {user_info.profile.timezone}")
        if user_info.profile.avatar_url:
            print(f"    头像: {user_info.profile.avatar_url}")
        if user_info.profile.additional_info:
            print(f"    其他信息: {user_info.profile.additional_info}")
    
    if user_info.created_at:
        print(f"  创建时间: {user_info.created_at}")
    if user_info.updated_at:
        print(f"  更新时间: {user_info.updated_at}")


async def error_handling_example():
    """错误处理示例"""
    from treer_sso_sdk import (
        SSOConfigError, 
        SSOInvalidCodeError, 
        SSONetworkError
    )
    
    print("错误处理示例")
    print("=" * 30)
    
    try:
        # 故意使用无效配置
        config = SSOConfig(
            client_id="",  # 空的client_id会触发配置错误
            client_secret="test"
        )
    except SSOConfigError as e:
        print(f"配置错误: {e}")
    
    try:
        config = SSOConfig(
            client_id="test_client",
            client_secret="test_secret"
        )
        
        async with TreerSSOClient(config) as client:
            # 使用无效的授权码
            await client.get_user_info_by_code("invalid_code")
            
    except SSOInvalidCodeError as e:
        print(f"无效授权码: {e}")
    except SSONetworkError as e:
        print(f"网络错误: {e}")
    except SSOError as e:
        print(f"其他SSO错误: {e}")


if __name__ == "__main__":
    print("Treer SSO SDK 高级使用示例")
    print("请确保设置了正确的环境变量:")
    print("- SSO_CLIENT_ID")
    print("- SSO_CLIENT_SECRET")
    print()
    
    # 运行高级示例
    asyncio.run(advanced_example())
    
    print("\n" + "="*60 + "\n")
    
    # 运行错误处理示例
    asyncio.run(error_handling_example())