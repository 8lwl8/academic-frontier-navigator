# 工具脚本

> 依据：SPEC-02 §6 格式转换链、SPEC-03 §7 CI 边界

## 校验脚本

| 脚本 | 用途 | 依据 |
| --- | --- | --- |
| `validate_schemas.py` | 校验 `data/` 下 JSON 是否符合 `schemas/` 契约 | SPEC-02 §4 |
| `scan_secrets.py` | 扫描疑似密钥 | SPEC-02 §8 |
| `block_private_data.py` | 拦截真实个人数据入库 | SPEC-02 §7 |

## 使用

```bash
python scripts/validate_schemas.py
python scripts/scan_secrets.py
python scripts/block_private_data.py
```

`scan_secrets.py` 与 `block_private_data.py` 支持传入文件列表（供 pre-commit 钩子调用）。

## 待补充

数据导出脚本（`knowledge/` → `data/`）尚未实现，按 SPEC-02 §6 的转换链补充：

```text
knowledge/domains/*.md  →  scripts/export_*.py  →  data/*.json
```

> 转换链**单向**，禁止反向手工编辑 `data/`。
