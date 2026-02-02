+++
title = "OpenClaw 爆火：“主权 AI”的大胆探索"
date = 2026-02-01T11:30:00+08:00
draft = false
categories = ["tech"]
tags = ["AI", "Agent", "OpenClaw", "Sovereign AI", "Safety"]
slug = "openclaw-viral-truth-sovereign-ai"
+++

简单来说：**Clawdbot $\rightarrow$ Moltbot $\rightarrow$ OpenClaw** 是同一个项目在短短两周内的被迫演变。

这不仅仅是一个改名事件，它折射出了当前 AI Agent 领域的**野蛮生长**和**脆弱性**。

## 1. 发生了什么？（The Drama）

OpenClaw 的前世今生简直是一部硅谷情景喜剧：

*   **Clawdbot (起源)**：德国开发者 Peter Steinberger (PSPDFKit 创始人) 写了一个在本地运行、通过 WhatsApp/Telegram 控制电脑的 AI Agent。因为它太好用了（GitHub Stars 飙升），名字又太像 Anthropic 的 **Claude**，收到了商标律师函。
*   **Moltbot (混乱)**：作者被迫改名 Moltbot（意为“蜕皮的龙虾”）。但在改名间隙，发生了极其魔幻的事情：推特账号被抢注、骗子发币 ($CLAWD) 割韭菜、作者手忙脚乱把自己的 GitHub 个人账号都改错了。
*   **OpenClaw (定局)**：最终在 1 月底定名为 **OpenClaw**。这名字更“正规”，也宣告它从一个个人玩具变成了一个严肃的开源基础设施。

## 2. 它到底是什么？

去掉炒作的泡沫，OpenClaw 的本质是：**Local-First Action Agent**。

*   **反 Chatbot**：它不是陪聊的。它的核心逻辑是 **Tool Use**。
*   **反 SaaS**：它运行在你家里的 Mac Mini 上，而不是云端。（这一点上，**Claude Cowork** 也是同类，它们都选择让计算发生在数据所在的地方，而不是把数据搬到计算所在的地方。）
*   **反 Web UI**：它寄生在你常用的 IM (Telegram/WhatsApp) 里。

它就像是钢铁侠的 **Jarvis 的低配现实版**：你发消息给它“帮我把这周的周报写了发给老板”，它会自己去读你的 Calendar，查你的 Git Log，写好邮件，然后发出去。

## 3. 技术解密：构建“全能管家”的四块拼图

OpenClaw 的成功不在于单一技术的突破，而在于它通过精妙的工程设计，解决了 AI Agent 落地最难的“最后一公里”问题。

如果说 LLM 提供了“大脑”，那么 OpenClaw 则通过以下四大支柱，为这个大脑装上了“手脚”和“记忆”，让它真正能够介入你的生活与工作：

### A. AgentSkills：开源界的 "Claude Skills"
你提到的 **Claude Skills**（Anthropic 官方的工具集）确实是灵感来源。但 OpenClaw 更进一步，它构建了一个**社区驱动的技能市场**（AgentSkills）。
*   **不仅仅是官方工具**：任何人都可以写一个 Skill（比如“查询当地油价”、“监控特定股票”），然后通过 Pull Request 提交。
*   **自我进化**：最疯狂的是，如果它发现缺少某个 Skill，它甚至可以**自己编写代码**来创建一个新 Skill。
*   **即插即用**：这些 Skills 被打包成模块，支持 Spotify、Hue 智能灯泡、Obsidian 笔记等，用户像安装 Chrome 插件一样安装它们。

### B. Gateway 架构：把 AI 塞进聊天框里
这是 OpenClaw 最聪明的工程设计。它没有试图去写一个复杂的 Electron 桌面应用，而是做了一个 **Gateway（网关）**。
*   它作为一个中间人，连接了 **LLM**（大脑）和 **IM 软件**（手脚）。支持 WhatsApp, Telegram, Discord, Slack, Signal 甚至 iMessage。
*   这意味着你不需要学习新的 UI，你的交互界面就是你用了十年的聊天窗口。这种 **"Invisible UI"** 才是它爆火的 UX 密码。

