+++
title = "从 Trae Skills 迁移到 Claude Code Skills"
date = "2026-04-07T16:17:02+08:00"
draft = false
tags = ["Claude Code", "Trae", "AI IDE", "Skills"]
categories = ["Tech"]
author = "jackley"
+++

# Trae Skills vs Claude Code Skills

> 踩坑将 Skills 从 Trae 迁移到 VSCode + Claude Code，搞清楚了三种机制的本质差异。

---

## Trae Skills：自动发现 + 渐进加载

```
.trae/skills/
└── pdf/
    ├── SKILL.md          ← 触发入口（name + description 常驻上下文）
    ├── references/       ← 按需懒加载
    └── scripts/          ← 直接执行，不占 token
```

- **自动发现**：放进目录即生效，零配置
- **模型自主触发**：模型读取 description，自判断何时调用
- **三层渐进加载**：Metadata 常驻 → SKILL.md 触发时加载 → references/scripts 按需加载

---

## Claude Code 的现状（2026年4月）

官方文档原文：

> Custom commands have been merged into skills. A file at `.claude/commands/deploy.md` and a skill at `.claude/skills/deploy/SKILL.md` both create `/deploy` and work the same way.

Commands 和 Skills **已合并**，现在有两种写法，能力不同：

### 写法一：单文件（兼容旧 commands）

```
.claude/commands/pdf.md   或   .claude/skills/pdf.md
```

- 自动发现，无需安装
- 默认模型和用户均可触发
- **全量加载**，无渐进加载，无 scripts

### 写法二：文件夹（新 skills）

```
.claude/skills/
└── pdf/
    ├── SKILL.md          ← 触发入口
    ├── references/       ← 按需加载
    └── scripts/          ← 执行不占 token
```

- 自动发现，无需安装
- 默认模型和用户均可触发
- **渐进加载**，references/scripts 完整支持

通过 frontmatter 控制触发权限：

```yaml
---
name: deploy
description: Deploy to production
disable-model-invocation: true   # 仅用户手动触发（敏感操作用这个）
# user-invocable: false          # 仅模型触发
---
```

### Plugin Skills（分发用）

结构与 `.claude/skills/` 完全一致，但需要显式安装，内容缓存到 `~/.claude/plugins/cache/`，**修改源文件后需重装才生效**。

Plugin 的价值在于**分发**——打包给团队、发布到 Marketplace，而不是个人项目使用。

---

## 对比

| | Trae Skills | CC 单文件（commands） | CC `.claude/skills/` | CC Plugin Skills |
|--|-------------|----------|----------------------|-----------------|
| 发现方式 | 自动 | 自动 | 自动 | 需安装 |
| 触发方式 | 模型自主 | 模型/用户均可 | 模型/用户均可 | 模型/用户均可 |
| 渐进加载 | ✅ | ❌ | ✅ | ✅ |
| Scripts 不占 token | ✅ | ❌ | ✅ | ✅ |
| 修改实时生效 | ✅ | ✅ | ✅ | ❌ 需重装 |
| 适用场景 | 任务型能力 | 轻量指令 | 任务型能力 | 分发/团队共享 |

---

## 结论

**从 Trae 迁移到 Claude Code**：直接用软链接，一行命令搞定，`.trae/skills/` 作为唯一维护点，两边同步：

```bash
ln -s .trae/skills .claude/skills
```

改 skill 实时生效，无需任何额外操作，体验与 Trae 完全对等。

**Plugin** 是为分发设计的——打包给团队、发布到 Marketplace。个人项目用 Plugin 是过度设计，徒增安装和缓存刷新的摩擦。

**单文件 commands** 适合轻量的流程型操作（`/commit`、`/review`），不适合需要 references 的重度任务型 skill。

