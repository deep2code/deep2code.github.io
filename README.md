# deep2code.github.io

资深程序员个人技术博客。纯静态 HTML 站点，零构建依赖，直接编辑 `.html` 文件即可。

## 目录结构

```
├── index.html              # 首页
├── 404.html                # 404 页面
├── CNAME                   # 自定义域名（yijunjun.asia）
├── robots.txt              # 爬虫规则
├── sitemap.xml             # 站点地图
├── llms.txt / ai.txt       # 给 LLM 与 AI 爬虫的站点说明
├── search-index.json       # 客户端搜索索引（gen_search_index.py 生成）
├── feed.xml / atom.xml     # 订阅（gen_feed.py 生成）
├── css/  js/  images/      # 样式、脚本、图片
├── vendor/                 # 自托管的 mermaid / echarts / highlight
├── programming/            # 编程语言、算法、设计模式、测试
├── database/               # 关系库、缓存、OLAP、向量检索
├── api/                    # REST、GraphQL、RPC、认证与安全
├── architecture/           # 分布式、消息、微服务、治理
├── devops/                 # 容器、K8s、CI/CD、IaC、Nginx
├── observability/          # 指标、日志、链路、性能定位
├── frontend/               # 框架原理、渲染时机、跨端
├── media/                  # 封装与编码、FFmpeg、分发
├── tools/                  # Git、Shell、文档与图、开发环境
├── ai/                     # LLM、RAG、Agent 与编程助手
├── life/                   # 生活与非技术
├── about/                  # 关于本站
├── categories/  tags/      # 分类页与标签页
├── scripts/                # 正文批量改写与校验工具（不入库）
└── zh-blog-lint/           # 中文博客写作规范与审核清单
```

## 编辑方式

直接修改对应的 `.html` 文件，保存即生效。每个 HTML 文件都是完整的独立页面（含 `<!DOCTYPE>`、`<head>`、`<header>` 导航、`<footer>`）。

### 批量修改公共部分（导航、footer）

如果需要修改所有页面的导航栏或 footer，使用批量替换：

```bash
# 替换所有 HTML 文件中的某个字符串
sed -i '' 's/旧内容/新内容/g' **/*.html
```

### 新增文章

1. 复制一篇现有文章作为模板
2. 修改 `<title>`、`<h1>`、面包屑、正文内容
3. `python3 gen_search_index.py` 重建搜索索引
4. `python3 gen_categories.py`、`python3 gen_feed.py` 按需重建分类页与订阅
5. 更新 `sitemap.xml`（如需要）

## 写作规范与正文批量改写

规范原文：`zh-blog-lint/中文技术博客审核清单.md`、`zh-blog-lint/去AI味改写规范.md`。

正文改动全部走 `scripts/` 下的工具，改完必须过门再落盘：

