# 配置

> 依据：SPEC-02 §5 YAML 约定、SPEC-03 §7 CI 边界

| 文件 | 用途 |
| --- | --- |
| `afn.config.yaml` | **主配置**：定时任务、知识库、合规、Web、数据格式 |
| `commitlint.config.js` | 提交信息格式校验规则 |
| `.pre-commit-config.yaml` | 提交前本地校验钩子 |

## 主配置说明

`afn.config.yaml` 是唯一的运行配置入口，承载架构书三(二)定时任务的可配置项：

| 配置段 | 依据 |
| --- | --- |
| `frontier_radar` | 架构书 三(二) 定时任务设计（触发策略、任务范围、产出形态、幂等性、失败处理） |
| `relevance` | 架构书 四(二) 按相关性分层的列表 |
| `knowledge_base` | 架构书 三(四) 知识库设计（分库结构、语料准入） |
| `memory` | 架构书 三(三) 长期记忆策略 |
| `compliance` | 架构书 六(二) 合规设计要点（五条） |
| `web` | 架构书 四(二)、五(二) Web 侧约束 |
| `formats` | 架构书 五(一) 数据格式选型 |

## ⚠️ 密钥管理

**本目录下任何文件都不得包含真实密钥。** 需要时用 `${ENV_VAR_NAME}` 引用环境变量。

```yaml
service:
  api_key: ${AFN_API_KEY}   # ✅ 正确
  # api_key: "sk-xxxxx"     # ❌ 严禁
```

> 架构书五(一)已说明智能体能力全部由 LearnBuddy 平台承载，Web 侧不独立调用大模型 API，
> 因此本项目理论上不需要在仓库中存放任何模型密钥。
> 若出现「需要往仓库放 API Key」的需求，先回头确认是否违背了架构书五(三)的排除项。

## 启用钩子

```bash
pip install pre-commit
pre-commit install --config configs/.pre-commit-config.yaml
```
