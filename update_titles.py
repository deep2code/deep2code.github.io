#!/usr/bin/env python3
"""更新页面标题"""

import json
import re
from pathlib import Path

BASE_DIR = Path(__file__).parent
CONTENT_FILE = BASE_DIR / 'extracted_content.json'


def update_titles():
    with open(CONTENT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    pages = data['pages']

    # 更新的标题映射
    title_updates = {
        '/other/tencent/': '腾讯云与微信公众号',
        '/ai/__index/': 'Fine-tuning 深度学习微调',
        '/other/opensource/': '开源软件推荐',
        '/other/search/': '搜索技巧与 SEO',
        '/other/wasm/': 'WebAssembly',
    }

    for url_path, new_title in title_updates.items():
        if url_path in pages:
            old_title = pages[url_path].get('title', '')
            pages[url_path]['title'] = new_title
            print(f"Updated {url_path}: '{old_title}' -> '{new_title}'")

    with open(CONTENT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n标题更新完成！共更新 {len(title_updates)} 个页面")


if __name__ == '__main__':
    update_titles()