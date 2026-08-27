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
                // Re-init mermaid with new theme, then re-render every
                // diagram from data-src (mermaid.render replaces div
                // content; reading textContent would hit stale SVG).
                if (window.mermaid && window.__renderMermaid) {
                    window.mermaid.initialize({
                        startOnLoad: false,
                        theme: next === 'dark' ? 'dark' : 'default'
                    });
                    window.__renderMermaid();
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

    // === Code Copy & Fold Buttons ===
    var copyText = '复制';
    var foldText = '折叠';
    var unfoldText = '展开';

    function setCopied(btn) {
        btn.textContent = '已复制';
        btn.classList.add('copied');
        setTimeout(function () {
            btn.textContent = copyText;
            btn.classList.remove('copied');
        }, 2000);
    }

    function copyString(text, btn) {
        if (navigator.clipboard) {
            navigator.clipboard.writeText(text).then(function () {
                setCopied(btn);
            });
        } else {
            // Fallback
            var textarea = document.createElement('textarea');
            textarea.value = text;
            document.body.appendChild(textarea);
            textarea.select();
            try {
                document.execCommand('copy');
                setCopied(btn);
            } catch (e) {}
            document.body.removeChild(textarea);
        }
    }

    function makeFoldBtn(container) {
        var btn = document.createElement('button');
        btn.className = 'code-copy-btn code-fold-btn';
        btn.textContent = foldText;
        btn.addEventListener('click', function () {
            var collapsed = container.classList.toggle('collapsed');
            btn.textContent = collapsed ? unfoldText : foldText;
        });
        return btn;
    }

    // Mermaid blocks: copy the raw source and fold the diagram. The page
    // module script renders them before main.js runs (and re-renders on
    // theme switch), wiping div content, so the tools are attached here AND
    // re-attached on the 'mermaid:rendered' event (idempotent).
    function initMermaidTools() {
        var blocks = document.querySelectorAll('#body-content div.mermaid');
        blocks.forEach(function (div) {
            if (div.querySelector('.code-copy-btn')) return;

            var btn = document.createElement('button');
            btn.className = 'code-copy-btn mermaid-btn';
            btn.textContent = copyText;
            btn.addEventListener('click', function () {
                var src = div.getAttribute('data-src') || div.textContent;
                copyString(src, btn);
            });
            div.appendChild(btn);

            div.appendChild(makeFoldBtn(div));
        });
    }

    function initCodeCopy() {
        var pres = document.querySelectorAll('#body-content pre');
        pres.forEach(function (pre) {
            // Skip if already handled
            if (pre.querySelector('.code-copy-btn')) return;

            var btn = document.createElement('button');
            btn.className = 'code-copy-btn';
            btn.textContent = copyText;
            btn.addEventListener('click', function () {
                var code = pre.querySelector('code');
                if (!code) return;
                copyString(code.textContent, btn);
            });
            pre.appendChild(btn);

            pre.appendChild(makeFoldBtn(pre));
        });

        // First paint: if the module script already rendered, tools land on
        // the svg; otherwise the 'mermaid:rendered' event re-attaches them.
        initMermaidTools();
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

    // === Homepage journey timeline: scroll-in reveal ===
    function initTimeline() {
        var section = document.querySelector('.timeline-section');
        if (!section) return;

        // Gate the hidden state behind JS so no-JS visitors see content
        section.classList.add('js-anim');

        var reveal = function () {
            section.classList.add('in-view');
        };

        if (!('IntersectionObserver' in window)) {
            reveal();
            return;
        }

        var observer = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                // Start the reveal once a meaningful chunk is visible
                if (entry.isIntersecting && entry.intersectionRatio >= 0.08) {
                    reveal();
                    observer.disconnect();
                }
            });
        }, { threshold: [0.08, 0.3, 0.6], rootMargin: '0px 0px -60px 0px' });
        observer.observe(section);
    }

    // === Reading Progress Bar ===
    function initReadingProgress() {
        var bar = document.querySelector('.reading-progress');
        if (!bar) return;
        var ticking = false;
        function update() {
            var h = document.documentElement;
            var scrollPercent = (h.scrollTop / (h.scrollHeight - h.clientHeight)) * 100;
            bar.style.width = Math.min(100, Math.max(0, scrollPercent)) + '%';
            ticking = false;
        }
        window.addEventListener('scroll', function () {
            if (!ticking) {
                window.requestAnimationFrame(update);
                ticking = true;
            }
        }, { passive: true });
        update();
    }

    // === Scroll Reveal: fade-in elements as they enter viewport ===
    function initScrollReveal() {
        if (!('IntersectionObserver' in window)) return;
        var body = document.getElementById('body-content');
        if (!body) return;

        // Select elements to animate
        var selectors = [
            '#body-content > h2',
            '#body-content > h3',
            '#body-content > p',
            '#body-content > ul',
            '#body-content > ol',
            '#body-content > pre',
            '#body-content > blockquote',
            '#body-content > table',
            '#body-content > .mermaid',
            '#body-content > img',
            '#body-content > hr',
            '#body-content > .callout',
            '#body-content > .gradient-divider'
        ];
        var els = document.querySelectorAll(selectors.join(', '));

        // Skip first h1 and first few elements (above the fold)
        var observer = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.08,
            rootMargin: '0px 0px -40px 0px'
        });

        els.forEach(function (el, idx) {
            // Don't animate elements that are already in viewport on load
            var rect = el.getBoundingClientRect();
            if (rect.top < window.innerHeight && rect.bottom > 0) {
                return;
            }
            el.classList.add('reveal');
            observer.observe(el);
        });
    }

    // === Auto Table of Contents ===
    function initAutoTOC() {
        var body = document.getElementById('body-content');
        if (!body) return;
        // Only generate TOC for article pages with enough headings
        var headings = body.querySelectorAll('h2, h3, h4');
        if (headings.length < 4) return;

        // Skip if a TOC already exists
        if (body.querySelector('.auto-toc')) return;

        var toc = document.createElement('nav');
        toc.className = 'auto-toc';
        toc.innerHTML = '<div class="auto-toc-title">\u76ee\u5f55</div>';

        var list = document.createElement('ul');
        var currentLevel = 0;
        var currentList = list;
        var stack = [list];

        headings.forEach(function (h) {
            var level = parseInt(h.tagName[1]);
            var id = h.getAttribute('id');
            if (!id) return;

            while (stack.length > 1 && level <= parseInt(stack[stack.length - 1].dataset.level || '2')) {
                stack.pop();
            }

            var li = document.createElement('li');
            li.className = 'toc-h' + level;
            var a = document.createElement('a');
            a.href = '#' + id;
            a.textContent = h.textContent.replace(/^\d+\.\s*/, '');
            a.addEventListener('click', function (e) {
                e.preventDefault();
                var target = document.getElementById(this.getAttribute('href').slice(1));
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            });
            li.appendChild(a);

            if (level > currentLevel && stack[stack.length - 1].children.length > 0) {
                var newList = document.createElement('ul');
                newList.dataset.level = level;
                stack[stack.length - 1].lastElementChild.appendChild(newList);
                stack.push(newList);
                newList.appendChild(li);
            } else {
                stack[stack.length - 1].appendChild(li);
            }
            currentLevel = level;
        });

        toc.appendChild(list);

        // Insert after the h1 or AI card, whichever comes first
        var h1 = body.querySelector('h1');
        var aiCard = body.querySelector('.ai-card');
        var insertBefore = null;
        if (h1 && h1.nextElementSibling) {
            insertBefore = h1.nextElementSibling;
        } else if (aiCard && aiCard.nextElementSibling) {
            insertBefore = aiCard.nextElementSibling;
        }
        if (insertBefore) {
            body.insertBefore(toc, insertBefore);
        } else {
            body.insertBefore(toc, body.firstChild);
        }
    }

    // === Heading anchor copy on click ===
    function initHeadingAnchors() {
        var headings = document.querySelectorAll('#body-content h2[id], #body-content h3[id]');
        headings.forEach(function (h) {
            if (h.querySelector('.anchor-link')) return;
            h.style.cursor = 'pointer';
            h.title = '点击复制锚点链接';
            var anchor = document.createElement('span');
            anchor.className = 'anchor-link';
            anchor.textContent = '#';
            anchor.style.cssText = 'opacity:0;transition:opacity 0.3s;margin-left:0.4em;color:var(--accent);font-weight:400;';
            h.appendChild(anchor);
            h.addEventListener('mouseenter', function () { anchor.style.opacity = '1'; });
            h.addEventListener('mouseleave', function () { anchor.style.opacity = '0'; });
            h.addEventListener('click', function () {
                var id = h.getAttribute('id');
                if (!id) return;
                var url = location.origin + location.pathname + '#' + id;
                if (navigator.clipboard) {
                    navigator.clipboard.writeText(url).then(function () {
                        h.style.transition = 'color 0.3s ease';
                        var origColor = h.style.color;
                        h.style.color = 'var(--accent)';
                        setTimeout(function () { h.style.color = origColor; }, 600);
                    });
                }
            });
        });
    }

    // === Section numbering for h2 ===
    function initSectionNumbers() {
        var h2s = document.querySelectorAll('#body-content h2[id]');
        if (h2s.length < 1) return;
        var idx = 0;
        h2s.forEach(function (h) {
            if (h.textContent.indexOf('同组阅读') !== -1) return;
            var badge = document.createElement('span');
            badge.className = 'section-badge';
            badge.textContent = (idx + 1).toString().padStart(2, '0');
            h.insertBefore(badge, h.firstChild);
            idx++;
        });
    }

    // === Bento card expand/collapse (homepage) ===
    function initBentoExpand() {
        var moreLinks = document.querySelectorAll('.arch-more-link');
        if (!moreLinks.length) return;
        moreLinks.forEach(function (link) {
            link.addEventListener('click', function (e) {
                e.preventDefault();
                var card = link.closest('.arch-card');
                if (!card) return;
                var hiddenList = card.querySelector('.arch-hidden-list');
                if (!hiddenList) return;
                var isHidden = hiddenList.hasAttribute('hidden');
                if (isHidden) {
                    hiddenList.removeAttribute('hidden');
                    link.classList.add('expanded');
                    var span = link.querySelector('span:first-child');
                    if (span) span.textContent = '收起列表';
                } else {
                    hiddenList.setAttribute('hidden', '');
                    link.classList.remove('expanded');
                    var span = link.querySelector('span:first-child');
                    if (span) {
                        var card2 = link.closest('.arch-card');
                        var total = card2 ? card2.querySelectorAll('.arch-item').length : 0;
                        span.textContent = '查看全部';
                    }
                }
            });
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
        initTimeline();
        initReadingProgress();
        initScrollReveal();
        initAutoTOC();
        initHeadingAnchors();
        initSectionNumbers();
        initBentoExpand();
        document.addEventListener('mermaid:rendered', initMermaidTools);
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
