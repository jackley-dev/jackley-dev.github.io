#!/usr/bin/env python3
"""
文字卡片生成器 - 用于小红书发布
使用 PIL 生成简洁清新的文字卡片图
"""

from PIL import Image, ImageDraw, ImageFont
import os
import sys

# 卡片配置
CARD_WIDTH = 1080
CARD_HEIGHT = 1350
PADDING = 80
LINE_HEIGHT = 1.6

# 配色方案
BG_COLOR = (255, 255, 255)  # 白色背景
PRIMARY_COLOR = (102, 126, 234)  # 主色调（渐变起点）
SECONDARY_COLOR = (118, 75, 162)  # 次色调（渐变终点）
TEXT_COLOR = (51, 51, 51)  # 主文字颜色
LIGHT_TEXT_COLOR = (136, 136, 136)  # 浅色文字
DIVIDER_COLOR = (238, 238, 238)  # 分割线颜色

def get_font(size, bold=False):
    """获取字体，优先使用系统中文字体"""
    font_paths = [
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Medium.ttc",
        "/System/Library/Fonts/Hiragino Sans GB.ttc",
        "/Library/Fonts/Arial Unicode.ttf",
    ]

    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except:
                continue

    return ImageFont.load_default()

def create_gradient_text_color(ratio):
    """根据比例生成渐变色"""
    r = int(PRIMARY_COLOR[0] * (1 - ratio) + SECONDARY_COLOR[0] * ratio)
    g = int(PRIMARY_COLOR[1] * (1 - ratio) + SECONDARY_COLOR[1] * ratio)
    b = int(PRIMARY_COLOR[2] * (1 - ratio) + SECONDARY_COLOR[2] * ratio)
    return (r, g, b)

def wrap_text(text, font, max_width, draw):
    """文本自动换行"""
    lines = []
    for paragraph in text.split('\n'):
        line = ""
        for char in paragraph:
            test_line = line + char
            bbox = draw.textbbox((0, 0), test_line, font=font)
            if bbox[2] - bbox[0] <= max_width:
                line = test_line
            else:
                if line:
                    lines.append(line)
                line = char
        if line:
            lines.append(line)
    return lines

def generate_card(title, subtitle, points, author, tags, output_path):
    """
    生成文字卡片（简约白色风格）

    参数:
        title: 主标题
        subtitle: 副标题
        points: [(number, title, desc, time), ...] 要点列表
        author: 作者名
        tags: 标签列表
        output_path: 输出图片路径
    """
    # 创建白色背景
    img = Image.new('RGB', (CARD_WIDTH, CARD_HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)

    # 字体
    title_font = get_font(56, bold=True)
    subtitle_font = get_font(28)
    number_font = get_font(32, bold=True)
    point_title_font = get_font(32, bold=True)
    point_desc_font = get_font(26)
    time_font = get_font(24)
    footer_font = get_font(24)

    y = PADDING

    # 绘制标题（渐变色）
    title_lines = wrap_text(title, title_font, CARD_WIDTH - 2*PADDING, draw)
    for i, line in enumerate(title_lines):
        ratio = i / max(len(title_lines) - 1, 1)
        color = create_gradient_text_color(ratio)
        draw.text((PADDING, y), line, font=title_font, fill=color)
        y += 70

    y += 10

    # 绘制副标题
    draw.text((PADDING, y), subtitle, font=subtitle_font, fill=LIGHT_TEXT_COLOR)
    y += 60

    # 绘制分割线
    draw.line([(PADDING, y), (CARD_WIDTH - PADDING, y)], fill=DIVIDER_COLOR, width=2)
    y += 50

    # 绘制要点
    for idx, (number, point_title, point_desc, read_time) in enumerate(points):
        # 序号（渐变色圆圈）
        ratio = idx / max(len(points) - 1, 1)
        number_color = create_gradient_text_color(ratio)

        # 绘制序号
        draw.text((PADDING, y), str(number), font=number_font, fill=number_color)

        # 标题和阅读时间
        title_x = PADDING + 50
        time_text = f"⏱ {read_time}"
        time_bbox = draw.textbbox((0, 0), time_text, font=time_font)
        time_width = time_bbox[2] - time_bbox[0]
        time_x = CARD_WIDTH - PADDING - time_width

        draw.text((title_x, y), point_title, font=point_title_font, fill=TEXT_COLOR)
        draw.text((time_x, y + 5), time_text, font=time_font, fill=LIGHT_TEXT_COLOR)

        y += 45

        # 描述（带项目符号）
        desc_lines = point_desc.split('\n')
        for line in desc_lines:
            if line.strip():
                # 绘制项目符号
                draw.text((title_x, y), "•", font=point_desc_font, fill=LIGHT_TEXT_COLOR)
                # 绘制描述文本
                desc_text = line.strip().lstrip('•').strip()
                wrapped_lines = wrap_text(desc_text, point_desc_font, CARD_WIDTH - title_x - PADDING - 30, draw)
                for wrapped_line in wrapped_lines:
                    draw.text((title_x + 25, y), wrapped_line, font=point_desc_font, fill=TEXT_COLOR)
                    y += 38

        y += 30

    # 底部信息
    y = CARD_HEIGHT - 120

    # 分割线
    draw.line([(PADDING, y), (CARD_WIDTH - PADDING, y)], fill=DIVIDER_COLOR, width=2)
    y += 40

    # 作者
    footer_text = f"Produced by AI Assistant | @{author}"
    draw.text((PADDING, y), footer_text, font=footer_font, fill=LIGHT_TEXT_COLOR)

    # 保存
    img.save(output_path, 'PNG', quality=95)
    print(f"✅ 卡片已生成: {output_path}")
    return output_path


if __name__ == "__main__":
    # 示例：生成博客工作流卡片
    output = generate_card(
        title="用 AI IDE 打造博客写作工作流",
        subtitle="Trae 与 Claude Code 双平台实践",
        points=[
            (1, "对话式写作 (Brainstorming)",
             "• 通过与 AI 对话激发想法\n• 自然过渡到文章，降低写作阻力",
             "默认模式"),
            (2, "触发词控制 (ga)",
             "• 输入 ga 生成文章\n• AI 不会过度主动，完全可控",
             "生成文章"),
            (3, "一键发布 (commit)",
             "• 自动 git 操作\n• 推送到 GitHub，触发部署",
             "自动部署"),
            (4, "双平台通用",
             "• Trae 和 Claude Code 规则几乎相同\n• 无缝切换，知识外化",
             "可复用"),
        ],
        author="jackley",
        tags=["AIGC", "效率工具", "AI编程"],
        output_path="/Users/lifeng/myblog/static/images/ai-ide-workflow-card.png"
    )
