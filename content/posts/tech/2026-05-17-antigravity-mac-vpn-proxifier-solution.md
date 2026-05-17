+++
title = "当 Antigravity 遇上公司 VPN：Mac 用户的终极网络解决方案"
date = 2026-05-17T00:00:00+08:00
slug = "antigravity-mac-vpn-proxifier-solution"
categories = ["tech"]
tags = ["Antigravity", "VPN", "macOS", "Proxifier", "Proxy"]
description = "利用 Proxifier 进行精细化流量隔离，完美解决 Antigravity 编辑器与公司 VPN 之间的网络路由冲突问题。"
+++

macOS 环境下，使用 Antigravity 编辑器的 AI 功能时常面临与公司内网 VPN 代理冲突的问题。

## 痛点分析

### 痛点一：无视系统代理
Antigravity 需要通过代理访问外部 AI 服务。开启 Clash 等工具的“系统代理”模式后，Antigravity 本身并未遵循 macOS 的标准网络代理设置，导致流量未被正确接管，AI 功能连接失败。

### 痛点二：TUN 模式与公司 VPN 冲突
若开启 Clash 的 TUN（虚拟网卡）模式，Antigravity 流量会被成功接管。但 TUN 模式与公司内网 VPN 在路由表层面存在抢占冲突。结果只能二选一：要么连内网 VPN，要么用 Antigravity 的 AI 功能。

## 问题根源与目标

*   **根源**：
    1.  **应用限制**：Antigravity 未实现对 macOS 系统代理的兼容。
    2.  **路由冲突**：TUN 模式与 VPN 客户端在系统级网络接管上存在互斥。
*   **目标**：在**不开启 TUN 模式**的前提下，精准强制 Antigravity 走代理，同时保证 VPN 等其他网络连接正常。

## 解决方案：Proxifier 精准流量控制

[Proxifier](https://www.proxifier.com/) 可以在应用层面对特定程序进行强制代理转发，实现应用级别的流量隔离。

### 1. 关闭全局网络接管
关闭 Clash 的 TUN 模式，仅开启“系统代理”。让 Clash 作为一个本地 SOCKS5 代理服务器（例如在 `127.0.0.1:7890` 待命）运行，避免干扰整个系统的网络路由。

### 2. 配置 Proxifier 规则
打开 Proxifier，进行精细化配置。

**步骤一：添加 Proxy Server**
进入 `Profile -> Proxy Servers...`：
*   **Address**: `127.0.0.1`
*   **Port**: `7890`（根据你的 Clash 端口调整）
*   **Protocol**: `SOCKS5`

**步骤二：设置转发规则 (Rules)**
进入 `Profile -> Rules...`，**必须严格按照以下顺序**建立规则：

| 规则名称 | Applications | Target Hosts | Action | 目的 |
| :--- | :--- | :--- | :--- | :--- |
| **mihomo [auto-created]** | `mihomo` | `Any` | `Direct` | 排除代理工具核心，防止流量死循环（最关键一步）。 |
| **Localhost** | `Any` | `localhost; 127.0.0.1; ::1; %ComputerName%` | `Direct` | 排除本地流量，防止本地服务代理异常。 |
| **Antigravity Rule** | `Antigravity.app; Antigravity; com.google.antigravity` | `Any` | `Proxy SOCKS5 127.0.0.1:7890` | 精准捕获 Antigravity 并强制走 Clash 代理。 |
| **Default** | `Any` | `Any` | `Proxy SOCKS5 127.0.0.1:7890` | 默认全局代理（将流量交由 Clash 的分流规则处理）。 |

### 3. 工作流验证
完成上述配置并保存后，日常标准工作流变为：
1. 正常连接公司 VPN。
2. 启动 Clash（保持系统代理模式，确保 TUN 已关闭）。
3. 运行 Proxifier。
4. 打开 Antigravity。

实测结果：Antigravity AI 对话连接顺畅，同时公司内网资源访问无碍。

## 结论

利用 Proxifier 进行应用级流量接管，完美解决了 Antigravity 在 macOS 下与公司 VPN 的共存难题。该思路同样适用于其他“不遵循系统代理规则”且“与 VPN 存在路由冲突”的应用场景。
