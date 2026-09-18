# SPEC-05 Git 与 GitHub 建仓推送手册

> 文档编号：SPEC-05
> 文档版本：V1.0
> 生效日期：2026-09-18
> 上游依据：架构书 五(一) 版本管理选型、赛事手册 第 4 步（GitHub 开源与部署）
> 适用对象：首次操作仓库的团队成员

---

## 一、前置准备

### 1.1 需要安装

| 工具 | 最低版本 | 说明 |
| --- | --- | --- |
| Git | 2.30+ | 版本管理（架构书五(1) 选定） |
| Python | 3.10+ | 自研 Skills 与本地脚本（架构书五(1) 选定） |

检查是否已安装：

```bash
git --version
python --version
```

### 1.2 首次配置身份（每人一次）

**必须**使用真实姓名与邮箱，否则 Git 历史无法对应到人。

```bash
git config --global user.name "你的姓名"
git config --global user.email "你的邮箱"
git config --global init.defaultBranch main
git config --global core.autocrlf false    # 统一用 LF，与 SPEC-02 §2.1 一致
git config --global core.quotepath false   # 中文文件名正常显示
```

验证：

```bash
git config --global --list
```

---

## 二、场景 A：仓库已存在，克隆到本地（多数人用这个）

仓库建好后，团队成员直接克隆：

```bash
git clone https://github.com/<你的账号>/academic-frontier-navigator.git
cd academic-frontier-navigator
```

推荐仓库名：**`academic-frontier-navigator`**（与架构书英文名 Academic Frontier Navigator 一致）。

### 日常开发流程

```bash
# 1. 同步主干，避免基于旧代码开发
git checkout main
git pull origin main

# 2. 建功能分支（命名见 SPEC-03 §3）
git checkout -b feat/briefing-skill

# 3. 开发……然后提交
git add <具体文件>            # 建议逐个 add，避免误提交
git commit -m "feat(skill): 新增简报生成 Skill 的相关性排序"

# 4. 推送分支
git push -u origin feat/briefing-skill

# 5. 在 GitHub 上创建 PR，用 PR 模板填写，等待评审
```

> **重要**：不要用 `git add .`。它会把 `.env`、临时文件、个人数据一并提交。若确实要用，先 `git status` 确认待提交清单。

---

## 三、场景 B：从零创建仓库并首次推送

如果仓库还未创建，按以下步骤操作。

### 3.1 方式一：在 GitHub 网页创建（推荐，最直观）

1. 登录 GitHub，右上角 **+** → **New repository**
2. 填写：
   - **Repository name**：`academic-frontier-navigator`
   - **Description**：`学术前沿知识导航智能体 | 粤港澳大湾区 AI Coding 创新大赛`
   - **Visibility**：**Public** ← 赛事硬性要求，必须选公开
   - **Add a license**：选择 **MIT License** ← 手册第 4 步要求
   - **Initialize this repository with a README**：**不勾选**（本地已有 README）
   - `.gitignore` 与 `Add .gitattributes`：**都不选**（本地已有）
3. 点击 **Create repository**

### 3.2 方式二：用 GitHub CLI

```bash
gh repo create academic-frontier-navigator \
  --public \
  --description "学术前沿知识导航智能体 | 粤港澳大湾区 AI Coding 创新大赛" \
  --license MIT \
  --source . \
  --remote origin
```

> 注意：`--source .` 要求当前目录已是 git 仓库，且要配合 `--push` 才会推送。

### 3.3 绑定远端并推送

```bash
cd academic-frontier-navigator

# 绑定远端（把 <你的账号> 换成实际用户名）
git remote add origin https://github.com/<你的账号>/academic-frontier-navigator.git

# 确认远端
git remote -v

# 推送主干
git push -u origin main

# 推送标签
git push origin --tags
```

---

## 四、认证方式

### 4.1 HTTPS + Personal Access Token（推荐）

GitHub 已不支持密码推送，需用 Token。

**创建 Token（经典 PAT）**：

1. GitHub → **Settings** → **Developer settings** → **Personal access tokens** → **Tokens (classic)**
2. **Generate new token (classic)**
3. Scopes 勾选：
   - ✅ **`repo`**（完整仓库读写权限，必需）
   - ✅ **`workflow`**（如需修改 `.github/workflows/`）
4. 设置有效期（建议覆盖整个赛事周期）
5. **立即复制保存** —— 页面关闭后无法再查看

**使用**：推送时用户名填 GitHub 用户名，密码填 Token。

**避免每次输入**：

```bash
# 方式一：凭据缓存（推荐，15 分钟或更久）
git config --global credential.helper 'cache --timeout=86400'

# 方式二：macOS 钥匙串
git config --global credential.helper osxkeychain

# 方式三：Windows
git config --global credential.helper manager
```

> ⚠️ **安全红线**：Token 等同于密码，**绝对不能**写入代码、配置文件、`remote url` 或提交到仓库。若已经把 Token 写进了 remote URL，用以下命令清除：
> ```bash
> git remote set-url origin https://github.com/<你的账号>/academic-frontier-navigator.git
> ```

### 4.2 SSH 密钥（可选）

```bash
# 生成密钥
ssh-keygen -t ed25519 -C "你的邮箱"

# 查看公钥并复制
cat ~/.ssh/id_ed25519.pub

# 添加到 GitHub：Settings → SSH and GPG keys → New SSH key

# 测试
ssh -T git@github.com
```

使用 SSH 时远端地址改为：

```bash
git remote set-url origin git@github.com:<你的账号>/academic-frontier-navigator.git
```

---

## 五、配置 Gitee 镜像

### 5.1 方式一：Gitee 自动镜像（推荐，零维护）

