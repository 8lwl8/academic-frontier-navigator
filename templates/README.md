# 版本留痕模板

> 依据：SPEC-03 §6 版本留痕体系

五类留痕载体，对应六个模板文件。

| 模板 | 对应留痕载体 | 使用时机 | 落位 |
| --- | --- | --- | --- |
| `commit-message.template.txt` | ① 提交信息 | 每次提交 | Git 历史 |
| `CHANGELOG.template.md` | ② 变更日志 | 每次发版 | `CHANGELOG.md` |
| `iteration-log.template.md` | ③ **AI 迭代记录** | 每轮迭代 24h 内 | `iteration-log/` |
| `decision-record.template.md` | ④ 架构决策记录 | 决策发生时 | `docs/decisions/` |
| `pr.template.md` | ⑤ 拉取请求 | 每次提 PR | GitHub PR |
| `release-note.template.md` | ⑥ 发布说明 | 每次打标签 | GitHub Release |

> **③ AI 迭代记录是评审举证的核心材料**（AI 工具使用占评分 25%）。
> 记录要求：含**原始提示词全文**与**人工调整说明**，且**只增不删**。

## 使用方式

直接复制模板到目标位置并按格式填写。`iteration-log.template.md` 的文件名应为
`iteration-log/YYYY-MM-DD-<主题>.md`。
