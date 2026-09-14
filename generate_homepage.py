#!/usr/bin/env python3
"""Generate a modern homepage and migrate original homepage content."""

import os
import re
import json
from pathlib import Path
from html import escape

BASE_DIR = Path(__file__).parent

# Import helper functions from generate_pages
import sys
sys.path.insert(0, str(BASE_DIR))
from generate_pages import (
    load_data, build_nav_tree, add_missing_nav_items,
    generate_nav_html, generate_html, clean_content, clean_title,
    build_breadcrumbs, generate_page_nav
)


# Category data for homepage cards
CATEGORIES = [
    {'url': '/golang/', 'title': 'Golang', 'desc': 'Go 语言基础、框架、泛型与实战'},
    {'url': '/python/', 'title': 'Python', 'desc': 'Python 语言与生态工具'},
    {'url': '/ai/', 'title': 'AI', 'desc': '人工智能、机器学习与 LLM'},
    {'url': '/redis/', 'title': 'Redis', 'desc': '内存数据库与消息队列'},
    {'url': '/mysql/', 'title': 'MySQL', 'desc': '关系型数据库与 SQL'},
    {'url': '/nginx/', 'title': 'Nginx', 'desc': 'Web 服务器与反向代理'},
    {'url': '/grpc/', 'title': 'gRPC', 'desc': '远程过程调用与 Protobuf'},
    {'url': '/elastic/', 'title': 'Elasticsearch', 'desc': '搜索引擎与数据分析'},
    {'url': '/memcached/', 'title': 'Memcached', 'desc': '内存缓存系统'},
    {'url': '/git/', 'title': 'Git', 'desc': '版本控制与代码管理'},
    {'url': '/flutter/', 'title': 'Flutter', 'desc': '跨平台移动应用开发'},
    {'url': '/mac/', 'title': 'macOS', 'desc': 'macOS 使用技巧与工具'},
    {'url': '/other/', 'title': '更多工具', 'desc': 'Docker、Vim、Rust、Shell 等'},
]


def generate_homepage_content():
    """Generate homepage HTML content with category cards."""
    cards_html = []
    for cat in CATEGORIES:
        cards_html.append(f'''<a href="{cat['url']}" class="category-card">
    <h3>{escape(cat['title'])}</h3>
    <p>{escape(cat['desc'])}</p>
    <span class="card-arrow">\u2192</span>
</a>''')

    cards = '\n'.join(cards_html)

    return f'''<div class="home-hero">
    <h1>deep2code</h1>
    <p class="subtitle">\u8d44\u6df1\u7a0b\u5e8f\u5458\u7684\u6280\u672f\u7b14\u8bb0\u4e0e\u601d\u8003</p>
    <p class="update-info">\u6db5\u76d6 Go \u3001Python \u3001Redis \u3001MySQL \u3001Nginx \u3001Docker \u7b49 13 \u4e2a\u6280\u672f\u9886\u57df \xb7 \u6301\u7eed\u66f4\u65b0\u4e2d</p>
</div>

<h2 class="home-section-title">\u6280\u672f\u5206\u7c7b</h2>
<div class="category-grid">
{cards}
</div>

<h2 class="home-section-title">\u5173\u4e8e</h2>
<p>\u8fd9\u662f\u4e00\u4e2a\u4e2a\u4eba\u6280\u672f\u535a\u5ba2\uff0c\u8bb0\u5f55\u4e86\u5728\u65e5\u5e38\u5f00\u53d1\u4e2d\u79ef\u7d2f\u7684\u6280\u672f\u7b14\u8bb0\u3001\u8e29\u5751\u7ecf\u9a8c\u548c\u601d\u8003\u603b\u7ed3\u3002\u5185\u5bb9\u6db5\u76d6\u591a\u4e2a\u6280\u672f\u9886\u57df\uff0c\u5305\u62ec\u7f16\u7a0b\u8bed\u8a00\u3001\u6570\u636e\u5b58\u50a8\u3001\u8fd0\u7ef4\u5de5\u5177\u3001\u5f00\u53d1\u5de5\u7a0b\u7b49\u3002</p>
<p>\u5982\u679c\u4f60\u5728\u5bfb\u627e\u7279\u5b9a\u6280\u672f\u5185\u5bb9\uff0c\u53ef\u4ee5\u4f7f\u7528\u5de6\u4fa7\u7684\u641c\u7d22\u529f\u80fd\uff0c\u6216\u8005\u6d4f\u89c8\u5404\u4e2a\u5206\u7c7b\u67e5\u770b\u76f8\u5173\u6587\u7ae0\u3002</p>

<h2 class="home-section-title">\u6700\u8fd1\u66f4\u65b0</h2>
<ul>
<li>2026 \u5e74 8 \u6708\uff1a\u535a\u5ba2\u6574\u4f53\u6539\u7248\u5347\u7ea7\uff0c\u91c7\u7528\u73b0\u4ee3\u5316\u54cd\u5e94\u5f0f\u8bbe\u8ba1\uff0c\u652f\u6301\u6697\u9ed1\u6a21\u5f0f</li>
<li>2026 \u5e74 8 \u6708\uff1a\u8865\u5145 AI/LLM \u3001Go \u6cdb\u578b\u3001Rust \u7b49\u6280\u672f\u5185\u5bb9</li>
<li>\u539f\u6709\u5185\u5bb9\u6301\u7eed\u6574\u7406\u4e2d\uff0c\u4ee3\u7801\u5757\u5168\u90e8\u4f7f\u7528 highlight.js \u91cd\u65b0\u9ad8\u4eae</li>
</ul>'''


