#!/usr/bin/env python3
"""Generate modern HTML pages from extracted content."""

import os
import re
import json
from pathlib import Path
from html import escape

BASE_DIR = Path(__file__).parent


def load_data():
    """Load extracted content."""
    with open(BASE_DIR / 'extracted_content.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return _normalize_paths(data)


# ============================================================
# URL and title normalization (applied at load time)
# ============================================================

URL_MAP = {
    '/ai/__index/': '/ai/finetuning/',  # Hugo 产物残留路径，重命名为可读路径
}

NAV_TITLE_MAP = {
    '/ai/': 'AI',
    '/ai/finetuning/': 'Fine-tuning 微调',
    '/elastic/': 'Elasticsearch',
    '/flutter/': 'Flutter',
    '/git/': 'Git',
    '/golang/': 'Golang',
    '/golang/regexp/': 'regexp 包',
    '/grpc/': 'gRPC',
    '/mac/': 'macOS',
    '/memcached/': 'Memcached',
    '/mysql/': 'MySQL',
    '/nginx/': 'Nginx',
    '/other/mermaid/': 'Mermaid',
    '/python/': 'Python',
    '/redis/': 'Redis',
    '/categories/': '分类',
    '/tags/': '标签',
}

# ============================================================
# Semantic content groups (display-layer information architecture)
# ============================================================
# Keys are URL paths from pages dict. URLs stay unchanged; only the
# homepage / related-navigation grouping is driven by this table.
CONTENT_GROUPS = [
    {
        'id': 'golang',
        'title': 'Go 语言',
        'nav_text': 'Go',
        'blurb': '主力语言：标准库、Web 框架、并发与工具链',
        'pages': [
            '/golang/',
            '/golang/stringer/',
            '/golang/echo/',
            '/golang/context/',
            '/golang/regexp/',
            '/golang/sort/',
            '/golang/freetype/',
            '/golang/iris/',
            '/golang/shell/',
            '/golang/io/',
            '/golang/code/',
            '/golang/groupby/',
            '/golang/log/',
            '/golang/generic/',
            '/golang/gin/',
            '/golang/package/',
            '/golang/go-git/',
            '/golang/generics-update/',
        ],
    },
    {
        'id': 'database',
        'title': '数据库与缓存',
        'nav_text': 'DB',
        'blurb': 'MySQL · Redis · Memcached · Elasticsearch',
        'pages': ['/mysql/', '/redis/', '/memcached/', '/elastic/'],
    },
    {
        'id': 'ai',
        'title': 'AI 与机器学习',
        'nav_text': 'AI',
        'blurb': 'LLM · RAG · 微调 · 机器学习',
        'pages': ['/ai/', '/ai/llm/', '/ai/rag/', '/ai/finetuning/', '/other/machinelearn/'],
    },
    {
        'id': 'middleware',
        'title': '中间件与服务端',
        'nav_text': '中间件',
        'blurb': 'Nginx · gRPC · RPC',
        'pages': ['/nginx/', '/nginx/install/', '/nginx/use/', '/nginx/http/', '/nginx/rtmp/',
                  '/grpc/', '/grpc/golang/', '/other/rpc/'],
    },
    {
        'id': 'cloud',
        'title': '云与 DevOps',
        'nav_text': '云·DevOps',
        'blurb': 'Docker · Harbor · 阿里云 · 腾讯云 · 开源运维',
        'pages': ['/other/docker/', '/other/harbor/', '/other/aliyun/', '/other/tencent/',
                  '/other/self-hosted/', '/other/brew/'],
    },
    {
        'id': 'lang',
        'title': '编程语言',
        'nav_text': '语言',
        'blurb': 'Python · Rust · Shell · WebAssembly · Flutter',
        'pages': ['/python/', '/other/rust/', '/other/shell/', '/other/wasm/', '/flutter/'],
    },
    {
        'id': 'tools',
        'title': '开发工具与效率',
        'nav_text': '工具',
        'blurb': 'Git · GitHub · Vim · Hugo · Mermaid · Markdown 等',
        'pages': ['/git/', '/other/github/', '/other/gitlab/', '/other/svn/', '/other/opensource/',
                  '/other/vim/', '/other/hugo/', '/other/mermaid/', '/other/markdown/',
                  '/other/makefile/', '/other/search/', '/other/geocode/', '/other/tesseract/'],
    },
    {
        'id': 'system',
        'title': '系统与网络',
        'nav_text': '系统',
        'blurb': 'macOS · Windows · Wireshark · Web · Firefox',
        'pages': ['/mac/', '/other/windows/', '/other/wireshark/', '/other/web/', '/other/firefox/'],
    },
    {
        'id': 'game',
        'title': '图形与游戏',
        'nav_text': '游戏',
        'blurb': 'Unity · ET 框架',
        'pages': ['/other/unity/', '/other/unity/et/'],
    },
    {
        'id': 'misc',
        'title': '其他',
        'nav_text': '更多',
        'blurb': '零散主题合集',
        'pages': ['/other/'],
    },
]

CONTENT_GROUP_BY_URL = {}
for _g in CONTENT_GROUPS:
    for _u in _g['pages']:
        CONTENT_GROUP_BY_URL[_u] = _g

# Group ordering used for in-group prev/next navigation
GROUP_ARTICLE_ORDER = [u for g in CONTENT_GROUPS for u in g['pages']]


def _normalize_paths(data):
    """Rewrite moved URLs in page keys, filepaths, contents and nav."""
    pages = data['pages']

    # 1. Rewrite content references to moved URLs
    for url in list(pages):
        c = pages[url].get('content', '')
        for old, new in URL_MAP.items():
            c = c.replace('"' + old + '"', '"' + new + '"')
        pages[url]['content'] = c

    # 2. Move page keys and filepaths
    for old, new in URL_MAP.items():
        if old in pages:
            p = pages.pop(old)
            fp = p.get('filepath', '')
            if fp:
                p['filepath'] = fp.replace(old.strip('/'), new.strip('/'))
            pages[new] = p

    # 3. Normalize navigation titles and ids (apply after URL moves so
    #    renames like /ai/__index/ -> /ai/finetuning/ hit the title map)
    for item in data['navigation']:
        nid = item.get('nav_id', '')
        for old, new in URL_MAP.items():
            if nid == old:
                item['nav_id'] = new
                item['href'] = new
                nid = new
        if nid in NAV_TITLE_MAP:
            t = NAV_TITLE_MAP[nid]
            item['title'] = t
            item['text'] = t

    # 4. Clean page titles (share the nav map plus known typos)
    for url, p in pages.items():
        t = p.get('title')
        if t:
            if url in NAV_TITLE_MAP:
                p['title'] = NAV_TITLE_MAP[url]
            else:
                t2 = t.replace('exgexp包', 'regexp 包')
                if t2 != t:
                    p['title'] = t2

    return data


def _strip_relearn_residue(content):
    """Remove Hugo Relearn theme artifacts left in extracted page bodies.

    Page extraction captured theme chrome at the end of most articles: the
    footline footer, the old in-article prev/next <div id="navigation">
    block, orphaned </section> closers, fa restart icons and a
    scrollbar-detection div. These are redundant now (we ship our own
    page-nav and footer), and their unbalanced divs break the layout.
    """
    # footline footer (theme artifact)
    content = re.sub(
        r'\n?\s*<footer class="\s*footline"\s*>\s*.*?</footer>',
        '\n', content, flags=re.DOTALL)
    # old in-article prev/next navigation block
    content = re.sub(
        r'\n?\s*<div id="navigation">.*?</div>',
        '\n', content, flags=re.DOTALL)
    # leftover fa restart / chevron icons inside those blocks
    content = re.sub(r'\s*<i class="fa fa-chevron[^"]*">\s*</i>', '', content)
    # scrollbar-detection div (opening tag only; never closed in source)
    content = re.sub(
        r'\n?\s*<div\s*[\n\s]*style="left: -1000px; overflow: scroll;[^"]*">',
        '\n', content, flags=re.DOTALL)
    # Note: orphaned </section> closers are balanced later in clean_content()
    # (count-aware), so legitimate sections are preserved.
    return content


def clean_content(content):
    """Remove old script tags, HTML residue, and detection elements."""
    # Strip Hugo Relearn theme chrome first so div balancing below works
    content = _strip_relearn_residue(content)
    # Remove script tags and their content
    content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL)
    # Remove link tags
    content = re.sub(r'<link[^>]*/?\s*>', '', content)
    # Remove style tags
    content = re.sub(r'<style[^>]*>.*?</style>', '', content, flags=re.DOTALL)
    # Remove detection divs (Hugo Relearn theme artifacts)
    content = re.sub(r'<div style="border:\s*none[^"]*">.*?</div>', '', content, flags=re.DOTALL)
    # Remove </body> and </html>
    content = content.replace('</body>', '').replace('</html>', '')
    # Remove trailing empty div tags
    content = re.sub(r'(\s*<div>\s*</div>\s*)+$', '', content)
    # Remove trailing whitespace-only lines
    content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)

    # Remove Hugo sidebar-toggle artifact (leftover from the Relearn theme)
    content = re.sub(r'<span id="sidebar-toggle-span">.*?</span>', '', content, flags=re.DOTALL)

    # Convert Pygments highlight divs (Hugo theme artifacts) to clean pre/code.
    # Tolerance for truncated blocks: match up to </pre> and optional closing div.
    content = re.sub(r'<div class="highlight">.*?</pre>(?:</div>)?', _convert_pygments, content, flags=re.DOTALL)

    # Fix protocol-less github.com links (become relative links otherwise)
    content = re.sub(r'href="github\.com/', 'href="https://github.com/', content)
    # Fix typo: hhttps://
    content = content.replace('hhttps://', 'https://')

    # Fix relative image paths: /golang/code/ refers to files one level up
    content = content.replace('src="golang_redis.webp"', 'src="../golang_redis.webp"')
    content = content.replace('src="golang_trace.webp"', 'src="../golang_trace.webp"')
    # Fix missing extension: aliyun_ecs_ipv6.web -> .webp
    content = content.replace('src="aliyun_ecs_ipv6.web"', 'src="aliyun_ecs_ipv6.webp"')

    # Remove dangling link to non-existent /ai/agent/ page
    content = re.sub(r'<li><a href="/ai/agent/">.*?</a>.*?</li>', '', content, flags=re.DOTALL)
    # nginx home: "http模块" should point to the existing /nginx/http/ page
    content = content.replace('href="module/"', 'href="/nginx/http/"')

    # Repair a mangled link whose href was accidentally set to link text
    content = content.replace(
        'href="%E5%8F%AF%E8%A7%86%E5%8C%96%E7%89%88pipeline%EF%BC%8C%E5%80%BC%E5%BE%97%E5%AE%89%E8%A3%85"',
        'href="https://www.jenkins.io/projects/blueocean/"')

    # Housekeeping images live at the site root; use absolute paths so they
    # resolve from nested pages like /other/self-hosted/
    for img, root_img in [
        ('darkreader.webp', '/darkreader.webp'),
        ('mac_display_deep.webp', '/mac_display_deep.webp'),
        ('blog_qr.webp', '/blog_qr.webp'),
        ('workwiki_qr.webp', '/workwiki_qr.webp'),
        ('official_qr.jpg', '/official_qr.jpg'),
    ]:
        content = content.replace(f'src="{img}"', f'src="{root_img}"')

    # Rebalance stray closing divs left by truncated page extraction
    open_cnt = len(re.findall(r'<div[ >]', content))
    close_cnt = len(re.findall(r'</div>', content))
    if close_cnt > open_cnt:
        for _ in range(close_cnt - open_cnt):
            idx = content.rfind('</div>')
            if idx == -1:
                break
            content = content[:idx] + content[idx + 6:]
    elif open_cnt > close_cnt:
        content += '</div>' * (open_cnt - close_cnt)

    # Rebalance </section> closers: extraction sometimes dropped the
    # opening <section> tag, leaving orphaned closers. Only remove the
    # excess closers so legitimate <section> blocks survive (our homepage
    # archive groups rely on them).
    sec_open = len(re.findall(r'<section\b', content))
    sec_close = len(re.findall(r'</section>', content))
    if sec_close > sec_open:
        for _ in range(sec_close - sec_open):
            idx = content.rfind('</section>')
            if idx == -1:
                break
            content = content[:idx] + content[idx + 10:]

    # Strip
    content = content.strip()
    return content


