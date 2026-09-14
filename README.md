# deep2code.github.io

资深程序员个人技术博客。纯静态 HTML 站点，零构建依赖，直接编辑 `.html` 文件即可。

## 目录结构

```
├── index.html              # 首页
├── 404.html                # 404 页面
├── CNAME                   # 自定义域名（yijunjun.asia）
├── robots.txt              # 爬虫规则
├── sitemap.xml             # 站点地图
├── llms.txt                # LLM 友好的站点地图
├── search-index.json       # 客户端搜索索引
├── css/                    # 样式
├── js/                     # 脚本（主题切换、搜索、mermaid、echarts）
├── images/                 # 图片资源
├── mermaid/                # mermaid 库
├── ai/                     # AI 系列文章
├── golang/                 # Go 语言系列文章
├── mysql/                  # MySQL 文章
├── redis/                  # Redis 文章
├── nginx/                  # Nginx 文章
├── git/                    # Git 文章
├── python/                 # Python 文章
├── elastic/                # Elasticsearch 文章
├── memcached/              # Memcached 文章
├── mac/                    # macOS 文章
├── flutter/                # Flutter 文章
├── grpc/                   # gRPC 文章
├── other/                  # 其他主题文章
├── categories/             # 分类页
├── tags/                   # 标签页
└── zh-blog-lint/           # 中文博客检查规范（参考用）
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
3. 更新 `search-index.json`（如需要搜索功能）
4. 更新 `sitemap.xml`（如需要）

## 部署

推送到 GitHub 仓库的 `main` 分支，GitHub Pages 自动部署。

或手动同步到服务器：

```bash
rsync -avz --exclude='.git' --exclude='node_modules' --exclude='zh-blog-lint' ./ user@server:/var/www/blog/
```

## 历史

本项目最初由 Hugo（Relearn 主题）生成，后重构为 `extracted_content.json` + Python 生成器模式。2026 年 9 月改为纯静态 HTML，移除生成器和数据源，直接维护 HTML 文件。