### C. CDP (Chrome DevTools Protocol)：无头浏览器之眼
很多 Web 任务是没有 API 的（比如去某个老旧的政府网站查数据）。OpenClaw 内置了对 **CDP** 的支持。
*   它可以启动一个看不见的 Chrome 浏览器，模拟点击、截图、抓取数据。
*   这让它的能力边界从“API 世界”扩展到了“整个万维网”。

### D. Persistent Memory：它记得你
大多数 Agent 是“阅后即焚”的，每次对话都是新的开始。但 OpenClaw 引入了**持久化记忆**。
*   它会记住你的偏好（“我喜欢周五下午开会”、“我不吃香菜”）。
*   它是**Private by default**的。所有记忆都存储在本地，不上传云端。
*   更重要的是，它**不绑定模型**。你可以用 Claude，也可以用 OpenAI，甚至是用本地跑的 Llama。模型可以换，但记忆永远属于你。

## 4. OpenClaw vs Claude Cowork：谁是更好的管家？

既然 Claude Cowork 也是本地运行，它俩有啥区别？
简单来说：**OpenClaw 是给“不在电脑前”的你用的，Cowork 是给“坐在电脑前”的你用的。**

*   **控制端不同**：
    *   **OpenClaw**：通过 **WhatsApp/Telegram** 控制。你可以在吃饭、走路、躺在床上时指挥家里的电脑。
    *   **Claude Cowork**：通过 **Desktop App** 控制。你必须坐在电脑前，把它当成一个并肩作战的同事（Co-worker）。
*   **交互逻辑不同**：
    *   **OpenClaw**：是 **Remote Command（远程遥控）**。发一条指令，等待结果。
    *   **Claude Cowork**：是 **Side-by-Side Collaboration（即时协作）**。你拖拽文件给它，看着它实时处理，随时打断和调整。

## 5. 深度视角与真实评价

我必须泼一盆冷水。虽然它很酷，但站在系统工程的角度，它目前是一个**安全噩梦**。

这不仅仅是我个人的担忧，业界大佬们在称赞其创新性的同时，也表达了深深的忧虑。

> **Andrej Karpathy (OpenAI 联合创始人):**
>
> "每一个 Agent 现在都相当独立，拥有独特的上下文、数据和工具。当它们联网形成规模时，这种网络简直是前所未有的（unprecedented）。"
> *(注：Karpathy 同时也指出 OpenClaw 就像是早期的 MS-DOS，强大但没有任何保护措施。)*

> **David Sacks (著名投资人 & 前 PayPal COO):**
>
> 对 OpenClaw 的迅速崛起表示了高度赞扬，称其为“个人 AI 助理的未来”。

> **Simon Willison (LLM 安全研究员) & Palo Alto Networks:**
>
> 发出了严厉警告，指出 OpenClaw 代表了 AI 安全危机的**“致命三连击” (Lethal Trifecta)**：
> 1.  **访问私有数据** (Access to private data)
> 2.  **接触不可信内容** (Exposure to untrusted content)
> 3.  **对外通讯能力** (Ability to communicate externally)
>
> *想象一下：一封恶意邮件里的 Prompt Injection 攻击，就能指挥你的 OpenClaw 把你的 SSH 密钥发给黑客。*

## 6. 总结与建议

OpenClaw 是一场激动人心的实验，但请保持清醒：

1.  **玩玩可以**：在虚拟机或闲置的旧 Mac 上跑。
2.  **别给真权限**：不要绑定你的主 Google 账号或公司 Slack。
3.  **关注趋势**：OpenClaw 证明了 **MCP (Model Context Protocol)** 是未来的标准，这是值得学习的技术点。

它也许不完美，但它推开了未来的一扇门。