def _convert_pygments(match):
    """Convert a Hugo/Pygments highlight div into a clean pre/code block.

    Strips inline color spans so highlighting is handled by our own
    highlight.js CSS instead of Pygments' hard-coded light theme.
    """
    block = match.group(0)
    code = re.search(r'<code[^>]*>(.*?)</code>', block, re.DOTALL)
    if not code:
        return ''
    # Remove all inline span wrappers (Pygments tokens, line-flex divs)
    body = re.sub(r'</?span[^>]*>', '', code.group(1))
    # Extract language hint
    lang = ''
    attrs = re.search(r'<code([^>]*)>', code.group(0))
    if attrs:
        a = attrs.group(1)
        m = re.search(r'language-([a-zA-Z0-9_+-]+)', a)
        if not m:
            m = re.search(r'data-lang="([^"]+)"', a)
        if m:
            lang = m.group(1)
    cls = f' class="language-{lang}"' if lang else ''
    return f'<pre><code{cls}>{body}</code></pre>'


def clean_title(title, url_path):
    """Clean up page title and provide fallback."""
    if title:
        # Remove "category ::" or "tag ::" prefixes
        title = re.sub(r'^(category|tag)\s*::\s*', '', title, flags=re.IGNORECASE)
        # Clean up whitespace and newlines
        title = ' '.join(title.split())
    
    if not title:
        # Fallback: use URL path
        parts = [p for p in url_path.strip('/').split('/') if p]
        if parts:
            title = parts[-1]
        else:
            title = '\u6280\u672f\u535a\u5ba2'
    
    return title