def generate_homepage(nav_tree, nav_html):
    """Generate the homepage HTML."""
    content = generate_homepage_content()

    return f'''<!DOCTYPE html>
<html lang="zh" data-theme="light">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="deep2code \u6280\u672f\u535a\u5ba2 - \u8d44\u6df1\u7a0b\u5e8f\u5458\u7684\u6280\u672f\u7b14\u8bb0\u4e0e\u601d\u8003">
    <meta name="author" content="deep2code">
    <link rel="icon" href="/images/favicon.jpeg" type="image/jpeg">
    <title>\u6280\u672f\u535a\u5ba2 :: deep2code</title>
    <link rel="stylesheet" href="/css/style.css?v=20260825">
</head>
<body>
    <nav id="sidebar">
        <div class="sidebar-header">
            <img src="/images/logo.jpeg" alt="logo">
            <a href="/" class="blog-title">deep2code</a>
        </div>
        <div class="searchbox">
            <svg class="search-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
            <input type="search" id="search-input" placeholder="\u641c\u7d22...">
            <div class="search-results" id="search-results"></div>
        </div>
        <div class="nav-section">
            <ul>
{nav_html}
            </ul>
        </div>
    </nav>

    <div class="sidebar-overlay"></div>

    <div id="main-area">
        <div class="top-bar">
            <button class="menu-toggle" onclick="document.getElementById('sidebar').classList.add('open');document.querySelector('.sidebar-overlay').classList.add('active');">\u2630</button>
            <span class="top-title">\u6280\u672f\u535a\u5ba2</span>
        </div>

        <button class="theme-toggle" title="\u5207\u6362\u4e3b\u9898">
            <span class="icon-moon">\U0001f319</span>
            <span class="icon-sun">\u2600\ufe0f</span>
        </button>

        <div id="content-wrapper">
            <div id="body-content">
                {content}
            </div>
        </div>

        <footer class="site-footer">
            <p>deep2code \u6280\u672f\u535a\u5ba2 \xb7 <a href="https://github.com/deep2code">GitHub</a> \xb7 \u66f4\u65b0\u4e8e 2026 \u5e74</p>
        </footer>
    </div>

    <button class="back-to-top" title="\u56de\u5230\u9876\u90e8" style="display:none;position:fixed;bottom:2rem;right:2rem;z-index:90;width:40px;height:40px;border-radius:50%;border:1px solid var(--border-color);background:var(--bg-primary);color:var(--text-secondary);cursor:pointer;font-size:1.2rem;box-shadow:var(--shadow);align-items:center;justify-content:center;">\u2191</button>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
    <script>
    window.addEventListener('load', function() {{
        if (window.hljs) {{
            document.querySelectorAll('#body-content pre code').forEach(function(block) {{
                try {{ window.hljs.highlightElement(block); }} catch(e) {{}}
            }});
        }}
    }});
    </script>
    <script type="module">
    import mermaid from "https://cdnjs.cloudflare.com/ajax/libs/mermaid/10.9.0/mermaid.esm.min.mjs";
    window.mermaid = mermaid;
    mermaid.initialize({{ startOnLoad: false, theme: document.documentElement.getAttribute('data-theme') === 'dark' ? 'dark' : 'default', securityLevel: 'loose' }});
    mermaid.run({{ querySelector: '.mermaid' }});
    </script>
    <script src="/js/main.js?v=20260825"></script>
</body>
</html>'''


