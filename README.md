# Academic Frontier Navigator（AFN）

> **学术前沿知识导航智能体**
> 粤港澳大湾区 AI Coding 创新大赛 · 方向二

本仓库是 AFN 的**源代码与文档仓库**，承载赛事的开源要求，并作为团队协作与版本留痕的唯一事实来源。

---

## 一、项目定位

面向科研入门者的学术导航智能体，让「进入一个新方向」不再依赖零散搜索。通过三项相互闭环的能力，把「找方向 → 跟前沿 → 沉淀知识」串成一条可持续的路径。

| 核心能力 | 解决什么问题 | 由谁承载 |
| --- | --- | --- |
| **领域学习路线定制** | 不知道这个方向该按什么顺序学 | 路线规划智能体 |
| **前沿动态每日追踪** | 不知道最近有什么新进展 | 前沿雷达智能体 |
| **知识资产沉淀** | 读过的东西留不下来 | 知识管家智能体 |

三项能力并非并列，而是构成闭环：**前沿雷达发现论文 → 触发知识管家记录 → 用户决定精读 → 路线规划插入当前阶段 → 精读结论回流沉淀**。这一编排由主控智能体完成。

---

## 二、技术架构

采用「**三横一纵**」结构 —— 横向为交互层、智能体层、能力层与数据层，纵向为贯穿全层的安全与合规机制。

| 层级 | 承载内容 | 技术载体 |
| --- | --- | --- |
| 交互层 | 对话交互、路线图可视化、简报呈现 | LearnBuddy 对话界面、Web 入口页面 |
| 智能体层 | 主控智能体 + 三个领域子智能体 | LearnBuddy 多智能体协作 |
| 能力层 | Skills 组件、定时任务、长期记忆、知识库检索 | LearnBuddy Skills 生态、平台定时任务 |
| 数据层 | 领域知识库、用户画像、学习轨迹、知识资产 | LearnBuddy / ima 知识库 |
| 纵向 | 知识边界声明、出处标注、权限与可见度控制 | 提示词约束 + 平台权限体系 |

**技术栈原则**：优先复用平台能力，Web 侧采用最小化实现。

| 侧 | 选型 |
| --- | --- |
| 平台侧（智能体能力） | LearnBuddy 平台、LearnBuddy/ima 知识库、Python |
| Web 侧（展示能力） | HTML + CSS + 原生 JavaScript + ECharts，静态 JSON 数据源，无构建工具 |
| 数据格式 | Markdown（知识单元）、JSON（结构化输出）、YAML（配置） |
| 版本管理 | Git + GitHub（主仓）+ Gitee（镜像） |

> 术语说明：**领域方法论助手**对应赛事「专家数字分身」的能力形态。本项目采用「基于公开学术资源的方法论提炼」路线，**不依赖真人专家参与校准**，并在交互中明确告知用户其方法论提炼自公开学术资源。

---

## 三、目录结构

```text
afn/
├── README.md              项目说明（本文）
├── LICENSE                MIT 开源协议
├── CHANGELOG.md           版本变更记录
├── CONTRIBUTING.md        协作流程说明
│
├── docs/                  规范与决策
│   ├── spec/              规范正文（SPEC-00 ~ SPEC-05）
│   └── decisions/         架构决策记录（ADR）
│
├── templates/             版本留痕模板
├── schemas/               JSON Schema 校验文件
├── configs/               配置与工具链
│
├── knowledge/             数据层 · 知识库
│   ├── domains/             领域知识库
│   ├── intelligence/        动态情报库
│   └── personal/            个人资产库（仅脱敏样例）
│
├── prompts/               智能体层 · 分层提示词
│   ├── role/                角色层
│   ├── principle/           原则层
│   ├── task/                任务层
│   └── context/             上下文层
│
├── skills/                能力层 · 自研 Skills
├── data/                  交互层 · Web 只读数据源
├── web/                   交互层 · 只读展示
│
├── iteration-log/         AI 使用留痕（评审举证材料，只增不删）
└── .github/               协作机制
```

目录与架构书四层分层的映射关系见 [`docs/spec/01-目录结构规范.md`](docs/spec/01-目录结构规范.md)。

---

## 四、文档规范索引

**开始工作前请先读规范。** 规范不是形式，它决定了产出物能否被评审追溯。

