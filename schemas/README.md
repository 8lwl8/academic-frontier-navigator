# JSON Schema 契约

> 依据：SPEC-02 §4 JSON 约定 —— 每个 JSON 类型必须有对应 Schema

| Schema | 对应数据 | 存放位置 |
| --- | --- | --- |
| `route.schema.json` | 学习路线 | `data/route/` |
| `briefing.schema.json` | 每日简报 | `data/briefing/` |
| `asset.schema.json` | 知识资产 | `data/assets/` |

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
