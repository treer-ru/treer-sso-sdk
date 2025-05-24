#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
构建脚本

用于构建和发布Treer SSO SDK包到PyPI
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def run_command(cmd, check=True):
    """运行命令"""
    print(f"运行命令: {cmd}")
    result = subprocess.run(cmd, shell=True, check=check)
    return result


def clean():
    """清理构建文件"""
    print("清理构建文件...")
    
    # 要清理的目录和文件
    clean_targets = [
        "dist",
        "build",
        "*.egg-info",
        "src/*.egg-info",
        "__pycache__",
        "*.pyc",
        "*.pyo",
        ".pytest_cache",
        ".mypy_cache",
        ".coverage",
    ]
    
    for target in clean_targets:
        for path in Path(".").glob(f"**/{target}"):
            if path.is_dir():
                print(f"删除目录: {path}")
                shutil.rmtree(path, ignore_errors=True)
            elif path.is_file():
                print(f"删除文件: {path}")
                path.unlink(missing_ok=True)


def check_tools():
    """检查必要的工具"""
    print("检查必要的工具...")
    
    tools = ["python", "pip", "twine"]
    
    for tool in tools:
        try:
            result = subprocess.run([tool, "--version"], 
                                  capture_output=True, 
                                  text=True)
            if result.returncode == 0:
                print(f"✓ {tool}: {result.stdout.strip()}")
            else:
                print(f"✗ {tool}: 未找到")
                return False
        except FileNotFoundError:
            print(f"✗ {tool}: 未安装")
            return False
    
    return True


def lint():
    """代码检查"""
    print("运行代码检查...")
    
    # 检查工具列表
    checks = [
        ("black --check src/", "代码格式检查"),
        ("isort --check-only src/", "导入排序检查"),
        ("flake8 src/", "代码风格检查"),
        ("mypy src/", "类型检查"),
    ]
    
    all_passed = True
    
    for cmd, description in checks:
        print(f"\n{description}...")
        result = run_command(cmd, check=False)
        if result.returncode != 0:
            print(f"✗ {description}失败")
            all_passed = False
        else:
            print(f"✓ {description}通过")
    
    return all_passed


def test():
    """运行测试"""
    print("运行测试...")
    
    result = run_command("pytest tests/ -v --cov=src/treer_sso_sdk", check=False)
    return result.returncode == 0


def build():
    """构建包"""
    print("构建包...")
    
    # 清理之前的构建
    clean()
    
    # 构建源码包和wheel包
    result = run_command("python -m build")
    
    if result.returncode == 0:
        print("✓ 包构建成功")
        
        # 显示构建结果
        dist_dir = Path("dist")
        if dist_dir.exists():
            print("\n构建文件:")
            for file in dist_dir.iterdir():
                print(f"  {file.name} ({file.stat().st_size} bytes)")
        
        return True
    else:
        print("✗ 包构建失败")
        return False


def check_package():
    """检查包"""
    print("检查包...")
    
    result = run_command("twine check dist/*", check=False)
    
    if result.returncode == 0:
        print("✓ 包检查通过")
        return True
    else:
        print("✗ 包检查失败")
        return False


def upload_test():
    """上传到测试PyPI"""
    print("上传到测试PyPI...")
    
    cmd = "twine upload --repository testpypi dist/*"
    result = run_command(cmd, check=False)
    
    if result.returncode == 0:
        print("✓ 成功上传到测试PyPI")
        print("测试安装: pip install --index-url https://test.pypi.org/simple/ treer-sso-sdk")
        return True
    else:
        print("✗ 上传到测试PyPI失败")
        return False


def upload_prod():
    """上传到生产PyPI"""
    print("上传到生产PyPI...")
    
    # 确认操作
    response = input("确定要发布到生产PyPI吗？(y/N): ")
    if response.lower() != 'y':
        print("取消发布")
        return False
    
    cmd = "twine upload dist/*"
    result = run_command(cmd, check=False)
    
    if result.returncode == 0:
        print("✓ 成功发布到PyPI")
        print("安装: pip install treer-sso-sdk")
        return True
    else:
        print("✗ 发布到PyPI失败")
        return False


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python scripts/build.py <command>")
        print("命令:")
        print("  clean      - 清理构建文件")
        print("  check      - 检查工具和环境")
        print("  lint       - 代码检查")
        print("  test       - 运行测试")
        print("  build      - 构建包")
        print("  check-pkg  - 检查包")
        print("  test-pypi  - 上传到测试PyPI")
        print("  pypi       - 发布到生产PyPI")
        print("  all        - 执行完整的构建流程")
        return
    
    command = sys.argv[1]
    
    if command == "clean":
        clean()
    elif command == "check":
        if not check_tools():
            sys.exit(1)
    elif command == "lint":
        if not lint():
            sys.exit(1)
    elif command == "test":
        if not test():
            sys.exit(1)
    elif command == "build":
        if not build():
            sys.exit(1)
    elif command == "check-pkg":
        if not check_package():
            sys.exit(1)
    elif command == "test-pypi":
        if not upload_test():
            sys.exit(1)
    elif command == "pypi":
        if not upload_prod():
            sys.exit(1)
    elif command == "all":
        steps = [
            ("检查工具", check_tools),
            ("代码检查", lint),
            ("运行测试", test),
            ("构建包", build),
            ("检查包", check_package),
        ]
        
        for step_name, step_func in steps:
            print(f"\n{'='*50}")
            print(f"步骤: {step_name}")
            print('='*50)
            
            if not step_func():
                print(f"\n✗ {step_name}失败，停止构建")
                sys.exit(1)
        
        print(f"\n{'='*50}")
        print("✓ 所有步骤完成！")
        print("='*50")
        print("包已准备好发布。运行以下命令:")
        print("  python scripts/build.py test-pypi  # 发布到测试PyPI")
        print("  python scripts/build.py pypi       # 发布到生产PyPI")
        
    else:
        print(f"未知命令: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main() 