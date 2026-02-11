+++
title = "告别长图：构建基于 Markdown 和 Playwright 的自动化技术写作流"
date = 2026-02-11T12:00:00+08:00
draft = false
tags = ["Automation", "Python", "Playwright", "Technical Writing", "Xiaohongshu"]
categories = ["Tech", "Workflow"]
description = "如何用工程师的方式做小红书？本文介绍了一套 'gen-rich' 方案，实现了从 Markdown 源码到 Notion 风格分页卡片的自动化渲染。"
+++

在技术传播的领域，我们常常面临一个两难的选择：是追求 **内容的深度与结构化**（如 Blog、Docs），还是追求 **流量与易读性**（如小红书、Twitter）？

长期以来，为了在小红书分享技术内容，我不得不维护两套工作流：
1.  在 IDE 中写 Markdown，发布到个人博客。
2.  打开设计工具（Figma/Canva）或长图生成器，复制粘贴文字，手动调整排版，导出图片。

这种**“数据孤岛”**不仅效率低下，而且让我失去了对版本的控制。一旦代码示例需要修改，我就得重新走一遍作图流程。

于是，我决定用工程师的方式解决这个问题。我构建了一套名为 **`gen-rich`** 的自动化流水线，实现了 **"Write Once, Publish Everywhere"**。

## 核心理念：Single Source of Truth

整个方案的核心在于：**Markdown 是唯一真理**。

所有的内容都应当源自 Git 仓库中的 Markdown 文件。无论是在 Web 端展示，还是生成社交媒体图片，都只是对同一份数据的不同**渲染（Rendering）**方式。

## 架构概览

这一方案主要由三个环节组成：

1.  **解析层 (Parser)**：读取 Markdown，转换为语义化的 HTML。
2.  **渲染层 (Renderer)**：应用 CSS 样式，并进行智能分页。
3.  **生成层 (Generator)**：使用 Headless Browser 截图保存。

### 1. 像写代码一样写文章

我希望生成的图片具有类似 **Notion** 或 **Obsidian** 的“技术笔记”质感：
*   清晰的层级结构（H1, H2, Callouts）。
*   完美的**代码高亮**（这是技术内容的灵魂）。
*   模块化的视觉组件。

为此，我设计了一套基于 CSS Variables 的样式系统。通过定义 `--page-width`, `--bg-color`, `--card-radius` 等变量，我可以轻松切换不同的“皮肤”。

```css
:root {
    --page-width: 1080px;
    --page-height: 1440px;
    --primary-color: #333;
    --code-bg: #f5f6f7;
    /* ... */
}
```

### 2. 智能分页算法

小红书的展示形式是 **4:5 的卡片组**，而不是一张无限长的图片。因此，我们不能简单地截图整个网页，必须进行**分页（Pagination）**。

我编写了一段 JavaScript 逻辑，运行在渲染模板中。它会遍历 HTML 节点，模拟计算高度，并在内容溢出时自动“切断”，创建新的页面容器。

```javascript
// 伪代码逻辑
elements.forEach(el => {
  if (currentHeight + el.height > PAGE_HEIGHT) {
     createNewPage();
     currentHeight = 0;
  }
  appendToCurrentPage(el);
});
```

这确保了标题不会被切成两半，代码块也能完整展示（或优雅截断）。

### 3. Playwright 自动化截图

为了保证渲染的绝对准确性（包括字体渲染、阴影、圆角），我选择了 **Playwright**。它是一个强大的端到端测试工具，可以驱动 Chromium 内核。

Python 脚本会启动一个无头浏览器，加载我们在本地生成的临时 HTML 文件，然后针对每一个 `.page` 容器进行高分辨率截图。

```python
# 自动化截图核心逻辑
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(f'file://{html_path}')
    
    # 查找所有页面元素并截图
    cards = page.locator('.page')
    for i in range(cards.count()):
        cards.nth(i).screenshot(path=f'output_{i+1}.png')
```

## 最终效果

现在，当我在博客写完一篇技术文章后，只需要运行一行命令：

```bash
trae-cli gen-rich my-post.md
```

系统就会自动：
1.  提取文章核心内容。
2.  生成分页的 HTML 预览。
3.  调用 Playwright 截取 4-5 张高清 PNG 图片。
4.  保存到草稿目录，准备发布。

## 总结

**`gen-rich`** 方案不仅解放了我的生产力，更重要的是它保证了**排版的一致性**。无论我写的是复杂的 Kubernetes 配置，还是简单的 Python 脚本，生成的卡片永远保持着统一、专业的高级感。

这正是“自动化”的魅力所在：把重复的劳动交给机器，把创造的乐趣留给自己。
