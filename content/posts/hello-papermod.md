+++
date = '2025-12-05T23:25:56+08:00'
draft = false
title = '配置Github Pages'

tags = ["Github Pages", "Hugo"]  # 标签
categories = ["Blog"]  # 分类
+++


我想建立一个长期的写作基地，所以试着创建了自己的github pages，本篇记录了创建过程。

**3分钟极简版，创建GitHub Pages**

1. 新建仓库：

登录 GitHub，点击右上角 + -> New repository。

关键步骤： 仓库名（Repository name）必须填写为 用户名.github.io。例如：用户名是 tom, 仓库名必须是 tom.github.io。

勾选 Public，点击 Create repository。

2. 创建网页文件：

在仓库页面，点击 creating a new file 链接。

文件名填写：index.html

文件内容随便写，例如：

```
HTML

<h1>这是我的技术博客</h1>
<p>Hello World! 2025年开始写作。</p>
```
滚动到底部，点击绿色按钮 Commit changes。

3. 见证奇迹：

等待 1-2 分钟。

在浏览器输入地址：https://用户名.github.io。

应该能看到刚才写的网页了。

总结：GitHub Pages 的本质就是————你把文件放在仓库里，它自动帮你变成一个网站。