def rel_prefix(url_path):
    """Relative path prefix from the site root to this page's directory.

    '/' -> '', '/golang/' -> '../', '/golang/context/' -> '../../'.
    Lets every page reference css/js/images and internal links with
    relative paths, so pages render correctly both when opened directly
    from the filesystem (file://) and when deployed at a domain root.
    """
    depth = len([p for p in url_path.strip('/').split('/') if p])
    return '../' * depth


def _rewrite_ref(match, prefix):
    """Rewrite one site-root-absolute href=/src= reference."""
    attr, value = match.group(1), match.group(2)
    frag = ''
    if '#' in value:
        value, frag = value.split('#', 1)
        frag = '#' + frag
    # Directory-style internal page links ("/xxx/" or "/xxx/#frag") need
    # index.html appended so they resolve under the file:// protocol instead
    # of showing a raw directory index. Real-file references keep their name.
    last_seg = value.rstrip('/').rsplit('/', 1)[-1]
    if value.endswith('/') and '.' not in last_seg:
        value += 'index.html'
    return f'{attr}="{prefix}{value}{frag}"'


def relativize_static_refs(html, prefix):
    """Rewrite site-root-absolute href=/src= references to be relative.

    href="/" becomes "{prefix}index.html", every other "/xxx" gets the
    prefix prepended (protocol-relative "//cdn..." URLs are left alone).
    Directory-style page links ("/xxx/") additionally get "index.html"
    appended, so every internal link resolves both when the site is
    deployed at a domain root and when opened directly as file://.
    """
    html = html.replace('href="/"', f'href="{prefix}index.html"')
    html = re.sub(
        r'(href|src)="/(?!/)([^"]*?)"',
        lambda m: _rewrite_ref(m, prefix),
        html)
    return html


