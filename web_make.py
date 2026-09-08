#!/usr/bin/env python3
"""把所有大视频转成网页流畅版（1080p 封顶 ~4.5Mbps）到 .web/，日志续传"""
import json, os, re, subprocess, time, datetime, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(ROOT, ".web.log")
os.makedirs(os.path.join(ROOT, ".web"), exist_ok=True)

def clean(n): return re.sub(r"\.[^.]+$", "", n).strip()
def find_src(title):
    for cat in os.listdir(os.path.join(ROOT, "视频原片")):
        cp = os.path.join(ROOT, "视频原片", cat)
        if not os.path.isdir(cp): continue
        for f in os.listdir(cp):
            if clean(f) == title and os.path.isfile(os.path.join(cp, f)):
                return os.path.join(cp, f)
    return None

remotes = json.load(open(os.path.join(ROOT, "remotes.json"), encoding="utf-8"))
plan = []
for r in remotes:
    base = os.path.basename(r["file"])
    if not base: continue
    if "portfolio-videos-01" in r["file"]:   # 猫咪在另一个 release，跳过
        continue
    src = find_src(r["title"])
    if src:
        plan.append((src, os.path.join(ROOT, ".web", base), r["title"]))

now = lambda: datetime.datetime.now().strftime("%H:%M:%S")
done = set()
if os.path.exists(LOG):
    for line in open(LOG, encoding="utf-8"):
        if " OK " in line: done.add(line.split(" OK ")[1].strip())

print(f"待转码 {len(plan)} 个", flush=True)
for i, (src, out, title) in enumerate(plan, 1):
    name = os.path.basename(out)
    if name in done: continue
    t0 = time.time()
    r = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src,
        "-vf", "scale='min(1920,iw)':-2",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "24",
        "-maxrate", "5M", "-bufsize", "10M",
        "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", out],
        capture_output=True, text=True)
    if r.returncode == 0:
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(f"{now()} OK {name}\n")
        print(f"[{now()}] ({i}/{len(plan)}) OK {name} {time.time()-t0:.0f}s", flush=True)
    else:
        print(f"[{now()}] ({i}/{len(plan)}) FAIL {name}: {r.stderr[-150:]}", flush=True)
with open(LOG, "a", encoding="utf-8") as f:
    f.write("WEB_DONE\n")
print("WEB_DONE", flush=True)
