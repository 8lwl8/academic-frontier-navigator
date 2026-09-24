---
id: kn-0009
title: 层归一化
domain: 自然语言处理
sub_domain: 训练与优化
knowledge_point: 层归一化
level: 经典
tags: [LayerNorm, 归一化, 训练稳定性, 激活分布]
source:
  type: paper
  title: Layer Normalization
  authors: [Jimmy Lei Ba, Jamie Ryan Kiros, Geoffrey E. Hinton]
  url: https://arxiv.org/abs/1607.06450
  published_date: 2016-07-21
prerequisites: []
created_at: 2026-09-18
updated_at: 2026-09-18
---

# 层归一化

## 一句话概括

对单个样本在特征维度上做归一化，使每层的激活分布保持稳定，且不依赖批大小，因而适配变长序列与在线推理。

## 核心内容

神经网络的训练依赖各层输入分布相对稳定。当浅层参数更新时，深层的输入分布随之漂移，深层需要不断重新适应 —— 这被称为内部协变量偏移，是深层网络难以训练的原因之一。

**归一化的通用思路**是：把某一组数值的均值与方差拉回标准范围，再用两个可学习参数 `γ`（缩放）与 `β`（平移）恢复必要的表达能力：

```text
y = γ · (x − μ) / √(σ² + ε) + β
```

关键在于**沿哪个维度统计 `μ` 与 `σ`**。这决定了归一化方案能否用于序列任务：

| 方案 | 统计维度 | 是否依赖批大小 | 适配变长序列 | 适配在线推理 |
| --- | --- | --- | --- | --- |
| **批归一化**（BatchNorm） | 跨样本，对每个特征 | ✅ 依赖 | ❌ 困难 | ❌ 需存运行时统计量 |
| **层归一化**（LayerNorm） | 单样本内，跨特征 | ❌ 不依赖 | ✅ 天然适配 | ✅ 逐样本独立 |

**LayerNorm 之所以成为 Transformer 的标配**，原因正在最后两列：

1. **不依赖批大小**。NLP 的序列长度可变，同一批内的样本长度不一，按批统计会产生有偏的均值方差。LayerNorm 对每个样本独立统计，完全规避这一问题。
2. **推理时行为一致**。BatchNorm 在训练时用批统计、推理时用累积的运行时统计，两者不一致会引入误差；LayerNorm 在两种模式下计算完全相同。

**在 Transformer 中的两种摆放方式**（这是实践中最重要的细节）：

| 方式 | 公式 | 特点 |
| --- | --- | --- |
| **Post-LN**（原论文） | `LayerNorm(x + Sublayer(x))` | 残差路径上的值未被归一化，深层易发散，需学习率预热 |
| **Pre-LN**（后续主流） | `x + Sublayer(LayerNorm(x))` | 残差路径保持恒等，梯度更稳定，**免预热即可训练深层模型** |

Pre-LN 的普及是大模型能堆叠到数十层的工程前提之一，它通常与 `kn-0008`（残差连接）配套出现 —— 两者一起构成深度网络可训练性的基础。

> **本知识点同样不依赖 NLP 前置**：LayerNorm 是通用优化技术，源自对循环网络的改进。`prerequisites` 为空，可与 `kn-0001`、`kn-0008` 并行学习。

## 与学习路线的关联

前置知识点：无（可最先学习）。

后继知识点：

- `kn-0006`（Transformer 架构）—— 作为其三个必要前置之一。
- `kn-0008`（残差连接）—— 与之配对使用，顺序上两者可互换（此处按 `id` 升序建立 `related_to` 关系）。

> 学习提示：建议动手对比 Post-LN 与 Pre-LN 在 12 层模型上的训练曲线。这是理解「为什么原论文需要学习率预热而现代实现不需要」的最直接方式，也是把本知识点从「知道」变为「会用」的分界线。

## 参考来源

1. Ba, J. L., Kiros, J. R., & Hinton, G. E. *Layer Normalization*. arXiv:1607.06450, 2016. <https://arxiv.org/abs/1607.06450>
2. He, K., Zhang, X., Ren, S., & Sun, J. *Deep Residual Learning for Image Recognition*. arXiv:1512.03385, 2015. <https://arxiv.org/abs/1512.03385>