def build_nav_tree(nav_items):
    """Build a tree from flat nav items based on URL path depth."""
    tree = []
    by_path = {}

    for item in nav_items:
        path = item['nav_id']  # e.g., /golang/context/
        parts = [p for p in path.strip('/').split('/') if p]
        depth = len(parts)
        item['children'] = []
        item['depth'] = depth
        by_path[path] = item

        if depth == 1:
            tree.append(item)
        else:
            parent_path = '/' + '/'.join(parts[:-1]) + '/'
            parent = by_path.get(parent_path)
            if parent:
                parent['children'].append(item)
            else:
                tree.append(item)

    return tree


def add_missing_nav_items(nav_tree, all_pages):
    """Add pages that exist but are not in the navigation.

    Missing pages are attached to their closest existing ancestor item so the
    sidebar stays complete even when content is added without touching the
    navigation data. Root-level orphans are appended to the tree directly.
    """
    existing_paths = set()
    by_path = {}

    def collect(items):
        for item in items:
            existing_paths.add(item['nav_id'])
            by_path[item['nav_id']] = item
            collect(item.get('children', []))

    collect(nav_tree)

    missing = []
    for url, page in all_pages.items():
        if url in ('/', '/categories/', '/tags/') or url in existing_paths:
            continue
        parts = [p for p in url.strip('/').split('/') if p]
        parent_path = None
        for i in range(len(parts) - 1, 0, -1):
            cand = '/' + '/'.join(parts[:i]) + '/'
            if cand in by_path:
                parent_path = cand
                break
        title = page.get('title', url.strip('/'))
        missing.append({
            'nav_id': url,
            'title': title,
            'href': url,
            'text': title,
            'children': [],
            'depth': len(parts),
            '_parent': parent_path,
        })

    for item in missing:
        parent = item.pop('_parent')
        if parent and parent in by_path:
            by_path[parent]['children'].append(item)
        else:
            nav_tree.append(item)