1. 在 Gitee 创建仓库 `academic-frontier-navigator`（公开）
2. 进入仓库 → **管理** → **仓库镜像管理** → **新建镜像**
3. 镜像方向：**Pull（从 GitHub 拉取）**
4. 填入 GitHub 仓库地址，授权后保存
5. Gitee 会定期自动同步，无需本地操作

### 5.2 方式二：本地手动推送

```bash
# 添加 Gitee 远端
git remote add gitee git@gitee.com:<你的账号>/academic-frontier-navigator.git

# 每次推送主仓后同步
git push origin main
git push gitee main
```

> **只做单向同步**（GitHub → Gitee）。双向同步会导致循环拉取与冲突，10 天周期没有精力处理。

---

## 六、赛事前必查项

### 6.1 开源合规（手册硬性要求）

| 检查项 | 命令 / 位置 | 通过标准 |
| --- | --- | --- |
| 仓库为公开 | GitHub 仓库页 | 显示 **Public** |
| 含 LICENSE 文件 | 仓库根目录 | `LICENSE` 存在，内容为 MIT |
| README 完整 | 仓库根目录 | 含项目定位、功能、技术架构、运行指令、协议说明 |
| 在线链接可用 | README 中 | 链接真实可点击，非 localhost |

```bash
# 本地自检
ls LICENSE README.md CHANGELOG.md .gitignore
head -3 LICENSE          # 应显示 MIT License
```

### 6.2 仓库卫生检查

```bash
# 查看是否有敏感文件被追踪
git ls-files | grep -i -E '\.env|secret|token|credential|\.private\.' || echo "✅ 无敏感文件"

# 查看仓库体积（应远小于 50MB）
du -sh .git

# 查看未被 .gitignore 覆盖的临时文件
git status --ignored --short | head -20
```

### 6.3 留痕完整性检查

```bash
# 迭代记录数量与命名
ls iteration-log/

# 含 AI 参与的提交数量（评审参考）
git log --grep="AI-assisted" --oneline | wc -l

# 提交历史是否完整
git log --oneline | head -20
```

---

## 七、常见问题

| 问题 | 原因 | 解决 |
| --- | --- | --- |
| `remote: Permission denied` | Token 无 `repo` 权限或已过期 | 重新生成 Token，勾选 `repo` |
| `failed to push some refs` | 远端有本地没有的提交 | 先 `git pull --rebase origin main` |
| 中文文件名显示为八进制 | Git 默认转义非 ASCII | `git config --global core.quotepath false` |
| 换行符导致整文件 diff | Windows 的 CRLF 与 LF 混用 | `git config --global core.autocrlf false`，仓库已配 `.gitattributes` |
| 推送大文件失败 | 超过 GitHub 100MB 限制 | 大文件走网盘，仓库只放链接（SPEC-01 §3） |
| 误提交了 `.env` | 未看 `git status` 直接 `git add .` | 见 §8 补救流程 |
| Gitee 同步后中文乱码 | 编码不一致 | 确认文件为 UTF-8 无 BOM（SPEC-02 §2.1） |

---

## 八、误提交敏感信息的补救流程

**关键认知：改代码无效，密钥已进入 Git 历史，必须吊销。**

### 处置顺序（不可颠倒）

1. **立即吊销密钥** —— 到 GitHub/服务商后台删除或重置该 Token。这一步优先于任何代码操作。
2. **从索引移除并补进 `.gitignore`**：
   ```bash
   git rm --cached .env
   echo ".env" >> .gitignore
   git add .gitignore
   git commit -m "chore(repo): 移除误提交的本地配置并更新忽略规则"
   ```
3. **清理历史**（若密钥含高敏感权限，且仓库已公开）：
   ```bash
   # 使用 git-filter-repo（推荐）或 BFG
   pip install git-filter-repo
   git filter-repo --path .env --invert-paths
   git push --force --all
   ```
   > ⚠️ `--force` 会重写历史，**必须**先通知所有协作者。小团队可接受，但要在群里同步。
4. **记录事故**：在 `iteration-log/` 中新建记录，说明泄露内容、处置措施、后续防范。这**不是**丢脸的事 —— 主动记录体现的是工程规范性。

### 个人数据误提交

用户画像、学习轨迹等（架构书六(1)「中」敏感级）误提交，处置同上述流程，并在 `iteration-log/` 记录。

---

## 九、建仓检查清单

### 首次建仓

- [ ] 已安装 Git 2.30+、Python 3.10+
- [ ] 已配置 `user.name` / `user.email`
- [ ] 已配置 `core.autocrlf false`、`core.quotepath false`
- [ ] 仓库已创建为 **Public**
- [ ] 已添加 **MIT License**
- [ ] 远端 `origin` 已绑定并验证（`git remote -v`）
- [ ] `main` 分支已推送（`git push -u origin main`）
- [ ] 标签已推送（`git push origin --tags`）
- [ ] Gitee 镜像已配置

### 日常开发

- [ ] 开发前 `git pull origin main` 同步
- [ ] 使用功能分支，命名符合正则
- [ ] 提交信息符合 Conventional Commits
- [ ] 用 `git add <具体文件>` 而非 `git add .`
- [ ] 含 AI 参与的提交已加 `AI-assisted` footer

### 提交作品前

- [ ] 仓库为 Public，LICENSE/README 齐全
- [ ] README 中在线链接真实可用（非 localhost）
- [ ] 无敏感文件被追踪
- [ ] `iteration-log/` 完整
- [ ] 已打 `v1.0.0` 标签并发布 Release

---

## 十、修订记录

| 版本 | 日期 | 修订人 | 说明 |
| --- | --- | --- | --- |
| V1.0 | 2026-09-18 | 文档与留痕 | 首次发布；覆盖建仓、认证、镜像、赛事合规与事故处置 |
