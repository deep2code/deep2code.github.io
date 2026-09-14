#!/usr/bin/env bash
set -euo pipefail

# pack.sh - 将博客打包为纯静态文件目录，用于部署到其他机器
#
# 用法:
#   ./pack.sh              # 重建 + 打包到 ./dist
#   ./pack.sh --no-build   # 跳过重建，直接打包当前文件
#   ./pack.sh --output DIR # 自定义输出目录

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BUILD=1
OUTPUT_DIR="${SCRIPT_DIR}/dist"

while [[ $# -gt 0 ]]; do
    case "$1" in
        --no-build)  BUILD=0; shift ;;
        --output)    OUTPUT_DIR="$2"; shift 2 ;;
        -h|--help)
            echo "用法: ./pack.sh [--no-build] [--output DIR]"
            echo "  --no-build   跳过 generate_pages.py 重建"
            echo "  --output DIR 自定义输出目录 (默认 ./dist)"
            exit 0 ;;
        *) echo "未知参数: $1"; exit 1 ;;
    esac
done

cd "$SCRIPT_DIR"

if [[ $BUILD -eq 1 ]]; then
    echo ">> 重建站点..."
    python3 generate_pages.py
    echo ""
fi

echo ">> 清理旧输出目录..."
rm -rf "$OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR"

echo ">> 复制运行时文件..."
rsync -a \
    --exclude='.git/' \
    --exclude='__pycache__/' \
    --exclude='.tmp/' \
    --exclude='.dumate/' \
    --exclude='_drafts/' \
    --exclude='_mtest/' \
    --exclude='dist/' \
    --exclude='*.pyc' \
    --exclude='.DS_Store' \
    --exclude='generate_pages.py' \
    --exclude='generate_homepage.py' \
    --exclude='extract_content.py' \
    --exclude='update_content.py' \
    --exclude='update_all_content.py' \
    --exclude='extracted_content.json' \
    --exclude='.gitignore' \
    --exclude='README.md' \
    --exclude='LICENSE' \
    --exclude='pack.sh' \
    ./ "$OUTPUT_DIR/"

HTML_COUNT=$(find "$OUTPUT_DIR" -name '*.html' | wc -l | tr -d ' ')
IMG_COUNT=$(find "$OUTPUT_DIR" \( -name '*.webp' -o -name '*.jpg' -o -name '*.jpeg' -o -name '*.png' -o -name '*.svg' \) | wc -l | tr -d ' ')
XML_COUNT=$(find "$OUTPUT_DIR" -name '*.xml' | wc -l | tr -d ' ')
TOTAL_FILES=$(find "$OUTPUT_DIR" -type f | wc -l | tr -d ' ')
TOTAL_SIZE=$(du -sh "$OUTPUT_DIR" | cut -f1)

echo ""
echo ">> 打包完成"
echo "   HTML 页面:  $HTML_COUNT"
echo "   图片资源:  $IMG_COUNT"
echo "   RSS feeds: $XML_COUNT"
echo "   总文件数:  $TOTAL_FILES"
echo "   总体积:    $TOTAL_SIZE"
echo "   输出目录:  $OUTPUT_DIR"
echo ""
echo ">> 部署方法:"
echo "   rsync -avz $OUTPUT_DIR/ user@server:/var/www/blog/"
echo "   # 或: scp -r $OUTPUT_DIR user@server:/var/www/blog"
