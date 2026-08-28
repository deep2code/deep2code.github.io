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
        'icon': '\U0001f439',
        'accent': '#00add8',
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
        'nav_text': '数据库',
        'blurb': 'MySQL · Redis · Memcached · Elasticsearch',
        'icon': '\U0001f4be',
        'accent': '#dc382d',
        'pages': ['/mysql/', '/redis/', '/memcached/', '/elastic/'],
    },
    {
        'id': 'ai',
        'title': 'AI 与机器学习',
        'nav_text': 'AI',
        'blurb': 'LLM · RAG · 微调 · 机器学习',
        'icon': '\U0001f916',
        'accent': '#9c27b0',
        'pages': ['/ai/', '/ai/llm/', '/ai/rag/', '/ai/finetuning/', '/other/machinelearn/'],
    },
    {
        'id': 'server',
        'title': '服务端与云',
        'nav_text': '服务端·云',
        'blurb': 'Nginx · gRPC · RPC · Docker · Harbor · 云平台',
        'icon': '\u2601\ufe0f',
        'accent': '#2563eb',
        'pages': [
            '/nginx/', '/nginx/install/', '/nginx/use/', '/nginx/http/', '/nginx/rtmp/',
            '/grpc/', '/grpc/golang/', '/other/rpc/',
            '/other/docker/', '/other/harbor/', '/other/aliyun/', '/other/tencent/',
            '/other/self-hosted/', '/other/brew/',
        ],
    },
    {
        'id': 'tools',
        'title': '开发工具与效率',
        'nav_text': '工具',
        'blurb': 'Git · Vim · Hugo · Mermaid · Markdown · 搜索与效率',
        'icon': '\U0001f527',
        'accent': '#f59e0b',
        'pages': [
            '/git/', '/other/github/', '/other/gitlab/', '/other/svn/', '/other/opensource/',
            '/other/vim/', '/other/hugo/', '/other/mermaid/', '/other/markdown/',
            '/other/makefile/', '/other/search/', '/other/geocode/', '/other/tesseract/',
        ],
    },
    {
        'id': 'misc',
        'title': '语言·系统·图形及其他',
        'nav_text': '更多',
        'blurb': 'Python · Rust · Shell · macOS · Unity · 零散主题',
        'icon': '\U0001f4da',
        'accent': '#10b981',
        'pages': [
            '/python/', '/other/rust/', '/other/shell/', '/other/wasm/', '/flutter/',
            '/mac/', '/other/windows/', '/other/wireshark/', '/other/web/', '/other/firefox/',
            '/other/unity/', '/other/unity/et/', '/other/',
        ],
    },
]

CONTENT_GROUP_BY_URL = {}
for _g in CONTENT_GROUPS:
    for _u in _g['pages']:
        CONTENT_GROUP_BY_URL[_u] = _g

# Group ordering used for in-group prev/next navigation
GROUP_ARTICLE_ORDER = [u for g in CONTENT_GROUPS for u in g['pages']]


def clean_pitch(text):
    """Strip version-year labels like （2026 版）and 2026 版 (not 2026 版本)."""
    if not text:
        return text
    text = re.sub(r'[（(]\s*2026\s*版\s*[）)]', '', text)
    text = re.sub(r'\s+2026\s*版(?![本])', '', text)
    return ' '.join(text.split())


# ============================================================
# Per-technology icon + representative command for homepage cards
# ============================================================
TECH_META = {
    # Go
    '/golang/':              ('🐹', 'go build -o app && go test ./...'),
    '/golang/stringer/':     ('🔤', 'go generate ./...'),
    '/golang/echo/':         ('🌐', 'e.Start(":8080")'),
    '/golang/context/':       ('⏱️', 'ctx, cancel := context.WithTimeout()'),
    '/golang/regexp/':       ('🔍', 'regexp.MustCompile(`pat`).FindAll()'),
    '/golang/sort/':         ('📊', 'slices.Sort(s)'),
    '/golang/freetype/':     ('🖋️', 'freetype.ParseFont(b)'),
    '/golang/iris/':         ('🌈', 'app.Listen(":8080")'),
    '/golang/shell/':        ('💻', 'exec.Command("sh", "-c", cmd)'),
    '/golang/io/':           ('📥', 'io.Copy(dst, src)'),
    '/golang/code/':         ('📝', 'go vet ./... && go fmt'),
    '/golang/groupby/':      ('🗂️', 'slices.GroupBy(s, keyFn)'),
    '/golang/log/':          ('📋', 'slog.Info("msg", "k", v)'),
    '/golang/generic/':      ('🔧', 'func F[T any](x T) T'),
    '/golang/gin/':          ('🍸', 'r := gin.Default()'),
    '/golang/package/':      ('📦', 'go get -u module@version'),
    '/golang/go-git/':       ('🌿', 'git.Clone(ctx, &opts)'),
    '/golang/generics-update/': ('⬆️', 'func F[T ~int | ~float64](x T)'),
    # Database
    '/mysql/':               ('🐬', 'mysql -u root -p < schema.sql'),
    '/redis/':               ('🔴', 'redis-cli SET k v && GET k'),
    '/memcached/':           ('⚡', 'echo "set k 0 0 5" | nc :11211'),
    '/elastic/':             ('🔎', 'curl :9200/_search?q=hello'),
    # AI
    '/ai/':                  ('🧠', 'AutoModel.from_pretrained()'),
    '/ai/llm/':              ('💬', 'model.generate(tokenizer(p))'),
    '/ai/rag/':              ('📚', 'llm.gen(retriever.search(q))'),
    '/ai/finetuning/':       ('🔧', 'Trainer(model).train(data)'),
    '/other/machinelearn/':  ('📈', 'model.fit(X_train, y_train)'),
    # Server & Cloud
    '/nginx/':               ('🟢', 'nginx -t && nginx -s reload'),
    '/nginx/install/':       ('🔨', './configure --with-http_v3 && make'),
    '/nginx/use/':           ('⚙️', 'location / { proxy_pass backend; }'),
    '/nginx/http/':          ('🔒', 'add_header Strict-Transport-Security'),
    '/nginx/rtmp/':          ('📡', 'rtmp { server { live on; } }'),
    '/grpc/':                ('🔗', 'grpc.Serve(lis, srv)'),
    '/grpc/golang/':         ('📋', 'protoc --go_out=. hello.proto'),
    '/other/rpc/':           ('📡', 'rpc.Call("Svc.Method", args)'),
    '/other/docker/':        ('🐳', 'docker build -t app . && docker run -p 80:80 app'),
    '/other/harbor/':        ('⚓', 'docker push harbor.io/app:tag'),
    '/other/aliyun/':        ('☁️', 'aliyun configure && aliyun cli'),
    '/other/tencent/':       ('☁️', 'tcloud configure && tcloud cli'),
    '/other/self-hosted/':   ('🏠', 'git init --bare repo.git'),
    '/other/brew/':          ('🍺', 'brew install package'),
    # Tools
    '/git/':                 ('🌳', 'git add . && git commit -m "msg"'),
    '/other/github/':        ('🐙', 'gh pr create --title "feat"'),
    '/other/gitlab/':        ('🦊', 'gitlab-ctl reconfigure'),
    '/other/svn/':           ('📋', 'svn checkout URL && svn commit -m'),
    '/other/opensource/':    ('🌍', 'fork → clone → branch → PR'),
    '/other/vim/':           ('✏️', 'vim file.py → :wq'),
    '/other/hugo/':          ('🏗️', 'hugo new site blog && hugo server'),
    '/other/mermaid/':       ('📐', 'mermaid render diagram.mmd'),
    '/other/markdown/':      ('📝', 'markdown file.md -o out.html'),
    '/other/makefile/':      ('🔨', 'make build && make test'),
    '/other/search/':        ('🔍', 'grep -rn "pattern" .'),
    '/other/geocode/':       ('📍', 'geocode("address") → lat,lng'),
    '/other/tesseract/':     ('👁️', 'tesseract image.png output.txt'),
    # Misc
    '/python/':              ('🐍', 'python -m venv venv && pip install'),
    '/other/rust/':          ('🦀', 'cargo build --release'),
    '/other/shell/':         ('🐚', 'bash script.sh && echo $?'),
    '/other/wasm/':          ('🟨', 'wasm-pack build --target web'),
    '/flutter/':             ('💙', 'flutter create app && flutter run'),
    '/mac/':                 ('🍎', 'brew install --cask app'),
    '/other/windows/':       ('🪟', 'winget install Package'),
    '/other/wireshark/':     ('🦈', 'tshark -i eth0 -f "port 80"'),
    '/other/web/':           ('🌐', 'curl -sL https://api.io | jq .'),
    '/other/firefox/':       ('🦎', 'firefox --headless --screenshot'),
    '/other/unity/':         ('🎮', 'unity build --platform android'),
    '/other/unity/et/':      ('🎲', 'C# ET 框架: C/S 游戏架构'),
    '/other/':               ('📦', 'ls ~/tools && which tool'),
}


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


