+++
title = "一键发布博客到小红书:从Markdown到图文笔记的自动化"
date = "2026-01-12T22:56:32+08:00"
draft = false
tags = ["自动化", "小红书", "MCP", "Python"]
categories = ["AIGC"]
author = "jackley"
+++

## 背景

有了博客文章后,想同步发布到小红书获取更多流量。但手动操作太繁琐:
- 复制粘贴内容,需要重新排版
- 小红书限制(标题≤20字,正文≤1000字)
- 需要配图才有好的展示效果
- 每次发布都要重复这些步骤

能不能输入一个 `pub` 命令,自动完成这一切?

## 解决方案

通过 **xiaohongshu-mcp + Python 卡片生成器**,实现一键发布:

```
输入 pub → 生成卡片图 → 调用API → 发布成功
```

## 实现步骤

### 1. 安装 xiaohongshu-mcp

xiaohongshu-mcp 是一个通过浏览器自动化操作小红书的 MCP 服务。

```bash
# 克隆项目
git clone https://github.com/xpzouying/xiaohongshu-mcp.git
cd xiaohongshu-mcp

# 编译(Go项目)
go build

# 启动服务
./xiaohongshu-mcp --port :18060
```

**首次登录**:
- 启动后会打开浏览器
- 扫码登录小红书
- 登录状态会保存,下次无需重复

**验证服务**:
```bash
curl -s http://localhost:18060/api/v1/login/status | python3 -m json.tool
# 返回: {"success":true,"data":{"is_logged_in":true}}
```

### 2. 创建卡片生成器

小红书图文笔记需要配图,用 Python PIL 实现简约白色风格的卡片:

**核心特性**:
- 白色背景 + 渐变色标题
- 左侧序号 + 右侧标签布局
- 尺寸 1080x1350(小红书标准比例)
- 自动换行和排版

**实现代码** (`scripts/card_generator.py`):

```python
from PIL import Image, ImageDraw, ImageFont

def generate_card(title, subtitle, points, author, tags, output_path):
    # 创建白色背景
    img = Image.new('RGB', (1080, 1350), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    # 绘制渐变色标题
    for i, line in enumerate(title_lines):
        ratio = i / max(len(title_lines) - 1, 1)
        color = create_gradient_text_color(ratio)  # 蓝→紫渐变
        draw.text((80, y), line, font=title_font, fill=color)

    # 绘制要点列表
    for idx, (number, title, desc, time) in enumerate(points):
        # 渐变色序号
        draw.text((80, y), str(number), font=number_font, fill=gradient_color)
        # 标题和描述
        draw.text((130, y), title, font=title_font, fill=TEXT_COLOR)
        draw.text((time_x, y), f"⏱ {time}", font=time_font, fill=GRAY)

    img.save(output_path, 'PNG', quality=95)
```

**使用示例**:
```python
generate_card(
    title="用AI IDE打造博客写作工作流",
    subtitle="Trae与Claude Code双平台实践",
    points=[
        (1, "对话式写作", "通过与AI对话激发想法", "默认模式"),
        (2, "触发词控制", "输入ga生成文章", "生成文章"),
        (3, "一键发布", "自动git操作", "自动部署"),
        (4, "双平台通用", "规则几乎相同", "可复用")
    ],
    author="jackley",
    tags=["AIGC", "效率工具"],
    output_path="card.png"
)
```

### 3. 调用发布API

xiaohongshu-mcp 提供了简洁的 REST API:

**接口**: `POST http://localhost:18060/api/v1/publish`

**参数**:
```json
{
  "title": "标题(≤20字)",
  "content": "正文(≤1000字)",
  "images": ["/绝对路径/图片.png"]
}
```

**完整发布脚本**:

```bash
# 1. 生成卡片图片
python scripts/card_generator.py

# 2. 准备发布内容
cat > /tmp/xhs_publish.json <<EOF
{
  "title": "用AI IDE打造博客写作工作流",
  "content": "写博客最难的不是写作,而是从想法到成文的过程...",
  "images": ["/Users/lifeng/myblog/static/images/card.png"]
}
EOF

# 3. 调用API发布
curl -X POST http://localhost:18060/api/v1/publish \
  -H "Content-Type: application/json" \
  -d @/tmp/xhs_publish.json

# 返回:
# {"success":true,"data":{"status":"发布完成"},"message":"发布成功"}
```

