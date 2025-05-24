# GitHub自动发布到PyPI指南

本项目已配置GitHub Actions自动化工作流，可以实现版本管理和PyPI发布的完全自动化。

## 🔧 初始设置

### 1. 创建PyPI API Token

#### 生产环境 (PyPI)
1. 访问 [PyPI Account Settings](https://pypi.org/manage/account/)
2. 滚动到 "API tokens" 部分
3. 点击 "Add API token"
4. 设置Token名称：`treer-sso-sdk-github-actions`
5. 选择Scope：`Entire account` 或 `treer-sso-sdk` (包创建后)
6. 复制生成的token（以 `pypi-` 开头）

#### 测试环境 (Test PyPI)
1. 访问 [Test PyPI Account Settings](https://test.pypi.org/manage/account/)
2. 重复上述步骤
3. 复制生成的token

### 2. 配置GitHub Secrets

1. 进入GitHub仓库 → Settings → Secrets and variables → Actions
2. 点击 "New repository secret" 添加以下secrets：

```
PYPI_API_TOKEN = pypi-AgEIcHlwaS5vcmca...  (生产环境token)
TEST_PYPI_API_TOKEN = pypi-AgEIcHlwaS5vcmca...  (测试环境token)
```

### 3. 配置GitHub Environments (可选)

为了增加安全性，可以选择配置环境保护：

1. 进入 Settings → Environments
2. 创建两个环境：
   - `test` (用于Test PyPI)
   - `production` (用于生产PyPI)
3. 为 `production` 环境配置保护规则：
   - Required reviewers: 添加团队成员
   - Deployment branches: 限制为 `main` 分支
4. 在 `.github/workflows/publish.yml` 中添加相应的 `environment` 配置

> **注意**: 如果不配置环境，工作流将直接使用 secrets，这对于个人项目是完全可以的。

## 📦 发布流程

### 方法1: 通过GitHub Release (推荐)

这是最简单的方法，适合正式版本发布：

1. **更新版本号**：
   ```bash
   # 在本地更新版本号
   # 或者使用GitHub Actions工作流 "更新版本号"
   ```

2. **创建Release**：
   - 进入GitHub仓库 → Releases → "Create a new release"
   - Tag version: `v1.0.1` (版本号前加v)
   - Release title: `Release v1.0.1`
   - 描述发布内容
   - 点击 "Publish release"

3. **自动发布**：
   - GitHub Actions会自动触发
   - 运行测试 → 构建包 → 发布到PyPI

### 方法2: 手动触发工作流

适合测试或紧急发布：

1. **进入Actions页面**：
   - 仓库 → Actions → "发布到PyPI"

2. **手动运行**：
   - 点击 "Run workflow"
   - 选择分支（通常是main）
   - 选择目标：
     - `testpypi`: 发布到测试环境
     - `pypi`: 发布到生产环境
   - 点击 "Run workflow"

### 方法3: 自动版本更新 + 发布

完全自动化的版本管理：

1. **触发版本更新工作流**：
   - Actions → "更新版本号" → "Run workflow"
   - 选择版本类型：
     - `patch`: 1.0.0 → 1.0.1 (修复bug)
     - `minor`: 1.0.0 → 1.1.0 (新功能)
     - `major`: 1.0.0 → 2.0.0 (破坏性变更)
   - 或输入自定义版本号

2. **自动执行**：
   - 更新版本号文件
   - 更新CHANGELOG.md
   - 创建Git tag
   - 创建GitHub Release
   - 自动触发PyPI发布

## 🔍 监控发布状态

### 查看工作流状态
- 仓库 → Actions → 查看运行中的工作流
- 每个步骤都有详细日志

### 验证发布
1. **Test PyPI**: https://test.pypi.org/project/treer-sso-sdk/
2. **生产PyPI**: https://pypi.org/project/treer-sso-sdk/

### 测试安装
```bash
# 测试环境
pip install --index-url https://test.pypi.org/simple/ treer-sso-sdk

# 生产环境
pip install treer-sso-sdk
```

## 🚨 故障排除

### 常见错误

1. **HTTP 403: Invalid or non-existent authentication information**
   - 检查PyPI API token是否正确配置
   - 确认token权限和scope

2. **HTTP 400: File already exists**
   - PyPI不允许覆盖已存在的版本
   - 需要更新版本号

3. **测试失败**
   - 检查代码是否通过所有测试
   - 查看Actions日志定位问题

### 紧急发布

如果需要跳过某些检查：

1. 修改 `.github/workflows/publish.yml`
2. 临时注释掉测试步骤
3. 发布后记得恢复

## 📋 发布检查清单

发布前确认：

- [ ] 代码已提交到main分支
- [ ] 所有测试通过
- [ ] 版本号已更新
- [ ] CHANGELOG.md已更新
- [ ] GitHub secrets已配置
- [ ] 已在测试环境验证

## 🔄 版本管理策略

### 语义化版本 (SemVer)

- **MAJOR.MINOR.PATCH** (如 1.2.3)
- **MAJOR**: 不兼容的API变更
- **MINOR**: 向下兼容的新功能
- **PATCH**: 向下兼容的bug修复

### 预发布版本

```bash
1.0.0-alpha.1  # Alpha版本
1.0.0-beta.1   # Beta版本
1.0.0-rc.1     # Release Candidate
```

### 分支策略

- `main`: 稳定版本，用于生产发布
- `develop`: 开发版本，用于功能集成
- `feature/*`: 功能分支

## 📚 相关资源

- [PyPI API Token Guide](https://pypi.org/help/#apitoken)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Semantic Versioning](https://semver.org/)
- [Keep a Changelog](https://keepachangelog.com/) 