def generate_nav_html(nav_tree, current_path, level=0):
    """Legacy sidebar navigation HTML (kept for reference, unused by pages)."""
    return ''


def page_href(url_path):
    """Directory-style site URL -> file://-friendly href with index.html.

    Browsers never auto-resolve 'index.html' for file:// directories, so a
    link to /elastic/ would open the raw directory listing. Appending
    index.html keeps every internal link working both when the site is
    served at a domain root (where /elastic/index.html is equivalent) and
    when pages are opened directly from disk.
    """
    if not url_path or url_path == '/':
        return '/'
    return url_path.rstrip('/') + '/index.html'


def build_breadcrumbs(url_path, nav_items):
    """Build breadcrumb navigation."""
    if url_path == '/':
        return ''

    breadcrumbs = [{'url': '/', 'text': '\u4e3b\u9875'}]
    parts = [p for p in url_path.strip('/').split('/') if p]

    nav_by_path = {item['nav_id']: item for item in nav_items}

    current_path = ''
    for part in parts:
        current_path += '/' + part + '/'
        item = nav_by_path.get(current_path)
        if item:
            breadcrumbs.append({'url': item['href'], 'text': item['text']})
        else:
            breadcrumbs.append({'url': current_path, 'text': part})

    html_parts = ['<div class="breadcrumbs">']
    for i, crumb in enumerate(breadcrumbs):
        if i > 0:
            html_parts.append('<span class="separator">/</span>')
        if i == len(breadcrumbs) - 1:
            html_parts.append(f'<span>{escape(crumb["text"])}</span>')
        else:
            html_parts.append(f'<a href="{page_href(crumb["url"])}">{escape(crumb["text"])}</a>')
    html_parts.append('</div>')

    return '\n'.join(html_parts)


def build_group_meta(pages_by_url):
    """Resolve group titles for every known URL (for breadcrumbs/related)."""
    return {}


def build_homepage_content(pages):
    """Build the content-first homepage: terminal hero + stat strip +
    every semantic group presented as a card grid.

    Links use site-root-absolute paths (e.g. /golang/context/); the page
    template later rewrites them to relative paths via relativize_static_refs,
    so the result works both under a domain root and opened as file://.
    """

    def title_of(u):
        if u in pages and pages[u].get('title'):
            return clean_title(pages[u].get('title', ''), u)
        return u.strip('/')

    # Index-only pages are not articles; count real posts for honest stats.
    article_count = sum(1 for u in pages if u not in ('/', '/categories/', '/tags/'))
    topic_names = ' '.join(g['nav_text'] for g in CONTENT_GROUPS)

    groups = []
    for idx, g in enumerate(CONTENT_GROUPS, start=1):
        articles = ''.join(
            f'<li class="arch-item">'
            f'<a class="arch-link" href="{page_href(u)}">'
            f'<span class="arch-title">{escape(title_of(u))}</span>'
            f'<span class="arch-arrow">\u2192</span></a></li>'
            for u in g['pages'] if u in pages)
        if not articles:
            continue
        groups.append(
            f'<section class="arch-card" id="arch-{g["id"]}">'
            f'<header class="arch-card-head">'
            f'<span class="group-idx">{idx:02d}</span>'
            f'<div class="arch-card-titles">'
            f'<h2 class="group-name">{escape(g["title"])}</h2>'
            f'<p class="group-blurb">{escape(g["blurb"])}</p>'
            f'</div>'
            f'<span class="group-meta">{len(g["pages"])} \u7bc7</span>'
            f'</header>'
            f'<ul class="arch-list">{articles}</ul>'
            f'</section>')
    grid = '\n'.join(groups)

    return (
        f'<div class="hero-section">'
        f'<div class="hero-inner">'
        f'<div class="hero-copy">'
        f'<h1 class="hero-title">\u6280\u672f\u535a\u5ba2\uff0c'
        f'\u4e00\u7bc7\u7bc7\u8e29\u5751\u4e0e\u5b9e\u8df5\u3002</h1>'
        f'<p class="hero-desc">\u4ece Go\u3001Python \u5230\u4e91\u539f\u751f\u4e0e AI\u3001\u4ece'
        f'\u6570\u636e\u5e93\u5230\u5f00\u53d1\u5de5\u5177\uff1a'
        f'\u5168\u90e8\u7b14\u8bb0\u6309\u8bed\u4e49\u5206\u7ec4\uff0c'
        f'\u591a\u6570\u7bc7\u7ae0\u9644\u4ee3\u7801\u4e0e\u56fe\u8868\uff0c'
        f'\u53ef\u4ee5\u4f7f\u7528\u9876\u90e8\u641c\u7d22\u76f4\u8fbe\u5185\u5bb9\u3002</p>'
        f'</div>'
        f'<div class="terminal-card" role="img" aria-label="\u7ec8\u7aef\u98ce\u683c\u7684\u535a\u5ba2\u4ecb\u7ecd">'
        f'<div class="terminal-bar">'
        f'<span class="term-dot dot-red"></span><span class="term-dot dot-yellow"></span>'
        f'<span class="term-dot dot-green"></span><span class="term-title">zsh \u2014 \u8d44\u6df1\u7801\u519c</span>'
        f'</div>'
f'<div class="terminal-body">'
        f'<div class="term-line"><span class="term-prompt">~$</span> echo "hello, world"</div>'
        f'<div class="term-line term-out">\u8d44\u6df1\u7801\u519c \u2014 \u6280\u672f\u535a\u5ba2 dev notes</div>'
        f'<div class="term-line"><span class="term-prompt">~$</span> ls topics</div>'
        f'<div class="term-line term-out">{escape(topic_names)}</div>'
        f'<div class="term-line"><span class="term-prompt">~$</span> ./reading_notes.sh</div>'
        f'<div class="term-line term-out-go">\u5df2\u6574\u7406 {article_count} \u7bc7\u7b14\u8bb0 \u2191</div>'
        f'<div class="term-line term-cursor"><span class="term-prompt">~$</span> <span class="cursor-block"></span></div>'
        f'</div>'
        f'</div>'
        f'</div>'
        f'</div>'
        f'<div class="group-grid">{grid}</div>'
    )


