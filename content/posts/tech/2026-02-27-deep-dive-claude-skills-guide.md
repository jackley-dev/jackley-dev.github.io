+++
title = "深度解读 Claude Skills：打造 Agent 的“食谱”与“大脑”"
date = 2026-02-27T10:00:00+08:00
draft = false
tags = ["Claude", "AI", "Agent", "MCP", "Skills", "LLM"]
categories = ["Tech"]
description = "Anthropic 发布了构建 Claude Skills 的完整指南。如果说 MCP 是连接工具的“厨房”，那么 Skills 就是烹饪佳肴的“食谱”。本文深入解析 Skills 的渐进式披露设计、核心架构以及五种能够大幅提升 Agent 稳定性的设计模式。"
+++

在 AI Agent 的开发生态中，我们一直在寻找一种能够稳定复现复杂工作流的方法。最近，Anthropic 发布了一份重磅文档——**《构建 Claude 技能（Skills）的完整指南》**，为我们提供了一个标准化的答案。

如果你正在使用 MCP (Model Context Protocol) 连接各种工具，或者试图让 Claude 遵循特定的 SOP（标准作业程序），这份指南绝对不容错过。本文将为你提炼其中的核心洞见，带你理解 Skills 是如何成为 Agent 的“食谱”的。

## 什么是 Skill？：厨房与食谱

Anthropic 给出了一个非常精妙的比喻来解释 Skill 与 MCP 的关系：

*   **MCP (Model Context Protocol)** 是**专业厨房**。它提供了各种食材（数据）、刀具（工具）和设备（API）。有了 MCP，Claude 可以访问 Linear、GitHub、Notion，但这只意味着它“能”做什么，不代表它知道“怎么做”最好。
*   **Skill (技能)** 是**食谱**。它是一套封装好的指令集，教 Claude 如何利用厨房里的工具，按步骤制作出一道完美的菜肴。

简单来说，**Skill = 显性知识 + 最佳实践**。它将你脑海中的“业务流程”固化为 Claude 可以理解和执行的文件。

## 核心设计哲学：渐进式披露 (Progressive Disclosure)

Skill 的设计中通过**渐进式披露**机制来平衡 Token 消耗和上下文质量。这是一个非常值得借鉴的 Prompt Engineering 模式：

1.  **Level 1: 索引层 (Frontmatter)**
    *   **加载时机**：始终加载到 System Prompt 中。
    *   **内容**：仅包含 Skill 的名称和一段简短的描述（Description）。
    *   **作用**：让 Claude 知道“我会什么”，以及“什么时候该用什么”。Claude 根据用户的 Prompt 决定是否唤醒某个 Skill。

2.  **Level 2: 指令层 (SKILL.md 正文)**
    *   **加载时机**：仅当 Claude 决定使用该 Skill 时加载。
    *   **内容**：详细的操作步骤、注意事项、错误处理逻辑。
    *   **作用**：提供执行任务所需的核心逻辑。

3.  **Level 3: 知识层 (References)**
    *   **加载时机**：按需加载。
    *   **内容**：引用的外部文档、API 规范、模板文件等。
    *   **作用**：提供深度的领域知识，而不必每次都塞满上下文窗口。

这种分层设计极其聪明，它解决了 Agent 开发中常见的 Context Window 挤占问题，让 Claude 能够同时挂载数十个 Skill 而不降低智商。

## 技术实现：解剖一个 Skill

一个标准的 Skill 其实就是一个文件夹，结构非常清晰：

```text
my-cool-skill/
├── SKILL.md              # [必须] 核心指令文件
├── scripts/              # [可选] Python/Bash 脚本
│   └── validate_data.py
├── references/           # [可选] 详细文档
│   └── api-guide.md
└── assets/               # [可选] 模板资源
    └── report-template.md
```

其中 `SKILL.md` 是灵魂所在。它的头部必须包含 YAML Frontmatter：

```yaml
---
name: linear-sprint-planning  # 必须 kebab-case
description: Manages Linear project workflows including sprint planning. Use when user mentions "sprint", "Linear tasks", or asks to "create tickets".
---

# Linear Sprint Planning
... (这里写 Markdown 格式的详细指令)
```

**关键点**：`description` 字段决定了 Skill 的触发准确率。好的描述必须包含 **"What it does" (它做什么)** 和 **"When to use it" (何时使用/触发词)**。

## 五种核心设计模式

指南中最具价值的部分，莫过于总结了五种 Skill 设计模式。这些模式几乎覆盖了当前 Agent 开发的绝大多数场景：

### 1. 顺序编排 (Sequential Workflow Orchestration)
最基础的模式，适用于严格线性的流程。
*   **场景**：新用户入职流程。
*   **逻辑**：`创建账号` -> `设置权限` -> `发送欢迎邮件`。
*   **价值**：确保步骤不遗漏，依赖关系被正确处理。

### 2. 多 MCP 协作 (Multi-MCP Coordination)
这是 Agent 的高光时刻，跨越多个隔离的服务。
*   **场景**：设计交付。
*   **逻辑**：从 Figma 导出资源 (Figma MCP) -> 上传到 Google Drive (Drive MCP) -> 在 Linear 创建任务 (Linear MCP) -> 在 Slack 通知团队 (Slack MCP)。
*   **价值**：打破数据孤岛，实现真正的自动化闭环。

### 3. 迭代优化 (Iterative Refinement)
利用 LLM 的自我反思能力提升质量。
*   **场景**：生成技术报告。
*   **逻辑**：`生成初稿` -> `运行脚本检查` (格式/数据) -> `根据反馈修正` -> `生成终稿`。
*   **价值**：通过 Loop 循环解决 LLM 一次性生成质量不稳定的问题。

### 4. 上下文感知 (Context-Aware Tool Selection)
根据环境动态决策。
*   **场景**：文件存储。
*   **逻辑**：
    *   如果文件 > 10MB -> 使用 S3 上传工具。
    *   如果是代码文件 -> 使用 GitHub 提交工具。
    *   如果是临时文件 -> 存放在本地。
*   **价值**：将业务规则内嵌到 Agent 中，而不是让用户每次都指定工具。

### 5. 领域专精 (Domain-Specific Intelligence)
在执行动作前加入“专家判断”。
*   **场景**：金融支付。
*   **逻辑**：在调用 `支付API` 之前，先运行一套 `合规检查规则`（检查制裁名单、风险等级）。只有合规检查通过，才执行物理动作。
*   **价值**：这是“Copilot”向“Agent”进化的关键——不仅仅是执行命令，更是**负责任地**执行命令。

## 结语：从 Prompt 到 Engineering

Anthropic 的这份指南标志着 Agent 开发正在从“玄学”的 Prompt 调优，走向工程化的 **Skill Engineering**。

通过标准化的目录结构、版本控制和测试流程，我们可以像管理代码一样管理 AI 的行为。对于开发者而言，这意味着我们终于有了一种可复用、可分发、可维护的方式来沉淀 AI 应用的最佳实践。

如果你正在构建 Agent，不妨现在就开始尝试把你的 Workflow 封装成一个 Skill。这不仅是给 Claude 的“食谱”，更是你作为架构师的核心资产。
