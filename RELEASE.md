# 发布指南

本文档描述如何将 Treer SSO SDK 发布到 PyPI。

## 准备工作

### 1. 安装必要工具

```bash
pip install build twine
```

### 2. 配置 PyPI 凭据

创建 `~/.pypirc` 文件：

```ini
[distutils]
index-servers = 
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-your-api-token-here

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-your-test-api-token-here
```

或者使用环境变量：

```bash
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-your-api-token-here
```

## 发布流程

### 1. 更新版本号

在 `pyproject.toml` 中更新版本号：

```toml
[project]
version = "1.0.1"  # 更新版本号
```

在 `src/treer_sso_sdk/__init__.py` 中同步更新：

```python
__version__ = "1.0.1"
```

### 2. 更新变更日志

在 `CHANGELOG.md` 中添加新版本的变更记录。

### 3. 运行测试

```bash
# 运行基本功能测试
python test_package.py

# 运行单元测试（如果有）
pytest tests/
```

### 4. 清理和构建

```bash
# 使用构建脚本
python scripts/build.py clean
python scripts/build.py build

# 或者手动执行
rm -rf dist/ build/ *.egg-info/
python -m build
```

### 5. 检查包

```bash
twine check dist/*
```

### 6. 发布到测试 PyPI

```bash
twine upload --repository testpypi dist/*
```

测试安装：

```bash
pip install --index-url https://test.pypi.org/simple/ treer-sso-sdk
```

### 7. 发布到生产 PyPI

确认测试无误后，发布到生产环境：

```bash
twine upload dist/*
```

### 8. 验证发布

```bash
pip install treer-sso-sdk
python -c "import treer_sso_sdk; print(treer_sso_sdk.__version__)"
```

## 自动化脚本

使用提供的构建脚本可以简化流程：

```bash
# 完整的构建和检查流程
python scripts/build.py all

# 发布到测试 PyPI
python scripts/build.py test-pypi

# 发布到生产 PyPI
python scripts/build.py pypi
```

## 版本管理

遵循 [语义化版本](https://semver.org/lang/zh-CN/) 规范：

- **主版本号**：不兼容的 API 修改
- **次版本号**：向下兼容的功能性新增
- **修订号**：向下兼容的问题修正

示例：
- `1.0.0` → `1.0.1`：修复 bug
- `1.0.0` → `1.1.0`：新增功能
- `1.0.0` → `2.0.0`：破坏性变更

## 发布检查清单

- [ ] 更新版本号
- [ ] 更新变更日志
- [ ] 运行所有测试
- [ ] 构建包
- [ ] 检查包
- [ ] 发布到测试 PyPI
- [ ] 测试安装
- [ ] 发布到生产 PyPI
- [ ] 验证发布
- [ ] 创建 Git 标签
- [ ] 推送到仓库

## 回滚

如果发现问题需要回滚：

1. 从 PyPI 删除有问题的版本（如果可能）
2. 发布修复版本
3. 在文档中说明问题和解决方案

## 注意事项

1. **不要删除已发布的版本**：PyPI 不允许重新上传相同版本号的包
2. **测试充分**：确保在测试 PyPI 上充分测试
3. **文档同步**：确保文档与代码版本同步
4. **依赖管理**：检查依赖版本兼容性
5. **安全性**：不要在代码中包含敏感信息 