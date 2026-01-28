+++
title = "Demis Hassabis 的反击：与其更好，不如不同"
date = "2026-01-19T20:48:36+08:00"
draft = false
tags = ["AI Strategy", "Gemini", "Google", "Management", "Demis Hassabis"]
categories = ["Tech"]
author = "jackley"
+++

在 ChatGPT 横空出世后的很长一段时间里，Google 看起来像是一个被时代抛弃的巨人。尽管它拥有 Transformer 的发明权，拥有全球最顶尖的 AI 人才库，但在产品化的战场上，它被 OpenAI 打得毫无还手之力。

然而，战局在 2023 年底开始扭转。随着 Gemini 1.0、1.5 Pro 以及后续 Flash 版本的密集发布，Google 不仅稳住了阵脚，更构建了一套能与 GPT-4 分庭抗礼甚至在某些维度实现反超的体系。

这一切的操盘手，正是 DeepMind 的创始人 Demis Hassabis。复盘这场绝地反击，我们会发现，Hassabis 并没有试图造一个“更好的 ChatGPT”，而是践行了一个深刻的竞争哲学：**“与其更好，不如不同” (Different is better than better)**。

## 核心困境：康威定律的诅咒

Google 起初的落后，并非技术不如人，而是组织架构出了问题。在很长一段时间里，Google 内部存在两个顶级 AI 团队：
1.  **Google Brain**：Transformer 的发源地，隶属于 Google 内部。
2.  **DeepMind**：AlphaGo 的缔造者，作为独立子公司运营。

这两个团队虽然都才华横溢，但彼此之间存在着微妙的竞争关系（赛马机制）。这种内耗导致算力分散，数据不通，无法集中力量办大事。这正是典型的**康威定律（Conway's Law）**困局——系统设计受限于组织沟通结构。

## 关键动作一：组织大一统 (The Consolidation)

Hassabis 的第一刀，没有砍向代码，而是砍向了组织。

2023 年 4 月，Google 宣布合并 Brain 和 DeepMind，成立全新的 **Google DeepMind**，由 Hassabis 挂帅。这一动作的价值被严重低估了。它结束了 Google 内部长达数年的路线之争，将全球最顶尖的 AI 人才和最宝贵的 TPU 算力资源统一到了一个指挥棒下。

这是战时 CEO 的决断：在生死存亡之际，效率优于多元。

## 关键动作二：技术路线的“非对称竞争”

如果 Google DeepMind 成立后，只是为了训练一个参数更大、跑分更高一点的 GPT-4，那它依然很难赢。因为在纯文本生成领域，GPT-4 已经占领了用户心智。

Hassabis 选择了**差异化（Differentiation）**。

### 1. 原生多模态 (Native Multimodal)
OpenAI 的 GPT-4V 早期采用了“拼凑”架构（语言模型 + 视觉编码器）。这种方式虽然能看图，但在理解复杂的时空关系时存在“翻译损耗”。

Gemini 从第一行代码开始，就是为多模态设计的。它不区分文本、图像、音频，所有模态在同一个高维空间对齐。这使得 Gemini 在理解视频、跨模态推理上具有先天的架构优势。这是 Hassabis 为未来物理世界 Agent（机器人）埋下的伏笔。

### 2. 超长上下文 (Infinite Context)
当 ChatGPT 还在为 32k、128k 的窗口限制纠结时，Gemini 1.5 Pro 直接甩出了 **1M+（甚至 2M/10M）** 的超长上下文窗口。

这不仅仅是数字的提升，更是维度的打击。它让用户不再需要“RAG（检索增强生成）”就能处理海量文档和代码库。Hassabis 敏锐地意识到，**“记忆”和“吞吐”**是 Google 作为一个搜索巨头的天然主场。

## 关键动作三：引入 AlphaGo 基因 (RL & Planning)

目前的 LLM 本质上是 System 1（快思考），基于概率预测下一个 Token。它缺乏逻辑，不会规划。

而 DeepMind 最擅长的，正是 System 2（慢思考）。Hassabis 正在将 AlphaGo/AlphaZero 中的**强化学习（RL）**、**树搜索（Tree Search）**和**规划（Planning）**能力引入大模型。

让模型学会“停下来想一想”，用测试时的计算量（Test-time Compute）换取更高的智能精度。这不仅是为了解决数学题，更是为了让 AI 具备解决复杂现实问题的能力。

## 关键动作四：战时工程化 (Velocity)

最后，Hassabis 解决的是 Google 的“富贵病”——发布焦虑。

过去，Google 因为害怕出错（Hallucination）和声誉风险，总是“起个大早赶个晚集”。Hassabis 上任后，与 CEO Sundar Pichai 保持每日高频沟通，将实验室模式切换为**“战时兵工厂”模式**。

我们看到了 Gemini 1.0 -> 1.5 -> Flash 的极速迭代，看到了模型迅速被“蒸馏”进 Android、Workspace 和 Search。虽然早期也出现了图像生成的翻车事故，但团队展现出了极强的纠错和迭代能力。**Ship & Iterate** 终于取代了 **Research & Publish**。

## 结语

Demis Hassabis 的这一仗，给所有后发者上了一课：

在红海竞争中，**不要试图在对手最擅长的维度上击败对手**。与其在纯文本上和 GPT-4 硬刚，不如开辟多模态和长上下文的新战场。

因为，Different is better than better.
