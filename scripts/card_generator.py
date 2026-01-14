#!/usr/bin/env python3
"""
文字卡片生成器 - 用于小红书发布
使用 PIL 生成简洁清新的文字卡片图
"""

from PIL import Image, ImageDraw, ImageFont
import os
import sys

# 卡片配置 (匹配 ai-waiting-card.png 风格)
CARD_WIDTH = 1080
CARD_HEIGHT = 1440
PADDING = 60
LINE_HEIGHT = 1.4

# 配色方案
BG_COLOR = (255, 255, 255)  # 白色背景
PRIMARY_COLOR = (51, 51, 51)  # 主色调（黑色 - 用于序号）
ACCENT_COLOR = (235, 69, 55)  # 强调色（红色 - 用于警示）
TEXT_COLOR = (51, 51, 51)  # 主文字颜色
GRAY = (136, 136, 136)  # 辅助文字颜色
LIGHT_GRAY = (248, 248, 248)  # 标签背景色
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

def create_tag_background(draw, x, y, text, font):
    """绘制灰色标签背景"""
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    padding_x = 12
    padding_y = 6

    # 绘制圆角矩形背景
    rect_coords = [
        x - padding_x,
        y - padding_y,
        x + text_width + padding_x,
        y + text_height + padding_y
    ]
    draw.rounded_rectangle(rect_coords, radius=4, fill=LIGHT_GRAY)
    return x, y

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

    # 字体（更大，匹配 ai-waiting-card 的紧凑风格）
    title_font = get_font(56, bold=True)
    subtitle_font = get_font(28)
    number_font = get_font(48, bold=True)
    point_title_font = get_font(34, bold=True)
    point_desc_font = get_font(28)
    tag_font = get_font(24)
    footer_font = get_font(24)

    y = PADDING

    # 绘制标题（纯黑）
    title_lines = wrap_text(title, title_font, CARD_WIDTH - 2*PADDING, draw)
    for line in title_lines:
        draw.text((PADDING, y), line, font=title_font, fill=TEXT_COLOR)
        y += 68

    y += 18

    # 绘制副标题
    draw.text((PADDING, y), subtitle, font=subtitle_font, fill=GRAY)
    y += 60

    # 绘制分割线
    draw.line([(PADDING, y), (CARD_WIDTH - PADDING, y)], fill=DIVIDER_COLOR, width=2)
    y += 50

    # 绘制要点
    for idx, (number, point_title, point_desc, tag_text) in enumerate(points):
        # 序号（黑色）
        draw.text((PADDING, y), str(number) + ".", font=number_font, fill=PRIMARY_COLOR)

        # 标题和右侧标签
        title_x = PADDING + 80

        # 计算标签位置
        tag_bbox = draw.textbbox((0, 0), tag_text, font=tag_font)
        tag_width = tag_bbox[2] - tag_bbox[0]
        tag_x = CARD_WIDTH - PADDING - tag_width - 24

        # 绘制标签背景和文字
        create_tag_background(draw, tag_x, y + 12, tag_text, tag_font)
        draw.text((tag_x, y + 12), tag_text, font=tag_font, fill=GRAY)

        # 绘制标题
        # 如果是"绝对禁区"或"Critical"，使用红色
        title_color = TEXT_COLOR
        if "禁区" in point_title or "Critical" in tag_text:
             title_color = ACCENT_COLOR
             # 对应序号也变红
             draw.text((PADDING, y), str(number) + ".", font=number_font, fill=ACCENT_COLOR)

        draw.text((title_x, y), point_title, font=point_title_font, fill=title_color)

        y += 52

        # 描述（带项目符号）
        desc_lines = point_desc.split('\n')
        for line in desc_lines:
            if line.strip():
                # 绘制项目符号
                draw.text((title_x, y), "•", font=point_desc_font, fill=GRAY)
                # 绘制描述文本
                desc_text = line.strip().lstrip('•').strip()
                wrapped_lines = wrap_text(desc_text, point_desc_font, CARD_WIDTH - title_x - PADDING - 30, draw)
                for wrapped_line in wrapped_lines:
                    draw.text((title_x + 35, y), wrapped_line, font=point_desc_font, fill=TEXT_COLOR)
                    y += 42

        y += 35

    # 底部信息
    y = CARD_HEIGHT - 100

    # 分割线
    draw.line([(PADDING, y), (CARD_WIDTH - PADDING, y)], fill=DIVIDER_COLOR, width=1)
    y += 35

    # 作者
    footer_text = f"Produced by AI Assistant | @{author}"
    draw.text((PADDING, y), footer_text, font=footer_font, fill=GRAY)

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