| 编号 | 文档 | 什么时候看 |
| --- | --- | --- |
| SPEC-00 | [仓库与文档规范总纲](docs/spec/00-仓库与文档规范总纲.md) | **第一次参与项目时必读** |
| SPEC-01 | [目录结构规范](docs/spec/01-目录结构规范.md) | 新建文件或目录时 |
| SPEC-02 | [格式约定](docs/spec/02-格式约定.md) | 写 Markdown / JSON / YAML 时 |
| SPEC-03 | [版本管理与留痕规范](docs/spec/03-版本管理与留痕规范.md) | 提交代码、打版本、写留痕时 |
| SPEC-04 | [AI 使用边界规范](docs/spec/04-AI使用边界规范.md) | 使用 AI 工具时 |
| SPEC-05 | [Git 与 GitHub 建仓推送手册](docs/spec/05-Git与GitHub建仓推送手册.md) | 首次建仓或遇到 Git 问题时 |

### 三条最容易踩的红线

1. **AI 生成内容必须留痕** —— 含 AI 参与的提交要加 `AI-assisted:` footer，并在 `iteration-log/` 归档完整过程（含原始提示词与人工调整说明）。这直接关系 25% 的评分。
2. **真实个人数据不入库** —— 仓库是公开的。用户画像、学习轨迹、个人资产只保留 `.example.md` 形式的脱敏样例。
3. **`data/` 不得手工编辑** —— 该目录由 `scripts/` 从上游生成。手工改会丢失溯源信息，评审追问「这数据哪来的」时无法回答。

---

## 五、本地快速开始

### 环境要求

| 工具 | 版本 |
| --- | --- |
| Git | 2.30+ |
| Python | 3.10+ |

```bash
# 克隆
git clone https://github.com/8lwl8/academic-frontier-navigator.git
cd academic-frontier-navigator

# 配置身份
git config user.name "你的姓名"
git config user.email "你的邮箱"
```

### 校验命令

```bash
# 校验 JSON 数据是否符合 Schema 契约
python scripts/validate_schemas.py

# 扫描疑似密钥
python scripts/scan_secrets.py

# 拦截真实个人数据
python scripts/block_private_data.py
```

### 启用提交钩子（可选）

```bash
pip install pre-commit
pre-commit install --config configs/.pre-commit-config.yaml
```

> 钩子若拖慢迭代节奏，可临时用 `git commit --no-verify` 绕过，但**必须**在 `iteration-log/` 记录绕过原因。

---

## 六、协作方式

详见 [`CONTRIBUTING.md`](CONTRIBUTING.md)。核心流程：

```text
同步主干 → 建功能分支 → 开发 → 提交（Conventional Commits）
   → 推送 → 提 PR（用模板，填 AI 参与情况）→ 评审合并
```

| 项 | 约定 |
| --- | --- |
| 分支命名 | `^(feat\|fix\|docs\|hotfix\|release)/[a-z0-9-]+$` |
| 提交信息 | `<type>(<scope>): <subject>`，中文，不超过 50 字 |
| 合并方式 | 功能分支 → `main` 用 Squash Merge |

---

## 七、在线访问

| 入口 | 链接 | 状态 |
| --- | --- | --- |
| Web 展示入口 | <待部署后补充> | ⏳ 待部署 |
| GitHub 仓库（主仓） | <https://github.com/8lwl8/academic-frontier-navigator> | ✅ 公开可访问 |
| Gitee 镜像 | <待配置> | ⏳ 待配置 |

> 赛事要求作品必须是在线可点击访问的 Web 链接，不能提交本地 `localhost`。

---

## 八、开源协议

本项目采用 [MIT License](LICENSE) 发布。

使用的第三方资源均在 [`docs/第三方资源清单.md`](docs/第三方资源清单.md) 中注明。

---

## 九、AI 使用声明

本项目在开发过程中深度使用 LearnBuddy 平台辅助生成代码、提示词与文档，所有 AI 参与的过程记录完整保存在 [`iteration-log/`](iteration-log/) 目录中。

遵循赛事手册 8.3：**AI 用于提效，而非替代。** 所有 AI 产出均经人工审核、修改与验证，迭代记录中包含每轮的人工调整说明及理由。
