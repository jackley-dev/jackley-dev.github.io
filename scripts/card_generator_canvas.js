#!/usr/bin/env node
/**
 * Canvas 卡片生成器 (需要先安装: npm install canvas)
 */
const { createCanvas, registerFont } = require('canvas');
const fs = require('fs');

// 配置
const WIDTH = 1080;
const HEIGHT = 1440;
const PADDING = 50;

function generateCard() {
  const canvas = createCanvas(WIDTH, HEIGHT);
  const ctx = canvas.getContext('2d');

  // 白色背景
  ctx.fillStyle = '#ffffff';
  ctx.fillRect(0, 0, WIDTH, HEIGHT);

  // 标题
  ctx.font = 'bold 56px "PingFang SC"';
  ctx.fillStyle = '#333333';
  ctx.fillText('用 AI IDE 打造博客写作工作流', PADDING, PADDING + 60);

  // 副标题
  ctx.font = '28px "PingFang SC"';
  ctx.fillStyle = '#999999';
  ctx.fillText('Trae 与 Claude Code 双平台实践', PADDING, PADDING + 120);

  // 分割线
  ctx.strokeStyle = '#eeeeee';
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(PADDING, PADDING + 170);
  ctx.lineTo(WIDTH - PADDING, PADDING + 170);
  ctx.stroke();

  // 要点
  const points = [
    { num: 1, title: '对话式写作 (Brainstorming)', tag: '默认模式' },
    { num: 2, title: '触发词控制 (ga)', tag: '生成文章' },
    { num: 3, title: '一键发布 (commit)', tag: '自动部署' },
    { num: 4, title: '双平台通用', tag: '可复用' }
  ];

  let y = PADDING + 220;
  points.forEach(point => {
    // 序号
    ctx.font = 'bold 48px "PingFang SC"';
    ctx.fillStyle = '#6474F0';
    ctx.fillText(point.num.toString(), PADDING, y);

    // 标题
    ctx.font = 'bold 34px "PingFang SC"';
    ctx.fillStyle = '#333333';
    ctx.fillText(point.title, PADDING + 80, y);

    // 标签
    ctx.font = '24px "PingFang SC"';
    ctx.fillStyle = '#999999';
    const tagWidth = ctx.measureText(point.tag).width;
    ctx.fillText(point.tag, WIDTH - PADDING - tagWidth - 24, y);

    y += 250;
  });

  // 底部
  ctx.font = '24px "PingFang SC"';
  ctx.fillStyle = '#999999';
  ctx.fillText('Produced by AI Assistant | @jackley', PADDING, HEIGHT - 50);

  // 保存
  const buffer = canvas.toBuffer('image/png');
  fs.writeFileSync('/Users/lifeng/myblog/static/images/demo-canvas.png', buffer);
  console.log('✅ Canvas 卡片生成完成: demo-canvas.png');
}

generateCard();