def annotate_mermaid_src(content):
    """Store raw mermaid source into data-src for copy/collapse tools.

    Mermaid divs are rendered by the per-page module script (which runs
    before DOMContentLoaded), so by the time main.js executes the raw
    source text is gone. Keeping an escaped copy in data-src preserves
    the copy-button and the 'show source' fallback of the fold feature.
    """
    def _annotate(m):
        tag = m.group(1)
        body = m.group(2)
        if 'data-src' in tag:
            return m.group(0)
        return '<div class="mermaid"%s data-src="%s">%s</div>' % (
            tag, escape(body.strip()), body)
    return re.sub(r'<div class="mermaid"([^>]*)>([\s\S]*?)</div>',
                  _annotate, content)


def annotate_echart_containers(content):
    """Convert <div class="echart" data-option="..."> blocks into render-ready containers.

    ECharts chart definitions are embedded in article content as:
        <div class="echart" data-option='{"type":"radar","title":"...","data":...}'></div>
    This function wraps them in a styled container with a unique id for
    the runtime renderer to pick up.
    """
    counter = [0]
    def _annotate(m):
        attrs = m.group(1)
        inner = m.group(2).strip()
        counter[0] += 1
        cid = f'echart-{counter[0]}'
        # If data-option is already in attrs, use it; otherwise treat inner as option JSON
        if 'data-option' in attrs:
            return f'<div class="echart-container" id="{cid}"{attrs}>{inner}</div>'
        elif inner:
            return f'<div class="echart-container" id="{cid}" data-option="{escape(inner)}"></div>'
        return m.group(0)
    return re.sub(
        r'<div class="echart"([^>]*)>([\s\S]*?)</div>',
        _annotate, content)


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

    def pitch_of(u):
        p = pages.get(u, {})
        pitch = clean_pitch(p.get('ai_pitch', '') or '')
        return ' '.join(pitch.split())

    # Index-only pages are not articles; count real posts for honest stats.
    article_count = sum(1 for u in pages if u not in ('/', '/categories/', '/tags/'))
    topic_names = ' '.join(g['nav_text'] for g in CONTENT_GROUPS)

    groups = []
    for idx, g in enumerate(CONTENT_GROUPS, start=1):
        page_list = [u for u in g['pages'] if u in pages]
        count = len(page_list)
        show_count = 6 if count > 6 else count
        visible = page_list[:show_count]
        hidden_count = count - len(visible)

        items_html = ''.join(
            f'<li class="arch-item">'
            f'<a class="arch-link" href="{page_href(u)}">'
            f'<span class="arch-icon" aria-hidden="true">{TECH_META.get(u, ("\U0001f4c4",""))[0]}</span>'
            f'<span class="arch-title">{escape(title_of(u))}</span>'
            f'<span class="arch-arrow">\u2192</span></a>'
            + (
                f'<div class="arch-cmd"><span class="arch-cmd-prompt">$</span><code class="arch-cmd-text">{escape(TECH_META[u][1])}</code></div>'
                if u in TECH_META and TECH_META[u][1]
                else (f'<p class="arch-pitch">{escape(pitch_of(u))}</p>' if pitch_of(u) else '')
            )
            + '</li>'
            for u in visible)
        if hidden_count > 0:
            items_html += (
                f'<li class="arch-item arch-more">'
                f'<a class="arch-more-link" href="#arch-{g["id"]}">'
                f'<span>\u67e5\u770b\u5168\u90e8</span>'
                f'<span class="arch-arrow">\u2193</span></a></li>')
            rest_items = ''.join(
                f'<li class="arch-item arch-hidden">'
                f'<a class="arch-link" href="{page_href(u)}">'
                f'<span class="arch-icon" aria-hidden="true">{TECH_META.get(u, ("📄",""))[0]}</span>'
                f'<span class="arch-title">{escape(title_of(u))}</span>'
                f'<span class="arch-arrow">\u2192</span></a></li>'
                for u in page_list[show_count:])
            articles_html = f'<ul class="arch-list">{items_html}</ul><ul class="arch-list arch-hidden-list" hidden>{rest_items}</ul>'
        else:
            articles_html = f'<ul class="arch-list">{items_html}</ul>'

        groups.append(
            f'<section class="group-section" id="arch-{g["id"]}" style="--grp-accent:{g["accent"]}">'
            f'<header class="group-section-head">'
            f'<span class="group-section-icon" aria-hidden="true">{g["icon"]}</span>'
            f'<span class="group-section-idx">{idx:02d}</span>'
            f'<div class="group-section-titles">'
            f'<h2 class="group-section-name">{escape(g["title"])}</h2>'
            f'<p class="group-section-blurb">{escape(g["blurb"])}</p>'
            f'</div>'
            f'</header>'
            f'{articles_html}'
            f'</section>')
    grid = '\n'.join(groups)

    # AI era timeline: ChatGPT → Tool → RAG → MCP → Skill → Agent
    ai_era_items = [
        ('💬', '2022·11', 'ChatGPT',
         'OpenAI 发布 ChatGPT，大语言模型从实验室走向大众。自然语言成为新的人机交互界面，AI 从"能力"变成"产品"。',
         '#10b981'),
        ('🛠️', '2023·06', 'Function Calling / Tool',
         'OpenAI 推出 Function Calling，LLM 不再只是聊天，而是可以调用外部工具——搜索、计算、数据库查询。AI 有了"手"。',
         '#3b82f6'),
        ('📚', '2023·08', 'RAG 检索增强生成',
         '检索增强生成（Retrieval-Augmented Generation）成为主流架构。LLM 接入企业知识库，从"通才"变"专家"，幻觉问题大幅缓解。',
         '#8b5cf6'),
        ('🔌', '2024·11', 'MCP 协议',
         'Anthropic 发布 Model Context Protocol，为 AI 与外部数据源/工具的连接建立统一标准。如同 USB-C 之于硬件，MCP 让 AI 接入标准化。',
         '#f59e0b'),
        ('⚡', '2025·03', 'Skill 技能化',
         '大模型从"调用工具"进化到"拥有技能"。Skill 封装了完整的领域工作流，AI 不再是单次调用，而是自主编排多步骤任务。',
         '#ef4444'),
        ('🤖', '2025·06+', 'Agent 自主智能体',
         '从单轮对话到多轮自主决策。Agent 能理解目标、规划步骤、调用工具链、执行并验证——软件开发从"人写代码"走向"人审代码"。',
         '#ec4899'),
    ]
    ai_era_nodes = ''.join(
        f'<div class="ae-node" style="--c:{color};--n:{i}">'
        f'<div class="ae-ring" aria-hidden="true">{emoji}</div>'
        f'<span class="ae-date">{escape(date)}</span>'
        f'<span class="ae-name">{escape(name)}</span>'
        f'</div>'
        for i, (emoji, date, name, desc, color) in enumerate(ai_era_items))

    # AI era impact on software development
    ai_impact_items = [
        (' architect', '🧩', '架构变革',
         '从单体→微服务→AI-native：系统设计不再只考虑人读 API，更要为 Agent 设计可发现、可调用的接口。MCP 成为新的"API 网关"。'),
        ('coding', '⌨️', '编码方式',
         '从手写每一行代码到自然语言描述意图→AI 生成→人工审查。Copilot/Codeium 已是标配，Claude Code/Cursor 让"对话式编程"成为日常。'),
        ('testing', '🧪', '测试与质量',
         'AI 自动生成测试用例、发现边界条件、审计代码安全。从"写完再测"到"边写边测边修复"，CI/CD 管线深度嵌入 AI。'),
        ('ops', '🚀', '运维与部署',
         'Agent 自主排查线上故障、生成修复方案、执行回滚。从人盯监控大盘到 AI 预警→自动止损→人工确认。'),
        ('team', '👥', '团队与协作',
         '一人+多 Agent 成为新型"全栈团队"。PRD 由 AI 起草、代码由 AI 生成、文档由 AI 编写——人的角色从"执行者"变为"决策者"。'),
        ('future', '🔮', '未来趋势',
         '模型即基础设施，Skill 即应用，Agent 即用户。软件开发的终局不是"写代码"，而是"定义意图、约束边界、验证结果"。'),
    ]
    _aic_colors = ["#3b82f6", "#8b5cf6", "#10b981", "#f59e0b", "#ef4444", "#ec4899"]
    ai_impact_slides = ''.join(
        f'<div class="ai-impact-slide" data-i="{i}" style="--aic:{_aic_colors[i]}">'
        f'<div class="ai-impact-card">'
        f'<div class="ai-impact-icon" aria-hidden="true">{emoji}</div>'
        f'<h3 class="ai-impact-title">{escape(title)}</h3>'
        f'<p class="ai-impact-desc">{escape(desc)}</p>'
        f'</div>'
        f'</div>'
        for i, (_, emoji, title, desc) in enumerate(ai_impact_items))
    ai_impact_dots = ''.join(
        f'<span class="ai-impact-dot" data-i="{i}"></span>'
        for i in range(len(ai_impact_items)))

    # === 码农进化史宣传片 — 循环动画 ===
    _DEV_SVG_INNER = (
        '<ellipse cx="100" cy="248" rx="50" ry="6" fill="rgba(0,0,0,0.18)"/>'
        '<path d="M45 145 Q100 128 155 145 L160 232 Q100 248 40 232 Z" fill="#4A7CB8" stroke="#2E5A8A" stroke-width="2"/>'
        '<path d="M60 142 Q100 120 140 142 Q140 130 100 112 Q60 130 60 142 Z" fill="#2E5A8A"/>'
        '<path d="M70 175 Q100 168 130 175 L125 195 Q100 200 75 195 Z" fill="#3A6BA8" opacity="0.5"/>'
        '<line x1="92" y1="142" x2="90" y2="165" stroke="#2E5A8A" stroke-width="2.5" stroke-linecap="round"/>'
        '<line x1="108" y1="142" x2="110" y2="165" stroke="#2E5A8A" stroke-width="2.5" stroke-linecap="round"/>'
        '<circle cx="90" cy="167" r="2.5" fill="#2E5A8A"/>'
        '<circle cx="110" cy="167" r="2.5" fill="#2E5A8A"/>'
        '<g class="dev-arm-l">'
        '<path d="M45 148 Q28 170 22 195" stroke="#4A7CB8" stroke-width="14" fill="none" stroke-linecap="round"/>'
        '<circle cx="22" cy="197" r="9.5" fill="#F0C8A0" stroke="#D4A070" stroke-width="1"/>'
        '</g>'
        '<g class="dev-arm-r">'
        '<path d="M155 148 Q172 170 178 195" stroke="#4A7CB8" stroke-width="14" fill="none" stroke-linecap="round"/>'
        '<circle cx="178" cy="197" r="9.5" fill="#F0C8A0" stroke="#D4A070" stroke-width="1"/>'
        '</g>'
        '<path d="M86 128 L86 145 Q100 150 114 145 L114 128 Z" fill="#F0C8A0"/>'
        '<circle cx="100" cy="88" r="42" fill="#F0C8A0" stroke="#D4A070" stroke-width="1.5"/>'
        '<circle cx="58" cy="90" r="6" fill="#F0C8A0" stroke="#D4A070" stroke-width="1"/>'
        '<circle cx="142" cy="90" r="6" fill="#F0C8A0" stroke="#D4A070" stroke-width="1"/>'
        '<path d="M58 85 Q60 45 100 42 Q140 45 142 85 Q138 58 118 55 Q112 48 100 48 Q88 48 82 55 Q62 58 58 85 Z" fill="#2D1B0E"/>'
        '<path d="M58 85 Q55 95 59 103 L63 88 Z" fill="#2D1B0E"/>'
        '<path d="M142 85 Q145 95 141 103 L137 88 Z" fill="#2D1B0E"/>'
        '<path d="M68 74 Q78 71 88 74" stroke="#2D1B0E" stroke-width="3" fill="none" stroke-linecap="round"/>'
        '<path d="M112 74 Q122 71 132 74" stroke="#2D1B0E" stroke-width="3" fill="none" stroke-linecap="round"/>'
        '<circle cx="78" cy="88" r="16" fill="rgba(180,210,255,0.12)" stroke="#1a1a2e" stroke-width="2.5"/>'
        '<circle cx="122" cy="88" r="16" fill="rgba(180,210,255,0.12)" stroke="#1a1a2e" stroke-width="2.5"/>'
        '<path d="M94 88 L106 88" stroke="#1a1a2e" stroke-width="2.5" stroke-linecap="round"/>'
        '<path d="M62 85 L55 80" stroke="#1a1a2e" stroke-width="2" stroke-linecap="round"/>'
        '<path d="M138 85 L145 80" stroke="#1a1a2e" stroke-width="2" stroke-linecap="round"/>'
        '<circle cx="78" cy="89" r="3.5" fill="#1a1a2e"/>'
        '<circle cx="122" cy="89" r="3.5" fill="#1a1a2e"/>'
        '<circle cx="80" cy="87" r="1.2" fill="#fff"/>'
        '<circle cx="124" cy="87" r="1.2" fill="#fff"/>'
        '<path d="M100 98 L98 105 Q100 107 102 105 Z" fill="#D4A070" opacity="0.5"/>'
        '<path d="M82 110 Q100 120 118 110" stroke="#1a1a2e" stroke-width="2.5" fill="none" stroke-linecap="round"/>'
        '<circle cx="65" cy="102" r="6" fill="#FFB088" opacity="0.4"/>'
        '<circle cx="135" cy="102" r="6" fill="#FFB088" opacity="0.4"/>'
    )
    _dev_sprite = (
        '<svg style="position:absolute;width:0;height:0;overflow:hidden" aria-hidden="true">'
        '<symbol id="cine-dev" viewBox="0 0 200 260">' + _DEV_SVG_INNER + '</symbol>'
        '</svg>'
    )
    journey_scenes = [
        ('2004\u20142008', '\u81ea\u5b66\u8d77\u6b65',
         '\u7406\u5de5\u79d1\u51fa\u8eab\uff0c\u8de8\u4e13\u4e1a\u8f6c\u884c\uff0c\u4ece\u96f6\u5f00\u59cb\u81ea\u5b66\u8ba1\u7b97\u673a\u2014\u2014\u8bed\u8a00\u3001\u6570\u636e\u7ed3\u6784\u3001\u7b97\u6cd5\uff0c\u4e00\u672c\u672c\u556e\u4e0b\u6765\u3002',
         '#E94560', ['\U0001F4DA', '\u270F\uFE0F', '\U0001F4A1', '\U0001F4D6', '\U0001F4D0'], '\U0001F4D5'),
        ('2008\u20142012', '\u6572\u5f00\u884c\u4e1a\u5927\u95e8',
         '\u51ed\u81ea\u5b66\u79ef\u7d2f\u7684\u4ee3\u7801\u80fd\u529b\uff0c\u6b63\u5f0f\u8fdb\u5165\u8f6f\u4ef6\u5f00\u53d1\u884c\u4e1a\uff0c\u5f00\u59cb\u4ee5\u5199\u4ee3\u7801\u4e3a\u4e1a\u3002',
         '#00D2D3', ['\U0001F4BC', '\U0001F3E2', '\U0001F5A5\uFE0F', '\U0001F454', '\U0001F511'], '\U0001F6AA'),
        ('2012\u20142016', '\u4e00\u7ebf\u957f\u671f\u4e3b\u4e49',
         '\u957f\u671f\u5728\u4e1a\u52a1\u4e00\u7ebf\u5199\u4ee3\u7801\uff1a\u4ece\u5355\u4f53\u5230\u5206\u5e03\u5f0f\u3001\u4ece\u5e94\u7528\u5230\u7cfb\u7edf\uff0c\u8e29\u8fc7\u7684\u5751\u90fd\u6c89\u6dc0\u6210\u7ecf\u9a8c\u3002',
         '#1B9C85', ['\U0001F41B', '\U0001F527', '\u26A1', '\U0001F4DD', '\U0001F3AF'], '\U0001F4BB'),
        ('2016\u20142020', '\u62e5\u62b1\u6280\u672f\u6f14\u8fdb',
         '\u6280\u672f\u6808\u968f\u65f6\u4ee3\u5237\u65b0\u2014\u2014Go\u3001Python\u3001\u4e91\u539f\u751f\u3001AI\uff0c\u5b66\u4e60\u4ece\u672a\u505c\u6b65\u3002',
         '#C77DFF', ['\U0001F431', '\U0001F40D', '\u2601\uFE0F', '\U0001F916', '\u26A1'], '\U0001F680'),
        ('2020\u20142024', '\u5199\u4f5c\u4e0e\u5206\u4eab',
         '\u628a\u8e29\u5751\u4e0e\u5b9e\u6218\u5199\u6210\u535a\u5ba2\uff0c\u4e00\u7bc7\u7bc7\u90fd\u662f\u771f\u5b9e\u7684\u4e00\u7ebf\u7b14\u8bb0\u3002',
         '#FF6B6B', ['\U0001F4DD', '\U0001F4C4', '\U0001F4A1', '\U0001F4CA', '\U0001F517'], '\u270D\uFE0F'),
        ('2024\u20142026', '\u4f9d\u7136\u70ed\u7231',
         '\u4e8c\u5341\u4f59\u5e74\u4e00\u7ebf\u5f00\u53d1\uff0c\u4fdd\u6301\u597d\u5947\uff0c\u4fdd\u6301\u70ed\u7231\uff0c\u7ee7\u7eed\u5199\u4ee3\u7801\u3002',
         '#FFB703', ['\u2764\uFE0F', '\u2728', '\U0001F4BB', '\U0001F525', '\u2B50'], '\u2764\uFE0F'),
    ]
    _fslots = [(8, 15, 0.0, 4.0), (24, 72, 0.5, 3.5), (50, 20, 1.0, 4.5),
               (76, 68, 1.5, 3.8), (92, 28, 2.0, 4.2)]
    _scene_parts = []
    for _si, (_yr, _ph, _desc, _ac, _floats, _prop) in enumerate(journey_scenes):
        _fl = ''.join(
            f'<span class="cine-fl" style="--fx:{_fx}%;--fy:{_fy}%;--fd:{_fd}s;--fu:{_fu}s">{_fe}</span>'
            for _fe, (_fx, _fy, _fd, _fu) in zip(_floats, _fslots))
        _scene_parts.append(
            f'<div class="cine-scene" data-i="{_si}" style="--ac:{_ac}">'
            f'<div class="cine-bg cine-bg{_si}"></div>'
            f'<div class="cine-floats" aria-hidden="true">{_fl}</div>'
            f'<div class="cine-char" aria-hidden="true"><svg class="cine-dev" viewBox="0 0 200 260" aria-hidden="true"><use href="#cine-dev"/></svg></div>'
            f'<div class="cine-prop" aria-hidden="true">{_prop}</div>'
            f'<div class="cine-text">'
            f'<span class="cine-year">{escape(_yr)}</span>'
            f'<h3 class="cine-phase">{escape(_ph)}</h3>'
            f'<p class="cine-desc">{escape(_desc)}</p>'
            f'</div></div>')
    _dots = ''.join(
        f'<span class="cinema-dot" data-i="{_i}"></span>'
        for _i in range(len(journey_scenes)))
    timeline_html = (
        f'{_dev_sprite}'
        f'<section class="journey-cinema" aria-label="\u7801\u519c\u8fdb\u5316\u53f2\u5ba3\u4f20\u7247">'
        f'<div class="cinema-head">'
        f'<span class="cinema-kicker">MY JOURNEY</span>'
        f'<h2 class="cinema-title">\u4ece 2004 \u5230 2026\uff0c\u4e00\u4e2a\u7406\u5de5\u7537\u7684\u7f16\u7a0b\u4e4b\u8def</h2>'
        f'<p class="cinema-sub">\u8de8\u4e13\u4e1a\u81ea\u5b66 \u00b7 \u4e00\u7ebf\u5f00\u53d1\u4e8c\u5341\u4f59\u5e74 \u00b7 \u4e0d\u65ad\u5b66\u4e60\uff0c\u4fdd\u6301\u70ed\u7231</p>'
        f'</div>'
        f'<div class="cinema-screen" id="cinema-screen">'
        f'<div class="cinema-bar cinema-bar-top"></div>'
        f'<div class="cinema-bar cinema-bar-bottom"></div>'
        f'<div class="cinema-stage">{"".join(_scene_parts)}</div>'
        f'<div class="cinema-vignette" aria-hidden="true"></div>'
        f'<div class="cinema-hud">'
        f'<div class="cinema-progress"><div class="cinema-progress-bar" id="cinema-bar"></div></div>'
        f'<div class="cinema-dots">{_dots}</div>'
        f'<span class="cinema-counter" id="cinema-counter">1 / {len(journey_scenes)}</span>'
        f'</div>'
        f'</div>'
        f'</section>'
    )

    return (
        f'<div class="hero-section">'
        f'<div class="hero-glow"></div>'
        f'<div class="hero-inner">'
        f'<div class="hero-copy">'
        f'<h1 class="hero-title">\u6280\u672f\u535a\u5ba2\uff0c'
        f'\u4e00\u7bc7\u7bc7\u8e29\u5751\u4e0e\u5b9e\u8df5\u3002</h1>'
        f'<p class="hero-desc">\u4ece Go\u3001Python \u5230\u4e91\u539f\u751f\u4e0e AI\u3001\u4ece'
        f'\u6570\u636e\u5e93\u5230\u5f00\u53d1\u5de5\u5177\uff1a'
        f'\u5168\u90e8\u7b14\u8bb0\u6309\u8bed\u4e49\u5206\u7ec4\uff0c'
        f'\u591a\u6570\u7bc7\u7ae0\u9644\u4ee3\u7801\u4e0e\u56fe\u8868\uff0c'
        f'\u53ef\u4ee5\u4f7f\u7528\u9876\u90e8\u641c\u7d22\u76f4\u8fbe\u5185\u5bb9\u3002</p>'
        f'<div class="hero-tags">'
        f'<span class="hero-tag">Go</span>'
        f'<span class="hero-tag">Python</span>'
        f'<span class="hero-tag">Cloud Native</span>'
        f'<span class="hero-tag">AI / LLM</span>'
        f'<span class="hero-tag">Database</span>'
        f'</div>'
        f'</div>'
        f'<div class="terminal-card" role="img" aria-label="\u7ec8\u7aef\u98ce\u683c\u7684\u535a\u5ba2\u4ecb\u7ecd">'
        f'<div class="terminal-bar">'
        f'<span class="term-dot dot-red"></span><span class="term-dot dot-yellow"></span>'
        f'<span class="term-dot dot-green"></span><span class="term-title">zsh \u2014 \u8d44\u6df1\u7801\u519c</span>'
        f'</div>'
        f'<div class="terminal-body" id="terminal-body">'
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
        f'{timeline_html}'
        f'<section class="ai-era-section" aria-label="AI 时代大事记">'
        f'<div class="ai-era-head">'
        f'<span class="ai-era-kicker">AI ERA</span>'
        f'<h2 class="ai-era-title">AI 时代关键演进</h2>'
        f'<p class="ai-era-sub">ChatGPT → Tool → RAG → MCP → Skill → Agent</p>'
        f'</div>'
        f'<div class="ae-anim">'
        f'<div class="ae-line"></div>'
        f'<div class="ae-nodes">{ai_era_nodes}</div>'
        f'</div>'
        f'</section>'
        f'<section class="ai-impact-section" aria-label="AI 时代对软件开发的改变">'
        f'<div class="ai-impact-head">'
        f'<span class="ai-impact-kicker">SHIFT</span>'
        f'<h2 class="ai-impact-title">AI 正在如何改变软件开发</h2>'
        f'</div>'
        f'<div class="ai-impact-slider" id="ai-impact-slider">'
        f'<div class="ai-impact-track">{ai_impact_slides}</div>'
        f'<button class="ai-impact-nav ai-impact-prev" aria-label="上一张">\u2039</button>'
        f'<button class="ai-impact-nav ai-impact-next" aria-label="下一张">\u203a</button>'
        f'<div class="ai-impact-dots">{ai_impact_dots}</div>'
        f'<div class="ai-impact-progress"><div class="ai-impact-progress-bar" id="ai-impact-bar"></div></div>'
        f'<span class="ai-impact-counter" id="ai-impact-counter">1 / {len(ai_impact_items)}</span>'
        f'</div>'
        f'</section>'
        f'<div class="group-list">{grid}</div>'
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
    """List other posts of the same semantic group as a bottom strip."""
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
        f'<h2 class="related-title">\u540c\u7ec4\u9605\u8bfb \xb7 {escape(group["title"])}</h2>'
        f'<ul class="related-list">{items}</ul>'
        f'</aside>'
    )


