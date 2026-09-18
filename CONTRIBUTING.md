# 协作流程说明

> 依据：[SPEC-03 版本管理与留痕规范](docs/spec/03-版本管理与留痕规范.md)、[SPEC-04 AI 使用边界规范](docs/spec/04-AI使用边界规范.md)
> 首次参与项目请先读 [SPEC-00 总纲](docs/spec/00-仓库与文档规范总纲.md)。

---

## 一、一次性准备

```bash
git config --global user.name "你的姓名"
git config --global user.email "你的邮箱"
git config --global core.autocrlf false
git config --global core.quotepath false
```

---

## 二、标准工作流

```text
① 同步主干
      ↓
② 建功能分支
      ↓
③ 开发（先读规范，用 AI 时留痕）
      ↓
④ 提交（Conventional Commits）
      ↓
⑤ 推送并提 PR（用模板，填 AI 参与情况）
      ↓
⑥ 评审合并
```

### ① 同步主干

```bash
git checkout main
git pull origin main
```

### ② 建功能分支

```bash
git checkout -b feat/your-topic
```

| 前缀 | 用途 |
| --- | --- |
| `feat/` | 新功能 |
| `fix/` | 缺陷修复 |
| `docs/` | 纯文档变更 |
| `hotfix/` | 紧急修复 |
| `release/` | 提交前冻结版本 |

命名正则：`^(feat|fix|docs|hotfix|release)/[a-z0-9-]+$`

### ③ 开发

开工前确认三件事：

| 要做什么 | 先看哪份规范 |
| --- | --- |
| 新建文件/目录 | [SPEC-01 目录结构](docs/spec/01-目录结构规范.md) |
| 写 Markdown / JSON / YAML | [SPEC-02 格式约定](docs/spec/02-格式约定.md) |
| 使用 AI 工具 | [SPEC-04 AI 使用边界](docs/spec/04-AI使用边界规范.md) |

### ④ 提交

```bash
git status                    # 先看清单
git add <具体文件>             # 逐个 add，避免误提交
git commit -m "feat(skill): 新增简报生成 Skill 的相关性排序"
```

> ⚠️ **不要用 `git add .`** —— 容易把 `.env`、临时文件、个人数据一并提交。

提交信息格式：`<type>(<scope>): <subject>`

| type | 用途 |
| --- | --- |
| `feat` | 新增功能 |
| `fix` | 缺陷修复 |
| `docs` | 文档变更 |
| `data` | 数据文件变更 |
| `prompt` | 提示词变更 |
| `refactor` | 重构 |
| `chore` | 杂务 |
| `revert` | 回滚 |

| scope | 覆盖范围 |
| --- | --- |
| `spec` | `docs/spec/` |
| `adr` | `docs/decisions/` |
| `kb` | `knowledge/` |
| `skill` | `skills/` |
| `prompt` | `prompts/` |
| `web` | `web/` |
| `data` | `data/` |
| `config` | `configs/` |
| `log` | `iteration-log/` |
| `repo` | 仓库级 |

**含 AI 生成内容的提交必须加 footer**：

```text
feat(skill): 新增简报生成 Skill 的相关性排序

AI-assisted: LearnBuddy, session-2026-09-20-02
Refs: 迭代记录 2026-09-20-简报生成Skill.md
Reviewed-by: <人名>
```

### ⑤ 提 PR

```bash
git push -u origin feat/your-topic
```

然后在 GitHub 上创建 PR，模板会自动加载。**「AI 参与情况」一节为必填。**

### ⑥ 合并

- 功能分支 → `main`：**Squash Merge**（保持主干历史线性）
- `hotfix` → `main`：**Merge Commit**（保留修复痕迹）
- 合并后删除功能分支

---

## 三、按目录分工

| 目录 | 负责人 | 变更前须知 |
| --- | --- | --- |
| `docs/` | 文档与留痕 | 规范条款会约束团队行为，需谨慎 |
| `knowledge/domains/` | 知识库负责人 | 每个知识单元必须有真实可达的 `source.url` |
| `knowledge/personal/` | 知识库负责人 | **只提交脱敏样例** |
| `skills/` | 能力层负责人 | README 须含输入契约、输出格式、失败处理三节 |
| `configs/` | 能力层负责人 | 不得硬编码密钥 |
| `prompts/` | 提示词负责人 | 须更新 front matter 的 `version` 与验证状态 |
| `web/`、`data/` | Web 负责人 | 不引入重型框架；不手工编辑 `data/` |
| `iteration-log/` | 文档与留痕 + 队长 | **只增不删** |

---

## 四、四类留痕场景

| 场景 | 要做什么 | 模板 |
| --- | --- | --- |
| **一次提交** | 写规范的提交信息 | [`templates/commit-message.template.txt`](templates/commit-message.template.txt) |
| **一轮 AI 迭代** | 归档迭代记录（含原始提示词与人工调整） | [`templates/iteration-log.template.md`](templates/iteration-log.template.md) |
| **一个架构取舍** | 新增 ADR（编号永不复用） | [`templates/decision-record.template.md`](templates/decision-record.template.md) |
| **一次发版** | 更新 CHANGELOG + 发布 Release Note | [`templates/release-note.template.md`](templates/release-note.template.md) |

---

## 五、检查清单

### 提交前

- [ ] 提交信息格式符合 `<type>(<scope>): <subject>`
- [ ] 无敏感文件被提交（`git status` 确认过）
- [ ] 含 AI 参与的已加 `AI-assisted:` footer
- [ ] JSON 变更已跑 `python scripts/validate_schemas.py`

### 每轮迭代结束（24 小时内）

- [ ] `iteration-log/` 已归档，含原始提示词与人工调整说明
- [ ] `CHANGELOG.md` 的 `[未发布]` 段落已更新
- [ ] 提示词变更已同步 front matter 的 `version`

### 提交作品前

- [ ] 仓库为 Public，LICENSE 为 MIT
- [ ] README 中在线链接真实可用（非 localhost）
- [ ] 全部 `iteration-log/` 完整
- [ ] 无真实个人数据、无密钥
- [ ] 已打 `v1.0.0` 标签

---

## 六、遇到问题

| 问题 | 参考 |
| --- | --- |
| Git 推送失败、认证问题 | [SPEC-05 Git 与 GitHub 建仓推送手册](docs/spec/05-Git与GitHub建仓推送手册.md) |
| 误提交了敏感信息 | SPEC-05 §8 误提交敏感信息的补救流程 |
| 不确定文件放哪 | [SPEC-01 目录结构规范](docs/spec/01-目录结构规范.md) §5 新增目录判定流程 |
| 不确定该不该用 AI | [SPEC-04 AI 使用边界规范](docs/spec/04-AI使用边界规范.md) §2 四个层级 |
| 不确定格式怎么写 | [SPEC-02 格式约定](docs/spec/02-格式约定.md) |
