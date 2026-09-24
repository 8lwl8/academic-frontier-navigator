# 变更日志

本项目所有值得注意的变更都记录在此文件。

格式遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，
版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

> **维护规则**（SPEC-03 §6.2）：
> - `[未发布]` 段落常驻，积累当前未发版的变更
> - 只记**面向使用者可见**的变更，不记内部重构细节
> - 发版时将 `[未发布]` 转为版本段落并补日期
> - 分类：`新增` / `变更` / `废弃` / `移除` / `修复` / `安全`

---

## [未发布]

### 新增

- **知识库分库与语料准入规范（SPEC-06）**：将架构书三(四)知识库设计从结论性描述落地为可执行规则
  - 三分库判据：按「是否稳定 / 是否有时效 / 是否个人专属」三个属性划分，替代按内容主题划分
  - 四层组织模型：领域 → 子方向 → 知识点 → 文献，由 front matter 字段承载
  - 依赖关系模型：`prerequisites` 字段为唯一事实来源，导出为机器可读的边表
  - 四维语料准入量表：可访问性 / 出处明确 / 权威性 / 时效性，采用**一票否决制**
  - 权威性分级 C1~C5，其中 C5（不可采信）为硬拒绝
  - 语料的复核与退出机制：链接失效、结论被推翻、时效衰减三类情况的处置路径
- **领域知识库首个样例领域**：以「自然语言处理 · 序列建模与 Transformer」为例，落地 15 个知识单元
  - 覆盖 5 个子方向：表示学习、序列建模、Transformer 架构、训练与优化、跨模态与架构迁移
  - 知识单元编号 `kn-0001` ~ `kn-0015`，全局唯一且不可复用
  - 全部 15 条 `source.url` 均为经人工核验可达的真实 arXiv 页面
- **知识点依赖图导出**：`knowledge/domains/_graph.json`
  - 15 个节点、19 条边（12 条前置关系 + 7 条相关关系）
  - 无循环依赖，起始节点 5 个：kn-0001 / kn-0008 / kn-0009 / kn-0014 / kn-0015
  - 汇点 7 个：kn-0002 / kn-0007 / kn-0010 / kn-0012 / kn-0013 / kn-0014 / kn-0015
- **知识库索引**：`knowledge/domains/_index.md`，登记子方向、知识点清单、依赖概览与已知缺口
  - 起点与汇点清单标注计算口径（只数前置边，`related_to` 不计入）
- **动态情报库说明**：`knowledge/intelligence/README.md`，含双层存储（JSON 机器可读 + Markdown 人读）、
  幂等命名规则、降级处理约定
- **个人资产库说明与脱敏样例**：`knowledge/personal/README.md`，含四层记忆结构
  （用户画像 / 进度记忆 / 偏好记忆 / 项目轨迹）与脱敏规则
- **知识点依赖图 Schema**：`schemas/knowledge-graph.schema.json`
  - 采用 JSON Schema Draft 2020-12，`stats.has_cycle` 硬约束为 `false`
  - 新增 `stats.sink_nodes` 字段，并在字段描述中明确 `root_nodes` / `sink_nodes` 的「只数前置边」口径
- **知识单元校验脚本**：`scripts/check_knowledge_units.py`
  - 校验 front matter 完整性、编号格式与全局唯一性、子方向登记状态
  - 校验悬空引用、自环、循环依赖（Kahn 拓扑排序）
  - **校验 `_graph.json` 派生数据与源数据一致**：节点集、前置边集、各项计数、
    `root_nodes` / `sink_nodes` 任一不符即失败（SPEC-06 §5.6）
  - `--url-check` 可选参数用于核验 `source.url` 可达性
- **架构决策记录 ADR-0001**：`docs/decisions/ADR-0001-explicit-dependency-graph.md`
  - 本仓库第一份 ADR，记录依赖图的技术选型、备选方案与已知局限
- **路线生成端到端验证样例**：`data/route/route-nlp-transformer.json`
  - 按拓扑深度自动分 7 个阶段，验证依赖图可实际驱动学习路线生成
- **迭代记录**：`iteration-log/2026-09-18-knowledge-base-and-corpus-admission.md`

### 变更

- **配置版本升级**：`configs/afn.config.yaml` 由 `config_version: 1.0` 升至 `1.1`
  - 新增 `knowledge_base` 段：准入约束、组织约束、依赖图开关、生命周期、检索口径
  - 新增 `validation` 段：登记四个校验脚本
  - 新增 `relevance.require_reason`：相关性判断必须给出理由
  - `frontier_radar.scope.keywords` 调整为 `[Transformer, 注意力机制, 序列建模]`
- **知识库入口重写**：`knowledge/README.md` 指向 SPEC-06，并保留三分库总表
- **Schema 索引更新**：`schemas/README.md` 登记 `knowledge-graph.schema.json`
- **脚本索引更新**：`scripts/README.md` 登记 `check_knowledge_units.py`，
  并明确列出脚本能检出与**检不出**的问题类型

### 废弃

### 移除

### 修复

- **依赖图派生数据与源数据不一致**：`_graph.json` 的 `stats.root_nodes` 误填为全部 15 个节点
  （真实起点为 5 个），`_index.md` §4.1 又写作 4 个（漏 `kn-0015`）、§4.2 汇点清单缺失 2 项。
  已修正三处，并在 `check_knowledge_units.py` 中新增派生数据一致性校验，
  同时明确 `root_nodes` / `sink_nodes` 的计算口径。详见 ADR-0001 §五 与 SPEC-06 §5.6
- **领域知识库文件名去中文化**：18 个含中文名的文件改为英文 kebab-case 命名，
  并同步更新 6 处内部引用（CHANGELOG / ADR-0001 / knowledge README / `_index.md` /
  scripts README / 迭代记录），避免跨平台归档与解压时出现文件名乱码

### 安全

- 提交前经 `scan_secrets.py` 扫描，34 个文件无密钥、Token、`.env` 泄露
- 经 `block_private_data.py` 校验，`knowledge/personal/` 下仅含脱敏样例，无真实个人数据
- 全部 15 条 `source.url` 均经匿名访问核验可达，未由 AI 生成或推测（符合 SPEC-04 §3.3）
- 明确 `knowledge/personal/` 目录下真实个人数据一律不入库，仅保留 `*.example.*` 脱敏样例
- 语料准入强制要求 `source.url` 必须经人工逐一访问确认，不接受 AI 自述
- 个人资产库明确不记录原始对话流水，只沉淀有长期价值的结构化信息
  （依据：架构书三(三) 长期记忆设计）

---

## [v1.0.0] - 2026-09-26

> 初赛提交版本：三项核心能力闭环可用。

### 新增

- 领域学习路线定制能力：依据用户基础、目标与时间预算生成分阶段路线
- 前沿动态每日追踪能力：定时抓取领域最新动态，按相关性分层生成每日简报
- 知识资产沉淀能力：对话结论与阅读笔记结构化提炼并可检索复用
- 分层提示词架构：角色层 / 原则层 / 任务层 / 上下文层
- 自研 Skills：论文精读、路线生成、简报生成、资产提炼
- Web 只读展示层：学习路线图、前沿简报、知识资产

### 安全

- 建立数据分类与可见度控制机制，个人资产默认私密
- 建立 AI 使用留痕机制，保留完整迭代记录以备评审

---

<!--
## [vX.Y.Z] - YYYY-MM-DD

### 新增
- 描述变更内容

### 变更
- 描述行为变化

### 修复
- 描述修复的缺陷

### 安全
- 描述安全或合规相关变更
-->
