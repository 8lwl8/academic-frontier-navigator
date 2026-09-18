#!/usr/bin/env python3
"""扫描仓库中的疑似密钥，防止凭据泄露。

依据：SPEC-02 §8 密钥管理。
背景：架构书 五(一) 已说明智能体能力全部由 LearnBuddy 平台承载，
      Web 侧不独立调用大模型 API，因此本项目理论上不需要在仓库中
      存放任何模型密钥。一旦检出，优先怀疑是否违背了架构书 五(三) 的排除项。

用法：
    python scripts/scan_secrets.py [文件...]
    不带参数时扫描整个仓库（跳过 .git 与二进制文件）

退出码：
    0 未发现疑似密钥
    1 发现疑似密钥
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# 常见密钥特征。刻意保守：宁可少报，也不要把正常文本误判为密钥。
PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("OpenAI 类密钥", re.compile(r"\bsk-[A-Za-z0-9]{20,}\b")),
    ("GitHub Token", re.compile(r"\b(gh[pousr]_[A-Za-z0-9]{16,})\b")),
    ("Anthropic 密钥", re.compile(r"\bsk-ant-[A-Za-z0-9\-_]{20,}\b")),
    ("AWS Access Key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("Google API Key", re.compile(r"\bAIza[0-9A-Za-z\-_]{35}\b")),
    ("私钥文件头", re.compile(r"-----BEGIN (RSA |EC |OPENSSH |PGP )?PRIVATE KEY-----")),
    ("Slack Token", re.compile(r"\bxox[baprs]-[A-Za-z0-9\-]{10,}\b")),
    (
        "硬编码敏感赋值",
        re.compile(
            r"""(?ix)
            (?:api[_-]?key|apikey|secret[_-]?key|access[_-]?token|auth[_-]?token)
            \s*[:=]\s*
            ["'][A-Za-z0-9\-_/+]{16,}["']
            """
        ),
    ),
]

# 允许出现的占位符（模板与示例中的正常内容）
ALLOWLIST = re.compile(
    r"""(?ix)
    (\$\{[A-Z_]+\}          # ${ENV_VAR} 形式
    |your[_-]?|<[^>]+>      # your_token / <token> 形式
    |xxx|example|placeholder|dummy|redacted|change[_-]?me)
    """
)

SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", ".mypy_cache"}
SKIP_SUFFIXES = {
    ".png", ".jpg", ".jpeg", ".gif", ".ico", ".pdf", ".zip",
    ".docx", ".xlsx", ".pptx", ".mp4", ".woff", ".woff2", ".ttf",
}
MAX_SIZE = 2 * 1024 * 1024  # 跳过超过 2MB 的文件


def iter_files(targets: list[str]) -> list[Path]:
    if targets:
        return [Path(t) for t in targets if Path(t).is_file()]
    found: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.suffix.lower() in SKIP_SUFFIXES:
            continue
        if path.stat().st_size > MAX_SIZE:
            continue
        found.append(path)
    return found


def scan(path: Path) -> list[str]:
    findings: list[str] = []
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return findings

    for lineno, line in enumerate(text.splitlines(), start=1):
        if ALLOWLIST.search(line):
            continue
        for label, pattern in PATTERNS:
            if pattern.search(line):
                findings.append(f"{path.name}:{lineno} 疑似 {label}")
                break
    return findings


def main() -> int:
    targets = sys.argv[1:]
    files = iter_files(targets)

    all_findings: list[str] = []
    for path in files:
        for finding in scan(path):
            try:
                rel = path.relative_to(ROOT)
            except ValueError:
                rel = path
            all_findings.append(f"{rel} -> {finding}")

    if all_findings:
        print("检测到疑似密钥，请立即处理（SPEC-02 §8）：\n")
        for line in all_findings:
            print(f"  ✗ {line}")
        print(
            "\n处置顺序（不可颠倒）：\n"
            "  1. 立即吊销该密钥（改代码无效，密钥已进入 Git 历史）\n"
            "  2. 改用 ${ENV_VAR_NAME} 环境变量引用\n"
            "  3. 在 iteration-log/ 记录本次事故与补救措施"
        )
        return 1

    print(f"密钥扫描通过（{len(files)} 个文件）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
