/* ============================================
   Main JavaScript
   Theme toggle, sidebar, search, code highlight
   ============================================ */
(function () {
    'use strict';

    // === Theme Toggle ===
    function initTheme() {
        var saved = localStorage.getItem('blog-theme');
        var prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        var theme = saved || (prefersDark ? 'dark' : 'light');
        document.documentElement.setAttribute('data-theme', theme);

        var toggle = document.querySelector('.theme-toggle');
        if (toggle) {
            toggle.addEventListener('click', function () {
                var current = document.documentElement.getAttribute('data-theme');
                var next = current === 'dark' ? 'light' : 'dark';
                document.documentElement.setAttribute('data-theme', next);
                localStorage.setItem('blog-theme', next);
                // Re-init mermaid with new theme
                if (window.mermaid) {
                    window.mermaid.initialize({
                        startOnLoad: false,
                        theme: next === 'dark' ? 'dark' : 'default'
                    });
                    window.mermaid.run();
                }
            });
        }
    }

    // === Header Navigation: highlight current semantic group ===
    function initHeaderNav() {
        var currentGroup = window.SITE_GROUP || '';
        var links = document.querySelectorAll('.header-nav a[data-group]');
        links.forEach(function (link) {
            if (link.getAttribute('data-group') === currentGroup) {
                link.classList.add('active');
            }
        });
    }

    // === Code Copy Buttons ===
    function initCodeCopy() {
        var pres = document.querySelectorAll('#body-content pre');
        pres.forEach(function (pre) {
            // Skip if already has a copy button
            if (pre.querySelector('.code-copy-btn')) return;

            var btn = document.createElement('button');
            btn.className = 'code-copy-btn';
            btn.textContent = '复制';
            btn.addEventListener('click', function () {
                var code = pre.querySelector('code');
                if (!code) return;
                var text = code.textContent;
                
                // Use clipboard API
                if (navigator.clipboard) {
                    navigator.clipboard.writeText(text).then(function () {
                        btn.textContent = '已复制';
                        btn.classList.add('copied');
                        setTimeout(function () {
                            btn.textContent = '复制';
                            btn.classList.remove('copied');
                        }, 2000);
                    });
                } else {
                    // Fallback
                    var textarea = document.createElement('textarea');
                    textarea.value = text;
                    document.body.appendChild(textarea);
                    textarea.select();
                    try {
                        document.execCommand('copy');
                        btn.textContent = '已复制';
                        btn.classList.add('copied');
                        setTimeout(function () {
                            btn.textContent = '复制';
                            btn.classList.remove('copied');
                        }, 2000);
                    } catch (e) {}
                    document.body.removeChild(textarea);
                }
            });
            pre.appendChild(btn);
        });
    }

    // === Code Highlighting ===
    function initHighlight() {
        if (window.hljs) {
            document.querySelectorAll('#body-content pre code').forEach(function (block) {
                try {
                    window.hljs.highlightElement(block);
                } catch (e) {
                    // Ignore errors for unknown languages
                }
                addCodeLangLabel(block);
            });
        }
    }

    // Shell-family languages rendered with the classic terminal look
    var SHELL_LANGS = ['bash', 'sh', 'shell', 'bashrc', 'zsh', 'console', 'terminal'];

    // === Code block language label ===
    function addCodeLangLabel(codeBlock) {
        var pre = codeBlock.closest('pre');
        if (!pre || pre.querySelector('.code-lang')) return;

        var lang = '';
        var cls = codeBlock.className || '';
        var m = cls.match(/language-([\w+-]+)/);
        if (m) lang = m[1];

        // Fallback to highlighted hljs class
        if (!lang && codeBlock.classList.contains('hljs')) {
            var langCls = codeBlock.getAttribute('data-highlighted');
            // hljs sets a data-highlighted="yes" attribute; language lives in
            // the language-* class carried over, so nothing more to do here.
        }

        if (!lang) return;

        // Shell-family blocks get the classic terminal look
        if (SHELL_LANGS.indexOf(lang.toLowerCase()) !== -1) {
            pre.classList.add('pre--shell');
        }

        var label = document.createElement('span');
        label.className = 'code-lang';
        label.textContent = lang;
        pre.appendChild(label);
    }

    // === Mermaid ===
    // Mermaid rendering is owned by the per-page <script type="module">
    // injected by the generator (defers until after DOM parse, runs before
    // DOMContentLoaded). Keep this stub out to avoid double rendering.

    // === Search ===
    var searchIndex = null;
    function initSearch() {
        var input = document.getElementById('search-input');
        var results = document.getElementById('search-results');
        if (!input || !results) return;

        var debounceTimer = null;

        input.addEventListener('input', function () {
            var query = input.value.trim().toLowerCase();
            clearTimeout(debounceTimer);

            if (query.length < 1) {
                results.classList.remove('active');
                return;
            }

            debounceTimer = setTimeout(function () {
                var base = window.SITE_BASE || '';
                if (!searchIndex) {
                    // Load search index
                    fetch(base + 'search-index.json')
                        .then(function (r) { return r.json(); })
                        .then(function (data) {
                            searchIndex = data;
                            performSearch(query, results);
                        })
                        .catch(function () {});
                } else {
                    performSearch(query, results);
                }
            }, 200);
        });

        // Close search on outside click
        document.addEventListener('click', function (e) {
            if (!e.target.closest('.header-search')) {
                results.classList.remove('active');
            }
        });
    }

    function performSearch(query, resultsEl) {
        var matches = [];
        searchIndex.forEach(function (item) {
            if (item.title.toLowerCase().indexOf(query) !== -1 ||
                (item.text && item.text.toLowerCase().indexOf(query) !== -1)) {
                matches.push(item);
            }
        });

        if (matches.length === 0) {
            resultsEl.innerHTML = '<div class="search-result-item">无搜索结果</div>';
        } else {
            var base = window.SITE_BASE || '';
            resultsEl.innerHTML = matches.slice(0, 15).map(function (item) {
                // Directory-style urls (e.g. /python/) need explicit index.html
                // for the local file:// protocol to resolve them. The site
                // root (item.url === '/') also resolves to index.html.
                var path = item.url.replace(/^\//, '');
                if (!path) {
                    path = 'index.html';
                } else if (path.charAt(path.length - 1) === '/') {
                    path += 'index.html';
                }
                var url = base + path;
                return '<a class="search-result-item" href="' + url + '">' + item.title + '</a>';
            }).join('');
        }
        resultsEl.classList.add('active');
    }

    // === Back to top ===
    function initBackToTop() {
        var btn = document.querySelector('.back-to-top');
        if (!btn) return;
        window.addEventListener('scroll', function () {
            if (window.scrollY > 400) {
                btn.style.display = 'flex';
            } else {
                btn.style.display = 'none';
            }
        });
        btn.addEventListener('click', function () {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    // === Init all ===
    function init() {
        initTheme();
        initHeaderNav();
        initCodeCopy();
        initHighlight();
        initSearch();
        initBackToTop();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
