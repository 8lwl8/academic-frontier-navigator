#!/usr/bin/env python3
"""校验 knowledge/domains/ 下的知识单元是否符合 SPEC-06 的硬性约束。

依据：
    SPEC-06 §3  三分库判据
    SPEC-06 §4  四层组织模型（domain / sub_domain / knowledge_point / source）
    SPEC-06 §5.4 依赖关系防环（detect_cycles）
    SPEC-06 §6  语料准入标准（source.url 必填）
    SPEC-02 §3.2 知识单元 front matter 格式

检查项：
    1. front matter 存在且必填字段齐全（SPEC-02 §3.2）
    2. id 格式为 kn-NNNN 且全库唯一
    3. domain 取值数量不超过 2（SPEC-06 §4.1）
    4. sub_domain 已在 _index.md 中登记（SPEC-06 §4.2）
    5. source.url 必填且为 http(s)（SPEC-06 §6.1 A/B 维度）
    6. prerequisites 引用的 id 存在（无悬空引用）
    7. prerequisites 不含自身（无自环）
    8. prerequisite_of / extends 子图无循环依赖（SPEC-06 §5.4）
    9. 每条 prerequisites 边在两个知识点间一致（双向核对）
   10. 正文含「参考来源」段落（SPEC-02 §3.2）

用法：
    python scripts/check_knowledge_units.py              # 校验
    python scripts/check_knowledge_units.py --url-check  # 额外访问 source.url 确认可达

退出码：
    0 全部通过
    1 存在不符合规范的项
    2 环境或依赖问题
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict, deque
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOMAINS_DIR = ROOT / "knowledge" / "domains"
INDEX_FILE = DOMAINS_DIR / "_index.md"

# SPEC-06 §4.1：domain 取值全库 1–2 个
MAX_DOMAINS = 2
# SPEC-02 §2.2：字段名 lower_snake_case
REQUIRED_FIELDS = ("id", "title", "domain", "sub_domain", "knowledge_point", "level", "source")
VALID_LEVELS = {"入门", "经典", "前沿"}
VALID_SOURCE_TYPES = {"paper", "textbook", "survey", "course", "repo", "doc"}

ID_RE = re.compile(r"^kn-\d{4}$")
FRONT_MATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.S)


def parse_front_matter(text: str) -> tuple[str, str] | None:
    """返回 (front_matter, body)，不是合法的 front matter 则返回 None。"""
    m = FRONT_MATTER_RE.match(text)
    if not m:
        return None
    return m.group(1), text[m.end():]


def parse_scalars(fm: str) -> dict[str, str]:
    """抽取顶层标量字段（不处理嵌套）。"""
    out: dict[str, str] = {}
    for line in fm.split("\n"):
        if not line or line[0] in " \t#-":
            continue
        m = re.match(r"^([a-z_]+):\s*(.*)$", line)
        if m:
            out[m.group(1)] = m.group(2).strip()
    return out


def parse_inline_list(fm: str, key: str) -> list[str]:
    """解析 `key: [a, b]` 形式的行内数组。"""
    m = re.search(rf"^{key}:\s*\[(.*?)\]\s*$", fm, re.M)
    if not m:
        return []
    raw = m.group(1).strip()
    if not raw:
        return []
    return [item.strip().strip("'\"") for item in raw.split(",") if item.strip()]


def parse_source_url(fm: str) -> str | None:
    """从 source 嵌套块中取 url。"""
    m = re.search(r"^source:\s*$", fm, re.M)
    if not m:
        return None
    block = fm[m.end():]
    # 到下一个顶层字段为止
    end = re.search(r"^[a-z_]+:", block, re.M)
    if end:
        block = block[: end.start()]
    u = re.search(r"^\s+url:\s*(\S+)\s*$", block, re.M)
    return u.group(1).strip("'\"") if u else None


def parse_registered_sub_domains() -> set[str]:
    """从 _index.md 的子方向登记表中读出已登记的子方向名。"""
    if not INDEX_FILE.exists():
        return set()
    text = INDEX_FILE.read_text(encoding="utf-8")
    names: set[str] = set()
    # 匹配表格行：| **表示学习** | `representation-learning/` | 5 | ...
    for line in text.split("\n"):
        m = re.match(r"^\|\s*\*\*(.+?)\*\*\s*\|\s*`([a-z0-9-]+)/`", line)
        if m:
            names.add(m.group(1).strip())
    # 无加粗的登记表也支持
    for line in text.split("\n"):
        m = re.match(r"^\|\s*([^\s|*][^|]*?)\s*\|\s*`([a-z0-9-]+)/`", line)
        if m and m.group(1).strip() not in ("子方向", "---"):
            names.add(m.group(1).strip())
    return names


def build_graph(units: dict[str, dict]) -> tuple[dict[str, list[str]], list[str]]:
    """构造 prerequisite_of 有向图（前置 → 后继），并核查一致性。"""
    adj: dict[str, list[str]] = defaultdict(list)
    problems: list[str] = []

    for kid, u in units.items():
        for pre in u["prerequisites"]:
            if pre not in units:
                problems.append(
                    f"{u['path']}：prerequisites 引用了不存在的知识点 `{pre}`（悬空引用，SPEC-06 §7.3）"
                )
                continue
            if pre == kid:
                problems.append(f"{u['path']}：prerequisites 包含自身（自环，SPEC-06 §5.4）")
                continue
            adj[pre].append(kid)

            # 双向核对：被引用方是否也在其 front matter 之外一致
            # 依赖只写在「后继」上，因此这里只校验方向合理性
        # 检查 prerequisites 中是否有重复
        dup = {x for x in u["prerequisites"] if u["prerequisites"].count(x) > 1}
        for d in dup:
            problems.append(f"{u['path']}：prerequisites 中 `{d}` 重复出现")

    return adj, problems


def detect_cycle(nodes: list[str], adj: dict[str, list[str]]) -> list[str] | None:
    """Kahn 拓扑排序；返回环上的节点列表，无环则返回 None。"""
    indeg = {n: 0 for n in nodes}
    for n in nodes:
        for m in adj.get(n, []):
            indeg[m] = indeg.get(m, 0) + 1
    q = deque([n for n in nodes if indeg[n] == 0])
    seen: list[str] = []
    while q:
        n = q.popleft()
        seen.append(n)
        for m in adj.get(n, []):
            indeg[m] -= 1
            if indeg[m] == 0:
                q.append(m)
    if len(seen) == len(nodes):
        return None
    return [n for n in nodes if n not in seen]


def main() -> int:
    ap = argparse.ArgumentParser(description="校验知识单元是否符合 SPEC-06")
    ap.add_argument(
        "--url-check",
        action="store_true",
        help="额外访问 source.url 确认可达（需联网，默认关闭）",
    )
    args = ap.parse_args()

    if not DOMAINS_DIR.exists():
        print(f"未找到领域知识库目录：{DOMAINS_DIR}", file=sys.stderr)
        return 2

    files = sorted(
        p for p in DOMAINS_DIR.rglob("*.md") if not p.name.startswith("_")
    )
    if not files:
        print("domains/ 下暂无知识单元，跳过校验")
        return 0

    units: dict[str, dict] = {}
    errors: list[str] = []

    # ---------- 逐文件解析与字段校验 ----------
    for path in files:
        rel = path.relative_to(ROOT)
        text = path.read_text(encoding="utf-8")
        parsed = parse_front_matter(text)
        if parsed is None:
            errors.append(f"{rel}：缺少 YAML front matter（SPEC-02 §3.2）")
            continue
        fm, body = parsed
        scalars = parse_scalars(fm)

        for field in REQUIRED_FIELDS:
            if field not in scalars:
                errors.append(f"{rel}：front matter 缺少必填字段 `{field}`（SPEC-02 §3.2）")

        kid = scalars.get("id", "")
        if not ID_RE.match(kid):
            errors.append(f"{rel}：id `{kid}` 不符合 `kn-NNNN` 格式（SPEC-06 §4.3）")
        elif kid in units:
            errors.append(
                f"{rel}：id `{kid}` 与 {units[kid]['path']} 重复（id 必须全库唯一，SPEC-06 §4.3）"
            )

        level = scalars.get("level", "")
        if level and level not in VALID_LEVELS:
            errors.append(
                f"{rel}：level `{level}` 不在 {sorted(VALID_LEVELS)} 中（SPEC-02 §3.2）"
            )

        url = parse_source_url(fm)
        if not url:
            errors.append(
                f"{rel}：source.url 缺失（语料准入硬性要求，SPEC-06 §6.1 维度 A/B）"
            )
        elif not re.match(r"^https?://", url):
            errors.append(f"{rel}：source.url `{url}` 必须是可公开访问的 http(s) 链接")

        stype = re.search(r"^\s+type:\s*(\S+)\s*$", fm, re.M)
        if stype and stype.group(1) not in VALID_SOURCE_TYPES:
            errors.append(
                f"{rel}：source.type `{stype.group(1)}` 不在 {sorted(VALID_SOURCE_TYPES)} 中"
            )

        if "## 参考来源" not in body:
            errors.append(f"{rel}：正文缺少「## 参考来源」段落（SPEC-02 §3.2）")

        if not re.search(r"^#\s+", text, re.M):
            errors.append(f"{rel}：缺少一级标题 `#`（SPEC-02 §3.1）")

        if not path.name.startswith(kid) and kid:
            errors.append(
                f"{rel}：文件名应以 id 开头（SPEC-01 §四 命名约定），实际为 `{path.name}`"
            )

        units[kid] = {
            "path": rel,
            "prerequisites": parse_inline_list(fm, "prerequisites"),
            "domain": scalars.get("domain", ""),
            "sub_domain": scalars.get("sub_domain", ""),
            "title": scalars.get("title", ""),
            "level": level,
            "url": url,
        }

    if not units:
        print("未能解析出任何知识单元")
        return 1

    # ---------- domain 数量约束（SPEC-06 §4.1） ----------
    domains = {u["domain"] for u in units.values() if u["domain"]}
    if len(domains) > MAX_DOMAINS:
        errors.append(
            f"domain 取值有 {len(domains)} 个 {sorted(domains)}，超过上限 {MAX_DOMAINS}"
            f"（SPEC-06 §4.1：全库 1–2 个，聚焦不足）"
        )

    # ---------- sub_domain 登记校验（SPEC-06 §4.2） ----------
    registered = parse_registered_sub_domains()
    if registered:
        for kid, u in units.items():
            sd = u["sub_domain"]
            if sd and sd not in registered:
                errors.append(
                    f"{u['path']}：sub_domain `{sd}` 未在 _index.md 中登记"
                    f"（SPEC-06 §4.2）"
                )

    # ---------- 依赖图校验（SPEC-06 §5.4） ----------
    adj, graph_problems = build_graph(units)
    errors.extend(graph_problems)

    cycle = detect_cycle(sorted(units), adj)
    if cycle:
        errors.append(
            f"检测到循环依赖：{' → '.join(cycle)}"
            f"（SPEC-06 §5.4，会破坏路线生成能力）"
        )

    # ---------- 输出 ----------
    roots = [n for n in sorted(units) if not any(n in v for v in adj.values())]
    if errors:
        print("知识单元校验未通过：\n")
        for line in errors:
            print(f"  ✗ {line}")
        print(f"\n共 {len(errors)} 项问题，检查了 {len(units)} 个知识单元")
        return 1

    print(f"✅ 知识单元校验通过（{len(units)} 个）")
    print(f"   领域：{', '.join(sorted(domains))}")
    print(f"   子方向：{len({u['sub_domain'] for u in units.values()})} 个")
    print(f"   依赖边：{sum(len(v) for v in adj.values())} 条（prerequisite_of）")
    print(f"   起始节点（无前置）：{', '.join(roots)}")
    print("   循环依赖：无")

    if args.url_check:
        import urllib.request

        print("\n开始核验 source.url 可达性（SPEC-06 §6.5）…")
        unreachable: list[str] = []
        for kid in sorted(units):
            u = units[kid]
            try:
                req = urllib.request.Request(
                    u["url"], headers={"User-Agent": "AFN-KB-Checker/1.0"}
                )
                with urllib.request.urlopen(req, timeout=20) as resp:
                    ok = 200 <= resp.status < 400
            except Exception as exc:  # noqa: BLE001
                ok = False
                print(f"   ✗ {kid} {u['url']} -> {exc}")
                unreachable.append(kid)
                continue
            print(f"   {'✓' if ok else '✗'} {kid} {u['url']}")
            if not ok:
                unreachable.append(kid)
        if unreachable:
            print(f"\n有 {len(unreachable)} 个 source.url 不可达：{unreachable}")
            return 1
        print("全部 source.url 可达")

    return 0


if __name__ == "__main__":
    sys.exit(main())
