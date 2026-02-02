+++
title = "用 AI IDE 打造博客写作工作流：Trae 与 Claude Code 双平台实践"
date = "2026-01-12T11:55:26+08:00"
draft = false
tags = ["AI IDE", "Trae", "Claude Code", "Hugo", "工作流"]
categories = ["tech"]
author = "jackley"
+++

## 背景

写博客最难的部分往往不是写作本身，而是从想法到成文的过程。很多时候，和朋友聊天时灵感迸发，但事后整理却觉得索然无味。

我想要一个这样的工作流：

```
对话激发想法 → 输入 "ga" → AI 整理成文章 → 输入 "commit" → 自动发布
```

这篇文章记录了我如何在 Trae 和 Claude Code 两个 AI IDE 中实现这套流程。

## 核心思路

无论是 Trae 还是 Claude Code，都支持「项目规则」机制——在特定目录下放置配置文件，AI 会自动读取并遵循这些规则。

| 平台 | 规则文件位置 |
|------|-------------|
| Trae | `.trae/rules/project_rules.md` |
| Claude Code | `.claude/CLAUDE.md` |

我的策略是：写一份规则，两个平台共用（稍作调整）。

## 规则设计

### SOP 结构

采用标准操作流程（SOP）的结构来组织规则：

```markdown
# Blog Automation SOP

Goal: Facilitate a seamless "Idea -> Content -> Publish" workflow.

## Role & Tone
- Role: Senior Technical Editor & Pair Programmer
- Language: Chinese (Simplified)

## Workflow Triggers (STRICT)
...
```

关键点：
- **Goal** 明确目标
- **Role & Tone** 定义 AI 的角色和语气
- **STRICT** 强调触发词的严格执行

### 三个工作阶段

#### 1. Brainstorming（默认模式）

```markdown
### 1. Brainstorming (Default)
- **Trigger**: General conversation.
- **Action**: Discuss, question, and refine ideas. Do NOT generate the post yet.
```

这是最重要的设计——默认情况下，AI 只负责对话和启发，**不会急于生成文章**。这避免了 AI 过度主动的问题。

#### 2. Content Generation（触发词：ga）

`ga` 是 "generate article" 的缩写，避免与其他常用指令冲突。

```markdown
### 2. Content Generation (Trigger: "ga")
- **Trigger**: User inputs "ga" (generate article).
- **Action**:
  - Summarize discussion into a structured blog post.
  - **File**: `content/posts/YYYY-MM-DD-{english-slug}.md`
  - **Front Matter** (TOML):
    +++
    title = "{中文标题}"
    date = "YYYY-MM-DDTHH:MM:SS+08:00"
    draft = false
    tags = ["{tag1}", "{tag2}"]
    categories = ["{Category}"]
    author = "jackley"
    +++
```

设计细节：
- 文件名用英文 slug（URL 兼容性好）
- Front Matter 用 TOML 格式（与 Hugo 原生一致）
- 自动填充当前日期

#### 3. Deployment（触发词：commit）

```markdown
### 3. Deployment (Trigger: "commit")
- **Trigger**: User inputs "commit".
- **Action**:
  - Run: `git add . && git commit -m "Add post: {English Slug}" && git push origin main`
  - Output: "Deployed to https://jackley-dev.github.io/"
```

一个词完成：git add → commit → push → 告知部署状态。

## 平台差异对比

| 机制 | Trae | Claude Code |
|------|------|-------------|
| 项目规则 | `.trae/rules/project_rules.md` | `.claude/CLAUDE.md` |
| 全局规则 | `user_rules.md` | `~/.claude/CLAUDE.md` |
| 自定义命令 | `@智能体` | `/skill` |
| 触发方式 | 直接输入触发词 | 直接输入触发词 |

两者的项目规则机制非常相似，规则内容可以直接复用。

## 实际效果

```
我: 最近在研究 Rust 的所有权机制，感觉和其他语言很不一样...

AI: [对话交流，讨论所有权、借用、生命周期等概念]

我: ga

AI: 📝 文章摘要：
    - 标题：Rust 学习心得：从入门到理解所有权
    - 分类：技术
    - 要点：
      1. 所有权机制的核心概念
      2. 借用与生命周期
      3. 错误处理的优雅方式
    请确认或修改。

我: 确认

AI: ✅ 已生成 content/posts/2026-01-12-rust-ownership.md

我: commit

AI: 📤 正在提交...
    ✅ 已推送到 GitHub，Actions 正在部署...
```

## 小结

这套工作流的核心价值：

1. **降低写作阻力** - 从对话自然过渡到文章
2. **触发词控制节奏** - AI 不会过度主动
3. **一键发布** - 消除繁琐的 git 操作
4. **双平台通用** - Trae 和 Claude Code 无缝切换

规则文件本身也是一种「知识外化」——把工作流程固化下来，让 AI 成为可预期的协作伙伴。