def find_group_prev_next(url_path):
    """Find previous and next pages within the current semantic group."""
    group = CONTENT_GROUP_BY_URL.get(url_path)
    if not group:
        return None, None
    ordered = group['pages']
    idx = ordered.index(url_path) if url_path in ordered else -1
    if idx < 0:
        return None, None
    prev = ordered[idx - 1] if idx > 0 else None
    nxt = ordered[idx + 1] if idx < len(ordered) - 1 else None
    return prev, nxt


def generate_page_nav(url_path, pages):
    """Generate previous/next page navigation within the semantic group."""
    if url_path == '/':
        return ''

    prev, next_item = find_group_prev_next(url_path)

    def title_of(u):
        if u in pages and pages[u].get('title'):
            return clean_title(pages[u].get('title', ''), u)
        return u.strip('/')

    html_parts = ['<div class="page-nav">']

    if prev:
        html_parts.append(
            f'<a class="nav-prev" href="{page_href(prev)}">'
            f'<span class="nav-label">\u2190 \u4e0a\u4e00\u7bc7</span>'
            f'<span class="nav-title">{escape(title_of(prev))}</span></a>'
        )
    else:
        html_parts.append('<span></span>')

    if next_item:
        html_parts.append(
            f'<a class="nav-next" href="{page_href(next_item)}">'
            f'<span class="nav-label">\u4e0b\u4e00\u7bc7 \u2192</span>'
            f'<span class="nav-title">{escape(title_of(next_item))}</span></a>'
        )

    html_parts.append('</div>')
    return '\n'.join(html_parts)


def generate_related_html(url_path, pages):
    """List other posts of the same semantic group in a sticky side card."""
    group = CONTENT_GROUP_BY_URL.get(url_path)
    if not group:
        return ''
    others = [u for u in group['pages'] if u != url_path]
    if not others:
        return ''

    def title_of(u):
        if u in pages and pages[u].get('title'):
            return clean_title(pages[u].get('title', ''), u)
        return u.strip('/')

    items = ''.join(
        f'<li><a class="side-post" href="{page_href(u)}">{escape(title_of(u))}</a></li>'
        for u in others)
    return (
        f'<aside class="related-card">'
        f'<h2 class="related-title">\u540c\u7ec4 \xb7 {escape(group["title"])}</h2>'
        f'<ul class="related-list">{items}</ul>'
        f'</aside>'
    )


# === HTML Template ===


