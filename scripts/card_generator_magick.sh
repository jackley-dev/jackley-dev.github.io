#!/bin/bash
# ImageMagick 卡片生成器

OUTPUT="/Users/lifeng/myblog/static/images/demo-magick.png"

# 创建白色背景
convert -size 1080x1440 xc:white \
  -font /System/Library/Fonts/PingFang.ttc \
  \
  -pointsize 56 -fill '#333333' -annotate +50+110 '用 AI IDE 打造博客写作工作流' \
  -pointsize 28 -fill '#999999' -annotate +50+170 'Trae 与 Claude Code 双平台实践' \
  \
  -strokewidth 1 -stroke '#eeeeee' -draw "line 50,220 1030,220" \
  \
  -pointsize 48 -fill '#6474F0' -annotate +50+318 '1' \
  -pointsize 34 -fill '#333333' -annotate +130+318 '对话式写作 (Brainstorming)' \
  -pointsize 24 -fill '#999999' -annotate +880+318 '默认模式' \
  \
  -pointsize 48 -fill '#6474F0' -annotate +50+568 '2' \
  -pointsize 34 -fill '#333333' -annotate +130+568 '触发词控制 (ga)' \
  -pointsize 24 -fill '#999999' -annotate +880+568 '生成文章' \
  \
  -pointsize 48 -fill '#6474F0' -annotate +50+818 '3' \
  -pointsize 34 -fill '#333333' -annotate +130+818 '一键发布 (commit)' \
  -pointsize 24 -fill '#999999' -annotate +880+818 '自动部署' \
  \
  -pointsize 48 -fill '#6474F0' -annotate +50+1068 '4' \
  -pointsize 34 -fill '#333333' -annotate +130+1068 '双平台通用' \
  -pointsize 24 -fill '#999999' -annotate +900+1068 '可复用' \
  \
  -pointsize 24 -fill '#999999' -annotate +50+1390 'Produced by AI Assistant | @jackley' \
  \
  "$OUTPUT"

echo "✅ ImageMagick 卡片生成完成: demo-magick.png"
