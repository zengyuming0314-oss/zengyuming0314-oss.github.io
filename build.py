#!/usr/bin/env python3
"""扫描 works/ 文件夹，自动生成 works.js（作品列表）

用法：
  1. 在 works/ 下按分类建文件夹，例如：
       works/宣传片/a.mp4
       works/MV/b.mp4
  2. 运行本脚本（或双击 build.command）
  3. 刷新网页即可看到作品

支持：mp4 mov m4v webm / jpg jpeg png gif
大文件：remotes.json 里写远程 URL（GitHub Releases），本脚本自动并入
分类名自动归一化为短名（人物IP/文旅/宣传片/访谈/纪录片/短片/AIGC/运营数据），
文件夹怎么命名都行（含 中文**English** 或 编号 都会被清洗）。
"""
import json, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
WORKS = os.path.join(ROOT, "works")
VIDEO_EXT = {".mp4", ".mov", ".m4v", ".webm"}
IMG_EXT = {".jpg", ".jpeg", ".png", ".gif", ".webp"}

def clean(name):
    name = os.path.splitext(name)[0]
    return re.sub(r"^[\s\-_\.]+|[\s\-_\.]+$", "", name)

def canon(cat):
    """把任意文件夹名归一化成短分类名"""
    s = cat.replace("**", " ").replace("—", " ").strip()
    s = re.sub(r"^[\d\.\s\u00b7·\-]+", "", s)
    rules = [
        (r"人物ip|个人ip", "人物IP"),
        (r"文旅", "文旅"),
        (r"宣传|招商", "宣传片"),
        (r"访谈", "访谈"),
        (r"纪录", "纪录片"),
        (r"短视频|短片", "短片"),
        (r"aigc|AI创作|ai创作", "AIGC"),
        (r"运营数据|数据", "运营数据"),
    ]
    for pat, tag in rules:
        if re.search(pat, cat, re.I) or re.search(pat, s, re.I):
            return tag
    return s or cat

def media_title(fname):
    return clean(fname)

items = []
if os.path.isdir(WORKS):
    for entry in sorted(os.listdir(WORKS)):
        p = os.path.join(WORKS, entry)
        if os.path.isfile(p):
            ext = os.path.splitext(entry)[1].lower()
            if ext in VIDEO_EXT | IMG_EXT:
                items.append({"file": "works/" + entry, "title": media_title(entry), "cat": canon("未分类")})
        elif os.path.isdir(p):
            for f in sorted(os.listdir(p)):
                fp = os.path.join(p, f)
                ext = os.path.splitext(f)[1].lower()
                if ext in VIDEO_EXT | IMG_EXT:
                    item = {"file": f"works/{entry}/{f}", "title": media_title(f), "cat": canon(entry)}
                    if os.path.exists(fp + ".poster.jpg"):
                        item["poster"] = f"works/{entry}/{f}.poster.jpg"
                    items.append(item)

# 远程大视频（remotes.json）
remotes_path = os.path.join(ROOT, "remotes.json")
if os.path.exists(remotes_path):
    with open(remotes_path, encoding="utf-8") as fp:
        for r in json.load(fp):
            r = dict(r)
            r["cat"] = canon(r.get("cat", "未分类"))
            items.append(r)

out = "window.WORKS = " + json.dumps(items, ensure_ascii=False, indent=2) + ";"
with open(os.path.join(ROOT, "works.js"), "w", encoding="utf-8") as fp:
    fp.write(out)

print(f"✅ 已生成 {len(items)} 件作品 → works.js")
counts = {}
for i in items:
    counts[i["cat"]] = counts.get(i["cat"], 0) + 1
for c in sorted(counts):
    print(f"   📁 {c}: {counts[c]} 件")