# === HTML Template ===


def render_ai_card(page_data):
    """Render a collapsible AI reading-guide card above the article.

    The card summarises the article in four blocks (core points, key
    conclusions, who it is for, what you gain). It is static: content is
    pre-generated from the article itself, no runtime API involved.
    """
    summary = page_data.get('ai_summary')
    if not summary:
        return ''
    points = summary.get('core_points') or []
    conclusions = summary.get('conclusions') or []
    audience = (summary.get('audience') or '').strip()
    takeaway = (summary.get('takeaway') or '').strip()

    def _ul(items):
        if not items:
            return ''
        lis = ''.join(f'<li>{escape(str(i))}</li>' for i in items)
        return f'<ul class="ai-grid-list">{lis}</ul>'

    blocks = []
    if points:
        blocks.append(
            f'<section class="ai-block"><h4 class="ai-block-title">\u6838\u5fc3\u89c2\u70b9</h4>{_ul(points)}</section>')
    if conclusions:
        blocks.append(
            f'<section class="ai-block"><h4 class="ai-block-title">\u5173\u952e\u7ed3\u8bba\u4e0e\u53d6\u820d</h4>{_ul(conclusions)}</section>')
    grid = f'<div class="ai-grid">{chr(10).join(blocks)}</div>' if blocks else ''

    meta = []
    if audience:
        meta.append(
            f'<span class="ai-meta-item"><b>\u9002\u5408\u8c01\u8bfb</b>{escape(audience)}</span>')
    if takeaway:
        meta.append(
            f'<span class="ai-meta-item"><b>\u8bfb\u5b8c\u53ef\u83b7\u5f97</b>{escape(takeaway)}</span>')
    meta_html = f'<div class="ai-meta">{chr(10).join(meta)}</div>' if meta else ''

    body = (grid + ((chr(10) + meta_html) if meta_html else '')).strip()

    return (
        f'<details class="ai-card" open>'
        f'<summary class="ai-card-head" tabindex="0">'
        f'<span class="ai-card-badge">AI \u5bfc\u8bfb</span>'
        f'<span class="ai-card-hint">\u4e00\u5206\u949f\u5bfc\u8bfb\uff0c\u5148\u638c\u63e1\u5168\u6587\u4e3b\u5e72\u3002</span>'
        f'<span class="ai-card-toggle" aria-hidden="true">\u25bc</span>'
        f'</summary>'
        f'<div class="ai-card-body">{body}</div>'
        f'</details>'
    )


