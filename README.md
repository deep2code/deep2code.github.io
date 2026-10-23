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
python3 scripts/deai/lint.py                    # 全站硬项命中数（导读框/编号标题/预告句式/套话转弯/顺序词/超长段落/段内 emoji）
python3 scripts/deai/lint.py --self-test        # 植入已知违规，证明每条规则都真能触发
python3 scripts/deai/lint.py database/redis     # 单页或目录前缀

python3 scripts/deai/strip_boilerplate.py --dry # 阶段 A：删「这篇怎么读」导读框 + 去标题编号前缀
python3 scripts/deai/strip_boilerplate.py       # 写盘后自动逐页复核：只允许前缀与框内的变化
python3 scripts/deai/strip_boilerplate.py --check-only --files a/index.html,b/index.html

python3 scripts/deai/plan.py --flagged          # 阶段 B：只把门判失败的段落切成批次 → _drafts/deai-in/batch-NN.json
python3 scripts/deai/from_jsonl.py batch-04     # agent 交付的 JSONL → batch-04.json，并自动跑 check_out
python3 scripts/deai/land.py 00,01,02           # 一波落盘：校验→回填→同步描述→与基线核对→复跑门→重建索引
python3 scripts/deai/land.py all --dry          # 只统计不写盘
DEAI_IN_DIR=_drafts/deai-in python3 scripts/shrink/check_out.py _drafts/deai-out/batch-04.json
python3 scripts/shrink/apply.py --in-dir _drafts/deai-out --desc-out _drafts/deai-descs.json --only 'batch-04.json'
python3 scripts/shrink/sync_meta.py --desc-in _drafts/deai-descs.json
python3 scripts/shrink/verify.py --all --snapshot _drafts/deai-snapshot   # 代码/图/表格/链接/数字与基线全等
```

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
