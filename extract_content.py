#!/usr/bin/env python3
"""Extract content and navigation from old Hugo-generated HTML files."""

import os
import re
import json
import html as html_module
from pathlib import Path

BASE_DIR = Path(__file__).parent


def extract_navigation(html_text):
    """Extract sidebar navigation tree from <ul class="topics">."""
    nav_items = []
    # Find all <li data-nav-id="..." title="..."> with their <a href="..." >text</a>
    pattern = re.compile(
        r'<li\s+data-nav-id="([^"]*)"\s+title="([^"]*)"[^>]*>\s*'
        r'<a\s+href="([^"]*)"[^>]*>\s*(.*?)\s*</a>',
        re.DOTALL
    )
    for match in pattern.finditer(html_text):
        nav_id = match.group(1)
        title = match.group(2)
        href = match.group(3)
        text = re.sub(r'<[^>]+>', '', match.group(4)).strip()
        nav_items.append({
            'nav_id': nav_id,
            'title': title,
            'href': href,
            'text': text,
        })
    return nav_items


def decode_entities(text):
    """Decode HTML entities."""
    return html_module.unescape(text)


def clean_code_blocks(content):
    """Convert Hugo chroma highlighted code blocks to clean <pre><code> format."""
    def replace_code_block(m):
        full = m.group(0)
        # Extract language
        lang_match = re.search(r'class="language-([^"]+)"', full)
        lang = lang_match.group(1) if lang_match else ''
        
        # Extract code content: everything inside <code ...>...</code>
        code_match = re.search(r'<code[^>]*>(.*?)</code>', full, re.DOTALL)
        if not code_match:
            return full
        code_html = code_match.group(1)
        
        # Remove all <span ...> tags, keep text
        code_text = re.sub(r'<span[^>]*>', '', code_html)
        code_text = code_text.replace('</span>', '')
        
        # Decode HTML entities
        code_text = decode_entities(code_text)
        
        # Clean up trailing whitespace per line but preserve newlines
        lines = code_text.split('\n')
        lines = [line.rstrip() for line in lines]
        # Remove leading/trailing empty lines
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()
        code_text = '\n'.join(lines)
        
        # Escape for HTML
        code_text = code_text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        
        lang_class = f' class="language-{lang}"' if lang else ''
        return f'<pre><code{lang_class}>{code_text}</code></pre>'
    
    # Match <div class="highlight">...</div>
    content = re.sub(
        r'<div class="highlight">.*?</div>',
        replace_code_block,
        content,
        flags=re.DOTALL
    )
    return content


def clean_hr_tags(content):
    """Convert <hr> to clean <hr>."""
    return re.sub(r'<hr\s*/?>', '<hr>', content)


def clean_img_tags(content):
    """Ensure img tags are clean and have alt text."""
    # Fix <img src="..." alt="..."></img> -> <img src="..." alt="...">
    content = re.sub(r'</img>', '', content)
    return content


def extract_page_content(html_text):
    """Extract body-inner content from a page."""
    # Find <div id="body-inner">
    start = html_text.find('<div id="body-inner">')
    if start == -1:
        return '', ''
    
    # Find the end: <footer class="footline"> or closing divs
    end_markers = [
        '<footer class="footline">',
        '</div>\n\n</div>\n\n<div id="navigation">',
        '</div>\n        </div>\n        <div id="navigation">',
    ]
    end = len(html_text)
    for marker in end_markers:
        pos = html_text.find(marker, start)
        if pos != -1 and pos < end:
            end = pos
    
    content = html_text[start:end]
    
    # Remove the outer <div id="body-inner"> wrapper
    content = content.replace('<div id="body-inner">', '', 1)
    # Remove trailing </div> tags that were part of the wrapper
    content = content.rstrip()
    if content.endswith('</div>'):
        content = content[:-6].rstrip()
    
    # Extract title from <h1>
    title_match = re.search(r'<h1[^>]*>\s*(.*?)\s*</h1>', content, re.DOTALL)
    title = ''
    if title_match:
        title = re.sub(r'<[^>]+>', '', title_match.group(1)).strip()
        # Remove the h1 from content (we'll add it back in the template)
        content = re.sub(r'<h1[^>]*>\s*.*?\s*</h1>', '', content, count=1, flags=re.DOTALL)
    
    # Clean up content
    content = content.strip()
    
    # Clean code blocks
    content = clean_code_blocks(content)
    
    # Clean other tags
    content = clean_hr_tags(content)
    content = clean_img_tags(content)
    
    # Remove leading <hr> if present
    content = re.sub(r'^<hr>\s*', '', content)
    
    return title, content


def find_all_pages():
    """Find all index.html files and their paths."""
    pages = []
    for root, dirs, files in os.walk(BASE_DIR):
        # Skip .git, node_modules, etc.
        parts = Path(root).relative_to(BASE_DIR).parts
        if any(p in ['.git', 'node_modules', '__pycache__'] for p in parts):
            continue
        if 'index.html' in files:
            filepath = Path(root) / 'index.html'
            rel_path = filepath.relative_to(BASE_DIR)
            # URL path: /dir/ or / for root
            if rel_path.parent == Path('.'):
                url_path = '/'
            else:
                url_path = '/' + str(rel_path.parent).replace(os.sep, '/') + '/'
            pages.append({
                'filepath': str(filepath),
                'rel_path': str(rel_path),
                'url_path': url_path,
            })
    return pages


def main():
    # Find all pages
    pages = find_all_pages()
    print(f"Found {len(pages)} pages")
    
    # Extract navigation from the homepage (it has the full sidebar)
    homepage = BASE_DIR / 'index.html'
    with open(homepage, 'r', encoding='utf-8') as f:
        home_html = f.read()
    nav_tree = extract_navigation(home_html)
    print(f"Extracted {len(nav_tree)} nav items")
    
    # Extract content from each page
    page_data = {}
    for page in pages:
        filepath = page['filepath']
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                html_text = f.read()
            title, content = extract_page_content(html_text)
            page_data[page['url_path']] = {
                'title': title,
                'content': content,
                'filepath': page['filepath'],
                'rel_path': page['rel_path'],
                'url_path': page['url_path'],
                'content_length': len(content),
            }
            print(f"  {page['url_path']:<40} title={title:<25} len={len(content)}")
        except Exception as e:
            print(f"  ERROR {page['url_path']}: {e}")
            page_data[page['url_path']] = {
                'title': '',
                'content': '',
                'filepath': page['filepath'],
                'rel_path': page['rel_path'],
                'url_path': page['url_path'],
                'content_length': 0,
                'error': str(e),
            }
    
    # Save to JSON
    output = {
        'navigation': nav_tree,
        'pages': page_data,
    }
    output_file = BASE_DIR / 'extracted_content.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"\nSaved to {output_file}")
    
    # Print summary
    total_content = sum(p['content_length'] for p in page_data.values())
    empty_pages = [url for url, p in page_data.items() if p['content_length'] < 500]
    print(f"\nTotal content: {total_content} chars across {len(page_data)} pages")
    print(f"Pages with <500 chars content (need filling): {len(empty_pages)}")
    for url in empty_pages:
        print(f"  {url}")


if __name__ == '__main__':
    main()