def assert_anchor_ids(original, rewritten):
    """Return the set of heading ids present in the original but missing
    from the rewritten body. Rewritten AI bodies must keep every heading id
    (including anchors like `-*_2024-update`) so external links don't break.
    """
    orig_ids = set(re.findall(r'<h[1-6][^>]*\bid="([^"]+)"', original))
    new_ids = set(re.findall(r'<h[1-6][^>]*\bid="([^"]+)"', rewritten))
    if not orig_ids:
        return set()
    return orig_ids - new_ids


def assert_code_blocks_preserved(original, rewritten):
    """Code blocks must survive the rewrite untouched (language, content).

    Returns the number of <pre> blocks in each version so callers can
    verify parity; missing code is a hard failure of the rewrite.
    """
    def blocks(html):
        return re.findall(r'<pre[^>]*>.*?</pre>', html, flags=re.DOTALL)
    return len(blocks(original)), len(blocks(rewritten))


SITE_DOMAIN = 'https://www.yijunjun.asia'
SITE_NAME = '\u8d44\u6df1\u7801\u519c'
SITE_TAGLINE = '\u6280\u672f\u535a\u5ba2\u2014\u2014Go\u3001\u4e91\u539f\u751f\u3001AI\u3001\u6570\u636e\u5e93\u3001\u5f00\u53d1\u5de5\u5177\u7684\u8e29\u5751\u4e0e\u5b9e\u8df5'
SITE_DESCRIPTION = '\u8d44\u6df1\u7801\u519c\u6280\u672f\u535a\u5ba2\uff1a\u4e00\u540d\u4e8c\u5341\u5e74\u4e00\u7ebf\u7a0b\u5e8f\u5458\u7684\u6280\u672f\u7b14\u8bb0\uff0c\u6db5\u76d6 Go \u8bed\u8a00\u3001\u4e91\u539f\u751f\u67b6\u6784\u3001AI \u4e0e\u5927\u6a21\u578b\u3001\u6570\u636e\u5e93\u4e0e\u7f13\u5b58\u3001\u5f00\u53d1\u5de5\u5177\u4e0e\u6548\u7387\u7b49\u9886\u57df\uff0c\u591a\u6570\u6587\u7ae0\u914d\u6709\u4ee3\u7801\u4e0e\u67b6\u6784\u56fe\u8868\u3002'

