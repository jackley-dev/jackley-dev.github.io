#!/usr/bin/env python3
"""
Matplotlib 卡片生成器
"""
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.font_manager import FontProperties

# 中文字体 (使用黑体)
font = FontProperties(fname='/System/Library/Fonts/STHeiti Medium.ttc')

# 创建画布
fig, ax = plt.subplots(figsize=(10.8, 14.4), dpi=100, facecolor='white')
ax.set_xlim(0, 1080)
ax.set_ylim(0, 1440)
ax.axis('off')
ax.invert_yaxis()  # 反转Y轴,让原点在左上角

# 标题
ax.text(50, 110, '用 AI IDE 打造博客写作工作流',
        fontproperties=font, fontsize=42, color='#333333', weight='bold')

# 副标题
ax.text(50, 170, 'Trae 与 Claude Code 双平台实践',
        fontproperties=font, fontsize=21, color='#999999')

# 分割线
ax.plot([50, 1030], [220, 220], color='#eeeeee', linewidth=1)

# 要点
points = [
    (1, '对话式写作 (Brainstorming)', '默认模式', 318),
    (2, '触发词控制 (ga)', '生成文章', 568),
    (3, '一键发布 (commit)', '自动部署', 818),
    (4, '双平台通用', '可复用', 1068)
]

for num, title, tag, y in points:
    # 序号
    ax.text(50, y, str(num), fontproperties=font, fontsize=36,
            color='#6474F0', weight='bold')
    # 标题
    ax.text(130, y, title, fontproperties=font, fontsize=25,
            color='#333333', weight='bold')
    # 标签
    ax.text(930, y, tag, fontproperties=font, fontsize=18,
            color='#999999', ha='right')

# 底部
ax.text(50, 1390, 'Produced by AI Assistant | @jackley',
        fontproperties=font, fontsize=18, color='#999999')

# 保存
plt.savefig('/Users/lifeng/myblog/static/images/demo-matplotlib.png',
            bbox_inches='tight', pad_inches=0, dpi=100, facecolor='white')
plt.close()

print('✅ Matplotlib 卡片生成完成: demo-matplotlib.png')
