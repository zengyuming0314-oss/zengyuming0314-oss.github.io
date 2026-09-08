#!/usr/bin/env python3
"""批次2：压 720p 强压缩网页版（≤~90MB/个，总量 <1GB），输出到 .web2/<cat>/<title>.mp4"""
import json, os, re, subprocess, time, datetime, glob

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

remotes = json.load(open(os.path.join(ROOT, "remotes.json"), encoding="utf-8"))
plan = []
for r in remotes:
    if "portfolio-videos-01" in r["file"]:  # 猫咪跳过（待决定）
        continue
    src = find_src(r["title"])
    if src:
        out = os.path.join(ROOT, ".web2", r["cat"], r["title"] + ".mp4")
        plan.append((src, out, r["title"], r["cat"]))

done = set()
if os.path.exists(LOG):
    for line in open(LOG, encoding="utf-8"):
        if " OK " in line: done.add(line.split(" OK ")[1].strip())
print(f"待转码 {len(plan)}", flush=True)
for i, (src, out, title, cat) in enumerate(plan, 1):
    key = cat + "/" + title + ".mp4"
    if key in done: continue
    os.makedirs(os.path.dirname(out), exist_ok=True)
    t0 = time.time()
    vf = "scale=w='min(1280,iw)':h='min(720,ih)':force_original_aspect_ratio=decrease,scale=trunc(iw/2)*2:trunc(ih/2)*2"
    r = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src,
        "-vf", vf, "-c:v", "libx264", "-preset", "veryfast", "-crf", "27",
        "-maxrate", "2M", "-bufsize", "4M", "-c:a", "aac", "-b:a", "96k",
        "-movflags", "+faststart", out], capture_output=True, text=True)
    if r.returncode == 0:
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(f"{NOW()} OK {key}\n")
        print(f"[{NOW()}] ({i}/{len(plan)}) OK {title} {time.time()-t0:.0f}s", flush=True)
    else:
        print(f"[{NOW()}] ({i}/{len(plan)}) FAIL {title}: {r.stderr[-150:]}", flush=True)
with open(LOG, "a", encoding="utf-8") as f:
    f.write("WEB2_DONE\n")
print("WEB2_DONE", flush=True)