# AI crawlers that should be explicitly allowed
AI_CRAWLERS = [
    'GPTBot',        # OpenAI
    'Claude-Web',    # Anthropic
    'PerplexityBot', # Perplexity
    'CCBot',         # Common Crawl
    'Google-Extended',# Google AI training
    'Bytespider',    # ByteDance
    'Cotoyogi',      # LLM indexer
    'Diffbot',       # Diffbot
    'FacebookBot',   # Meta
    'anthropic-ai',  # Anthropic alt
    'cohere-ai',     # Cohere
]


def build_meta_tags(page_data, current_path, title, prefix):
    """Build SEO + social + AI-crawler meta tags for a page."""
    is_home = current_path == '/'
    url = f'{SITE_DOMAIN}{current_path}'

    # Determine page description: prefer ai_pitch, then ai_summary takeaway,
    # then title-based fallback
    ai_pitch = clean_pitch(page_data.get('ai_pitch', ''))
    if ai_pitch and isinstance(ai_pitch, str):
        desc = ai_pitch
    else:
        ai_summary = page_data.get('ai_summary', {})
        if isinstance(ai_summary, dict):
            takeaway = ai_summary.get('takeaway', '')
            desc = takeaway if takeaway else (title or SITE_NAME)
        else:
            desc = title or SITE_NAME

    if is_home:
        desc = SITE_DESCRIPTION

    desc = re.sub(r'<[^>]+>', '', str(desc)).strip()
    if len(desc) > 160:
        desc = desc[:157] + '...'

    og_title = SITE_NAME
    page_type = 'website' if is_home else 'article'

    # Article-specific tags
    article_tags = ''
    if not is_home and title:
        group = CONTENT_GROUP_BY_URL.get(current_path, {})
        section = group.get('title', '')
        article_tags = f'''
    <meta property="article:author" content="{SITE_NAME}">
    <meta property="article:section" content="{escape(section)}">
    <meta property="article:tag" content="{escape(section)}">'''

    return f'''    <meta name="description" content="{escape(desc)}">
    <meta name="keywords" content="Go,Golang,AI,LLM,RAG,云原生,Nginx,Docker,MySQL,Redis,Elasticsearch,Python,\u6280\u672f\u535a\u5ba2,\u7a0b\u5e8f\u5458,\u8e29\u5751,\u5b9e\u8df5">
    <meta name="author" content="{SITE_NAME}">
    <meta name="generator" content="deep2code generator">
    <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">
    <meta name="googlebot" content="index, follow">
    <meta name="bingbot" content="index, follow">
    <meta name="baiduspider" content="index, follow">
    <!-- AI crawler friendly: explicitly allow indexing -->
    <meta name="GPTBot" content="index, follow">
    <meta name="Claude-Web" content="index, follow">
    <meta name="PerplexityBot" content="index, follow">
    <meta name="CCBot" content="index, follow">
    <meta name="Google-Extended" content="index, follow">
    <link rel="canonical" href="{url}">
    <!-- Open Graph -->
    <meta property="og:title" content="{escape(og_title)}">
    <meta property="og:description" content="{escape(desc)}">
    <meta property="og:type" content="{page_type}">
    <meta property="og:url" content="{url}">
    <meta property="og:site_name" content="{SITE_NAME}">
    <meta property="og:locale" content="zh_CN">
    <meta property="og:image" content="{SITE_DOMAIN}/images/favicon.jpeg">
    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{escape(og_title)}">
    <meta name="twitter:description" content="{escape(desc)}">
    <meta name="twitter:image" content="{SITE_DOMAIN}/images/favicon.jpeg">{article_tags}'''