**小红书限制**:
- ✅ 标题不超过20个字
- ✅ 正文不超过1000个字
- ✅ 图文流量 > 视频 > 纯文字

### 4. 配置触发词规则

在 `.claude/CLAUDE.md` 中添加 `pub` 触发词:

```markdown
### 4. Publish to Xiaohongshu (Trigger: "pub")
- **Trigger**: User inputs "pub"
- **Action**:
  1. Read article from content/posts/
  2. Generate card image via card_generator.py
  3. Extract title (truncate to 20 chars if needed)
  4. Summarize content (≤1000 chars)
  5. Call xiaohongshu-mcp API
  6. Output: Published status
```

## 实际使用

**发布命令**:
```bash
# 在 Claude Code 或 Trae 中输入
pub
```

**执行流程**:
1. ✅ 生成卡片图片 (2秒)
2. ✅ 提取文章标题和摘要 (1秒)
3. ✅ 调用 API 发布 (14秒,图片上传)
4. ✅ 返回发布成功

**发布结果**:
- 标题: 用AI IDE打造博客写作工作流
- 正文: 950字符,包含4个核心要点+标签
- 配图: 简约白色卡片
- 状态: ✅ 发布完成

**查看方式**:
- 打开小红书 App
- 进入"我"的页面
- 查看最新发布的笔记

## 技术细节

### API 路由发现

xiaohongshu-mcp 的代码结构:

```go
// routes.go
api := router.Group("/api/v1")
{
    api.GET("/login/status", checkLoginStatusHandler)
    api.POST("/publish", publishHandler)           // 图文发布
    api.POST("/publish_video", publishVideoHandler) // 视频发布
    api.GET("/feeds/list", listFeedsHandler)
    // ...
}
```

关键发现: **提供了简洁的 REST API,不需要复杂的 MCP 协议初始化**。

### 内容格式转换

从 Markdown 博客到小红书笔记:

| 元素 | Markdown | 小红书 | 处理方式 |
|------|----------|--------|---------|
| 标题 | `# 标题` | 20字限制 | 截断 |
| 代码块 | ` ```code``` ` | 不支持 | 删除 |
| 图片 | `![](url)` | 本地文件 | 生成卡片 |
| 链接 | `[text](url)` | 纯文本 | 提取text |
| 列表 | `- item` | `• item` | 保留 |
| Emoji | `:emoji:` | 原生emoji | 直接使用 |

### 卡片设计原则

参考了小红书优质笔记的设计:

1. **配色**: 白色背景 + 渐变强调色
2. **布局**: 左序号右标签,信息密度适中
3. **字体**: 苹方/黑体,清晰易读
4. **尺寸**: 1080x1350,适配小红书展示

## 遇到的坑

### 1. MCP 协议复杂

最初尝试通过 MCP 协议调用工具,发现需要复杂的初始化:
```json
{"jsonrpc":"2.0","method":"initialize","params":{...}}
{"jsonrpc":"2.0","method":"notifications/initialized"}
{"jsonrpc":"2.0","method":"tools/list"}
```

**解决**: 直接使用 REST API,简单直接。

### 2. 图片路径问题

API 要求**绝对路径**,相对路径会失败:
```json
{
  "images": ["./card.png"]  // ❌ 失败
  "images": ["/Users/lifeng/myblog/static/images/card.png"]  // ✅ 成功
}
```

### 3. 内容长度限制

第一次发布超过1000字被截断。

**解决**: 提取核心要点,用 emoji 和项目符号让内容更紧凑。

## 总结

通过 **xiaohongshu-mcp + Python 卡片生成器**,实现了博客到小红书的一键发布:

✅ **自动化程度高** - 一个 `pub` 命令完成
✅ **视觉效果好** - 简约白色卡片风格
✅ **扩展性强** - 可轻松支持其他平台

核心价值: **把重复的发布流程自动化,专注于内容创作本身**。

## 后续优化

1. **智能摘要** - 用 AI 自动提取文章要点
2. **多风格支持** - 根据内容类型选择卡片模板
3. **定时发布** - 设置最佳发布时间
4. **数据分析** - 跟踪笔记阅读和互动数据

---

**项目地址**: [xiaohongshu-mcp](https://github.com/xpzouying/xiaohongshu-mcp)
**相关文件**:
- 卡片生成器: `scripts/card_generator.py`
- 规则配置: `.claude/CLAUDE.md`
- 示例卡片: `static/images/ai-ide-workflow-card.png`
