---
id: kn-0004
title: 注意力机制
domain: 自然语言处理
sub_domain: 序列建模
knowledge_point: 注意力机制
level: 经典
tags: [注意力, 对齐, 编码器解码器, 长距离依赖, 动态上下文]
source:
  type: paper
  title: Neural Machine Translation by Jointly Learning to Align and Translate
  authors: [Dzmitry Bahdanau, Kyunghyun Cho, Yoshua Bengio]
  url: https://arxiv.org/abs/1409.0473
  published_date: 2014-09-01
prerequisites: [kn-0003]
created_at: 2026-09-18
updated_at: 2026-09-18
---

# 注意力机制

## 一句话概括

不再把源序列压成一个定长向量，而是让解码器在每一步**动态地**从源序列的全部位置中挑选当前最需要的信息。

## 核心内容

`kn-0003` 的编码器-解码器结构存在一个结构性瓶颈：无论源句多长，解码器只能看到一个固定维度的向量。**注意力机制**直接取消了这一瓶颈。

它的核心机制是用**加权求和**替代**固定压缩**：

1. 编码器不再只输出最后一个隐状态，而是保留**每一步**的隐状态 `h_1 ... h_T`；
2. 解码器在第 t 步生成时，计算当前状态与每个 `h_i` 的**相关性得分**；
3. 用 softmax 把得分归一化为权重 `α_i`；
4. 以 `α_i` 为权重对所有 `h_i` 加权求和，得到**针对当前步的上下文向量**。

这个上下文向量**每步都不同**，由当前解码需求动态决定。于是「对齐」不再由固定的空间结构承担，而是由可学习的相关性得分自然涌现 —— 论文标题中的「jointly learning to align」正是指这一点：对齐不是预先标注的，而是与翻译模型联合训练出来的。

**为什么这一改动如此关键**：它把信息通路的长度从「与序列长度成正比」缩短为「常数级」—— 解码器的每一步都能直接访问源序列的任意位置，无需经过隐状态的反复传递。这同时缓解了梯度在长序列上衰减的问题。

**代价**：计算复杂度从 O(T) 上升为 O(T²)（每个位置都要与所有位置计算相关性）。这在 2014 年是可接受的小代价，但成为后续 `kn-0006`（Transformer）在大规模场景下的主要成本来源，也是长上下文研究的核心议题。

## 与学习路线的关联

前置知识点：`kn-0003`（循环神经网络）—— 必须先理解「定长瓶颈」是什么，才能理解注意力在解决什么。

后继知识点：

- `kn-0006`（Transformer 架构）—— 把注意力从「RNN 的辅助组件」提升为**唯一的核心机制**，同时用缩放点积与多头设计加以强化。
- `kn-0007`（多头注意力）—— 对「注意力应该同时关注多种不同类型的关系」这一观察的工程化回应。

> 这是整条路线中**承上启下的枢纽知识点**。如果说 `kn-0006` 是当代大模型的地基，那么本知识点就是这块地基的第一块砖 —— 它提出了「动态加权检索」这一后来被反复复用的思想，包括检索增强生成等方法在概念上都可追溯至此。

## 参考来源

1. Bahdanau, D., Cho, K., & Bengio, Y. *Neural Machine Translation by Jointly Learning to Align and Translate*. arXiv:1409.0473, 2014. <https://arxiv.org/abs/1409.0473>
2. Sutskever, I., Vinyals, O., & Le, Q. V. *Sequence to Sequence Learning with Neural Networks*. arXiv:1409.3215, 2014. <https://arxiv.org/abs/1409.3215>
