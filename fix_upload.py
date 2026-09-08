#!/usr/bin/env python3
"""把 .fixed/ 里的快播版视频重新上传替换 GitHub Release 资产（断点续传）"""
import json, os, subprocess, time, datetime, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = "zengyuming0314-oss/zengyuming0314-oss.github.io"
REL = "portfolio-videos-02"
LOG = os.path.join(ROOT, ".fixup.log")

def now(): return datetime.datetime.now().strftime("%H:%M:%S")

done = set()
if os.path.exists(LOG):
    for line in open(LOG, encoding="utf-8"):
        if " OK " in line:
            done.add(line.split(" OK ")[1].strip())

plan = json.load(open(os.path.join(ROOT, ".fix_plan.json"), encoding="utf-8"))
failed = []
for src, name in plan:
    if name in done:
        continue
    path = os.path.join(ROOT, ".fixed", name)
    print(f"[{now()}] up {name}", flush=True)
    r = subprocess.run(
        ["gh", "release", "upload", REL, path, "--repo", REPO, "--clobber"],
        capture_output=True, text=True)
    if r.returncode == 0:
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(f"{now()} OK {name}\n")
        print(f"[{now()}] OK {name}", flush=True)
    else:
        print(f"[{now()}] FAIL {name}: {r.stderr[:180]}", flush=True)
        failed.append(name)
        time.sleep(8)
with open(LOG, "a", encoding="utf-8") as f:
    f.write("FIXUP_DONE" + ("" if not failed else " FAILS:" + ",".join(failed)) + "\n")
print("ALL_DONE_OR_FAILED", flush=True)
sys.exit(0 if not failed else 1)
