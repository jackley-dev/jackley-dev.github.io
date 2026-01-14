
import sys
import os

# Add current directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from card_generator import generate_card

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
