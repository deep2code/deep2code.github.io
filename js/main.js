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
            // 使用 DOM API 构建，避免 innerHTML XSS
            resultsEl.innerHTML = '';
            matches.slice(0, 15).forEach(function (item) {
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
                var a = document.createElement('a');
                a.className = 'search-result-item';
                a.href = url;
                a.textContent = item.title;
                resultsEl.appendChild(a);
            });
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

        // Fallback: start after 1.5s if observer hasn't fired
        setTimeout(function () {
            if (!started) {
                started = true;
                cycle();
                scheduleCycle();
            }
        }, 1500);
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
            var fallbackTimer = null;
            var isVisible = false;

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
                isVisible = true;
                if (fallbackTimer) { clearTimeout(fallbackTimer); fallbackTimer = null; }
                typeCommand();
            }

            function resume() {
                if (!started || isVisible) return;
                isVisible = true;
                typeCommand();
            }

            function pause() {
                isVisible = false;
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
                        if (started) resume();
                        else start();
                    } else {
                        pause();
                    }
                });
            }, { threshold: 0.1, rootMargin: '0px 0px 50px 0px' });
            observer.observe(cmd);

            // Fallback: start after 1.5s if IntersectionObserver hasn't fired.
            // This handles content-visibility:auto containers where the
            // observer may not report correct intersection for children.
            fallbackTimer = setTimeout(function () {
                if (!started) {
                    start();
                }
            }, 1500);
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
        if (!track || !slides.length) return;

        var total = slides.length;
        var SLIDE_MS = 5000;
        var current = 0;
        var timer = null;

        function go(idx) {
            current = ((idx % total) + total) % total;
            track.style.transform = 'translateX(-' + (current * 100) + '%)';
            slider.querySelectorAll('.ai-impact-dot').forEach(function (d, i) {
                d.classList.toggle('active', i === current);
            });
            var counter = document.getElementById('ai-impact-counter');
            if (counter) counter.textContent = (current + 1) + ' / ' + total;
            var bar = document.getElementById('ai-impact-bar');
            if (bar) {
                bar.style.transition = 'none';
                bar.style.transform = 'scaleX(0)';
                void bar.offsetWidth;
                bar.style.transition = '';
                bar.style.transform = 'scaleX(1)';
            }
        }

        function next() { go(current + 1); }
        function prev() { go(current - 1); }

        function schedule() {
            if (timer) clearTimeout(timer);
            timer = setTimeout(function () {
                next();
                schedule();
            }, SLIDE_MS);
        }

        // Nav buttons
        var prevBtn = slider.querySelector('.ai-impact-prev');
        var nextBtn = slider.querySelector('.ai-impact-next');
        if (prevBtn) prevBtn.addEventListener('click', function () { prev(); schedule(); });
        if (nextBtn) nextBtn.addEventListener('click', function () { next(); schedule(); });

        // Dots
        slider.querySelectorAll('.ai-impact-dot').forEach(function (dot) {
            dot.addEventListener('click', function () {
                go(parseInt(dot.getAttribute('data-i'), 10) || 0);
                schedule();
            });
        });

        // Hover pause
        slider.addEventListener('mouseenter', function () {
            if (timer) { clearTimeout(timer); timer = null; }
        });
        slider.addEventListener('mouseleave', function () {
            schedule();
        });

        // Touch swipe
        var touchX = 0, touchY = 0;
        slider.addEventListener('touchstart', function (e) {
            touchX = e.touches[0].clientX;
            touchY = e.touches[0].clientY;
        }, { passive: true });
        slider.addEventListener('touchend', function (e) {
            var dx = e.changedTouches[0].clientX - touchX;
            var dy = e.changedTouches[0].clientY - touchY;
            if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy)) {
                if (dx > 0) prev(); else next();
                schedule();
            }
        }, { passive: true });

        // Start immediately — no observer, no visibility checks, no fallback
        go(0);
        schedule();
    }

    // === Lazy Load Charts (mermaid + echarts) ===
    var mermaidLoaded = false;
    var echartsLoaded = false;

    function loadScript(src, callback) {
        var script = document.createElement('script');
        script.src = src;
        script.onload = callback;
        script.onerror = function () {
            console.warn('Failed to load script:', src);
        };
        document.head.appendChild(script);
    }

    function renderMermaid() {
        if (!window.mermaid) return;
        var isDark = document.documentElement.getAttribute('data-theme') === 'dark';
        window.mermaid.initialize({
            startOnLoad: false,
            theme: isDark ? 'dark' : 'default',
            securityLevel: 'strict'
        });
        var blocks = document.querySelectorAll('#body-content div.mermaid');
        var jobs = Array.prototype.map.call(blocks, function (div, i) {
            // 读取源代码：优先 data-src，否则从内容中提取（排除按钮等非代码元素）
            var src = div.getAttribute('data-src');
            if (!src) {
                var clone = div.cloneNode(true);
                clone.querySelectorAll('button, .mermaid-error, svg').forEach(function (el) { el.remove(); });
                src = clone.textContent || '';
            }
            if (!src.trim()) return Promise.resolve();
            var id = 'mmd-' + i + '-' + Math.random().toString(36).slice(2, 8);
            return window.mermaid.render(id, src).then(function (res) {
                div.innerHTML = res.svg;
                if (res.bindFunctions) { res.bindFunctions(div); }
                div.setAttribute('data-rendered', '1');
            }).catch(function (err) {
                div.innerHTML = '<pre class="mermaid-error">图表渲染失败：' + String(err && err.message || err) + '</pre>';
                div.setAttribute('data-rendered', '0');
            });
        });
        Promise.all(jobs).then(function () {
            document.dispatchEvent(new CustomEvent('mermaid:rendered'));
        });
    }
    window.__renderMermaid = renderMermaid;

    function renderEcharts() {
        if (!window.echarts || typeof window.buildEchartOption !== 'function') return;
        var containers = document.querySelectorAll('#body-content .echart-container, #body-content .echart');
        if (!containers.length) return;
        var isDark = document.documentElement.getAttribute('data-theme') === 'dark';
        containers.forEach(function (el) {
            var optAttr = el.getAttribute('data-option') || el.textContent || '';
            if (!optAttr.trim()) return;
            try {
                var opt = JSON.parse(optAttr);
                var chart = window.echarts.init(el, isDark ? 'dark' : null, { renderer: 'canvas' });
                var baseOpt = window.buildEchartOption(opt, isDark);
                chart.setOption(baseOpt);
                window.addEventListener('resize', function () { chart.resize(); });
                el.setAttribute('data-rendered', '1');
            } catch (e) {
                el.innerHTML = '<pre class="echart-error">图表渲染失败：' + String(e && e.message || e) + '</pre>';
                el.setAttribute('data-rendered', '0');
            }
        });
    }

    function initLazyCharts() {
        var base = window.SITE_BASE || '';
        var mermaidBlocks = document.querySelectorAll('#body-content div.mermaid');
        var echartBlocks = document.querySelectorAll('#body-content .echart-container, #body-content .echart');

        // Mermaid lazy load
        if (mermaidBlocks.length > 0 && !mermaidLoaded) {
            var loadMermaidNow = function () {
                if (mermaidLoaded) return;
                mermaidLoaded = true;
                loadScript(base + 'vendor/mermaid.min.js', function () {
                    renderMermaid();
                });
            };
            if ('IntersectionObserver' in window) {
                var mermaidObserver = new IntersectionObserver(function (entries) {
                    entries.forEach(function (entry) {
                        if (entry.isIntersecting) {
                            loadMermaidNow();
                            mermaidObserver.disconnect();
                        }
                    });
                }, { rootMargin: '800px' });
                mermaidBlocks.forEach(function (el) { mermaidObserver.observe(el); });
                // Fallback: force load after 2.5s even if observer hasn't fired
                setTimeout(function () { loadMermaidNow(); }, 2500);
            } else {
                loadMermaidNow();
            }
        }

        // ECharts lazy load
        if (echartBlocks.length > 0 && !echartsLoaded) {
            var loadEchartsNow = function () {
                if (echartsLoaded) return;
                echartsLoaded = true;
                loadScript(base + 'vendor/echarts.min.js', function () {
                    renderEcharts();
                });
            };
            if ('IntersectionObserver' in window) {
                var echartsObserver = new IntersectionObserver(function (entries) {
                    entries.forEach(function (entry) {
                        if (entry.isIntersecting) {
                            loadEchartsNow();
                            echartsObserver.disconnect();
                        }
                    });
                }, { rootMargin: '800px' });
                echartBlocks.forEach(function (el) { echartsObserver.observe(el); });
                setTimeout(function () { loadEchartsNow(); }, 2500);
            } else {
                loadEchartsNow();
            }
        }
    }

    // === Share buttons ===
    function initShareButtons() {
        var shareBtns = document.querySelectorAll('.share-btn');
        if (shareBtns.length === 0) return;

        shareBtns.forEach(function (btn) {
            btn.addEventListener('click', function (e) {
                e.preventDefault();
                var platform = btn.getAttribute('data-platform');
                var url = window.location.href;
                var title = document.title || '';
                var shareUrl = '';

                if (platform === 'copy') {
                    navigator.clipboard.writeText(url).then(function () {
                        var original = btn.textContent;
                        btn.textContent = '已复制';
                        btn.classList.add('share-copied');
                        setTimeout(function () {
                            btn.textContent = original;
                            btn.classList.remove('share-copied');
                        }, 2000);
                    });
                    return;
                } else if (platform === 'twitter') {
                    shareUrl = 'https://twitter.com/intent/tweet?url=' + encodeURIComponent(url) + '&text=' + encodeURIComponent(title);
                } else if (platform === 'weibo') {
                    shareUrl = 'https://service.weibo.com/share/share.php?url=' + encodeURIComponent(url) + '&title=' + encodeURIComponent(title);
                } else if (platform === 'qq') {
                    shareUrl = 'https://connect.qq.com/widget/shareqq/index.html?url=' + encodeURIComponent(url) + '&title=' + encodeURIComponent(title);
                } else if (platform === 'email') {
                    shareUrl = 'mailto:?subject=' + encodeURIComponent(title) + '&body=' + encodeURIComponent(url);
                }

                if (shareUrl) {
                    window.open(shareUrl, '_blank', 'width=600,height=500,noopener,noreferrer');
                }
            });
        });
    }

    // === Reading time & word count ===
    function initReadingTime() {
        var metaEl = document.querySelector('.post-meta-reading');
        if (!metaEl) return;

        var content = document.querySelector('#body-content') || document.querySelector('article') || document.body;
        if (!content) return;

        // 统计中文字符和英文单词
        var text = content.textContent || '';
        var chineseChars = (text.match(/[\u4e00-\u9fa5]/g) || []).length;
        var englishWords = (text.match(/[a-zA-Z]+/g) || []).length;
        var totalWords = chineseChars + englishWords;

        // 阅读速度：中文 500 字/分钟，英文 200 词/分钟
        var readingMinutes = Math.max(1, Math.round(chineseChars / 500 + englishWords / 200));

        // 格式化字数
        var wordStr = totalWords >= 10000 ? (totalWords / 10000).toFixed(1) + ' 万字' :
                      totalWords >= 1000 ? (totalWords / 1000).toFixed(1) + ' 千字' :
                      totalWords + ' 字';

        metaEl.textContent = wordStr + ' · 约 ' + readingMinutes + ' 分钟阅读';
    }

    // === Mobile Nav Toggle (汉堡菜单) ===
    function initNavToggle() {
        var toggle = document.querySelector('.nav-toggle');
        var nav = document.querySelector('.header-nav');
        if (!toggle || !nav) return;

        function closeNav() {
            nav.classList.remove('open');
            toggle.setAttribute('aria-expanded', 'false');
        }

        toggle.addEventListener('click', function (e) {
            e.stopPropagation();
            var isOpen = nav.classList.toggle('open');
            toggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
        });

        // 点击导航链接后关闭菜单
        nav.querySelectorAll('a').forEach(function (a) {
            a.addEventListener('click', closeNav);
        });

        // 点击菜单外部关闭
        document.addEventListener('click', function (e) {
            if (!nav.contains(e.target) && !toggle.contains(e.target)) {
                closeNav();
            }
        });

        // ESC 键关闭
        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape') closeNav();
        });
    }

    // === Mobile Video Optimization (移动端视频不自动播放，节省流量) ===
    function initMobileVideo() {
        var isTouch = 'ontouchstart' in window || navigator.maxTouchPoints > 0;
        var isSmallScreen = window.matchMedia('(max-width: 768px)').matches;
        if (!isTouch && !isSmallScreen) return;

        var videos = document.querySelectorAll('.hero-video, .journey-video, .ai-media-video');
        videos.forEach(function (video) {
            // 暂停自动播放
            video.pause();
            video.removeAttribute('autoplay');
            video.setAttribute('preload', 'none');

            // 点击播放/暂停
            video.style.cursor = 'pointer';
            video.addEventListener('click', function () {
                if (video.paused) {
                    video.play();
                } else {
                    video.pause();
                }
            });

            // 播放结束后回到 poster
            video.addEventListener('ended', function () {
                video.pause();
            });
        });
    }

    // === Init all ===
    var INIT_FNS = [
        initTheme, initHeaderNav, initCodeCopy, initHighlight,
        initSearch, initBackToTop, initTimeline, initAiEra,
        initReadingProgress, initScrollReveal,
        initHeadingAnchors, initSectionNumbers, initBentoExpand,
        initCardClick, initArchCmd, initAiImpact, initLazyCharts,
        initShareButtons, initReadingTime, initNavToggle, initMobileVideo
    ];

    function init() {
        for (var i = 0; i < INIT_FNS.length; i++) {
            try {
                INIT_FNS[i]();
            } catch (e) {
                // Continue even if one module fails
            }
        }
        document.addEventListener('mermaid:rendered', initMermaidTools);
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
