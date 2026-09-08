#!/usr/bin/env python3
"""等 .web.log 出现 WEB_DONE 后，把 .web/ 里的网页版上传替换 GitHub 资产；断点续传"""
import os, subprocess, time, datetime, glob, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = "zengyuming0314-oss/zengyuming0314-oss.github.io"
REL = "portfolio-videos-02"
NOW = lambda: datetime.datetime.now().strftime("%H:%M:%S")

# 1) 等待转码完成（最长 8 小时）
deadline = time.time() + 8 * 3600
while not os.path.exists(os.path.join(ROOT, ".web.log")) or "WEB_DONE" not in open(os.path.join(ROOT, ".web.log"), encoding="utf-8").read():
    if time.time() > deadline:
        sys.exit("timeout waiting WEB_DONE")
    time.sleep(30)

# 2) 逐个上传（.webup.log 断点）
uplog = os.path.join(ROOT, ".webup.log")
done = set()
if os.path.exists(uplog):
    for line in open(uplog, encoding="utf-8"):
        if " OK " in line: done.add(line.split(" OK ")[1].strip())

files = sorted(glob.glob(os.path.join(ROOT, ".web", "*")))
for path in files:
    name = os.path.basename(path)
    if name in done: continue
    print(f"[{NOW()}] up {name}", flush=True)
    r = subprocess.run(["gh", "release", "upload", REL, path, "--repo", REPO, "--clobber"],
                       capture_output=True, text=True)
    if r.returncode == 0:
        with open(uplog, "a", encoding="utf-8") as f:
            f.write(f"{NOW()} OK {name}\n")
        print(f"[{NOW()}] OK {name}", flush=True)
    else:
        print(f"[{NOW()}] FAIL {name}: {r.stderr[:150]}", flush=True)
        time.sleep(10)
with open(uplog, "a", encoding="utf-8") as f:
    f.write("UPLOAD_DONE\n")
print("UPLOAD_DONE", flush=True)
