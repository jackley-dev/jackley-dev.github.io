+++
title = "Gemini CLI 项目级配置机制解析"
date = "2026-05-20T00:00:00+08:00"
slug = "gemini-cli-project-level-configuration-guide"
categories = ["tech"]
tags = ["AI", "Gemini", "CLI", "Configuration"]
description = "解析除了 GEMINI.md 之外，Gemini CLI 还支持哪些项目级别的配置与上下文管理机制。"
+++

Gemini CLI 提供多种项目级配置机制，用于精细控制 AI 行为、工具权限和上下文管理。以下是基于官方文档整理的机制全景。

## 核心机制概览

| 机制 | 路径 | 状态 | 用途 |
| --- | --- | --- | --- |
| **项目约定** | `GEMINI.md` | ✅ 可用 | 编码规范、架构指南、业务术语库。支持按子目录拆分。 |
| **行为配置** | `.gemini/settings.json` | ✅ 可用 | 工具白名单、默认模型、上下文检索范围。 |
| **技能库** | `.gemini/skills/` | ✅ 可用 | 针对特定任务封装的可复用 Prompt 和工具链。 |
| **排除规则** | `.geminiignore` | ✅ 可用 | 屏蔽无需注入上下文的文件。 |
| **记忆管理** | `/memory` 命令 | ✅ 可用 | 会话级别的短期/长期事实记忆。 |
| **权限引擎** | `.gemini/policies/*.toml`| ❌ 禁用中 | 项目级（Workspace tier）Policy 当前不可用（Issue #18186）。 |

## 机制详解

### .gemini/settings.json (项目级行为配置)

覆盖全局（`~/.gemini/settings.json`）配置，控制当前项目核心行为。优先级最高。

```json
{
  "context": {
    "fileName": ["GEMINI.md", "AGENTS.md"],
    "discoveryMaxDirs": 200
  },
  "tools": {
    "allowed": ["run_shell_command(git status)", "run_shell_command(npm test)"]
  },
  "model": {
    "name": "gemini-2.5-pro"
  }
}
```

### .gemini/skills/ (项目级 Skills)

将复杂工作流抽象为可复用能力包。结构示例：

```text
my-project/
└── .gemini/
    └── skills/
        └── my-skill/
            ├── SKILL.md      # 技能核心指令
            ├── scripts/      # 辅助脚本
            └── assets/       # 静态资源
```

### 记忆与上下文控制

**命令管理 (`/memory`)**
支持自然语言交互（如“记住xxx”）或直接使用命令：
*   `/memory show`：查看当前加载的全部上下文片段。
*   `/memory reload`：修改配置文件后热刷新。

**排除文件 (`.geminiignore`)**
语法等同 `.gitignore`，有效防止日志、大型产物或敏感配置污染 AI 上下文窗口。

### Policy Engine (不可用说明)

Gemini CLI 独有权限控制引擎，通过 TOML 定义工具执行策略（`allow/deny/ask_user`）。
当前官方状态：**The Workspace tier (project-level policies) is currently non-functional.** 
现阶段仅支持用户级（`~/.gemini/policies/*.toml`）和系统管理员级配置。项目级（Tier 3）处于禁用状态，请勿在该目录配置。