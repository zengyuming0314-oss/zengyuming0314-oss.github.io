#!/usr/bin/env python3
"""扫描 works/ 文件夹，自动生成 works.js（作品列表）

用法：
  1. 在 works/ 下按分类建文件夹，例如：
       works/宣传片/a.mp4
       works/MV/b.mp4
  2. 运行本脚本（或双击 build.command）
  3. 刷新网页即可看到作品

支持：mp4 mov m4v webm / jpg jpeg png gif
"""
import json, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
WORKS = os.path.join(ROOT, "works")
VIDEO_EXT = {".mp4", ".mov", ".m4v", ".webm"}
IMG_EXT = {".jpg", ".jpeg", ".png", ".gif", ".webp"}

def clean(name):
    name = os.path.splitext(name)[0]
    name = re.sub(r"^[\s\-_\.]+|[\s\-_\.]+$", "", name)
    return name

items = []
if os.path.isdir(WORKS):
    for entry in sorted(os.listdir(WORKS)):
        p = os.path.join(WORKS, entry)
        if os.path.isfile(p):
            ext = os.path.splitext(entry)[1].lower()
            if ext in VIDEO_EXT | IMG_EXT:
                items.append({"file": "works/" + entry, "title": clean(entry), "cat": "未分类"})
        elif os.path.isdir(p):
            for f in sorted(os.listdir(p)):
                ext = os.path.splitext(f)[1].lower()
                if ext in VIDEO_EXT | IMG_EXT:
                    items.append({"file": f"works/{entry}/{f}", "title": clean(f), "cat": entry})

out = "window.WORKS = " + json.dumps(items, ensure_ascii=False, indent=2) + ";"

# 追加远程视频（remotes.json：大文件放 GitHub Releases，这里写完整 URL）
remotes_path = os.path.join(ROOT, "remotes.json")
if os.path.exists(remotes_path):
    with open(remotes_path, encoding="utf-8") as fp:
        remotes = json.load(fp)
    items.extend(remotes)
with open(os.path.join(ROOT, "works.js"), "w", encoding="utf-8") as fp:
    fp.write(out)

print(f"✅ 已生成 {len(items)} 件作品 → works.js")
for c in sorted({i["cat"] for i in items}):
    n = sum(1 for i in items if i["cat"] == c)
    print(f"   📁 {c}: {n} 件")
