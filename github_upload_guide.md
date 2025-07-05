# 📚 GitHub代码上传完整指南

## 🛠️ 准备工作

### 1. 安装Git

**方式1：官方安装包（推荐）**
1. 访问 https://git-scm.com/download/win
2. 下载Windows版本的Git
3. 运行安装程序，使用默认设置
4. 安装完成后重启PowerShell

**方式2：使用包管理器**
```powershell
# 如果有Chocolatey
choco install git

# 如果有Scoop  
scoop install git
```

### 2. 验证Git安装

```powershell
git --version
```

### 3. 配置Git用户信息

```powershell
git config --global user.name "你的姓名"
git config --global user.email "你的邮箱@example.com"
```

## 🌟 在GitHub上创建仓库

### 1. 注册GitHub账号
- 访问 https://github.com
- 点击"Sign up"注册账号

### 2. 创建新仓库
1. 登录GitHub后，点击右上角的"+"
2. 选择"New repository"
3. 填写仓库信息：
   - Repository name: `deepseek-langchain-integration`
   - Description: `DeepSeek LLM与LangChain集成模块`
   - 选择Public（公开）或Private（私有）
   - 不勾选"Initialize this repository with a README"
4. 点击"Create repository"

## 📤 上传代码到GitHub

### 方式1：从现有项目初始化

在您的项目目录（D:\deepseek）中执行以下命令：

```powershell
# 1. 初始化Git仓库
git init

# 2. 添加远程仓库（替换为您的GitHub仓库URL）
git remote add origin https://github.com/您的用户名/deepseek-langchain-integration.git

# 3. 创建并切换到main分支
git checkout -b main

# 4. 添加所有文件
git add .

# 5. 提交代码
git commit -m "Initial commit: DeepSeek LangChain Integration"

# 6. 推送到GitHub
git push -u origin main
```

### 方式2：克隆GitHub仓库

```powershell
# 1. 克隆仓库到本地
git clone https://github.com/您的用户名/deepseek-langchain-integration.git

# 2. 进入仓库目录
cd deepseek-langchain-integration

# 3. 复制您的代码文件到此目录
# 4. 添加文件
git add .

# 5. 提交更改
git commit -m "Add DeepSeek LangChain Integration code"

# 6. 推送到GitHub
git push origin main
```

## 📋 推荐的.gitignore文件

创建`.gitignore`文件来排除不需要的文件：

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# 环境变量
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# 操作系统
.DS_Store
Thumbs.db

# 测试
.pytest_cache/
.coverage
htmlcov/

# 日志
*.log

# 临时文件
*.tmp
*.bak
conversation_*.json
```

## 🔧 常用Git命令

### 基础操作
```powershell
# 查看状态
git status

# 查看提交历史
git log --oneline

# 查看远程仓库
git remote -v

# 拉取最新代码
git pull origin main

# 推送代码
git push origin main
```

### 分支管理
```powershell
# 创建并切换分支
git checkout -b feature/new-feature

# 切换分支
git checkout main

# 合并分支
git merge feature/new-feature

# 删除分支
git branch -d feature/new-feature
```

### 版本管理
```powershell
# 添加特定文件
git add filename.py

# 添加所有文件
git add .

# 提交更改
git commit -m "描述您的更改"

# 修改最后一次提交
git commit --amend -m "新的提交信息"
```

## 📱 GitHub Desktop（可选）

如果您更喜欢图形界面：

1. 下载GitHub Desktop：https://desktop.github.com
2. 安装并登录GitHub账号
3. 点击"Add a local repository"
4. 选择您的项目文件夹
5. 发布到GitHub

## 🚀 自动化部署（可选）

创建GitHub Actions工作流：

```yaml
# .github/workflows/test.yml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.8
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    - name: Run tests
      run: |
        python test_all.py
```

## 🔒 安全提醒

1. **永远不要将API密钥提交到GitHub**
2. 使用环境变量管理敏感信息
3. 检查`.gitignore`文件是否正确配置
4. 定期检查仓库中是否有敏感信息

## 📝 提交信息规范

推荐使用以下格式：

```
feat: 添加新功能
fix: 修复bug
docs: 更新文档
style: 代码格式化
refactor: 重构代码
test: 添加测试
chore: 构建过程或辅助工具的变动
```

## 🎯 下一步

代码上传成功后，您可以：

1. 在GitHub上查看您的代码
2. 编写更好的README文档
3. 添加License文件
4. 设置GitHub Pages展示项目
5. 邀请其他开发者协作

## 📞 需要帮助？

如果在上传过程中遇到问题，请检查：

1. Git是否正确安装
2. 网络连接是否稳定
3. GitHub仓库URL是否正确
4. 是否有推送权限

---

**提示**：首次使用Git时，可能需要配置身份验证。建议使用Personal Access Token而不是密码。 