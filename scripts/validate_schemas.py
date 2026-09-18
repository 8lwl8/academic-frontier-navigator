#!/usr/bin/env python3
"""校验 data/ 下的 JSON 文件是否符合 schemas/ 中定义的契约。

依据：SPEC-02 §4 JSON 约定 —— 每个 JSON 类型必须有对应 Schema。

用法：
    python scripts/validate_schemas.py

退出码：
    0 全部通过
    1 存在不符合契约的文件
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    from jsonschema import Draft202012Validator
except ImportError:
    print("缺少依赖：pip install jsonschema", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_DIR = ROOT / "schemas"

# 文件名前缀 -> Schema 文件名的映射
# 新增数据类型时在此登记，避免"有数据无契约"。
SCHEMA_MAP = {
    "route": "route.schema.json",
    "briefing": "briefing.schema.json",
    "asset": "asset.schema.json",
}


def pick_schema(file_name: str) -> Path | None:
    """按文件名前缀选择对应 Schema。"""
    for prefix, schema_name in SCHEMA_MAP.items():
        if file_name.startswith(f"{prefix}-") or file_name == f"{prefix}.json":
            candidate = SCHEMA_DIR / schema_name
            return candidate if candidate.exists() else None
    return None


def main() -> int:
    if not SCHEMA_DIR.exists():
        print(f"未找到 Schema 目录：{SCHEMA_DIR}", file=sys.stderr)
        return 1

    data_files = sorted((ROOT / "data").rglob("*.json")) if (ROOT / "data").exists() else []
    if not data_files:
        print("data/ 下暂无 JSON 文件，跳过校验")
        return 0

    validator_cache: dict[Path, Draft202012Validator] = {}
    errors: list[str] = []
    checked = 0

    for data_file in data_files:
        schema_path = pick_schema(data_file.name)
        if schema_path is None:
            errors.append(
                f"{data_file.relative_to(ROOT)}：未登记对应 Schema"
                f"（请在 scripts/validate_schemas.py 的 SCHEMA_MAP 中登记）"
            )
            continue

        if schema_path not in validator_cache:
            validator_cache[schema_path] = Draft202012Validator(
                json.loads(schema_path.read_text(encoding="utf-8"))
            )
        validator = validator_cache[schema_path]

        try:
            payload = json.loads(data_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{data_file.relative_to(ROOT)}：JSON 语法错误 -> {exc}")
            continue

        checked += 1
        for err in sorted(validator.iter_errors(payload), key=lambda e: list(e.path)):
            location = "/".join(str(p) for p in err.path) or "(根)"
            errors.append(
                f"{data_file.relative_to(ROOT)} @ {location}：{err.message}"
            )

    if errors:
        print("JSON 契约校验未通过：\n")
        for line in errors:
            print(f"  ✗ {line}")
        return 1

    print(f"JSON 契约校验通过（{checked} 个文件）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
