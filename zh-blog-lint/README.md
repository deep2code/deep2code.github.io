# zh-blog-lint · 中文技术博客审核工具包

一套可直接落地的中文技术博客质量检查配置，覆盖「排版格式 → 文档结构 → 术语统一 → 句子长度 → 用词规范」五层，剩下「错别字 → 语义逻辑 → 技术正确性 → 事实核查」四层交给大模型与人工。

---

## 快速开始

```bash
# 1. 安装依赖
npm install

# 2. 检查一篇文章（三个工具一起跑）
npm run lint
```

单独运行：

```bash
npx textlint --fix 你的文章.md        # 排版格式，--fix 可自动修复
npx markdownlint-cli2 --config .markdownlint.json 你的文章.md
vale 你的文章.md                       # 需自行安装 Vale CLI
```

---

## 目录结构

| 文件 | 作用 |
|---|---|
| `中文技术博客审核清单.md` | **核心交付物**。78 条规则，标注了每条规则该由谁执行；可直接整段贴给大模型当 prompt |
| `.textlintrc.json` | textlint 配置：中英文空格、数字单位、标点、行内代码、术语、长句 |
| `.markdownlint.json` | markdownlint 配置：针对中文与技术博客调优 |
| `.vale.ini` + `styles/ZHBlog/` | Vale 中文规则包：黑话、口语化、术语、被动语态、绝对表述、数字表述 |
| `sample.md` | 问题样本，用来验证工具是否正常工作 |

---

## 各工具负责什么

### textlint（排版格式，可自动修复）

启用 `textlint-rule-preset-zh-technical-writing` 中文预设：

- 中文与英文/数字之间的空格
- 行内代码 `code` 周围的空格
- 数字与单位符号之间的空格（`16 GB` vs `28℃`）
- 全角标点周围的多余空格
- 成对标点（引号、书名号）顺序
- 标准省略号 `……`
- 重复/多余标点
- 无效控制字符

外加 `terminology-zh` 做中英混排术语统一，`sentence-length` 限制长句（上限 100 字）。

### markdownlint（文档结构）

针对中文场景的关键调整：

| 规则 | 设置 | 原因 |
|---|---|---|
| `MD013` | **关闭** | 行长限制按字符算，中文段落会大量误报 |
| `MD033` | **关闭** | 技术博客常用行内 HTML |
| `MD041` | **关闭** | 不强制首行必须是 h1 |
| `MD024` | `siblings_only` | 只查同级重复标题，避免误伤 |
| `MD040` | **开启** | 代码块必须标注语言 |
| `MD001` | **开启** | 标题禁止跳级 |

### Vale（用词规范）

`styles/ZHBlog/` 下六个规则：

| 规则 | 类型 | 级别 | 抓什么 |
|---|---|---|---|
| `黑话.yml` | existence | warning | 赋能、抓手、闭环、底层逻辑… |
| `口语化.yml` | existence | warning | 众所周知、接下来让我们、搞定… |
| `术语.yml` | substitution | error | JavaScript/GitHub/macOS/iOS 大小写 |
| `被动语态.yml` | existence | suggestion | 疑似被动语态 |
| `绝对表述.yml` | existence | warning | 一定、绝对、100% 安全… |
| `数字表述.yml` | existence | error | 「降低 N 倍」这类不成立的表述 |

**中文场景的两个硬性约束**（已在配置注释里写明）：

1. 不要启用 Vale 内置拼写检查和 Microsoft/Google 风格包——它们面向英文散文，对中文会大量误报。
2. 中文没有空格分词，`\b` 之类的词边界正则不可靠，规则一律用**完整中文词**做词表匹配。

---

## 已知限制

1. **错别字无法用规则检查**。同音（在/再）、形近（戊/戌）、「的/地/得」这些错误必须靠上下文语义判断，本质上是模型任务。这是中文场景最大的空白，只能用秘塔写作猫、爱校对这类工具，或直接问大模型。
2. **语义逻辑、技术正确性、事实核查**没有规则可用，见清单的层级 5–7。
3. **Vale 配置文件未经实机验证**。本环境无法下载 Vale 二进制，仅验证了 YAML 语法正确、正则能命中目标文本。首次使用请先跑一次 `vale --version` 和少量样本确认。
4. `sentence-length` 上限设的是 100 字（对应「以逗号分隔的长句」口径）。textlint 按句号切分句子，中文全角句号「。」实测可以正常识别。

---

## 接入 pre-commit（可选）

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: textlint
        name: textlint
        entry: npx textlint --fix
        language: system
        types: [markdown]
      - id: markdownlint
        name: markdownlint
        entry: npx markdownlint-cli2 --config .markdownlint.json
        language: system
        types: [markdown]
```

---

## 规则的来源

- 《中文技术文档的写作规范》—— 阮一峰
- 《中文文案排版指北》—— sparanoid/chinese-copywriting-guidelines
- 主流大厂中文文档风格指南中的语言风格与用词规范部分
