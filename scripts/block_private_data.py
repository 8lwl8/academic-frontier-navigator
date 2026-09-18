#!/usr/bin/env python3
"""拦截真实个人数据进入公开仓库。

依据：SPEC-02 §7 数据分类与可见度（架构书 六(一)）。
背景：用户画像、学习轨迹、个人知识资产属架构书 六(一) 的「中」敏感级，
      访问控制为「仅用户本人及授权范围」与「用户自主控制可见度」。
      本项目仓库为 Public，因此真实数据一律不入库，仅保留脱敏样例。

用法：
    python scripts/block_private_data.py [文件...]

退出码：
    0 未发现真实个人数据
    1 发现真实个人数据
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# 允许入库的文件形态：脱敏样例与说明文件
ALLOWED_PATTERNS = [
    re.compile(r"\.example\.(md|json|ya?ml)$", re.IGNORECASE),
    re.compile(r"\.template\.(md|json|ya?ml)$", re.IGNORECASE),
    re.compile(r"^README\.md$", re.IGNORECASE),
    re.compile(r"^\.gitkeep$"),
]

# 明确禁止的数据文件后缀
FORBIDDEN_SUFFIXES = (".private.md", ".private.json", ".private.yaml", ".private.yml")

# 疑似真实个人数据的字段名（在 personal 目录中出现即告警）
SENSITIVE_KEYS = re.compile(
    r"""(?ix)
    "(user_id|open_id|student_id|real_name|email|phone|mobile
      |id_card|学号|姓名|手机号|邮箱)"
    \s*:
    """
)

SKIP_DIRS = {".git", "node_modules", "__pycache__"}


def iter_files(targets: list[str]) -> list[Path]:
    if targets:
        return [Path(t) for t in targets if Path(t).is_file()]
    base = ROOT / "knowledge" / "personal"
    if not base.exists():
        return []
    return [
        p for p in base.rglob("*")
        if p.is_file() and not any(part in SKIP_DIRS for part in p.parts)
    ]


def is_allowed(path: Path) -> bool:
    return any(pat.search(path.name) for pat in ALLOWED_PATTERNS)


def main() -> int:
    files = iter_files(sys.argv[1:])
    if not files:
        print("knowledge/personal/ 下暂无文件，跳过校验")
        return 0

    violations: list[str] = []

    for path in files:
        try:
            rel = path.relative_to(ROOT)
        except ValueError:
            rel = path

        if not is_allowed(path):
            violations.append(
                f"{rel}：非脱敏样例文件。"
                f"真实个人数据不得入库，请改用 *.example.md / *.example.json 形式"
            )
            continue

        if path.name.lower().endswith(FORBIDDEN_SUFFIXES):
            violations.append(f"{rel}：命中禁止入库的后缀")
            continue

        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue

        for lineno, line in enumerate(text.splitlines(), start=1):
            if SENSITIVE_KEYS.search(line):
                violations.append(
                    f"{rel}:{lineno}：疑似真实身份字段。"
                    f"样例文件请使用匿名占位（如 profile-anon-0001）"
                )

    if violations:
        print("检测到不应入库的个人数据（SPEC-02 §7）：\n")
        for line in violations:
            print(f"  ✗ {line}")
        return 1

    print(f"个人数据拦截校验通过（{len(files)} 个文件）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
