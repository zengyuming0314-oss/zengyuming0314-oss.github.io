#!/bin/bash
# GitHub 登录（一次性）
echo "=============================================="
echo "  GitHub 登录"
echo "  1. 按提示选：GitHub.com → HTTPS → 回车确认"
echo "  2. 浏览器会自动打开授权页（用你的 Google 账号登录的那个 GitHub）"
echo "  3. 授权完成后回来看这里显示 ✓ Logged in"
echo "=============================================="
echo ""
gh auth login --hostname github.com --git-protocol https --web --skip-ssh-key
echo ""
echo "登录结果如上。按回车关闭窗口…"
read -r
