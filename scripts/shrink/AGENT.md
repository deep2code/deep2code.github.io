# 正文精简 Agent 作业说明

你负责一批 HTML 文章页的**段落精简**。只做文字压缩，**绝不改结构**。

## 输入 / 输出

- 输入：一个 JSON 文件（路径由调用方给出），形如
  ```json
  {"id": 3, "files": ["a/b/index.html", ...], "items": [
     {"file": "a/b/index.html", "start": 12345, "end": 12678, "sha1": "…",
      "cjk": 147, "heading": "二、rate 与 irate 的差别", "prev": "上一段纯文本前 80 字",
      "next": "下一段纯文本前 80 字", "html": "<p> 内部的原始 HTML </p>"}
  ]}
  ```
- 输出：写成 JSON 文件（路径由调用方给出），形如
  ```json
  {"items": [{"file": "a/b/index.html", "start": 12345, "end": 12678,
              "sha1": "<原样抄输入里的 sha1>", "new_html": "<改写后的段落 inner HTML>"}],
   "descs": {"a/b/index.html": "新的 meta description"}}
  ```
- `start`/`end`/`sha1` **原样抄**，不要自己算。
- 每条输入 item 必须有一条输出 item，顺序不限，**不许漏**。
- 用 Python 写输出文件（`json.dump(..., ensure_ascii=False)`），不要手写转义。

## 改写规则

**压缩指标（硬要求）**：

| 原段长度 | 目标长度 | 压缩幅度 |
|---|---|---|
| >80 中文字 | **≤80 字** | 压 25%–35% |
| 60–80 中文字 | 55–75 字 | 压 15%–25% |

（中文字数 = 汉字个数，不含标点、数字、英文。）

改写手段，按顺序用：

1. **删铺垫**：交代背景、自我设问（「为什么会这样？」「这是什么意思？」）、
   「先说结论」「需要说明的是」「这里要注意」「另外注意」「换句话说」「事实上」
   「值得注意的是」「工程上的处理是」这类引导语，整句删掉。
2. **删重复**：同一段内前后说同一件事的、与相邻段（`prev`/`next` 字段）重复的过渡句，只留一处。
3. **删举例的枝节**：举例只保留能说明结论的那一半，举例里的修饰、铺垫、二次解释删掉。
   **但例子里的数字与结论必须留**。
4. **压长句**：一句话超过 60 字、或靠 `、` `；` 串起 4 个以上分句的，改写成 2–3 个短句。
5. **拆段**：删完仍 >80 字，就用 `</p>\n<p>` 拆成多段（不要加外层 `<p>` 包裹）。

**必须留住的**：技术结论、判据、失效条件、所有数字与单位、`<code>` 内容、
`<strong>` 强调的要点、链接。宁可少压几字，也不能丢信息。

## 硬约束（违反了会被校验脚本打回）

- **数字与单位一个都不能丢、不能改**：`4 个抓取间隔`、`30 秒`、`23.7 次`、`2.25 版本`、
  `p99`、`1m`、`2 到 3 倍`、`① ② ③` 全部原样保留。**禁止**把阿拉伯数字改写成中文数字
  （`15 分钟` 不能变成 `十几分钟`、`5 到 15` 不能变成 `十来个`）。
- **不能新增**任何数字。
- `<code>…</code>` 里的内容、`<strong>…</strong>` 的强调位置、`<a href="…">` 链接、
  `<img>`、实体转义（`&lt;` `&gt;` `&amp;` `&quot;`）—— 全部原样保留。要拆段时，
  行内标签必须各自闭合，不能跨段断开。
- **不新增/删除整段**：只改 `html` 字段里那一段的内容，段数可以变多（拆段），不能变少到 0。
- 不改语气、不加 emoji、不加网络黑话、不用「首先/其次/最后/综上所述」。
- 术语沿用原文写法（`区间向量`、`分位数`、`幂等` 等不要换词）。

## meta description

每个**文件**（不是每段）产出 1 条新 `meta description`，写在 `descs` 里：

- ≤80 中文字，保留原标题里的核心术语与关键数字
- 说明这篇讲什么、覆盖哪些要点，不要空话（「本篇文章介绍了…」这类删掉）
- 只写这一条，不要去改 HTML 里的 meta 标签

## 自检（写完输出文件后必须做）

```bash
python3 -c "
import json,sys
sys.path.insert(0,'scripts/shrink'); import common as C
inp=json.load(open('<输入路径>')); out=json.load(open('<输出路径>'))
src={(i['file'],i['start']):i for i in inp['items']}
assert len(out['items'])==len(inp['items']), '条目数不一致'
bad=0
for it in out['items']:
    o=src[(it['file'],it['start'])]
    n=C.cjk_len(C.plain(it['new_html']))
    if n>80: print('超长',n,it['file'],it['start']); bad+=1
    if '<p>' in it['new_html'].replace('</p>\n<p>','') or it['new_html'].strip().startswith('<p'): print('非法 p',it['file']); bad+=1
    if sorted(C.numeric_tokens(o['html']))!=sorted(C.numeric_tokens(it['new_html'])): print('数字变动',it['file'],it['start']); bad+=1
    if sorted(C.inline_codes(o['html']))!=sorted(C.inline_codes(it['new_html'])): print('code 变动',it['file'],it['start']); bad+=1
    if sorted(C.hrefs(o['html']))!=sorted(C.hrefs(it['new_html'])): print('链接变动',it['file'],it['start']); bad+=1
for f,d in out['descs'].items():
    if C.cjk_len(d)>80: print('描述超长',f,C.cjk_len(d)); bad+=1
print('自检失败项:',bad)
"
```

`自检失败项: 0` 才算完成。有失败就改，改完重跑自检。

## 交付

最后回报一行：批次号、处理段数、自检结果。不要贴改写全文。
