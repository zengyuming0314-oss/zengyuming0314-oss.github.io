#!/usr/bin/env python3
"""WEB2_DONE 后执行：把 .web2 产物搬进 works/<分类>/ 并带封面，清空远程大视频条目，重建 works.js"""
import json, os, re, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))

# 1) title→ascii 映射（用于封面）
remotes = json.load(open(os.path.join(ROOT, "remotes.json"), encoding="utf-8"))
ascii_by = {}
for r in remotes:
    base = os.path.basename(r["file"])
    if base: ascii_by[r["title"]] = base

# 2) 把 .web2/<cat>/<title>.mp4 → works/<cat>/<title>.mp4 + poster sidecar
moved = 0
for cat in os.listdir(os.path.join(ROOT, ".web2")):
    cp = os.path.join(ROOT, ".web2", cat)
    if not os.path.isdir(cp): continue
    for f in os.listdir(cp):
        if not f.endswith(".mp4"): continue
        title = f[:-4]
        dst_dir = os.path.join(ROOT, "works", cat)
        os.makedirs(dst_dir, exist_ok=True)
        dst = os.path.join(dst_dir, f)
        shutil.copy2(os.path.join(cp, f), dst)
        # 封面
        poster_src = None
        a = ascii_by.get(title)
        if a:
            cand = os.path.join(ROOT, "posters", os.path.splitext(a)[0] + ".jpg")
            if os.path.exists(cand): poster_src = cand
        if poster_src:
            shutil.copy2(poster_src, os.path.join(dst_dir, title + ".poster.jpg"))
        moved += 1
print(f"搬入 works: {moved}")

# 3) remotes.json：清空大视频条目（改走仓库），备份旧的
shutil.copy2(os.path.join(ROOT, "remotes.json"), os.path.join(ROOT, "remotes.backup.json"))
open(os.path.join(ROOT, "remotes.json"), "w", encoding="utf-8").write("[]\n")
print("remotes.json 已清空（备份 remotes.backup.json）")
