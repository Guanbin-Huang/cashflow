 # Cash Flow 项目贡献指南

*成为项目贡献者的全流程指南*

## 1. 安装必要工具

**安装 Git**
```bash
# macOS (使用 Homebrew)
brew install git

# Windows
# 下载并安装: https://git-scm.com/download/win

# Linux (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install git
```

**安装 Python 环境**
```bash
# macOS (使用 Homebrew)
brew install python

# Windows
# 下载并安装: https://www.python.org/downloads/windows/

# Linux (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install python3 python3-pip
```

## 2. 配置 Git

```bash
# 设置用户名和邮箱
git config --global user.name "你的名字"
git config --global user.email "你的邮箱"

# 设置 SSH 密钥 (推荐)
ssh-keygen -t ed25519 -C "你的邮箱"

# 查看并复制公钥
cat ~/.ssh/id_ed25519.pub
```

将复制的公钥添加到 GitHub 账户:
1. 登录 GitHub
2. 点击右上角头像 -> Settings
3. 点击左侧菜单中的 "SSH and GPG keys"
4. 点击 "New SSH key"，粘贴你的公钥并保存

## 3. 克隆仓库

```bash
# 使用 SSH 方式克隆 (推荐)
git clone git@github.com:Guanbin-Huang/cashflow.git

# 或使用 HTTPS 方式克隆
git clone https://github.com/Guanbin-Huang/cashflow.git

# 进入项目目录
cd cashflow
```

## 4. 设置项目环境

```bash
# 创建并激活虚拟环境
python -m venv venv

# macOS/Linux 激活虚拟环境
source venv/bin/activate

# Windows 激活虚拟环境
.\venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt  # 如果有requirements.txt文件
```

## 5. 了解项目结构

```
cash_flow/
├── README.md           # 项目说明文档
├── main.py             # 程序入口
├── cards/              # 卡片相关模块
├── game/               # 游戏核心逻辑
├── player/             # 玩家相关模块
├── ui/                 # 用户界面
├── data/               # 数据文件
└── future/             # 未来功能
```

## 6. 工作流程

### A. 更新本地代码库

每次开始工作前，先拉取最新代码：

```bash
# 确保你在主分支
git checkout main

# 拉取最新代码
git pull origin main
```

### B. 创建功能分支

```bash
# 创建并切换到新分支
git checkout -b feature/你的功能名称

# 例如
git checkout -b feature/add-dice-animation
```

### C. 开发你的功能

1. 编写代码
2. 测试功能
3. 确保代码符合项目规范

### D. 提交你的变更

```bash
# 查看变更的文件
git status

# 添加所有变更文件到暂存区
git add .

# 或者添加特定文件
git add 文件路径

# 提交变更
git commit -m "描述你的变更内容"
```

**提交信息规范:**
- `feat: 添加新功能`
- `fix: 修复bug`
- `docs: 更新文档`
- `style: 代码格式修改`
- `refactor: 代码重构`
- `test: 添加测试`
- `chore: 构建过程或辅助工具变动`

### E. 推送到远程仓库

```bash
# 第一次推送新分支
git push -u origin feature/你的功能名称

# 之后的推送
git push
```

### F. 创建 Pull Request

1. 访问 [https://github.com/Guanbin-Huang/cashflow](https://github.com/Guanbin-Huang/cashflow)
2. 点击 "Compare & pull request"
3. 填写 PR 标题和描述
4. 点击 "Create pull request"

### G. 代码审查与合并

1. 项目维护者会审查你的代码
2. 根据反馈进行必要的修改
3. 一旦通过审查，你的代码将被合并到主分支

## 7. 解决冲突

如果出现冲突：

```bash
# 拉取最新主分支
git checkout main
git pull origin main

# 切回你的分支并合并主分支
git checkout feature/你的功能名称
git merge main

# 解决冲突后
git add .
git commit -m "解决冲突"
git push
```

## 8. 保持分支同步

定期将主分支的更新合并到你的功能分支：

```bash
git checkout main
git pull origin main
git checkout feature/你的功能名称
git merge main
```

## 9. 贡献者行为准则

- 尊重其他贡献者的工作
- 在提交代码前进行充分测试
- 遵循项目的代码风格和命名约定
- 积极参与代码审查和讨论

## 10. 常用 Git 命令参考

```bash
# 查看分支
git branch

# 切换分支
git checkout 分支名

# 查看提交历史
git log

# 查看特定文件的变更
git diff 文件路径

# 撤销工作区的修改
git checkout -- 文件路径

# 撤销暂存区的修改
git reset HEAD 文件路径

# 暂存当前工作
git stash

# 恢复暂存的工作
git stash pop
```

如有任何问题，请联系项目维护者或在 GitHub 上提出 Issue。