
import sys
import os
import requests
import json

# Add current directory to sys.path to import card_generator
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from card_generator import generate_card

# 1. Generate Card
output_path = "/Users/lifeng/myblog/static/images/sleep-psychology-card.png"
generate_card(
    title="为什么越累越不想睡？",
    subtitle="揭秘“报复性晚睡”背后的生理欺骗",
    points=[
        (1, "生理欺骗",
         "• 越晚越亢奋 = 虚假繁荣\n• 皮质醇强行提神 (Tired but Wired)",
         "Mechanism"),
        (2, "认知偏差",
         "• 夜间CEO：只管爽 (双曲贴现)\n• 白天打工仔：负责还债 (后悔)",
         "Psychology"),
        (3, "高利贷模型",
         "• 晚睡1小时 = 借高利贷\n• 代价：明天3小时高效时间 + 坏情绪",
         "Mindset"),
        (4, "强制熔断",
         "• 承认意志力无效\n• 用iOS停用时间物理断电 (22:30)",
         "Action"),
    ],
    author="jackley",
    tags=["心理学", "自我管理", "睡眠"],
    output_path=output_path
)

# 2. Publish to Xiaohongshu
api_url = "http://localhost:18060/api/v1/publish"

title = "为什么越累越不想睡？揭秘晚睡心理学 🧠"
content = """你是否也陷入过这种死循环：明明累得要死，但越到睡前越精神？
这不是因为你精力旺盛，而是身体在“回光返照”。

🧠 1. 生理欺骗：Tired but Wired
当错过入睡窗口，大脑误判进入“危机模式”，分泌皮质醇强行提神。这种“亢奋”是透支明天的能量。

🎭 2. 认知偏差：夜间CEO vs 白天打工仔
“夜间CEO”拥有决策权，为了当下的爽快（刷手机），把痛苦甩给明天的“白天打工仔”。这是典型的双曲贴现。

💡 3. 破局：高利贷模型 & 强制熔断
• 认知重构：告诉自己“现在不睡是在借高利贷，利息极高”。
• 行为熔断：利用 iOS “停用时间” (22:30) 作为物理开关。

不要相信晚上的大脑，它被激素绑架了。把夜晚还给睡眠。😴

#心理学 #晚睡 #报复性熬夜 #自律 #时间管理 #个人成长 #睡眠质量 #认知偏差"""

payload = {
    "title": title,
    "content": content,
    "images": [output_path]
}

print("Publishing to Xiaohongshu...")
try:
    response = requests.post(api_url, json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
