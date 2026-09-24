---
kb: intelligence
briefing_date: 2026-09-18
keywords: [Transformer, 注意力机制, 长上下文]
generated_at: 2026-09-18T08:00:00+08:00
---

# 动态情报库 · 说明与示例

> 依据：SPEC-06 §3.3 分库判据、SPEC-01 §3 `knowledge/intelligence/` 职责
> 服务对象：**前沿雷达智能体**（架构书三(四)）
> 写入方：`briefing-generate` Skill（架构书三(一)）
> 数据契约：`schemas/briefing.schema.json`

---

## 一、本库的作用

`intelligence/` 承载**时效性内容** —— 每日抓取的论文与项目动态，供用户筛选后决定是否精读。

它与 `domains/` 的**唯一区别是时间尺度**：

| | `domains/` | `intelligence/` |
| --- | --- | --- |
| 时间尺度 | 年 | 周 |
| 是否经过时间检验 | ✅ 是 | ❌ 否 |
| 核心判据 | 三年后是否仍成立 | 是否与本用户方向相关且是新增的 |

> ⚠️ **最常见的错误是把情报当知识。** 一条 7 天前的 arXiv 新论文摘要，若被复制进 `domains/`，会让路线规划智能体把它当作必读经典推荐给用户。**跨库不得搬运，只能重新提炼**（SPEC-06 §2.3）。

---

## 二、数据存放方式

本库采用**双层存放**：

| 层 | 位置 | 格式 | 说明 |
| --- | --- | --- | --- |
| **结构化数据** | `data/briefing/briefing-YYYY-MM-DD.json` | JSON | Web 侧只读消费，Schema 校验 |
| **说明性条目** | `knowledge/intelligence/` | Markdown | 人读的条目说明与背景补充 |

> 这一划分对应 SPEC-02 §一的格式边界：**机器读的进 `data/`，人读的进 `knowledge/`**。
> `data/briefing/` 由 `scripts/` 从上游生成，**禁止手工编辑**（SPEC-01 §3 单向依赖铁律）。

---

## 三、幂等性要求

架构书三(2)明确规定定时任务「同一天重复触发不应产生重复简报」。

因此文件名固定为 `briefing-YYYY-MM-DD.json`，**同日重复生成直接覆盖**：

```text
✅ briefing-2026-09-18.json          ← 重复运行仍写这个文件
❌ briefing-2026-09-18-2.json        ← 禁止
❌ briefing-2026-09-18-final.json    ← 禁止（版本区分靠 Git，不靠文件名）
```

该约束已写入 `schemas/briefing.schema.json` 的 `briefing_date` 字段说明，并通过 `configs/afn.config.yaml` 的 `frontier_radar.idempotent: true` 生效。

---

## 四、准入检查清单（SPEC-06 §6.4(二)）

| 检查项 | 要求 |
| --- | --- |
| `source.url` 可访问 | ✅ |
| `relevance` 已分层 | ✅ `high` / `medium` / `low` |
| `relevance_reason` 非空泛 | ✅ 必须与用户研究方向关联，不得写「与方向相关」 |
| `quick_read` 已生成 | ✅ 一句话中文速读 |
| 时间窗口内 | ✅ `published_date` ∈ `time_window` |
| 幂等 | ✅ 同日覆盖 |
| 未混入 `domains/` 内容 | ✅ 已通过时间检验的内容须另行提炼 |

---

## 五、降级与失败处理

架构书三(2)要求：「抓取失败时降级为『本次暂无可更新内容』并记录，**不阻塞用户其他操作**」。

落地方式：简报 JSON 的 `degraded` 字段置为 `true`，`items` 为空数组，`stats.total_included` 为 0，并在 `logs/radar-failure.log` 记录失败原因。

> **这不是可选优化，是硬性要求。** SPEC-04 §3.1 特别提醒：这类降级逻辑必须人工检查，AI 默认生成的代码通常直接抛异常。前端消费方须能正确处理 `degraded: true` 的简报 —— 显示「本次暂无可更新内容」而非报错或空白。

---

## 六、示例条目

以下为一条**演示用**条目，用于说明字段填法。**它是示意数据，不是真实抓取结果，不参与任何展示。**

> ⚠️ 说明：此处的示例仅用于说明 `relevance_reason` 应如何书写（具体、可核验），**不作为情报入库**。
> 真实情报数据由定时任务写入 `data/briefing/`，其条目必须来自实际抓取并逐条核验 `source.url`。

| 字段 | 示范填法 | 反例（会被退回） |
| --- | --- | --- |
| `relevance` | `high` | `重要`（不在枚举内） |
| `relevance_reason` | 「该工作提出的稀疏注意力方案直接回应了用户当前关注的『长上下文推理成本』问题」 | 「与用户方向相关」（空泛，无法核验） |
| `quick_read` | 「用可学习的路由把注意力计算限制在 Top-K 位置，在长序列上把复杂度降到近线性」 | 「一篇关于注意力的论文」（无信息量） |
| `published_date` | `2026-09-16` | `前天`（格式违规，SPEC-02 §2.3） |

---

## 七、修订记录

| 版本 | 日期 | 修订人 | 说明 |
| --- | --- | --- | --- |
| V1.0 | 2026-09-18 | 知识库负责人 | 首次发布；明确本库定位、存放方式、幂等性与准入清单 |