```bash
python3 scripts/deai/lint.py                    # 全站硬项命中数（导读框/编号标题/预告句式/套话转弯/顺序词/超长段落/段内 emoji/自指叙述/自指主语）
python3 scripts/deai/lint.py --self-test        # 植入已知违规，证明每条规则都真能触发
python3 scripts/deai/lint.py database/redis     # 单页或目录前缀

python3 scripts/deai/strip_boilerplate.py --dry # 阶段 A：删「这篇怎么读」导读框 + 去标题编号前缀
python3 scripts/deai/strip_boilerplate.py       # 写盘后自动逐页复核：只允许前缀与框内的变化
python3 scripts/deai/strip_boilerplate.py --check-only --files a/index.html,b/index.html

python3 scripts/deai/strip_lead_frame.py --dry  # 机械删除段首「搞清这一节能解决的现象是：」这类预告框架
python3 scripts/deai/strip_lead_frame.py        # 写盘并逐页自检：段落数不变，每段只少段首那一截

python3 scripts/deai/plan.py --flagged          # 阶段 B1：只把门判失败的段落切成批次 → _drafts/deai-in/batch-NN.json
python3 scripts/deai/plan.py --min 60 --max-items 40 --max-files 4   # 阶段 B2 全站普压：只排 >=60 字的长段
python3 scripts/deai/plan.py --union --min 60 --max-items 40 --max-files 4   # 阶段 B3：触门段 + 长段合跑，一段只过一次
python3 scripts/deai/replan_batch.py --stale      # 只重算偏移失效的未派发批（手改过 HTML 之后用这个，别全站重排）
python3 scripts/deai/from_jsonl.py batch-04     # agent 交付的 JSONL → batch-04.json，并自动跑 check_out
python3 scripts/deai/review.py 00,01,02         # 落盘前人看：字数比、最长段、中文数字/条件词/术语三类逐段对照
python3 scripts/deai/dump.py 04 12486 15958     # 裁决 ◆▲ 时把这几段的原文/新文并排打出来（--all 打整批）
python3 scripts/deai/land.py 00,01,02           # 一波落盘：校验→回填→同步描述→与基线核对→复跑门→重建索引
python3 scripts/deai/land.py all --dry          # 只统计不写盘
python3 scripts/deai/check_pairs.py             # 落盘后跨段复查：并列序号只删了一半留下的悬空后件
DEAI_IN_DIR=_drafts/deai-in python3 scripts/shrink/check_out.py _drafts/deai-out/batch-04.json
python3 scripts/shrink/apply.py --in-dir _drafts/deai-out --desc-out _drafts/deai-descs.json --only 'batch-04.json'
python3 scripts/shrink/sync_meta.py --desc-in _drafts/deai-descs.json
python3 scripts/shrink/verify.py --all --snapshot _drafts/deai-snapshot   # 代码/图/表格/链接/数字与基线全等
```

`plan.py` 会清空 `_drafts/deai-in/` 重排批次，改变每批的段落归属，所以在途有 agent 正在按
`batch-NN` 写交付时它会直接拒绝执行（`.jsonl` 和 agent 分批攒的 `.part` 都算在途）；
必须先 `land.py` 落盘或把交付文件归档。确认要重排才加 `--force`。

《自指叙述》是把主语为文章本身的句子判成硬项：`这篇只讲 X` `本篇在路径里的位置是 Y`
`这一节解释…` `搞清这一节能解决的现象是：Z`。这类句子不携带技术信息，删掉框架后段落直接从
现象或结论开始讲。早期《预告句式》要求「解决」后面紧跟引号，因此放过了 579 处无引号变体，
补规则后全站才暴露出来。其中段首、冒号收尾、前缀不含数字与行内标签的 304 处由
`strip_lead_frame.py` 一次删干净（这类删除是可预测的机械操作，不必花 agent 逐段判断），
剩下的形状各异，进 `--union` 的改写批次由 agent 处理。
段落流水线只吃 `<p>`，所以命中还得按位置分一次类：`<div class="callout-title">这篇不覆盖的相邻问题</div>`
这类落在提示框标题上的 4 处不在任何批次里，是定长字符串替换，脚本改完逐页断言只少了那两个汉字。

《自指主语》是同一处盲区的另一半：`自指叙述` 要求主语后面 24 字内出现指定动词，于是
`这篇按三段组织` `本篇是这条路径的最后一环` `本文只在需要的地方指路` 这类没有那些动词的写法
全站漏了 240 段（159 页）。这 240 段按目录切 5 轮直改（逐段自检「改后不触门 +
`code`/`href`/数字多集合不变 + 汉字数不增」，`--dry` 先看拒绝清单），改干净之后才把词级规则
加进门——顺序反过来会让验收门在收尾途中变红。正则里三处后顾是必须的：`脚本本文`、`版本文档`、
`文本节点型` 里的「本文 / 本节」不是自指，`本节点`（分片与节点术语）和 `本文件`（图源注释）同理。
这条规则的口径也改过一次：阶段 B5 只扫正文 `<p>`，之后拿同一个正则直接扫整页 HTML，又挖出段落之外 45 处
（表格单元格 21、提示框标题与强调 10、表头 4、mermaid 标签 4、代码注释 4、小标题 1、路径导航 1），
B6 清掉其中 41 处，两条规则随之改成查整页正文区。唯一的豁免是 `<pre>`：代码块受「与基线全等」保护，
改不动，所以规则先剥掉 `<pre>` 再匹配，剩下 3 页 4 条代码注释里的「本文」登记在 `lint.PRE_EXEMPT`，
`--self-test` 会核对它们确实还在代码块里——跑到正文就去豁免、登记失效就报红。标题与图里的措辞改动
（1 个 h2、4 个 mermaid 标签）按同样的形状登记在 `verify.py` 的 `KNOWN_TEXT_EDITS`：逐对精确匹配才放行，
登记写错或借它夹带别的改动都照样判红。

