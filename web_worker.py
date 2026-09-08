#!/usr/bin/env python3
"""并行 worker：用法 web_worker.py <n> <total>，处理 title哈希%total==n 的那批"""
import json, os, re, subprocess, time, datetime, sys, hashlib

ROOT = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(ROOT, ".web2.log")
NOW = lambda: datetime.datetime.now().strftime("%H:%M:%S")
def clean(n): return re.sub(r"\.[^.]+$", "", n).strip()
def find_src(title):
    for cat in os.listdir(os.path.join(ROOT, "视频原片")):
        cp = os.path.join(ROOT, "视频原片", cat)
        if not os.path.isdir(cp): continue
        for f in os.listdir(cp):
            if clean(f) == title and os.path.isfile(os.path.join(cp, f)):
                return os.path.join(cp, f)
    return None

me, total = int(sys.argv[1]), int(sys.argv[2])
remotes = json.load(open(os.path.join(ROOT, "remotes.json"), encoding="utf-8"))
jobs = []
for r in remotes:
    if "portfolio-videos-01" in r["file"]: continue
    src = find_src(r["title"])
    if src:
        jobs.append((src, os.path.join(ROOT, ".web2", r["cat"], r["title"] + ".mp4"), r["title"], r["cat"]))
mine = [j for j in jobs if int(hashlib.md5(j[2].encode()).hexdigest(), 16) % total == me]
done = set()
if os.path.exists(LOG):
    for line in open(LOG, encoding="utf-8"):
        if " OK " in line: done.add(line.split(" OK ")[1].strip())
vf = "scale=w='min(1280,iw)':h='min(720,ih)':force_original_aspect_ratio=decrease,scale=trunc(iw/2)*2:trunc(ih/2)*2"
for src, out, title, cat in mine:
    key = cat + "/" + title + ".mp4"
    if key in done: continue
    os.makedirs(os.path.dirname(out), exist_ok=True)
    t0 = time.time()
    r = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-vf", vf,
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "27", "-maxrate", "2M",
        "-bufsize", "4M", "-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart", out],
        capture_output=True, text=True)
    if r.returncode == 0:
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(f"{NOW()} OK {key}\n")
        print(f"[W{me}] OK {title} {time.time()-t0:.0f}s", flush=True)
    else:
        print(f"[W{me}] FAIL {title}: {r.stderr[-140:]}", flush=True)
