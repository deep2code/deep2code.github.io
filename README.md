# deep2code.github.io

资深程序员个人技术博客。旧站为 Hugo（Relearn 主题）生成，现已重构为纯脚本生成静态站：直接消费 `extracted_content.json` 数据，输出全部 HTML 页面、搜索索引与 sitemap。

## 目录结构

- `extract_content.py` — 从旧 Hugo 站 HTML 提取内容与导航，产出 `extracted_content.json`
- `extracted_content.json` — 全站内容数据源（pages + navigation），生成管线的唯一输入
- `generate_pages.py` — 生成管线（唯一构建入口）
  - 清洗内容（剥离 Hugo 主题残留、Pygments 高亮、坏链接修复、div 平衡）
  - 路径/标题规范化（`URL_MAP`、`NAV_TITLE_MAP`，如 `/ai/__index/` → `/ai/finetuning/`）
  - 内容为先布局（无侧栏）：吸顶顶栏（brand + 语义分组快捷导航 + 全局搜索 + 主题切换），文章页底部同组「上一篇/下一篇」与同组文章 chip 列表
  - 语义分组信息架构（`CONTENT_GROUPS`，10 组覆盖全部 70 篇：Go、数据库与缓存、AI、中间件、云与 DevOps、编程语言、工具、系统与网络、图形与游戏、其他）
  - 门户首页（终端风 hero + 全部文章按语义分组归档流，打开即见全部内容）
  - 生成 `search-index.json` 与 `sitemap.xml`
- `css/style.css`、`js/main.js` — 新站资源（Hugo 旧资源已全部移除）

## 构建

```bash
python3 generate_pages.py
```

输出：全部内容页 HTML（含 `/index.html`）、`search-index.json`、`sitemap.xml`。生成幂等，可重复执行。

数据变更流程：改 `extracted_content.json` → 重跑 `python3 generate_pages.py`。

## 历史工具

- `update_content.py` / `update_all_content.py` — 旧的数据增量更新脚本，与新管线无依赖，可删除
- `generate_homepage.py` — 旧首页生成器（硬编码 13 个分类），已由 `generate_pages.py` 的 `build_homepage_content()` 取代，可删除