def generate_html(page_data, related_html, breadcrumbs_html, page_nav_html, current_path, article_count):
    """Generate a complete content-first HTML page (no side navigation).

    Layout: sticky top header (brand + group quick-nav + search + theme
    toggle) then the article as the main content area.
    """
    title = clean_title(page_data.get('title', ''), current_path)
    content = clean_content(page_data.get('content', ''))
    prefix = rel_prefix(current_path)

    # Page title for <title> tag
    if title and current_path != '/':
        page_title = f'{title} :: \u8d44\u6df1\u7801\u519c'
    else:
        page_title = '\u8d44\u6df1\u7801\u519c :: \u6280\u672f\u535a\u5ba2'

    # Meta description: only append the article title on article pages
    desc_title = f' - {escape(title)}' if title and current_path != '/' else ''

    # For homepage, don't show h1 if content has its own structure
    show_h1 = title and current_path != '/'

    h1_html = f'<h1>{escape(title)}</h1>' if show_h1 else ''

    # Article pages use a two-column layout: the article plus a sticky side
    # rail (same-group posts). The homepage is a single flowing column of
    # hero + card grid.
    is_home = current_path == '/'
    wrapper_class = 'home-layout' if is_home else 'article-layout'

    side_rail = ''
    if not is_home:
        side_rail = f'''<aside class="side-rail">
            {related_html}
        </aside>'''

    # Top header quick navigation (desktop): links to each group on the
    # homepage; on article pages points to the homepage anchor.
    home_ref = 'index.html' if prefix == '' else f'{prefix}index.html'
    nav_links = ''.join(
        f'<a href="{home_ref}#arch-{g["id"]}" data-group="{g["id"]}">{escape(g["nav_text"])}</a>'
        for g in CONTENT_GROUPS)

    # Current semantic group of this page (empty on the homepage), used to
    # highlight the matching group link in the header navigation.
    site_group = ''
    if current_path != '/':
        site_group = CONTENT_GROUP_BY_URL.get(current_path, {}).get('id', '')

    # Only load mermaid when the page actually contains diagrams
    mermaid_html = ''
    if 'class="mermaid"' in content:
        mermaid_html = '''    <script type="module">
    import mermaid from "https://cdnjs.cloudflare.com/ajax/libs/mermaid/10.9.0/mermaid.esm.min.mjs";
    window.mermaid = mermaid;
    mermaid.initialize({ startOnLoad: false, theme: document.documentElement.getAttribute('data-theme') === 'dark' ? 'dark' : 'default', securityLevel: 'loose' });
    mermaid.run({ querySelector: '.mermaid' });
    </script>
'''

    html = f'''<!DOCTYPE html>
<html lang="zh" data-theme="light">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="color-scheme" content="light dark">
    <meta name="description" content="\u8d44\u6df1\u7801\u519c \u6280\u672f\u535a\u5ba2{desc_title}">
    <meta name="author" content="\u8d44\u6df1\u7801\u519c">
    <meta name="generator" content="deep2code generator">
    <link rel="icon" href="/images/favicon.jpeg" type="image/jpeg">
    <title>{page_title}</title>
    <link rel="stylesheet" href="/css/style.css">
</head>
<body>
    <header class="site-header">
        <div class="header-inner">
            <a href="{home_ref}" class="header-brand">
                <span class="logo-mark">~$</span>
                <span class="blog-title">\u8d44\u6df1\u7801\u519c</span>
            </a>
            <nav class="header-nav" aria-label="\u5206\u7ec4\u5bfc\u822a">
                {nav_links}
            </nav>
            <div class="header-search">
                <svg class="search-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
                <input type="search" id="search-input" placeholder="\u641c\u7d22 {article_count} \u7bc7\u7b14\u8bb0...">
                <div class="search-results" id="search-results"></div>
            </div>
            <button class="theme-toggle" title="\u5207\u6362\u4e3b\u9898" aria-label="\u5207\u6362\u4e3b\u9898">
                <span class="icon-moon">\U0001f319</span>
                <span class="icon-sun">\u2600\ufe0f</span>
            </button>
        </div>
    </header>

    <div id="main-area">
        {breadcrumbs_html}

        <div id="content-wrapper" class="{wrapper_class}">
            <main id="body-content">
                {h1_html}
                {content}
                {page_nav_html}
            </main>
            {side_rail}
        </div>
    </div>

    <button class="back-to-top" title="\u56de\u5230\u9876\u90e8">\u2191</button>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
    {mermaid_html}
    <script>window.SITE_BASE = "{prefix}";window.SITE_GROUP = "{site_group}";</script>
    <script src="/js/main.js"></script>
</body>
</html>'''

    return relativize_static_refs(html, prefix)


