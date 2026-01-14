
import sys
import os
import requests
import json

# Add current directory to sys.path to import card_generator
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from card_generator import generate_card

# 1. Generate Card
output_path = "/Users/lifeng/myblog/static/images/ios-downtime-card.png"
generate_card(
    title="给手机设个“数字宵禁”",
    subtitle="利用 iOS 停用时间保障睡眠",
    points=[
        (1, "核心痛点",
         "• 晚间意志力耗尽 (Ego Depletion)\n• 靠自律对抗算法 = 徒手对抗重力",
         "背景"),
        (2, "核心方案",
         "• 开启 iOS \"停用时间\" (Downtime)\n• 设置 22:30 - 07:00 自动熔断",
         "Solution"),
        (3, "关键一步",
         "• 必须开启\"停用期间阻止使用\"\n• 增加输入密码的摩擦成本",
         "Critical"),
        (4, "沙箱思维",
         "• 白天边界内自由，夜晚边界外熔断\n• 用系统强制力代替意志力",
         "Philosophy"),
    ],
    author="jackley",
    tags=["iOS", "时间管理", "数字健康"],
    output_path=output_path
)

# 2. Publish to Xiaohongshu
api_url = "http://localhost:18060/api/v1/publish"

title = "给手机设个“数字宵禁”：iOS停用时间"
content = """晚睡往往不是因为“不想睡”，而是因为“停不下来”。经过一天的消耗，晚间意志力薄弱，试图靠自律对抗算法无异于徒手对抗重力。

更有效的策略是：承认意志力的局限，引入系统级的外部强制力。

📱 核心设置：iOS 停用时间 (Downtime)
1. 进入“屏幕使用时间” > “停用时间”
2. 设置时间：22:30 - 07:00
3. ✅ 关键一步：开启“停用期间阻止使用”！如果不开启，仅仅是变暗，没有任何强制力。开启后，必须输入密码才能延时，增加了摩擦成本。

🛡️ 沙箱思维
不追求24小时紧绷的自律。
• 边界内（白天）：适度放松，无负罪感
• 边界外（夜晚）：严格熔断，不依赖意志力

与其相信自己能战胜算法，不如利用系统来管理算法。把夜晚还给睡眠。😴

#iOS技巧 #时间管理 #睡眠 #数字健康 #自律 #沙箱思维"""

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