def build_json_ld(page_data, current_path, title, breadcrumbs_html):
    """Build JSON-LD structured data blocks for SEO and AI understanding."""
    blocks = []

    is_home = current_path == '/'

    # 1. WebSite schema (homepage only)
    if is_home:
        blocks.append({
            "@context": "https://schema.org",
            "@type": "WebSite",
            "name": SITE_NAME,
            "url": SITE_DOMAIN,
            "description": SITE_DESCRIPTION,
            "inLanguage": "zh-CN",
            "potentialAction": {
                "@type": "SearchAction",
                "target": f"{SITE_DOMAIN}/?q={{search_term_string}}",
                "query-input": "required name=search_term_string"
            }
        })

    # 2. BlogPosting schema (article pages)
    if not is_home and title:
        ai_pitch = clean_pitch(page_data.get('ai_pitch', ''))
        desc = ai_pitch if ai_pitch and isinstance(ai_pitch, str) else title
        group = CONTENT_GROUP_BY_URL.get(current_path, {})
        section = group.get('title', '')

        article_data = {
            "@context": "https://schema.org",
            "@type": "BlogPosting",
            "headline": title,
            "description": desc[:200],
            "url": f"{SITE_DOMAIN}{current_path}",
            "inLanguage": "zh-CN",
            "author": {
                "@type": "Person",
                "name": SITE_NAME,
                "url": SITE_DOMAIN
            },
            "publisher": {
                "@type": "Person",
                "name": SITE_NAME,
                "url": SITE_DOMAIN
            },
            "mainEntityOfPage": {
                "@type": "WebPage",
                "@id": f"{SITE_DOMAIN}{current_path}"
            },
            "articleSection": section
        }
        blocks.append(article_data)

    # 3. BreadcrumbList schema (if breadcrumbs exist)
    if breadcrumbs_html:
        # Extract breadcrumb items from HTML
        crumb_items = re.findall(r'<a[^>]*href="([^"]*)"[^>]*>([^<]+)</a>', breadcrumbs_html)
        if crumb_items:
            items = []
            for i, (href, text) in enumerate(crumb_items, 1):
                # Resolve relative URLs to absolute
                if href.startswith('../'):
                    href = SITE_DOMAIN + '/' + href.lstrip('../').lstrip('/')
                elif href.startswith('./'):
                    href = SITE_DOMAIN + current_path + href.lstrip('./')
                elif not href.startswith('http'):
                    href = SITE_DOMAIN + '/' + href.lstrip('/')
                items.append({
                    "@type": "ListItem",
                    "position": i,
                    "name": text.strip(),
                    "item": href
                })
            # Add current page as last item
            if title:
                items.append({
                    "@type": "ListItem",
                    "position": len(items) + 1,
                    "name": title,
                    "item": f"{SITE_DOMAIN}{current_path}"
                })
            if items:
                blocks.append({
                    "@context": "https://schema.org",
                    "@type": "BreadcrumbList",
                    "itemListElement": items
                })

    if not blocks:
        return ''

    json_blocks = '\n'.join(
        f'    <script type="application/ld+json">{json.dumps(b, ensure_ascii=False)}</script>'
        for b in blocks
    )
    return json_blocks


