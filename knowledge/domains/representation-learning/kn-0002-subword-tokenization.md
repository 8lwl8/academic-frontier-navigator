---
id: kn-0002
title: 子词切分与字节对编码
domain: 自然语言处理
sub_domain: 表示学习
knowledge_point: 子词切分
level: 经典
tags: [子词, BPE, 分词, 词表, 未登录词]
source:
  type: paper
  title: Enriching Word Vectors with Subword Information
  authors: [Piotr Bojanowski, Edouard Grave, Armand Joulin, Tomas Mikolov]
  url: https://arxiv.org/abs/1607.04606
  published_date: 2016-07-15
prerequisites: [kn-0001]
created_at: 2026-09-18
updated_at: 2026-09-18
---

# 子词切分与字节对编码

## 一句话概括

把词拆成比词更小的可复用单元（子词），在词表规模与表达能力之间取得平衡，同时让未登录词也能被表示。

## 核心内容

`kn-0001` 的词向量方案有一个结构性缺陷：**词表在训练前固定，未登录词无法表示**。这在形态丰富的语言（土耳其语、芬兰语）中尤为严重 —— 一个词根可以派生出成百上千种屈折形式，若每种都占一个词表位置，词表会爆炸；若全部归为 `<UNK>`，则丢失了全部语义信息。

**子词切分**的核心思路是：不按词切，而按**比词更小的可复用单元**切。高频词保持完整（`the`、`of`），低频词被拆成词根与词缀（`unhappiness` → `un` + `happi` + `ness`）。这样词表规模可控，而任何未见过的词都能由训练中见过的子词拼出，从根本上消除了 `<UNK>`。

**字节对编码（BPE）** 是最常用的实现，算法本身极为朴素：

1. 把所有词拆成字符序列，并在词尾追加结束符；
2. 统计所有相邻符号对的出现频次；
3. 把频次最高的一对合并为新符号；
4. 重复第 2–3 步，直到词表达到预设规模。

这个过程的本质是**一种贪心的数据压缩**：用最少的符号表示最多的文本。合并在高频共现的字符对上，自然会把常见词缀（`-ing`、`-tion`）和常见词整体结晶为单个符号。

Bojanowski 等的贡献在于把子词切分与词向量学习结合：词向量不再由整词查表得到，而是由其子词向量之和构成。这带来两个直接收益 —— 未登录词可表示，且形态相近的词（`work` / `works` / `working`）自动共享大部分表示。

**与后续架构的关系**：Transformer 时代几乎所有模型都沿用子词切分，只是不再训练词向量层。`kn-0006`（Transformer 架构）的输入嵌入层前必然先经过子词分词器，两者的接口是「文本 → 整数 id 序列」。

## 与学习路线的关联

前置知识点：`kn-0001`（分布式表示）—— 需先理解「为什么需要把词变成向量」，才能理解子词方案是在解决这一范式的哪一环。

后继知识点：`kn-0006`（Transformer 架构）。Transformer 的输入嵌入层直接消费子词分词器的输出，不理解子词会看不懂「词表大小」「序列长度」这些在论文中反复出现的关键参数。

> 本知识点属于「表示学习」子方向，与「序列建模」子方向在概念上有交叉（都涉及输入的离散化），但归类依据是**它的核心贡献在于表示粒度而非序列结构处理**。

## 参考来源

1. Bojanowski, P., Grave, E., Joulin, A., & Mikolov, T. *Enriching Word Vectors with Subword Information*. arXiv:1607.04606, 2016. <https://arxiv.org/abs/1607.04606>
2. Mikolov, T., Chen, K., Corrado, G., & Dean, J. *Efficient Estimation of Word Representations in Vector Space*. arXiv:1301.3781, 2013. <https://arxiv.org/abs/1301.3781>
