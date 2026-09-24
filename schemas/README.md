# JSON Schema 契约

> 依据：SPEC-02 §4 JSON 约定 —— 每个 JSON 类型必须有对应 Schema

| Schema | 对应数据 | 存放位置 |
| --- | --- | --- |
| `route.schema.json` | 学习路线 | `data/route/` |
| `briefing.schema.json` | 每日简报 | `data/briefing/` |
| `asset.schema.json` | 知识资产 | `data/assets/` |
| `knowledge-graph.schema.json` | 知识点依赖图导出 | `knowledge/domains/_graph.json` |

## 校验

```bash
python scripts/validate_schemas.py
```

## 新增数据类型的步骤

1. 在本目录新增 `<类型>.schema.json`。
2. 在 `scripts/validate_schemas.py` 的 `SCHEMA_MAP` 中登记「文件名前缀 → Schema 文件」映射。
3. 若涉及结构契约变更，在 `docs/decisions/` 新增 ADR。

## 版本约定

Schema 内的 `schema_version` 字段与 Schema 文件本身**同步演进**：
破坏性变更递增主版本号（`"1.0"` → `"2.0"`），且必须走 ADR 流程。

## 已有约定

- 所有数据文件必含 `schema_version`、`generated_at`（`generated_by` 建议填）。
- 学术内容必须含 `source` 对象，`source.url` 必填。
- 时间格式：`YYYY-MM-DD` 或带 `+08:00` 时区的 ISO 8601。
- 字段名一律 `lower_snake_case`。

## 关于 `knowledge-graph.schema.json`

该 Schema 校验的是**依赖图的导出产物** `knowledge/domains/_graph.json`，
不是人类阅读的 `knowledge/domains/_index.md`。两者是同源的两份视图：

- `_index.md` 面向人：子方向登记、知识点清单、缺口与待办。
- `_graph.json` 面向机器：节点表 + 边表 + 统计量，供路线生成与 Web 侧绘图消费。

它的权威来源仍是各知识单元 front matter 里的 `prerequisites` 字段
（详见 SPEC-06 §5 与 ADR-0001）。

### `stats.root_nodes` / `stats.sink_nodes` 的计算口径

这两个字段容易算错，口径已固化在 Schema 的字段描述里：

> **只在 `prerequisite_of` 与 `extends` 子图上计算**，`related_to` 不计入度数。

理由：`related_to` 是对称的弱关联，不构成学习顺序上的前置或后继。
`root_nodes` 是「可以直接开始学」的知识点，`sink_nodes` 是「没有后继依赖它」的知识点，
两者描述的都是**学习路线的头尾**，因此只应看前置边。

> ⚠️ **这个口径是被一次真实事故逼出来的。** 该 Schema 首次定稿时，`_graph.json` 的
> `root_nodes` 被误填为全部 15 个节点（真实为 5 个），`_index.md` 又写作 4 个 ——
> `additionalProperties: false` 与 `has_cycle` 的 `const: false` 都没能拦住它，
> **因为它们是手写 JSON 且与源数据比对从未发生过**。
> 现在由 `scripts/check_knowledge_units.py` 的 `check_graph_export()` 强制比对
> （SPEC-06 §5.6）。

Schema 校验**契约形状**（字段是否存在、类型是否正确），
派生数据校验**取值是否与源数据一致** —— 两者互补，缺一不可。
