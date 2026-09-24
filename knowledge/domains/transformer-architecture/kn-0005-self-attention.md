---
id: kn-0005
title: 缩放点积注意力与自注意力
domain: 自然语言处理
sub_domain: Transformer 架构
knowledge_point: 自注意力
level: 经典
tags: [自注意力, 缩放点积, QKV, 并行计算, Transformer]
source:
  type: paper
  title: Attention Is All You Need
  authors: [Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit]
  url: https://arxiv.org/abs/1706.03762
  published_date: 2017-06-12
prerequisites: [kn-0004]
created_at: 2026-09-18
updated_at: 2026-09-18
---

# 缩放点积注意力与自注意力

## 一句话概括

让序列中的每个位置直接与所有其他位置交互，并用「查询-键-值」三投影把这种交互表达为可并行的矩阵运算，彻底摆脱对循环结构的依赖。

## 核心内容

`kn-0004` 的注意力仍依附于 RNN：它需要 RNN 逐时间步产出隐状态作为被检索的对象，因此**无法并行**——第 t 步必须等第 t-1 步算完。这在大规模训练中成为效率瓶颈。

**自注意力**（self-attention）取消了这一依附：让序列**自己**同时充当查询方与被查询方。每个位置的向量被投影为三个角色：

| 角色 | 符号 | 含义 |
| --- | --- | --- |
| **查询** | Q | 当前位置「我想找什么」 |
| **键** | K | 每个位置「我是什么，可供谁匹配」 |
| **值** | V | 每个位置「匹配上之后我提供什么内容」 |

计算为：

```text
Attention(Q, K, V) = softmax(QKᵀ / √d_k) · V
```

**两个设计细节值得单独记住**：

1. **除以 √d_k**（缩放）。`d_k` 是键的维度。若不缩放，当 `d_k` 较大时，`QKᵀ` 的点积结果的方差随维度增长，导致 softmax 进入饱和区 —— 梯度趋近于零，训练停滞。除以 `√d_k` 使点积结果方差归一到 1 附近。**这是一个纯工程性的数值稳定性处理，但少了它模型训不起来**，是面试与复现中最常被考察的细节之一。
2. **不引入循环**。整个计算是三次矩阵乘法加一次 softmax，全部可以并行。序列位置之间的交互由 `QKᵀ` 一次性完成，无需逐步传递。

**与 RNN 的根本差异**：

| 维度 | RNN（`kn-0003`） | 自注意力（本知识点） |
| --- | --- | --- |
| 任意两位置的信息通路长度 | O(T) | **O(1)** |
| 单层计算复杂度 | O(T·d²) | **O(T²·d)** |
| 训练并行性 | ❌ 时间步串行 | ✅ 全部并行 |
| 位置信息 | 天然由顺序隐含 | ❌ **丢失，需显式注入**（见 `kn-0006`） |

最后一行是自注意力的**结构性代价**：由于所有位置被同时处理，模型无法从顺序本身获得位置感。因此必须额外加位置编码，这一处理被归类到 `kn-0006`（Transformer 架构）。

## 与学习路线的关联

前置知识点：`kn-0004`（注意力机制）—— 需先理解「动态加权检索」这一思想，本知识点只是把它改为自查询并加上数值缩放。

后继知识点：

- `kn-0006`（Transformer 架构）—— 本知识点是其核心组件，但完整架构还需位置编码、残差连接与 LayerNorm 配合（见 `kn-0008`、`kn-0009`）。
- `kn-0007`（多头注意力）—— 单头自注意力只能学到一种相关性模式，多头是对此的直接扩展。

> **学习提示**：本知识点是整个方向的**技术核心**，值得投入最多时间。建议动手实现一遍完整的缩放点积注意力（约 20 行代码），并验证：去掉 `√d_k` 缩放后，在 `d_k = 512` 时 softmax 输出是否退化为近似 one-hot。

## 参考来源

1. Vaswani, A., Shazeer, N., Parmar, N., & Uszkoreit, J. *Attention Is All You Need*. arXiv:1706.03762, 2017. <https://arxiv.org/abs/1706.03762>
2. Bahdanau, D., Cho, K., & Bengio, Y. *Neural Machine Translation by Jointly Learning to Align and Translate*. arXiv:1409.0473, 2014. <https://arxiv.org/abs/1409.0473>