阶段 B7 是逐页把正文读出来的，不再看词表计数。第一轮读 `ai/` 时发现一类躲过整条流水线的元素：
17 页里有 38 个 `<blockquote>` 框，全是 `核心结论：` `黄金法则：` `一句话定位：` 这种领起式总结，
内容都和紧邻的图或表格重复。`C.blocks()` 只认 `<p>`，所以 B 批改不到它们。整块删除会连带框里
自带的数字和行内 `<code>`，撞上「与基线全等」那两条，因此逐块登记在
`scripts/deai/deleted-chunks.json`，由 `verify.apply_known_deletions` 核对两件事：基线里必须找得到
这一块、现文件里必须找不到删前的那一版，两边都对才把基线里这块摘掉再比对；登记失效或者块被恢复都判红。
登记表存的是「基线文本 + 删前文本」两个形状，不是同一个——那 38 个框里有 4 个的文字在 B 批被改写工人动过，
只存删前文本会被判 4 页红。

第二读轮删的是复述标题的空转句：`ai/coding-assistants/prompt` 的「核心原则」五条里有四条各带一句
把标题重说一遍的话（`说清楚你要什么，不要模糊`），删掉后小标题直接接示例；同页的「总结」一节
（一个 h2、八个 `<li>`、一句「记住：Garbage in, garbage out」）整节删除，FAQ 里重复报出的
`500 到 2000 token` 也删掉一处。「总结」这个标题文本和那两个数字会打破与基线全等，所以这两块
同样进 `deleted-chunks.json`，登记表里不止 `<blockquote>`，文件名跟着改了。`ai/langchain/index` 那句 `；只谈框架本身。`
是 B5 把 `本篇只谈框架本身` 的主语剥掉后留下的半截，补成 `这里`——不能用 `本篇` `本文` `这一篇`，
那三个都是硬项。四条信号跨两个 `<p>` 的写法核对过快照，是作者原来的结构，合并会顶到 80 字上限，
所以不动。

并列序号是另一类只有跨段才看得出来的损伤：`第一，…第二，…`、`一是…二是…` 删掉前件，
留下的后件单独读不通。`lint.py` 的《顺序词》只匹配「首先…其次…最后」这一种形状，中文数字
检查看的是数字后跟量词，`一是` `第二，` 都不匹配；`check_out.py` 的字数、数字、code 三项对
它也无感。所以落盘后用 `check_pairs.py` 单独走一趟，只在前面三段里找前件。它对基线本来就有
的形状也会报（快照上 1 处，是「第三、五两问」这种指向表格行的用法），判据是**和快照比数量**，
不是要求零；本站落到现在只剩这一处已知误报。

`review.py` 的另一类提示是《条件词消失》（`▲`）：字数、数字、code 三门都只对留下来的内容负责，
判不了限定语没了——「堆再翻倍**才**触发 GC」压成「再翻倍触发 GC」、「**只有**复用率上来才开始串」
去掉「只有」，段落在机器眼里完全合格。它按触发词 / 保留词两组匹配：旧文出现严格写法
（必须、需要、只有、才、否则…）而新文连宽松写法（要、得、只、能否…）都没有才报，
所以「必须」换成「要」不报、整组消失才报。一批 37 段约报 3 段，逐条人工判是强调还是条件。

