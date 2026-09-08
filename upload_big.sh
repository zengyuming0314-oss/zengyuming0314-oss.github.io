#!/bin/bash
# 大视频批量上传到 GitHub Releases（断点续传 + 日志）
cd "$(dirname "$0")"
REPO="zengyuming0314-oss/zengyuming0314-oss.github.io"
REL="portfolio-videos-02"
LOG="$PWD/.upload.log"
STAGE="$PWD/.upload"
MAN="$STAGE/manifest.json"

# 1. 确保 release 存在
gh release view "$REL" --repo "$REPO" >/dev/null 2>&1 || gh release create "$REL" --repo "$REPO" --title "作品视频" --notes "大视频素材" >>"$LOG" 2>&1

# 2. 生成待办清单（跳过已上传的资产）
gh release view "$REL" --repo "$REPO" --json assets --jq '.assets[].name' >"$STAGE/done.txt" 2>/dev/null
python3 - "$MAN" "$STAGE/done.txt" "$STAGE/todo.txt" <<'PY'
import json, sys, os
man = json.load(open(sys.argv[1], encoding='utf-8'))
done = set(open(sys.argv[2], encoding='utf-8').read().split())
stage_dir = os.path.dirname(sys.argv[1])
with open(sys.argv[3], 'w', encoding='utf-8') as f:
    for m in man:
        if m['ascii'] not in done:
            f.write(f"{m['ascii']}\t{os.path.join(stage_dir, m['ascii'])}\n")
PY

# 3. 逐个上传
CNT=0
while IFS=$'\t' read -r ascii link; do
  [ -z "$ascii" ] && continue
  CNT=$((CNT+1))
  echo "[$(date '+%H:%M:%S')] ($CNT) 上传 $ascii ..." >>"$LOG"
  if gh release upload "$REL" "$link" --repo "$REPO" --clobber >>"$LOG" 2>&1; then
    echo "[$(date '+%H:%M:%S')] OK $ascii" >>"$LOG"
  else
    echo "[$(date '+%H:%M:%S')] 重试 $ascii ..." >>"$LOG"
    sleep 8
    gh release upload "$REL" "$link" --repo "$REPO" --clobber >>"$LOG" 2>&1 \
      && echo "[$(date '+%H:%M:%S')] OK $ascii (retry)" >>"$LOG" \
      || echo "[$(date '+%H:%M:%S')] FAIL $ascii" >>"$LOG"
  fi
done < "$STAGE/todo.txt"
echo "[$(date '+%H:%M:%S')] ALL_DONE" >>"$LOG"
