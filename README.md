# 🦞 作品集网站 — 使用说明

## 怎么加作品（超简单）
1. 把作品文件丢进 `works/` 文件夹
   - 视频：`.mp4` / `.mov` / `.webm`
   - 图片：`.jpg` / `.png` / `.gif`
2. 打开 `index.html`，找到网页里 **WORKS 数组**，照格式加一行：
   ```js
   {"file":"works/我的作品.mp4","title":"作品标题","tags":["宣传片","2024"]}
   ```
3. 保存，刷新页面 → 作品出现，点开可放大/播放

## 改个人信息
打开 `index.html`，找到 **SITE 配置**（名字、定位、头像、标签都在这改）。

头像：放一张 `avatar.jpg` 到根目录即可。

## 目录结构
```
portfolio-site/
├── index.html      ← 网站本体（改这里）
├── avatar.jpg      ← 你的头像（可选）
└── works/          ← 作品文件放这里
    ├── xxx.mp4
    └── xxx.jpg
```

## 预览
双击 `index.html` 就能在浏览器里看效果。

## 发布到网上（让别人/海外能打开）
选一种，告诉龙虾小弟即可帮你弄：
1. **GitHub Pages（推荐）**：免费、全球可开（新加坡 ✓）、还能绑自己的域名
2. 其他免费托管：Cloudflare Pages / Netlify / Vercel
