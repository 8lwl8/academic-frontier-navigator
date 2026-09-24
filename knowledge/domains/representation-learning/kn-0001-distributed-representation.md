---
id: kn-0001
title: 词的分布式表示与词向量
domain: 自然语言处理
sub_domain: 表示学习
knowledge_point: 分布式表示
level: 入门
tags: [词向量, 分布式表示, 表示学习, 神经语言模型]
source:
  type: paper
  title: Efficient Estimation of Word Representations in Vector Space
  authors: [Tomas Mikolov, Kai Chen, Greg Corrado, Jeffrey Dean]
  url: https://arxiv.org/abs/1301.3781
  published_date: 2013-01-16
prerequisites: []
created_at: 2026-09-18
updated_at: 2026-09-18
---

# 词的分布式表示与词向量

## 一句话概括

用低维稠密向量表示词，使语义相近的词在向量空间中距离相近，从而把离散的符号计算转化为可微的几何计算。

## 核心内容

在词向量之前，自然语言处理普遍使用**独热表示**（one-hot）：词表有 V 个词，每个词就是一个 V 维向量，只有一位是 1。这种方式有两个致命问题：一是维度随词表线性增长（V 常达 10⁵ 量级），二是任意两个词的向量内积恒为 0，无法表达「猫」和「狗」比「猫」和「银行」更接近这一显然的事实。

**分布式假设**（distributional hypothesis）提供了出路：一个词的意义由它经常出现的上下文决定。据此，Mikolov 等提出的 word2vec 用两种轻量结构从大规模语料中学习词向量：

| 结构 | 预测方向 | 输入 → 输出 |
| --- | --- | --- |
| **CBOW** | 由上下文预测中心词 | 多个上下文词 → 当前词 |
| **Skip-gram** | 由中心词预测上下文 | 当前词 → 多个上下文词 |

两者都用一个**不含非线性激活的浅层网络**完成训练，因此可以在数十亿词的语料上高效运行。训练得到的向量具有可加性结构，经典例子是 `vector("国王") - vector("男人") + vector("女人") ≈ vector("女王")`，这说明向量空间中出现了可以被线性运算捕捉的语义关系。

该工作的另一贡献是把训练复杂度从与词表大小成正比降到与之近似无关，使得在 2013 年的算力条件下用 16 亿词训练出高质量词向量成为可行。这直接推动了后续几乎所有自然语言处理任务从「人工特征 + 统计模型」转向「预训练词向量 + 神经模型」的范式迁移。

## 与学习路线的关联

本知识点是**表示学习子方向的起点**，不依赖任何前置知识点（`prerequisites` 为空），可安排在路线最前段。

它的后继关系：

- `kn-0002`（子词与 BPE 分词）解决本知识点遗留的关键问题 —— 词表固定导致未登录词无法表示。word2vec 的词表在训练时确定，遇到未见过的词只能映射为 `<UNK>`，而子词方案把词拆成更小的单元，从根本上绕开了这一限制。
- `kn-0003`（循环神经网络与序列建模）以本知识点产出的词向量作为输入，进入序列建模领域。

## 参考来源

1. Mikolov, T., Chen, K., Corrado, G., & Dean, J. *Efficient Estimation of Word Representations in Vector Space*. arXiv:1301.3781, 2013. <https://arxiv.org/abs/1301.3781>