def generate_search_index(pages, nav_items):
    """Generate search index JSON with full-text content for better matching."""
    index = []
    nav_by_path = {item['nav_id']: item for item in nav_items}

    for url, page in pages.items():
        title = page.get('title', '')
        if not title or url in ['/categories/', '/tags/']:
            continue

        # Get full text content (strip HTML tags and entities)
        content = page.get('content', '')
        text = re.sub(r'<[^>]+>', ' ', content)
        text = re.sub(r'&#\d+;', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()

        index.append({
            'url': url,
            'title': title,
            'text': text,
        })

    # Index-only pages: homepage portal, tags and categories listings.
    # Their raw data is Hugo residue; use hand-written entries so the
    # full site (70 pages) is searchable and local-file file:// works.
    index.append({'url': '/', 'title': '\u8d44\u6df1\u7801\u519c', 'text': '\u8d44\u6df1\u7801\u519c \u6280\u672f\u535a\u5ba2\u4e3b\u9875\uff1aGo\u3001Python\u3001AI\u3001Linux\u3001\u4e91\u539f\u751f\u7b49\u7cfb\u5217\u6280\u672f\u7b14\u8bb0\u7684\u5165\u53e3\uff0c\u6309\u5206\u7c7b\u6d4f\u89c8\u5168\u90e8\u6587\u7ae0\u3002'})
    index.append({'url': '/tags/', 'title': '标签', 'text': '按标签浏览全部技术文章。'})
    index.append({'url': '/categories/', 'title': '分类', 'text': '按分类浏览全部技术文章。'})

    return index


def main():
    print("Loading extracted content...")
    data = load_data()
    nav_items = data['navigation']
    pages = data['pages']

    print(f"Building navigation tree from {len(nav_items)} items...")
    nav_tree = build_nav_tree(nav_items)
    add_missing_nav_items(nav_tree, pages)

    # Flatten nav for prev/next (include added items)
    flat_nav = []
    for item in nav_tree:
        flat_nav.append(item)
        for child in item.get('children', []):
            flat_nav.append(child)

    print(f"Navigation tree: {len(nav_tree)} top-level, {len(flat_nav)} total")

    # Content-first homepage: hero + grouped archive of every article
    homepage_content = build_homepage_content(pages)

    # Count real articles (exclude the three index-only pages)
    article_count = sum(1 for u in pages if u not in ('/', '/categories/', '/tags/'))
    print(f"Article pages: {article_count} / {len(pages)} total entries")

    # Generate search index
    print("Generating search index...")
    search_index = generate_search_index(pages, nav_items)
    search_file = BASE_DIR / 'search-index.json'
    with open(search_file, 'w', encoding='utf-8') as f:
        json.dump(search_index, f, ensure_ascii=False, indent=2)
    print(f"  Saved search index: {len(search_index)} entries")

    # Generate sitemap.xml
    print("Generating sitemap...")
    domain = 'https://www.yijunjun.asia'
    with open(BASE_DIR / 'sitemap.xml', 'w', encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for url in sorted(pages.keys()):
            f.write(f'  <url><loc>{domain}{url}</loc></url>\n')
        f.write('</urlset>\n')
    print(f"  Saved sitemap: {len(pages)} urls")

    # Generate all pages
    print("\nGenerating HTML pages...")
    success_count = 0
    error_count = 0

    for url_path, page_data in pages.items():
        try:
            current_path = url_path

            # Homepage uses the portal content instead of the raw article dump
            if url_path == '/':
                page_data = dict(page_data)
                page_data['content'] = homepage_content
                page_data['title'] = ''

            # Breadcrumbs (only for article pages)
            breadcrumbs_html = build_breadcrumbs(current_path, flat_nav) if url_path != '/' else ''

            # In-group prev/next navigation
            page_nav_html = generate_page_nav(current_path, pages)

            # Related articles of the same semantic group
            related_html = generate_related_html(current_path, pages)

            # Generate full HTML (sidebar removed; content-first layout)
            html = generate_html(page_data, related_html, breadcrumbs_html, page_nav_html, current_path, article_count)

            # Write to file
            filepath = Path(page_data['filepath'])
            filepath.parent.mkdir(parents=True, exist_ok=True)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html)

            success_count += 1
            title = page_data.get('title', '(no title)')
            print(f"  OK  {url_path:<40} {title[:25]}")

        except Exception as e:
            error_count += 1
            print(f"  ERR {url_path:<40} {e}")

    print(f"\nDone: {success_count} pages generated, {error_count} errors")


if __name__ == '__main__':
    main()