def generate_robots_txt():
    """Generate robots.txt that welcomes search engines and AI crawlers."""
    lines = [
        '# robots.txt for www.yijunjun.asia',
        '# Search engine crawlers - all welcome',
        'User-agent: *',
        'Allow: /',
        '',
        '# AI model crawlers - explicitly welcomed',
        'User-agent: GPTBot',
        'Allow: /',
        '',
        'User-agent: Claude-Web',
        'Allow: /',
        '',
        'User-agent: PerplexityBot',
        'Allow: /',
        '',
        'User-agent: CCBot',
        'Allow: /',
        '',
        'User-agent: Google-Extended',
        'Allow: /',
        '',
        'User-agent: Bytespider',
        'Allow: /',
        '',
        'User-agent: Diffbot',
        'Allow: /',
        '',
        'User-agent: cohere-ai',
        'Allow: /',
        '',
        '# Block resource files from indexing (save crawl budget)',
        'Disallow: /css/',
        'Disallow: /js/',
        '',
        '# Sitemaps',
        f'Sitemap: {SITE_DOMAIN}/sitemap.xml',
    ]
    return '\n'.join(lines) + '\n'


def generate_llms_txt(pages):
    """Generate llms.txt - LLM-friendly site description (per llmstxt.org)."""
    # Group pages by content group for structured listing
    lines = [
        f'# {SITE_NAME}',
        '',
        f'> {SITE_DESCRIPTION}',
        '',
        f'',
        f'{SITE_NAME} is a technical blog by a senior developer with 20+ years of experience.',
        f'Content covers Go programming, cloud-native architecture, AI/LLM, databases,',
        f'development tools, and software engineering best practices.',
        f'All articles are in Chinese (Simplified) and include code examples and architecture diagrams.',
        '',
        '## Content Groups',
        '',
    ]

    for g in CONTENT_GROUPS:
        icon = g.get('icon', '')
        title = g['title']
        blurb = g.get('blurb', '')
        lines.append(f'### {icon} {title}')
        lines.append(f'{blurb}')
        lines.append('')
        for url in g['pages']:
            page = pages.get(url, {})
            ptitle = page.get('title', '')
            ai_pitch = clean_pitch(page.get('ai_pitch', ''))
            if isinstance(ai_pitch, str) and ai_pitch:
                desc = ai_pitch[:120]
            else:
                desc = ptitle
            if ptitle:
                lines.append(f'- [{ptitle}]({SITE_DOMAIN}{url}): {desc}')
        lines.append('')

    lines.extend([
        '## AI Era Evolution',
        '',
        '- [ChatGPT] launched 2022.11, started the LLM era',
        '- [Function Calling / Tool Use] 2023.06, LLMs can call external tools',
        '- [RAG - Retrieval Augmented Generation] 2023.08, grounding LLMs with external knowledge',
        '- [MCP - Model Context Protocol] 2024.11, standardized tool/data protocol for LLMs',
        '- [Skill] 2025.03, reusable AI capabilities as packaged skills',
        '- [Agent] 2025.06+, autonomous AI agents that plan and execute multi-step tasks',
        '',
        '## About',
        '',
        f'- Site URL: {SITE_DOMAIN}',
        '- Language: Chinese (Simplified, zh-CN)',
        '- Author: 资深码农 (Senior Developer)',
        '- ICP: 粤ICP备2026122855号',
        f'- Articles: {sum(1 for u in pages if u not in ("/", "/categories/", "/tags/"))} technical articles',
        f'- Sitemap: {SITE_DOMAIN}/sitemap.xml',
    ])

    return '\n'.join(lines) + '\n'


def generate_html(page_data, related_html, breadcrumbs_html, page_nav_html,
                  current_path, article_count):
    """Generate a complete content-first HTML page (no side navigation).

    Layout: sticky top header (brand + group quick-nav + search + theme
    toggle) then the article as the main content area.
    """
    title = clean_title(page_data.get('title', ''), current_path)
    # AI-rewritten body wins when present and passes the anchor check;
    # otherwise fall back to the original extracted content.
    raw_content = page_data.get('ai_body') or page_data.get('content', '')
    if page_data.get('ai_body'):
        missing = assert_anchor_ids(page_data.get('content', ''), raw_content)
        if missing:
            raise ValueError(
                f'ai_body \u4e22\u5931\u6807\u9898\u951a\u70b9 id: {sorted(missing)[:8]}')
        o_cnt, n_cnt = assert_code_blocks_preserved(
            page_data.get('content', ''), raw_content)
        if n_cnt < o_cnt:
            raise ValueError(
                f'ai_body \u4ee3\u7801\u5757\u6570\u91cf\u53d8\u5316: {o_cnt} -> {n_cnt}')
    content = clean_content(raw_content)
    content = annotate_mermaid_src(content)
    content = annotate_echart_containers(content)
    prefix = rel_prefix(current_path)

    # Page title for <title> tag
    page_title = '\u8d44\u6df1\u7801\u519c'

    # SEO meta tags and JSON-LD structured data
    meta_tags = build_meta_tags(page_data, current_path, title, prefix)
    json_ld = build_json_ld(page_data, current_path, title, breadcrumbs_html)

    # For homepage, don't show h1 if content has its own structure
    show_h1 = title and current_path != '/'

    h1_html = f'<h1>{escape(title)}</h1>' if show_h1 else ''

    # Article pages use a single centered column: the article is the subject.
    # Related same-group posts render as a bottom strip (not a sticky rail).
    is_home = current_path == '/'
    ai_card_html = render_ai_card(page_data) if not is_home else ''
    wrapper_class = 'home-layout' if is_home else 'article-layout'

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
    window.__renderMermaid = function () {
        var blocks = document.querySelectorAll('#body-content div.mermaid');
        var jobs = Array.prototype.map.call(blocks, function (div, i) {
            var src = div.getAttribute('data-src') || div.textContent || '';
            if (!src.trim()) return Promise.resolve();
            var id = 'mmd-' + i + '-' + Math.random().toString(36).slice(2, 8);
            return mermaid.render(id, src).then(function (res) {
                div.innerHTML = res.svg;
                if (res.bindFunctions) { res.bindFunctions(div); }
                div.setAttribute('data-rendered', '1');
            }).catch(function (err) {
                div.innerHTML = '<pre class="mermaid-error">\u56fe\u8868\u6e32\u67d3\u5931\u8d25\uff1a' + String(err && err.message || err) + '</pre>';
                div.setAttribute('data-rendered', '0');
            });
        });
        return Promise.all(jobs).then(function () {
            document.dispatchEvent(new CustomEvent('mermaid:rendered'));
        });
    };
    mermaid.initialize({ startOnLoad: false, theme: document.documentElement.getAttribute('data-theme') === 'dark' ? 'dark' : 'default', securityLevel: 'loose' });
    window.__renderMermaid();
    </script>
