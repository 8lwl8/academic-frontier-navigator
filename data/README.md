# Web 只读数据源

> 依据：架构书 四(二) Web 入口、SPEC-01 §3 目录结构规范

架构书四(二)明确：Web 侧「数据来自智能体输出结果的落地存储（静态数据文件或轻量存储服务），**不做实时双向同步**」。
本仓库采用**静态 JSON 文件**方案。

| 子目录 | 对应 Web 页面 | 数据来源 | Schema |
| --- | --- | --- | --- |
| `route/` | 学习路线 | 路线规划智能体输出 | `schemas/route.schema.json` |
| `briefing/` | 前沿简报 | 前沿雷达智能体输出 | `schemas/briefing.schema.json` |
| `assets/` | 知识资产 | 知识管家沉淀条目 | `schemas/asset.schema.json` |

## ⚠️ 单向依赖铁律

```text
knowledge/ → scripts/ → data/ → web/
```

- **禁止手工编辑本目录下的文件** —— 本目录由 `scripts/` 从上游生成。
- **禁止 `web/` 直接读 `knowledge/`** —— Web 只消费 `data/`。
- 手工编辑会丢失 `generated_by` 等溯源信息，评审追问「这数据哪来的」时无法回答。

## 校验

```bash
python scripts/validate_schemas.py
```

## 幂等性要求

架构书三(二)规定定时任务「同一天重复触发不应产生重复简报」。
因此简报文件名固定为 `briefing-YYYY-MM-DD.json`，**同日重复生成直接覆盖**，
不产生 `briefing-2026-09-18-2.json` 这类文件。