def migrate_original_homepage(data, nav_tree, nav_html, flat_nav):
    """Migrate original homepage content to /other/self-hosted/."""
    original_content = data['pages']['/'].get('content', '')
    original_content = clean_content(original_content)

    # Remove the sidebar-toggle span
    original_content = re.sub(r'<span id="sidebar-toggle-span">.*?</span>', '', original_content, flags=re.DOTALL)

    # Create page data
    page_data = {
        'title': '\u5efa\u7acb\u81ea\u5df1\u7684\u4ee3\u7801\u6258\u7ba1\u5e73\u53f0',
        'content': original_content,
    }

    # Generate breadcrumbs
    from generate_pages import build_breadcrumbs, generate_page_nav
    current_path = '/other/self-hosted/'
    breadcrumbs_html = build_breadcrumbs(current_path, flat_nav)
    page_nav_html = generate_page_nav(current_path, flat_nav)

    html = generate_html(page_data, nav_html, breadcrumbs_html, page_nav_html, current_path)

    # Write to file
    output_dir = BASE_DIR / 'other' / 'self-hosted'
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / 'index.html'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"  Migrated original homepage to /other/self-hosted/ ({len(original_content)} chars)")


def main():
    print("Loading data...")
    data = load_data()
    nav_items = data['navigation']

    print("Building navigation tree...")
    nav_tree = build_nav_tree(nav_items)
    add_missing_nav_items(nav_tree, data['pages'])

    # Flatten nav
    flat_nav = []
    for item in nav_tree:
        flat_nav.append(item)
        for child in item.get('children', []):
            flat_nav.append(child)

    # Add self-hosted to other's children
    other_item = None
    for item in nav_tree:
        if item['nav_id'] == '/other/':
            other_item = item
            break
    if other_item:
        # Check if already has self-hosted
        has_self_hosted = any(c['nav_id'] == '/other/self-hosted/' for c in other_item.get('children', []))
        if not has_self_hosted:
            other_item['children'].append({
                'nav_id': '/other/self-hosted/',
                'title': '\u4ee3\u7801\u6258\u7ba1',
                'href': '/other/self-hosted/',
                'text': '\u4ee3\u7801\u6258\u7ba1',
                'children': [],
                'depth': 2,
            })
            flat_nav.append(other_item['children'][-1])

    # Generate nav HTML for homepage
    nav_html = generate_nav_html(nav_tree, '/')

    # Migrate original homepage content
    print("Migrating original homepage content...")
    migrate_original_homepage(data, nav_tree, nav_html, flat_nav)

    # Generate new homepage
    print("Generating new homepage...")
    html = generate_homepage(nav_tree, nav_html)
    output_file = BASE_DIR / 'index.html'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"  Homepage generated: {len(html)} chars")

    # Re-generate all pages with updated nav (includes self-hosted)
    print("\nRe-generating all pages with updated navigation...")
    pages = data['pages']
    success = 0
    for url_path, page_data in pages.items():
        if url_path == '/':
            continue  # Skip homepage, already generated above
        try:
            current_path = url_path
            nav_html_page = generate_nav_html(nav_tree, current_path)
            breadcrumbs_html = build_breadcrumbs(current_path, flat_nav)
            page_nav_html = generate_page_nav(current_path, flat_nav)
            html = generate_html(page_data, nav_html_page, breadcrumbs_html, page_nav_html, current_path)
            filepath = Path(page_data['filepath'])
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html)
            success += 1
        except Exception as e:
            print(f"  ERR {url_path}: {e}")

    # Also generate the self-hosted page
    print(f"\n  Re-generated {success} pages")
    print("\nDone!")


if __name__ == '__main__':
    main()
