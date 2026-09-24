# 工具脚本

> 依据：SPEC-02 §6 格式转换链、SPEC-03 §7 CI 边界

## 校验脚本

| 脚本 | 用途 | 依据 |
| --- | --- | --- |
| `check_knowledge_units.py` | 校验知识单元 front matter、编号唯一性、悬空引用、自环、循环依赖 | SPEC-06 §4 §5 |
| `validate_schemas.py` | 校验 `data/` 下 JSON 是否符合 `schemas/` 契约 | SPEC-02 §4 |
| `scan_secrets.py` | 扫描疑似密钥 | SPEC-02 §8 |
| `block_private_data.py` | 拦截真实个人数据入库 | SPEC-02 §7 |

## 使用

```bash
python scripts/check_knowledge_units.py            # 结构校验
python scripts/check_knowledge_units.py --url-check  # 附带校验 source.url 可达性（联网）
python scripts/validate_schemas.py
python scripts/scan_secrets.py
python scripts/block_private_data.py
```

`scan_secrets.py` 与 `block_private_data.py` 支持传入文件列表（供 pre-commit 钩子调用）。

## `check_knowledge_units.py` 检出的问题类型

| 类型 | 说明 | 能否被脚本检出 |
| --- | --- | --- |
| front matter 缺失或字段不全 | 缺少 SPEC-02 §3.2 规定的必填字段 | ✅ |
| 编号格式错误 | 不符合 `^kn-\d{4}$` | ✅ |
| 编号重复 | 同一 `id` 出现两次 | ✅ |
| 子方向未登记 | `sub_domain` 未出现在 `_index.md` 的登记表中 | ✅ |
| 出处不合规 | `source.url` 缺失或非 http(s) | ✅ |
| 悬空引用 | `prerequisites` 指向不存在的编号 | ✅ |
| 自环 | 知识点的前置是它自己 | ✅ |
| 循环依赖 | 依赖图中存在环（Kahn 拓扑排序检出） | ✅ |
| **漏边** | 实际存在依赖关系但未写入 `prerequisites` | ❌ **只能靠人工评审** |

> 最后一行是**已知局限**，详见 `docs/decisions/ADR-0001-explicit-dependency-graph.md` §五。
> 脚本保证的是**一致性**（现有声明互相不矛盾），不是**完整性**（该有的边都写了）。

## 待补充

数据导出脚本（`knowledge/` → `data/`）尚未完全实现，按 SPEC-02 §6 的转换链补充：

```text
knowledge/domains/*.md   →  scripts/export_graph.py  →  knowledge/domains/_graph.json
knowledge/domains/*.md   →  scripts/export_route.py  →  data/route/*.json
```

当前状态：

- `knowledge/domains/_graph.json` 与 `data/route/route-nlp-transformer.json`
  **已生成并通过 Schema 校验**，但生成过程尚未脚本化（为一次性手工推导）。
- `scripts/export_graph.py` 待实现：从各知识单元的 `prerequisites` 读取边表，
  按拓扑深度分阶段，产出 `_graph.json` 与路线文件。
- 实现后应把 `_graph.json` 加入 CI 校验，确保**重新生成的产物与仓库中一致**
  （否则说明有人手工改了导出文件，违反"单一事实来源"）。

> 转换链**单向**，禁止反向手工编辑 `data/` 与 `_graph.json`。