第三类是《术语整页消失》（`■`）：把 `Bitmap Heap Scan` 写成「这种方式」、把 `ACCESS EXCLUSIVE 锁`
写成「这把锁」，字数、数字、code 三门照旧全过，词却从页面上蒸发了——行内代码外的标识词不在
任何多重集合里。它比的是**整页**：先把整批替换按 `start`/`end` 预套到页面文本上（同批两段一起丢
同一个词时逐段看会互相打掩护），再要求这个词在套用后的页面一个字都不剩才报，所以上一段刚提过
`ACCESS EXCLUSIVE`、这一段回指「这把锁」不算损失。校准后十来个批次只报 2 处，都是删「详见站内
DDD 那篇」这类自指指针时把词一起带走了，属于合格改写。`review.py` 只在交付还没落盘时用 `deai-in/`
的输入，落盘后要复看只能两边都取归档位（`deai-b2-archive/` 加 `deai-in-landed/`）——批次号会重复，
混代配出来的偏移量对不上还看不出配错。

落盘的另一半是交付标记：agent 把 `from_jsonl.py` 跑到退出码 0 后 `touch _drafts/deai-out/batch-NN.done`，
`land.py` 只接受带 `.done` 的批次（`all` 也就是「已交付未落盘」那几批，落成功即消耗掉标记）。
没标记就落盘，agent 收工前的最后一轮修订会补不回来——回填按 sha1 守卫，同一段落改过一次就不再接受第二次回填。

`land.py` 在回填前还会逐段核对 `sha1`：批次按文件互斥切，落别的批不会动到这一页，
所以对不上就说明这一页被手改过或重排过，整波直接停住不写盘。手改过的页要先把它所在的那一批
重算一遍（`replan_batch.py --stale`，只处理未派发的那几批），再派发。

落成功的批次，`land.py` 会把它的输入从 `_drafts/deai-in/` 移进 `_drafts/deai-in-landed/`。
批次号在两次 `plan.py` 之间会重复（每次按当次的文件集从 00 重新编号），所以「这批干过没有」
不能按号码查归档，只能看输入还在不在 `deai-in/`：留在 `deai-in/` 的才是可派发的活。
`replan_batch.py` 对已落盘的号直接拒改——重算它等于把同一批段落压第二遍，
那时 0.82 的逐段门会逼着 agent 删事实换字数。

门是两层的：逐段 ≤ 原字 × 0.82，**整批合计 ≤ 原字 × 0.78**（`check_out.py`）。
只按逐段口径写的批次会整批卡在 0.80–0.82 被打回，所以 `AGENT.md` 把整批这条放在压缩口径第一条。

`scripts/shrink/` 是段落级改写的通用流水线（scan → agent 产出 → apply → verify），
`scripts/deai/` 是在它之上做的去 AI 味专用门。**基线用 `--snapshot` 而不是 git HEAD**：
阶段 A 已经删掉的内容会让 HEAD 基线误报，所以阶段 A 落盘后要先快照一份
`_drafts/deai-snapshot/`，阶段 B 与它比。

`land.py` 在核对不过时会把本波涉及的所有页面退回回填前的内容，不会留下半批改写。
中文数字的门是双向的：改写里**新增**原文没有的中文数字（自己数出「三个阶段」）直接判失败；
删掉原文的中文数字只打 `[待核中文数字]` 提示——`先纠正一个流传很广的说法` 里的「一个」属于
被拆掉的句式骨架，可以删；`「只加了一个字段，调用量翻十倍」` 里的数量必须原词保留。

注意 `.gitignore` 里有 `*.py`，`scripts/` 下的工具不入版本库，换机器要一起拷走。

## 部署

推送到 GitHub 仓库的 `main` 分支，GitHub Pages 自动部署。

或手动同步到服务器：

```bash
rsync -avz --exclude='.git' --exclude='node_modules' --exclude='zh-blog-lint' ./ user@server:/var/www/blog/
```

## 历史

本项目最初由 Hugo（Relearn 主题）生成，后重构为 `extracted_content.json` + Python 生成器模式。2026 年 9 月改为纯静态 HTML，移除生成器和数据源，直接维护 HTML 文件。
