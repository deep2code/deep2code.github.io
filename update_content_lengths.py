#!/usr/bin/env python3
"""更新 extracted_content.json 中所有页面的 content_length 字段"""

import json
from pathlib import Path

BASE_DIR = Path(__file__).parent
CONTENT_FILE = BASE_DIR / 'extracted_content.json'


def update_content_lengths():
    with open(CONTENT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    pages = data.get('pages', {})
    updated_count = 0

    for path, page_data in pages.items():
        if 'content' in page_data and page_data['content'] is not None:
            content_length = len(page_data['content'])
            old_length = page_data.get('content_length')
            page_data['content_length'] = content_length
            if old_length != content_length:
                print(f"  {path}: {old_length} -> {content_length}")
                updated_count += 1

    with open(CONTENT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n更新完成！共更新 {updated_count} 个页面的 content_length 字段")


if __name__ == '__main__':
    update_content_lengths()