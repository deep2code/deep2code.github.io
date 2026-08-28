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
        var ticking = false;
        function update() {
            if (window.scrollY > 400) {
                btn.style.display = 'flex';
            } else {
                btn.style.display = 'none';
            }
            ticking = false;
        }
        window.addEventListener('scroll', function () {
            if (!ticking) {
                window.requestAnimationFrame(update);
                ticking = true;
            }
        }, { passive: true });
        btn.addEventListener('click', function () {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
        update();
    }

    // === Homepage cinema: 码农进化史循环动画 ===
    function initTimeline() {
        var screen = document.getElementById('cinema-screen');
        if (!screen) return;
        var scenes = screen.querySelectorAll('.cine-scene');
        var bar = document.getElementById('cinema-bar');
        var counter = document.getElementById('cinema-counter');
        var dots = screen.querySelectorAll('.cinema-dot');
        if (!scenes.length) return;

        var total = scenes.length;
        var SCENE_MS = 5000;   // each scene duration
        var current = 0;
        var started = false;
        var sceneTimer = null;

        function setScene(idx) {
            scenes.forEach(function (s, i) {
                s.classList.toggle('active', i === idx);
            });
            dots.forEach(function (d, i) {
                d.classList.toggle('active', i === idx);
            });
            if (counter) counter.textContent = (idx + 1) + ' / ' + total;
            current = idx;
        }

        function runProgress() {
            if (!bar) return;
            // CSS transition handles the animation — no JS timer needed
            bar.style.transition = 'none';
            bar.style.transform = 'scaleX(0)';
            void bar.offsetWidth;  // force reflow to apply reset
            bar.style.transition = '';  // restore CSS-defined 5s linear
            bar.style.transform = 'scaleX(1)';
        }

        function advance() {
            var next = (current + 1) % total;
            setScene(next);
            runProgress();
        }

        function scheduleNext() {
            if (sceneTimer) clearTimeout(sceneTimer);
            sceneTimer = setTimeout(function () {
                advance();
                scheduleNext();
            }, SCENE_MS);
        }

        function start() {
            if (started) return;
            started = true;
            setScene(0);
            runProgress();
            scheduleNext();
        }

        // Allow dot click to jump scenes
        dots.forEach(function (dot) {
            dot.addEventListener('click', function () {
                var idx = parseInt(dot.getAttribute('data-i'), 10);
                if (isNaN(idx)) return;
                setScene(idx);
                runProgress();
                scheduleNext();
            });
        });

        // Start when scrolled into view, pause when scrolled out
        if (!('IntersectionObserver' in window)) {
            start();
            return;
        }
        var observer = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting && entry.intersectionRatio >= 0.15) {
                    if (!started) {
                        start();
                    } else {
                        // Resume: re-activate current scene and restart timers
                        setScene(current);
                        runProgress();
                        scheduleNext();
                    }
                } else if (!entry.isIntersecting && started) {
                    // Pause: clear timer and deactivate scenes to stop CSS animations
                    if (sceneTimer) { clearTimeout(sceneTimer); sceneTimer = null; }
                    if (bar) { bar.style.transition = 'none'; bar.style.transform = 'scaleX(0)'; }
                    scenes.forEach(function (s) { s.classList.remove('active'); });
                }
            });
        }, { threshold: [0, 0.15, 0.3], rootMargin: '0px 0px -40px 0px' });
        observer.observe(screen);
    }

    // === AI ERA 循环动画 ===
    function initAiEra() {
        var anim = document.querySelector('.ae-anim');
        if (!anim) return;
        var nodes = anim.querySelectorAll('.ae-node');
        var line = anim.querySelector('.ae-line');
        if (!nodes.length || !line) return;

        var n = nodes.length;
        var stepMs = 1500;     // 每个节点间隔
        var startMs = 400;     // 首节点延迟
        var holdMs = 2000;     // 最后节点后停留
        var fadeMs = 600;      // 淡出时长
        var pauseMs = 1500;    // 淡出后空白暂停
        var cycleMs = startMs + (n - 1) * stepMs + holdMs + fadeMs + pauseMs;

        var started = false;
        var timers = [];

        function clearTimers() {
            timers.forEach(function (t) { clearTimeout(t); });
            timers = [];
        }

        function cycle() {
            clearTimers();

            // 重置
            nodes.forEach(function (el) {
                el.classList.remove('ae-on', 'ae-off');
            });
            line.classList.remove('ae-on', 'ae-off');

            // 画线
            timers.push(setTimeout(function () {
                line.classList.add('ae-on');
            }, 100));

            // 逐个弹出节点
            nodes.forEach(function (node, i) {
                timers.push(setTimeout(function () {
                    node.classList.add('ae-on');
                }, startMs + i * stepMs));
            });

            // 全部淡出
            var fadeStart = startMs + (n - 1) * stepMs + holdMs;
            timers.push(setTimeout(function () {
                line.classList.add('ae-off');
                nodes.forEach(function (el) {
                    el.classList.remove('ae-on');
                    el.classList.add('ae-off');
                });
            }, fadeStart));
        }

        // 进入视口后启动，离开视口时暂停
        var cycleTimer = null;
        function scheduleCycle() {
            cycleTimer = setTimeout(function () {
                cycle();
                scheduleCycle();
            }, cycleMs);
        }
        var observer = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    if (!started) {
                        started = true;
                    }
                    if (cycleTimer) { clearTimeout(cycleTimer); cycleTimer = null; }
                    cycle();
                    scheduleCycle();
                } else if (started) {
                    if (cycleTimer) { clearTimeout(cycleTimer); cycleTimer = null; }
                    clearTimers();
                }
            });
        }, { threshold: 0.2 });
        observer.observe(anim);
    }

    // === Reading Progress Bar ===
    function initReadingProgress() {
        var bar = document.querySelector('.reading-progress');
        if (!bar) return;
        var ticking = false;
        function update() {
            var h = document.documentElement;
            var scrollPercent = (h.scrollTop / (h.scrollHeight - h.clientHeight)) * 100;
            bar.style.transform = 'scaleX(' + (Math.min(100, Math.max(0, scrollPercent)) / 100) + ')';
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
                var card = link.closest('.group-section');
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
                        var card2 = link.closest('.group-section');
                        var total = card2 ? card2.querySelectorAll('.arch-item').length : 0;
                        span.textContent = '查看全部';
                    }
                }
            });
        });
    }

    // === Terminal Command Typing Animation ===
    function initArchCmd() {
        var cmds = document.querySelectorAll('.arch-cmd');
        if (!cmds.length) return;

        var reduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        var TYPE_SPEED = 32;
        var HOLD_MS = 2200;
        var FADE_MS = 250;

        cmds.forEach(function (cmd) {
            var codeEl = cmd.querySelector('.arch-cmd-text');
            var cursor = cmd.querySelector('.arch-cmd-cursor');
            var copyBtn = cmd.querySelector('.arch-cmd-copy');
            var countEl = cmd.querySelector('.arch-cmd-count');
            if (!codeEl) return;

            var raw = cmd.getAttribute('data-cmds');
            var commands = [];
            try { commands = JSON.parse(raw); } catch (e) {}
            if (!commands || !commands.length) return;
            var total = commands.length;
            var idx = 0;
            var started = false;
            var timer = null;

            function setCursorState(state) {
                if (!cursor) return;
                cursor.classList.remove('running', 'typing', 'done', 'holding');
                if (state) cursor.classList.add(state);
            }

            function updateCount() {
                if (countEl) countEl.textContent = (idx + 1) + '/' + total;
            }

            function showAll() {
                codeEl.textContent = commands[idx];
                setCursorState('done');
                if (copyBtn) copyBtn.classList.add('show');
                updateCount();
            }

            function typeCommand() {
                var text = commands[idx];
                updateCount();
                if (reduced) {
                    codeEl.textContent = text;
                    setCursorState('holding');
                    if (copyBtn) copyBtn.classList.add('show');
                    timer = setTimeout(nextCommand, HOLD_MS);
                    return;
                }
                setCursorState('running');
                codeEl.textContent = '';
                var i = 0;
                function typeNext() {
                    if (i < text.length) {
                        codeEl.textContent += text[i];
                        i++;
                        timer = setTimeout(typeNext, TYPE_SPEED);
                    } else {
                        setCursorState('holding');
                        if (copyBtn) copyBtn.classList.add('show');
                        timer = setTimeout(nextCommand, HOLD_MS);
                    }
                }
                typeNext();
            }

            function nextCommand() {
                idx = (idx + 1) % total;
                if (reduced) {
                    typeCommand();
                    return;
                }
                codeEl.classList.add('fading');
                timer = setTimeout(function () {
                    codeEl.textContent = '';
                    codeEl.classList.remove('fading');
                    typeCommand();
                }, FADE_MS);
            }

            function start() {
                if (started) return;
                started = true;
                typeCommand();
            }

            function pause() {
                if (timer) { clearTimeout(timer); timer = null; }
            }

            if (copyBtn) {
                copyBtn.addEventListener('click', function (e) {
                    e.stopPropagation();
                    copyString(commands[idx], copyBtn);
                });
            }

            if (!('IntersectionObserver' in window)) {
                showAll();
                return;
            }
            var observer = new IntersectionObserver(function (entries) {
                entries.forEach(function (entry) {
                    if (entry.isIntersecting) {
                        start();
                    } else {
                        pause();
                    }
                });
            }, { threshold: 0.3 });
            observer.observe(cmd);
        });
    }

    // === Card click navigation ===
    function initCardClick() {
        var cards = document.querySelectorAll('.arch-tech-card[data-href]');
        cards.forEach(function (card) {
            card.addEventListener('click', function (e) {
                if (e.target.closest('.arch-cmd-copy')) return;
                if (e.target.closest('a')) return;
                var href = card.getAttribute('data-href');
                if (href) window.location.href = href;
            });
            card.addEventListener('keydown', function (e) {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    var href = card.getAttribute('data-href');
                    if (href) window.location.href = href;
                }
            });
        });
    }

    // === AI Impact Slider (PPT-style carousel) ===
    function initAiImpact() {
        var slider = document.getElementById('ai-impact-slider');
        if (!slider) return;
        var track = slider.querySelector('.ai-impact-track');
        var slides = slider.querySelectorAll('.ai-impact-slide');
        var dots = slider.querySelectorAll('.ai-impact-dot');
        var prevBtn = slider.querySelector('.ai-impact-prev');
        var nextBtn = slider.querySelector('.ai-impact-next');
        var bar = document.getElementById('ai-impact-bar');
        var counter = document.getElementById('ai-impact-counter');
        if (!slides.length || !track) return;

        var total = slides.length;
        var SLIDE_MS = 5000;
        var current = 0;
        var started = false;
        var slideTimer = null;
        var reduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

        function go(idx) {
            current = (idx + total) % total;
            track.style.transform = 'translateX(-' + (current * 100) + '%)';
            dots.forEach(function (d, i) { d.classList.toggle('active', i === current); });
            if (counter) counter.textContent = (current + 1) + ' / ' + total;
            if (bar) {
                bar.style.transition = 'none';
                bar.style.transform = 'scaleX(0)';
                void bar.offsetWidth;
                if (reduced) {
                    bar.style.transition = 'none';
                    bar.style.transform = 'scaleX(1)';
                } else {
                    bar.style.transition = '';
                    bar.style.transform = 'scaleX(1)';
                }
            }
        }

        function next() { go(current + 1); }
        function prev() { go(current - 1); }

        function scheduleAuto() {
            if (slideTimer) clearTimeout(slideTimer);
            slideTimer = setTimeout(function () {
                next();
                scheduleAuto();
            }, SLIDE_MS);
        }

        function start() {
            if (started) return;
            started = true;
            go(0);
            scheduleAuto();
        }

        function pause() {
            if (slideTimer) { clearTimeout(slideTimer); slideTimer = null; }
            if (bar) { bar.style.transition = 'none'; bar.style.transform = 'scaleX(0)'; }
        }

        // Null-safe event listeners
        if (nextBtn) nextBtn.addEventListener('click', function () { next(); scheduleAuto(); });
        if (prevBtn) prevBtn.addEventListener('click', function () { prev(); scheduleAuto(); });
        dots.forEach(function (dot) {
            dot.addEventListener('click', function () {
                go(parseInt(dot.getAttribute('data-i'), 10) || 0);
                scheduleAuto();
            });
        });

        // Start when scrolled into view, pause when scrolled out
        if (!('IntersectionObserver' in window)) {
            start();
            return;
        }

        var observer = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting && entry.intersectionRatio > 0.05) {
                    if (!started) {
                        start();
                    } else {
                        go(current);
                        scheduleAuto();
                    }
                } else if (!entry.isIntersecting && started) {
                    pause();
                }
            });
        }, { threshold: [0, 0.05, 0.2, 0.5], rootMargin: '0px 0px -30px 0px' });
        observer.observe(slider);

        // Fallback: start after 1.5s if observer hasn't fired yet
        // (covers edge cases where slider is in a weird viewport position)
        setTimeout(function () {
            if (!started) {
                var rect = slider.getBoundingClientRect();
                if (rect.top < window.innerHeight && rect.bottom > 0) {
                    start();
                }
            }
        }, 1500);

        // Hover pause/resume
        slider.addEventListener('mouseenter', function () {
            if (slideTimer) { clearTimeout(slideTimer); slideTimer = null; }
            if (bar) { bar.style.transition = 'none'; }
        });
        slider.addEventListener('mouseleave', function () {
            if (started) { go(current); scheduleAuto(); }
        });

        // Touch swipe support
        var touchStartX = 0;
        var touchStartY = 0;
        slider.addEventListener('touchstart', function (e) {
            touchStartX = e.touches[0].clientX;
            touchStartY = e.touches[0].clientY;
        }, { passive: true });
        slider.addEventListener('touchend', function (e) {
            var dx = e.changedTouches[0].clientX - touchStartX;
            var dy = e.changedTouches[0].clientY - touchStartY;
            if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy)) {
                if (dx > 0) prev(); else next();
                scheduleAuto();
            }
        }, { passive: true });
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
        initAiEra();
        initReadingProgress();
        initScrollReveal();
        initAutoTOC();
        initHeadingAnchors();
        initSectionNumbers();
        initBentoExpand();
        initCardClick();
        initArchCmd();
        initAiImpact();
        document.addEventListener('mermaid:rendered', initMermaidTools);
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
