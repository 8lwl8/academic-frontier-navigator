---
id: kn-0013
title: 视觉 Transformer
domain: 自然语言处理
sub_domain: 跨模态与架构迁移
knowledge_point: 视觉 Transformer
level: 前沿
tags: [ViT, 跨模态, 架构迁移, 图像分块, 归纳偏置]
source:
  type: paper
  title: An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale
  authors: [Alexey Dosovitskiy, Lucas Beyer, Alexander Kolesnikov, Dirk Weissenborn]
  url: https://arxiv.org/abs/2010.11929
  published_date: 2020-10-22
prerequisites: [kn-0006]
created_at: 2026-09-18
updated_at: 2026-09-18
---

# 视觉 Transformer

## 一句话概括

把图像切成固定大小的图块并当作「词」处理，证明 `kn-0006` 的 Transformer 架构在几乎不做模态特化改造的前提下，即可在视觉任务上达到甚至超过专用卷积网络。

## 核心内容

在 ViT 之前，视觉领域的默认假设是**卷积的归纳偏置必不可少**：局部连接、权重共享、平移等变性被认为是高效学习图像特征的前提。

ViT 的质疑是：这些偏置究竟是**必要的**，还是仅仅在**数据不足时**有用？

**做法极为直接**：

1. 把图像切成为 16×16 像素的**图块**（patch）；
2. 每个图块拉平后经线性投影，得到一个向量 —— **这一步就是把图像「词元化」**，与 `kn-0002` 子词切分把文本词元化是同一思路；
3. 这些图块向量作为序列输入 `kn-0006` 的**编码器**（不含解码器，因为识别任务不需要生成）；
4. 额外加入可学习的位置嵌入与一个用于分类的全局标记。

**关键结论：归纳偏置的价值与数据规模呈反比。**

| 训练数据规模 | 卷积网络 | ViT |
| --- | --- | --- |
| 中小规模（如 ImageNet） | **更强** | 较弱 —— 缺乏必要的先验，学不到正确的局部模式 |
| 超大规模（数亿张以上） | 较弱 | **更强** —— 从数据中学到了比人工先验更合适的结构 |

这一结论的意义远超视觉领域：它说明**架构中的人工先验不是越多越好，而是要与数据规模匹配**。数据足够时，让模型自己学习结构优于强加结构。这正是 `kn-0011` 规模化路线在架构层面的呼应。

**对本项目学习路线的意义**：ViT 是「一个架构跨越模态边界」的最清晰案例。掌握 `kn-0006` 后，视觉、语音乃至其他模态的 Transformer 变体都可以理解为「如何把该模态的数据词元化」的问题。**这让 `kn-0006` 的学习回报被显著放大** —— 不是一个 NLP 专用架构，而是一个通用计算框架。

## 与学习路线的关联

前置知识点：`kn-0006`（Transformer 架构）—— ViT 直接复用其编码器。

同层对照：`kn-0010`（预训练语言模型范式）—— 两者都是「把 Transformer 用于特定模态」的实例，可对照理解「词元化」这一环节的通用性。

> **本知识点标注为 `前沿`**：跨模态架构仍在快速演进（对比学习式对齐、统一多模态编码器等），本知识点只描述架构迁移这一基础事实，不覆盖后续的对齐方法。
>
> **后续延伸方向**（尚未建为独立知识点）：对比学习式图文对齐、统一多模态表示。学习这些方向前，本知识点是必需的前置。

## 参考来源

1. Dosovitskiy, A., Beyer, L., Kolesnikov, A., & Weissenborn, D. *An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale*. arXiv:2010.11929, 2020. <https://arxiv.org/abs/2010.11929>
2. Vaswani, A., Shazeer, N., Parmar, N., & Uszkoreit, J. *Attention Is All You Need*. arXiv:1706.03762, 2017. <https://arxiv.org/abs/1706.03762>