'''

    # Only load ECharts when the page actually contains chart containers
    echart_html = ''
    if 'class="echart-container"' in content or 'class="echart"' in content:
        echart_html = '''    <script src="https://cdnjs.cloudflare.com/ajax/libs/echarts/5.5.0/echarts.min.js"></script>
    <script>
    (function () {
        var containers = document.querySelectorAll('#body-content .echart-container, #body-content .echart');
        if (!containers.length) return;
        var isDark = document.documentElement.getAttribute('data-theme') === 'dark';
        containers.forEach(function (el) {
            var optAttr = el.getAttribute('data-option') || el.textContent || '';
            if (!optAttr.trim()) return;
            try {
                var opt = JSON.parse(optAttr);
                var chart = echarts.init(el, isDark ? 'dark' : null, { renderer: 'canvas' });
                var baseOpt = buildEchartOption(opt, isDark);
                chart.setOption(baseOpt);
                window.addEventListener('resize', function () { chart.resize(); });
                el.setAttribute('data-rendered', '1');
            } catch (e) {
                el.innerHTML = '<pre class="echart-error">\u56fe\u8868\u6e32\u67d3\u5931\u8d25\uff1a' + String(e && e.message || e) + '</pre>';
                el.setAttribute('data-rendered', '0');
            }
        });

        function buildEchartOption(opt, isDark) {
            var textColor = isDark ? '#c9d1d9' : '#333';
            var axisColor = isDark ? '#555' : '#888';
            var splitColor = isDark ? '#30363d' : '#e8e8e8';
            var common = {
                color: ['#00add8', '#dc382d', '#9c27b0', '#2563eb', '#f59e0b', '#10b981', '#ef4444', '#8b5cf6'],
                title: { textStyle: { color: textColor, fontSize: 15, fontWeight: 600 }, subtextStyle: { color: axisColor } },
                legend: { textStyle: { color: textColor }, top: 30 },
                tooltip: { trigger: 'item' },
                grid: { left: '8%', right: '5%', bottom: '8%', top: '18%', containLabel: true }
            };

            if (opt.type === 'radar') {
                return Object.assign(common, {
                    tooltip: { trigger: 'item' },
                    radar: {
                        indicator: opt.indicators || [],
                        shape: 'polygon',
                        splitNumber: 5,
                        axisName: { color: textColor, fontSize: 12 },
                        splitLine: { lineStyle: { color: splitColor } },
                        splitArea: { areaStyle: { color: isDark ? ['rgba(255,255,255,0.02)', 'rgba(255,255,255,0.05)'] : ['rgba(0,0,0,0.02)', 'rgba(0,0,0,0.04)'] } },
                        axisLine: { lineStyle: { color: splitColor } }
                    },
                    series: [{
                        type: 'radar',
                        data: (opt.series || []).map(function (s) {
                            return { name: s.name, value: s.value, areaStyle: { opacity: 0.15 } };
                        })
                    }]
                });
            }

            if (opt.type === 'bar') {
                var categories = opt.categories || [];
                var series = (opt.series || []).map(function (s) {
                    return {
                        name: s.name,
                        type: 'bar',
                        data: s.value,
                        itemStyle: { borderRadius: [4, 4, 0, 0] }
                    };
                });
                return Object.assign(common, {
                    tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
                    xAxis: { type: 'category', data: categories, axisLabel: { color: textColor, fontSize: 11 }, axisLine: { lineStyle: { color: splitColor } } },
                    yAxis: { type: 'value', axisLabel: { color: textColor }, splitLine: { lineStyle: { color: splitColor } } },
                    series: series
                });
            }

            if (opt.type === 'pie') {
                return Object.assign(common, {
                    tooltip: { trigger: 'item', formatter: '{b}: {c} ({d}%)' },
                    series: [{
                        type: 'pie',
                        radius: ['35%', '65%'],
                        center: ['50%', '55%'],
                        data: (opt.series || []).map(function (s) {
                            return { name: s.name, value: s.value };
                        }),
                        label: { color: textColor, fontSize: 12 },
                        emphasis: { itemStyle: { shadowBlur: 10, shadowColor: 'rgba(0,0,0,0.3)' } }
                    }]
                });
            }

            if (opt.type === 'gauge') {
                return Object.assign(common, {
                    tooltip: { show: false },
                    series: [{
                        type: 'gauge',
                        data: opt.series || [],
                        axisLine: { lineStyle: { width: 12 } },
                        detail: { formatter: '{value}%', color: textColor, fontSize: 16 }
                    }]
                });
            }

            if (opt.type === 'line') {
                var cats = opt.categories || [];
                var lseries = (opt.series || []).map(function (s) {
                    return { name: s.name, type: 'line', data: s.value, smooth: true, symbolSize: 6 };
                });
                return Object.assign(common, {
                    tooltip: { trigger: 'axis' },
                    xAxis: { type: 'category', data: cats, axisLabel: { color: textColor, fontSize: 11 }, axisLine: { lineStyle: { color: splitColor } } },
                    yAxis: { type: 'value', axisLabel: { color: textColor }, splitLine: { lineStyle: { color: splitColor } } },
                    series: lseries
                });
            }

            // Fallback: pass option through directly
            return Object.assign(common, opt.option || {});
        }
    })();
    </script>
'''

    # Only load highlight.js when the page actually contains code blocks
    highlight_html = ''
    if '<pre><code' in content:
        highlight_html = '    <script defer src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>'

    html = f'''<!DOCTYPE html>
<html lang="zh" data-theme="light">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="color-scheme" content="light dark">
    <link rel="icon" href="/images/favicon.jpeg" type="image/jpeg">
    <title>{page_title}</title>
    <link rel="preconnect" href="https://cdnjs.cloudflare.com" crossorigin>
    <link rel="stylesheet" href="/css/style.css">
    {meta_tags}
    {json_ld}
</head>
<body>
    <div class="reading-progress"></div>

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
                {ai_card_html}
                {content}
                {page_nav_html}
                {related_html}
            </main>
        </div>
    </div>

    <footer class="site-footer">
        <p class="footer-icp">
            <a href="https://beian.miit.gov.cn/" target="_blank" rel="noopener noreferrer">粤ICP备2026122855号</a>
        </p>
    </footer>

    <button class="back-to-top" title="\u56de\u5230\u9876\u90e8">\u2191</button>

    {highlight_html}
    {mermaid_html}
    {echart_html}
    <script>window.SITE_BASE = "{prefix}";window.SITE_GROUP = "{site_group}";</script>
    <script src="/js/main.js" defer></script>
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

        # Get full text content (strip HTML tags and entities).
        # Prefer the AI-rewritten body so search matches the quality copy.
        content = page.get('ai_body') or page.get('content', '')
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

    # Generate sitemap.xml with lastmod
    print("Generating sitemap...")
    import datetime
    today = datetime.date.today().isoformat()
    with open(BASE_DIR / 'sitemap.xml', 'w', encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for url in sorted(pages.keys()):
            priority = '1.0' if url == '/' else '0.8'
            f.write(f'  <url><loc>{SITE_DOMAIN}{url}</loc><lastmod>{today}</lastmod><changefreq>weekly</changefreq><priority>{priority}</priority></url>\n')
        f.write('</urlset>\n')
    print(f"  Saved sitemap: {len(pages)} urls (with lastmod, changefreq, priority)")

    # Generate robots.txt
    print("Generating robots.txt...")
    with open(BASE_DIR / 'robots.txt', 'w', encoding='utf-8') as f:
        f.write(generate_robots_txt())
    print("  Saved robots.txt (AI crawlers welcomed)")

    # Generate llms.txt
    print("Generating llms.txt...")
    with open(BASE_DIR / 'llms.txt', 'w', encoding='utf-8') as f:
        f.write(generate_llms_txt(pages))
    print("  Saved llms.txt (LLM-friendly site description)")

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
