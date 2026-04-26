+++
title = "DeepTutor 拔草指南"
date = 2026-04-25T00:00:00+08:00
slug = "deeptutor-as-skills"
categories = ["tech"]
tags = ["AI", "DeepTutor", "Trae", "Claude Code", "Prompt Engineering", "Skills"]
description = "别再折腾DeepTutor了，我尝试把它最有价值的Guided Learning模块Skills化了"
+++

体验 DeepTutor 后，整体感觉**基本没必要安装**。核心功能完全可被 Gemini、ChatGPT 等 Chatbot 平替，且本地部署坑多。

与其折腾环境，不如抽离最有价值的功能，直接封装成 Skills。

## 一、避坑指南：为什么不建议折腾 DeepTutor？

### 1. 核心功能差异性小，可被 Chatbot 平替
DeepTutor 包装了许多看似高级的 Agent 模式，但实际体验发现，绝大部分场景仅需主流大模型的基础对话能力即可满足，缺乏不可替代的亮点。

![通用对话效果](/images/deeptutor-chat.jpg)

### 2. 部署繁琐，兼容性差且有 Bug
接入国内大模型（如 Minimax）存在接口兼容性问题，需深改源码。即便直接调用 OpenAI API，部分模块仍有 Bug 无法正常使用（如无法保存报错）。为一个平替工具修修补补，投入产出比极低，不值得折腾。

## 二、唯一亮点：Guided Learning 模块

项目中唯一值得一用的是 **Guided Learning** 模块。
该模块能根据目标主题，自动梳理关键知识点并生成多页交互式 HTML 学习文档，通过流程中的提问帮助查漏补缺。

![Guided Learning 效果演示](/images/deeptutor-guided-learning.jpg)

## 三、降维打击：将核心功能封装为 Skills

既然仅 Guided Learning 实用，不如直接将其封装为 Skills，在 Claude Code 或 Trae 中无缝调用。

**这样做的好处：**
- **零部署**：无需搭建 DeepTutor 前后端环境。
- **省钱**：直接复用 AI 工具订阅额度，免去额外 API 费用。
- **高效生成**：利用双 Agent 协作 Prompt 技巧，一键生成本地交互文档。

### 实际效果演示

在 Trae 中调用对应 Skills，AI 即可自动按步骤生成可交互的 HTML 教程合集。
生成出的文档包含导航页与独立知识点子页面，结构清晰并自带测验：

![Skill 生成的 HTML 页面 - 1](/images/deeptutor-skills-guided-learning1.jpg)
![Skill 生成的 HTML 页面 - 2](/images/deeptutor-skills-guided-learning2.jpg)

## 四、写在最后

总体而言，DeepTutor 不值得费力气折腾，真正有价值的只有它的 Guided Learning 模块。如果大家对我封装的这套 Skills 感兴趣，可以在评论区留言，后续我再把链接分享出来。
