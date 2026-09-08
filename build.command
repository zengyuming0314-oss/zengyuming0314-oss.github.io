#!/bin/bash
# 双击我：重新扫描 works/ 文件夹并生成作品列表
cd "$(dirname "$0")"
python3 build.py
echo ""
echo "刷新网页即可看到新作品。按回车关闭…"
read -r
