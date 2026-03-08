+++
title = "OpenClaw 更新：从“逻辑权限”到“物理沙箱”的纵深防御"
date = 2026-03-05T14:30:00+08:00
draft = false
tags = ["OpenClaw", "AI Agent", "Security", "Docker", "Sandboxing"]
categories = ["tech"]
description = "如果说 Tool Profiles 是 Agent 的“工牌”，那么 Sandboxing 就是它的“密闭实验室”。OpenClaw 引入的 Docker 沙箱机制，为 AI 执行提供了真正的物理隔离。"
+++

在上一篇关于 [Tool Profiles](file:///Users/lifeng/myblog/content/posts/tech/2026-03-05-openclaw-tool-profiles.md) 的讨论中，我们提到了“信任是分级的”。但作为一名务实的 Builder，我们深知：**逻辑上的约束永远只是第一道防线。**

当 Agent 拥有了 `coding` 权限，即使我们限制了它不能执行 `rm -rf`，它依然可能因为“幻觉”写出一些破坏性的代码。为了彻底解决“爆炸半径”问题，OpenClaw 推出了 [Sandboxing (沙箱机制)](https://docs.openclaw.ai/gateway/sandboxing)。

这是从“软件定义权限”向“基础设施定义安全”的跨越。

## 核心理念：物理隔离 (Physical Isolation)

OpenClaw 的沙箱本质上是利用 **Docker 容器** 来运行 Agent 的工具。

这意味着，虽然 OpenClaw 内置了沙箱的管理逻辑（Gateway 负责调度），但**你必须在宿主机上预先安装 Docker Engine**。它并不是一个完全独立的、零依赖的虚拟机，而是基于容器技术的轻量级隔离。

这意味着 `exec` (执行命令)、`read/write` (读写文件)、`edit` (编辑文件) 等高危操作不再直接作用于你的宿主机（Host），而是在一个受限的容器环境中运行。

这与我在[行为模式](file:///Users/lifeng/ai-memory/patterns.md)中提到的 **“沙箱思维” (Sandbox Thinking)** 高度契合：
> 在沙箱内，允许系统崩溃（Let it Crash）以积累数据；在沙箱外，严格设立熔断机制（Safety Layer）。

## 关键配置深度拆解

OpenClaw 的沙箱设计非常灵活，主要通过以下几个维度进行精细化控制：

### 1. 运行模式 (Modes)
通过 `agents.defaults.sandbox.mode` 控制：
- **`off`**: 裸奔模式，工具直接在宿主机运行（慎用）。
- **`non-main` (默认)**: 仅对非主会话（如群聊、自动化任务）启用。这是一个非常平衡的策略，保护了核心生产环境，同时不影响日常调试。
- **`all`**: 全量开启。

### 2. 隔离粒度 (Scope)
决定了容器的复用策略：
- **`session` (默认)**: 每个会话一个独立容器。最安全，但启动开销略大。
- **`agent`**: 每个 Agent 一个容器。
- **`shared`**: 所有沙箱共用一个容器。适合资源受限的环境。

### 3. 工作区访问 (Workspace Access)
这是最体现“控制力”的地方：
- **`none` (默认)**: 完全隔离。Agent 只能看到 `~/.openclaw/sandboxes` 下的临时空间。
- **`ro` (Read-Only)**: 以只读方式挂载项目目录。Agent 可以读代码分析，但无法修改。
- **`rw` (Read-Write)**: 读写挂载。这是生产力最高的模式，配合 `coding` Profile 使用，让 Agent 真正具备“重构能力”。

## 进阶玩法：自定义 Binds

如果你需要 Agent 访问宿主机的特定资源（例如 Python 虚拟环境、Maven 仓库缓存、或者特定的数据集），你可以使用 `binds` 功能：

```json
{
  "agents": {
    "defaults": {
      "sandbox": {
        "docker": {
          "binds": ["/home/user/cache:/cache:rw"]
        }
      }
    }
  }
}
```

**注意：** Binds 会绕过沙箱的文件系统保护，务必遵循“最小必要原则”，优先使用 `:ro` (只读)。

## 完美的中间方案：信任提权 + 自动执行

在实际使用中，我们往往面临一个两难：想要自动化（不审批），但又担心 `host: "gateway"` 这种全开模式太危险。

很多用户为了追求极致的自动化（不被审批弹窗打断），会倾向于配置成这样：

```json
// 🚫 危险配置：千万别这么做
"exec": {
  "host": "gateway",  // 所有命令默认在宿主机运行
  "ask": "off"        // 从不询问，直接执行
}
```

**这是极度危险的。** 一旦 Agent 出现幻觉（比如误删文件、执行了恶意脚本），你的宿主机将没有任何防线。

但我们又不想每次都点“批准”。这里推荐一个 **“默认沙箱 + 信任提权 + 自动执行”** 的黄金配置。

### 推荐配置

这个配置的逻辑是：

1.  **默认安全**：所有普通命令（如 `ls`, `git`, `npm`）依然在 **Sandbox (沙箱)** 中运行，不影响宿主机。
2.  **按需提权**：只有当你（信任用户）明确要求，或者智能体识别出需要宿主机权限（如 `openclaw` 命令）并请求提权时，才会切到宿主机。
3.  **消除卡顿**：`security: "full"` 和 `ask: "off"` 组合，意味着 **只要是你的提权请求，就直接通过，不再弹窗询问**。

请修改 `~/.openclaw/openclaw.json`：

```json
{
  "tools": {
    "profile": "full",
    "exec": {
      "host": "sandbox",   // 👈 关键点1：默认依然是沙箱，防止误伤
      "security": "full",  // 👈 关键点2：信任模式，不做白名单检查
      "ask": "off"         // 👈 关键点3：关闭审批弹窗，彻底自动化
    },
    "elevated": {
      "enabled": true,
      "allowFrom": {
        // 只有这里列出的用户才能触发上述的“自动提权”，其他人不行
        "feishu": ["ou_YOUR_FEISHU_ID"]
      }
    }
  }
}
```

### 为什么这个方案更好？

| 场景 | 你的旧方案 (`host: gateway`) | 我的推荐方案 |
| :--- | :--- | :--- |
| **智能体运行 `rm -rf /`** | 💥 **直接执行，系统崩溃** | 🛡️ **在沙箱内执行，宿主机安全** |
| **智能体运行 `openclaw ...`** | ✅ 直接执行 | ✅ **自动提权并执行 (无感)** |
| **安全性** | 🔴 极低 (裸奔) | 🟡 中等 (仅信任你的提权操作) |
| **体验** | 🚀 顺滑 | 🚀 顺滑 |

配置完成后，记得重启 OpenClaw 生效。

## 部署建议：如何“优雅”地开启？

**前提条件**：确保你的服务器已安装 Docker 且 OpenClaw 进程有权限访问 Docker Socket。

1.  **开箱即用 (Out of the Box)**:
    大多数官方安装方式（如 `docker-setup.sh` 或标准安装脚本）会自动检测 Docker 环境并尝试构建或拉取基础镜像 (`openclaw-sandbox:bookworm-slim`)。
    *   **验证方式**: 运行 `docker images | grep openclaw-sandbox` 查看是否存在基础镜像。
    *   **自动重建**: 如果你更新了配置，可以使用 `openclaw sandbox recreate --all` 命令，它会自动基于最新配置重建容器。

2.  **自定义构建 (推荐)**:
    虽然“开箱即用”很方便，但我**强烈建议**你选择此方案。
    默认的沙箱镜像 (`slim`) 几乎是空的。作为一名 Builder，你肯定希望 Agent 能运行 Python 脚本、安装 npm 包或使用 git。一个没有工具的沙箱只是“监狱”，而装满工具的沙箱才是“工作室”。
    ```bash
    # 一键构建包含 Python/Node/Git 的全能镜像
    ./scripts/sandbox-common-setup.sh
    ```
    构建完成后，记得在配置中将 `image` 指向 `openclaw-sandbox-common:bookworm-slim`。

3.  **默认安全**: 建议将 `workspaceAccess` 设为 `ro`。只有在需要 Agent 自动写代码的任务中，才在 `agents.list` 里针对特定 Agent 开启 `rw`。
3.  **监控与日志**: 沙箱并不代表可以放任不管。定期检查 Docker 容器的资源占用，防止 Agent 陷入死循环。

## 结语：Software 2.0 的安全哲学

在 Software 1.0 时代，我们通过静态的代码审计来保证安全。而在 Software 2.0 (AI 驱动) 时代，代码的行为是动态且不可预测的。

**安全不再是去消除不确定性，而是去包容不确定性。**

OpenClaw 的 Tool Profiles (逻辑) + Sandboxing (物理) 构成了一套完整的纵深防御体系。它让我们敢于赋予 Agent 强大的能力，因为我们知道，无论它在里面如何折腾，实验室外的世界依然稳固。

控制，是为了更自由地释放。
