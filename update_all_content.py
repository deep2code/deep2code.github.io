#!/usr/bin/env python3
"""Update all pages with 2024-2026 latest knowledge."""

import json
from pathlib import Path

BASE_DIR = Path(__file__).parent
CONTENT_FILE = BASE_DIR / 'extracted_content.json'


def load_data():
    with open(CONTENT_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_data(data):
    with open(CONTENT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ============================================================
# Update content for each page - appended to existing content
# ============================================================

UPDATES = {}


# --- Golang main page ---
UPDATES['/golang/'] = '''
<hr>
<h2 id="golang-2024-update">Go 1.21-1.24 新特性（2024-2026 更新）</h2>

<h3 id="go-124">Go 1.24（2025年2月）</h3>
<p>Go 1.24 是当前最新稳定版本，带来多项重要改进：</p>
<ul>
<li><strong>泛型类型别名</strong>：类型别名现在可以像普通类型一样被参数化，<code>type IntMap[V any] = map[string]V</code> 合法了。</li>
<li><strong>tool 依赖管理</strong>：<code>go.mod</code> 可以通过 <code>tool</code> 指令跟踪可执行依赖，不再需要 <code>tools.go</code> 文件 hack。</li>
<li><strong>新增标准库</strong>：<code>crypto/mlkem</code>（后量子密码学）、<code>crypto/hkdf</code>、<code>crypto/pbkdf2</code>、<code>crypto/sha3</code>、<code>weak</code>（弱指针）。</li>
<li><strong>FIPS 140-3 合规</strong>：crypto 模块符合 FIPS 140-3 标准。</li>
<li><strong>实验性 <code>testing/synctest</code></strong>：用于测试时间敏感代码的 fake-time 包。</li>
<li><strong>改进的 finalizer</strong>：<code>runtime.AddCleanup</code> 替代 <code>SetFinalizer</code>，更安全。</li>
<li><strong>GOCACHEPROG</strong>：支持外部缓存程序。</li>
</ul>

<h3 id="go-123">Go 1.23（2024年8月）</h3>
<ul>
<li><strong>函数迭代器（range-over-func）</strong>：可以在 <code>range</code> 中直接遍历函数迭代器。
<pre><code class="language-go">// Go 1.23+ 函数迭代器
func Count(n int) func(yield func(int) bool) {
    return func(yield func(int) bool) {
        for i := 0; i < n; i++ {
            if !yield(i) {
                return
            }
        }
    }
}
// 使用
for v := range Count(5) {
    fmt.Println(v) // 0 1 2 3 4
}</code></pre>
</li>
<li><strong>iter 包</strong>：标准库新增 <code>iter</code> 包，提供 <code>Seq</code> 和 <code>Seq2</code> 类型。</li>
<li><strong>structs 包</strong>：新增 <code>structs</code> 包，提供 <code>structs.Order</code> 等工具。</li>
<li><strong>unique 包</strong>：值驻留（interning），减少内存占用。</li>
<li><strong>Timers 性能提升</strong>：Windows 平台定时器精度从 15.6ms 提升到 0.5ms。</li>
</ul>

<h3 id="go-122-121">Go 1.21-1.22 回顾</h3>
<ul>
<li><strong>Go 1.22</strong>：<code>for range int</code> 语法（<code>for i := range 10</code>）、<code>http.ServeMux</code> 路由增强（支持方法和路径模式）、<code>slices</code> 和 <code>maps</code> 包进入标准库。</li>
<li><strong>Go 1.21</strong>：<code>min</code>/<code>max</code>/<code>clear</code> 内置函数、<code>context.WithoutCancel</code>、<code>context.AfterFunc</code>、<code>slog</code> 结构化日志、<code>cmp</code> 包、<code>maps</code>/<code>slices</code> 包（实验性）。</li>
</ul>

<h3 id="go-version-guide">版本选择建议（2026年）</h3>
<table>
<thead><tr><th>场景</th><th>推荐版本</th><th>说明</th></tr></thead>
<tbody>
<tr><td>生产环境</td><td>Go 1.23.x / 1.24.x</td><td>最新稳定版，安全性最好</td></tr>
<tr><td>保守环境</td><td>Go 1.22.x</td><td>已被大量线上验证</td></tr>
<tr><td>新项目</td><td>Go 1.24.x</td><td>享受最新语言特性</td></tr>
</tbody>
</table>

<h3 id="go-modern-tools">现代 Go 工具链</h3>
<pre><code class="language-bash"># Go 1.24+ 管理工具依赖
go get -tool golang.org/x/tools/cmd/goimports
go tool goimports -w .

# 结构化日志 slog
# go 1.21+
import "log/slog"

# 泛型工具函数（标准库）
import "slices"
import "maps"
slices.Sort(nums)
slices.Contains(nums, target)
maps.Keys(m)
maps.Values(m)</code></pre>
'''


# --- Python ---
UPDATES['/python/'] = '''
<hr>
<h2 id="python-2024-update">Python 3.12-3.14 新特性（2024-2026 更新）</h2>

<h3 id="py-314">Python 3.14（2025年10月发布）</h3>
<ul>
<li><strong>JIT 编译器正式可用</strong>：3.13 引入实验性 JIT，3.14 进一步优化，数值计算提速 30%+。</li>
<li><strong>自由线程（free-threaded）模式</strong>：去除 GIL 的实验性构建进入新阶段。</li>
<li><strong>延迟注解评估</strong>：<code>from __future__ import annotations</code> 成为默认行为。</li>
<li><strong><code>zoneinfo</code> 成为默认时区模块</strong>：替代 <code>pytz</code>。</li>
</ul>

<h3 id="py-313">Python 3.13（2024年10月发布）</h3>
<ul>
<li><strong>实验性 JIT 编译器</strong>：基于 copy-and-patch 技术，针对热点函数动态编译。</li>
<li><strong>自由线程构建（PEP 703）</strong>：实验性 no-GIL 模式，可利用多核并行。</li>
<li><strong>改进的交互式 REPL</strong>：多行编辑、语法高亮、历史浏览。</li>
<li><strong><code>typing</code> 增强</strong>：<code>TypeVar</code> 默认值、<code>ReadOnly</code> 等。</li>
</ul>

<h3 id="py-312">Python 3.12（2023年10月发布）</h3>
<ul>
<li><strong><code>@override</code> 装饰器</strong>：显式标记方法重写，类型检查器验证父类方法存在。
<pre><code class="language-python">from typing import override

class Base:
    def process(self, data: str) -> None: ...

class Derived(Base):
    @override
    def process(self, data: str) -> None:
        # 类型检查器会验证 Base.process 存在
        ...</code></pre>
</li>
<li><strong><code>TypeVar</code> 默认值</strong>：<code>T = TypeVar("T", default=str)</code></li>
<li><strong><code>tomllib</code> 标准库</strong>：内置 TOML 解析，不再需要第三方库。
<pre><code class="language-python">import tomllib
with open("config.toml", "rb") as f:
    config = tomllib.load(f)</code></pre>
</li>
<li><strong><code>pathlib</code> 增强</strong>：<code>Path.walk()</code>、<code>relative_to()</code> 改进。</li>
<li><strong>f-string 改进</strong>：支持嵌套引号、多行表达式、反斜杠。</li>
<li><strong><code>asyncio.TaskGroup</code></strong>：结构化并发（3.11 引入，3.12 完善）。
<pre><code class="language-python">import asyncio

async def main():
    async with asyncio.TaskGroup() as tg:
        task1 = tg.create_task(fetch("url1"))
        task2 = tg.create_task(fetch("url2"))
    # 两个任务都完成后继续
    print(task1.result(), task2.result())</code></pre>
</li>
</ul>

<h3 id="py-modern-tools">现代 Python 工具链（2026年）</h3>
<table>
<thead><tr><th>工具</th><th>用途</th><th>替代</th></tr></thead>
<tbody>
<tr><td><code>uv</code></td><td>包管理 + 虚拟环境</td><td>pip + venv + pip-tools</td></tr>
<tr><td><code>ruff</code></td><td>代码检查 + 格式化</td><td>flake8 + isort + black</td></tr>
<tr><td><code>mypy</code> / <code>pyright</code></td><td>类型检查</td><td>-</td></tr>
<tr><td><code>pytest</code></td><td>测试框架</td><td>unittest</td></tr>
<tr><td><code>rye</code> / <code>pixi</code></td><td>项目管理</td><td>poetry</td></tr>
<tr><td><code>FastAPI</code></td><td>Web 框架</td><td>Flask</td></tr>
<tr><td><code>Pydantic v2</code></td><td>数据验证</td><td>Pydantic v1</td></tr>
</tbody>
</table>

<pre><code class="language-bash"># uv - 极速 Python 包管理器（Rust 编写）
curl -LsSf https://astral.sh/uv/install.sh | sh
uv venv && source .venv/bin/activate
uv pip install fastapi uvicorn

# ruff - 极速 linter + formatter
pip install ruff
ruff check .  # 检查
ruff format .  # 格式化</code></pre>

<h3 id="py-version-status">版本状态（2026年）</h3>
<table>
<thead><tr><th>版本</th><th>状态</th><th>生命周期结束</th></tr></thead>
<tbody>
<tr><td>Python 3.14</td><td>最新稳定版</td><td>2030-10</td></tr>
<tr><td>Python 3.13</td><td>维护中</td><td>2029-10</td></tr>
<tr><td>Python 3.12</td><td>安全维护</td><td>2028-10</td></tr>
<tr><td>Python 3.11</td><td>安全维护</td><td>2027-10</td></tr>
<tr><td>Python 3.10</td><td>安全维护</td><td>2026-10</td></tr>
<tr><td>Python 3.9 及以下</td><td>已停止支持</td><td>-</td></tr>
</tbody>
</table>
'''


# --- Redis ---
UPDATES['/redis/'] = '''
<hr>
<h2 id="redis-2024-update">Redis 7.x-8.0 新特性（2024-2026 更新）</h2>

<h3 id="redis-8">Redis 8.0（2025年）</h3>
<p>Redis 8.0 是一次重大架构升级，将 RediSearch、RedisJSON、RedisTimeSeries、RedisBloom 等模块深度集成到核心中，不再需要单独安装模块。</p>
<ul>
<li><strong>内置全文搜索</strong>：RediSearch 成为核心功能，无需额外安装。</li>
<li><strong>内置向量搜索</strong>：支持 FLAT、HNSW 和 SVS-VAMANA 向量索引。</li>
<li><strong>内置 JSON 文档存储</strong>：RedisJSON 集成为核心数据类型。</li>
<li><strong>10 亿向量搜索</strong>：在 10 亿向量规模下达到 90% 精度，200ms 中位延迟。</li>
<li><strong>性能对比</strong>：比 PostgreSQL(pgvector) 高 9.5 倍 QPS、低 9.7 倍延迟；比 MongoDB Atlas 高 11 倍 QPS。</li>
</ul>

<h3 id="redis-vector">向量搜索（7.2+）</h3>
<p>Redis 7.2 引入了可扩展的向量相似性搜索，2025 年又新增了 Vector Sets 数据类型：</p>
<pre><code class="language-python"># Python 向量搜索示例
from redis import Redis
from redis.commands.search.field import VectorField, TextField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType

r = Redis(host='localhost', port=6379)

# 创建向量索引
schema = (
    TextField("title"),
    VectorField("embedding", "HNSW", {
        "TYPE": "FLOAT32",
        "DIM": 768,
        "DISTANCE_METRIC": "COSINE",
    }),
)
r.ft("doc_index").create_index(schema, definition=IndexDefinition(prefix=["doc:"]))

# 存储向量
import numpy as np
embedding = np.random.rand(768).astype(np.float32).tobytes()
r.hset("doc:1", mapping={"title": "Go 语言指南", "embedding": embedding})

# 向量搜索
from redis.commands.search.query import Query
q = Query("*=>[KNN 5 @embedding $vec]").return_fields("title", "__embedding_score")
results = r.ft("doc_index").search(q, query_params={"vec": query_embedding})
for doc in results.docs:
    print(f"{doc.title}: {doc.__embedding_score}")</code></pre>

<h3 id="redis-vector-sets">Vector Sets（2025年新数据类型）</h3>
<p>Vector Sets 是专为向量相似性搜索设计的独立数据类型，减少内存使用，简化索引管理：</p>
<pre><code class="language-bash"># Redis Vector Sets 命令
VADD myset element1 1.0 0.5 0.3 ...
VSIM myset 0.8 0.4 0.2 ... COUNT 10</code></pre>

<h3 id="redis-7-features">Redis 7.x 关键特性</h3>
<ul>
<li><strong>ACL v2</strong>：更细粒度的权限控制，支持用户管理和角色分配。</li>
<li><strong>Function</strong>：替代 EVAL/EVALSHA，支持持久化 Lua 脚本。</li>
<li><strong>Multi-part AOF</strong>：AOF 文件分多部分存储，避免重写阻塞。</li>
<li><strong>Sharded Pub/Sub</strong>：分片发布订阅，消息只传播到持有对应 slot 的节点。</li>
<li><strong>LISTPACK</strong>：替代 ziplist，更高效的紧凑编码。</li>
</ul>

<h3 id="redis-stack">Redis Stack（已被 8.0 集成）</h3>
<p>Redis Stack 是之前将 RediSearch、RedisJSON、RedisTimeSeries、RedisBloom 打包的发行版。Redis 8.0 已将这些模块集成到核心中，Redis Stack 不再作为独立产品维护。</p>

<h3 id="redis-modern-clients">现代客户端</h3>
<table>
<thead><tr><th>语言</th><th>推荐客户端</th><th>特点</th></tr></thead>
<tbody>
<tr><td>Python</td><td><code>redis-py</code> 5.x</td><td>异步支持、类型提示</td></tr>
<tr><td>Go</td><td><code>go-redis/redis</code> v9</td><td>集群支持、pipeline</td></tr>
<tr><td>Java</td><td><code>Jedis</code> / <code>Lettuce</code></td><td>Lettuce 支持异步响应式</td></tr>
<tr><td>Node.js</td><td><code>ioredis</code></td><td>集群、pipeline、Lua</td></tr>
</tbody>
</table>
'''


# --- MySQL ---
UPDATES['/mysql/'] = '''
<hr>
<h2 id="mysql-2024-update">MySQL 8.x-9.0 新特性（2024-2026 更新）</h2>

<h3 id="mysql-innovation">创新发布模型</h3>
<p>MySQL 从 8.1.0 起采用创新发布模型：LTS 版本（长期支持，如 8.0、8.4）和创新版本（如 8.1-8.3、9.0-9.3），创新版本每 3 个月发布一次。</p>

<table>
<thead><tr><th>版本</th><th>类型</th><th>状态</th></tr></thead>
<tbody>
<tr><td>MySQL 8.0</td><td>LTS</td><td>扩展支持至 2026-04</td></tr>
<tr><td>MySQL 8.4</td><td>LTS</td><td>支持至 2032-04</td></tr>
<tr><td>MySQL 9.x</td><td>创新版</td><td>每 3 个月更新</td></tr>
</tbody>
</table>

<h3 id="mysql-9-features">MySQL 9.x 新特性</h3>
<ul>
<li><strong>JavaScript 存储程序</strong>：<code>CREATE FUNCTION ... LANGUAGE JAVASCRIPT</code>，可以在 MySQL 中用 JS 编写存储函数。</li>
<li><strong>向量数据类型</strong>：<code>VECTOR</code> 数据类型（通过 MySQL HeatWave），支持 AI 向量搜索。</li>
<li><strong>EXPLAIN INTO</strong>：将执行计划保存到变量中。</li>
<li><strong>权限管理增强</strong>：<code>SET ANY PRIVILEGE</code> 等系统权限。</li>
<li><strong>权限分析</strong>：<code>PRIVILEGE_CHECKS_USER</code> 改进。</li>
</ul>

<h3 id="mysql-84-features">MySQL 8.4 LTS 新特性</h3>
<ul>
<li><strong>InnoDB 改进</strong>：并行查询、自适应搜索改进。</li>
<li><strong>JSON 增强</strong>：<code>JSON_TABLE</code>、<code>JSON_SCHEMA_VALID</code> 等函数。</li>
<li><strong>窗口函数</strong>：<code>ROW_NUMBER()</code>、<code>RANK()</code>、<code>LEAD()</code>/<code>LAG()</code> 等（8.0+）。</li>
<li><strong>CTE 递归查询</strong>：<code>WITH RECURSIVE</code>。</li>
<li><strong>不可见索引</strong>：<code>ALTER TABLE t ALTER INDEX i INVISIBLE</code>，测试索引删除效果。</li>
<li><strong>降序索引</strong>：支持 <code>INDEX(idx_col DESC)</code>。</li>
<li><strong>直方图统计</strong>：<code>ANALYZE TABLE t UPDATE HISTOGRAM ON col</code>。</li>
</ul>

<h3 id="mysql-heatwave">MySQL HeatWave</h3>
<p>MySQL HeatWave 是 Oracle 推出的内存查询加速器，集成在 MySQL 数据库服务中：</p>
<ul>
<li>查询性能比 MySQL 高 5400 倍（OLAP 查询）。</li>
<li>HeatWave ML：内置机器学习训练和推理。</li>
<li>HeatWave AutoML：自动模型选择、超参数调优。</li>
<li>向量搜索支持：可用于 RAG、语义搜索等 AI 应用。</li>
</ul>

<h3 id="mysql-modern-practices">现代 MySQL 实践</h3>
<pre><code class="language-sql">-- 8.0+ 窗口函数示例
SELECT 
    product_name,
    price,
    RANK() OVER (ORDER BY price DESC) as price_rank,
    DENSE_RANK() OVER (PARTITION BY category ORDER BY price DESC) as category_rank,
    LAG(price, 1) OVER (ORDER BY price) as prev_price
FROM products;

-- CTE 递归查询
WITH RECURSIVE org_tree AS (
    SELECT id, name, manager_id, 1 AS level
    FROM employees WHERE manager_id IS NULL
    UNION ALL
    SELECT e.id, e.name, e.manager_id, ot.level + 1
    FROM employees e
    JOIN org_tree ot ON e.manager_id = ot.id
)
SELECT * FROM org_tree ORDER BY level;

-- JSON 操作
INSERT INTO events (data) VALUES ('{"type":"login","user":"alice","ip":"10.0.0.1"}');
SELECT data->>'$.user', data->>'$.ip' FROM events WHERE data->>'$.type' = 'login';

-- 不可见索引（测试删除索引的影响）
ALTER TABLE products ALTER INDEX idx_old INVISIBLE;
-- 观察性能后决定是否删除
-- ALTER TABLE products DROP INDEX idx_old;</code></pre>
'''


# --- Nginx ---
UPDATES['/nginx/'] = '''
<hr>
<h2 id="nginx-2024-update">Nginx 新特性（2024-2026 更新）</h2>

<h3 id="nginx-http3">HTTP/3 与 QUIC 支持（1.25.0+）</h3>
<p>Nginx 从 1.25.0 版本开始原生支持 HTTP/3 和 QUIC 协议。HTTP/3 基于 UDP，解决了 TCP 队头阻塞问题，支持 0-RTT 快速连接恢复。</p>
<pre><code class="language-nginx"># nginx.conf HTTP/3 配置
server {
    listen 443 ssl;
    listen 443 quic reuseport;  # 启用 HTTP/3
    http3 on;                    # 显式启用（1.27+）
    
    server_name example.com;
    
    ssl_certificate     /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    ssl_protocols       TLSv1.3;  # HTTP/3 强制要求 TLSv1.3
    
    # 启用 0-RTT
    ssl_early_data on;
    
    # QUIC 地址验证
    quic_retry on;
    
    # GSO 优化（Linux）
    quic_gso on;
    
    # 通知浏览器支持 HTTP/3
    add_header Alt-Svc 'h3=":443"; ma=86400';
    
    location / {
        proxy_pass http://backend;
    }
}</code></pre>

<h3 id="nginx-early-hints">HTTP Early Hints（1.29.0+）</h3>
<p>Nginx 1.29.0 引入了对 HTTP 103 Early Hints 的支持，允许服务器在最终响应前预发送资源加载指令，加速页面渲染：</p>
<pre><code class="language-nginx"># 103 Early Hints 配置
location / {
    add_before_body "Link: </style.css>; rel=preload; as=style";
    # 客户端收到 103 状态码后开始预加载
    # 随后收到 200 和实际内容
    proxy_pass http://backend;
}</code></pre>

<h3 id="nginx-versions">版本选择建议</h3>
<table>
<thead><tr><th>版本</th><th>特点</th><th>推荐场景</th></tr></thead>
<tbody>
<tr><td>1.29.x（主线）</td><td>最新特性，HTTP/3 + Early Hints</td><td>新项目、需要 HTTP/3</td></tr>
<tr><td>1.27.x（稳定）</td><td>HTTP/3 稳定支持</td><td>生产环境</td></tr>
<tr><td>1.26.x（LTS）</td><td>经过长期验证</td><td>保守环境</td></tr>
</tbody>
</table>

<h3 id="nginx-security-2024">安全更新（2024-2025）</h3>
<ul>
<li><strong>CVE-2024-35200</strong>：HTTP/3 QUIC 模块空指针解引用导致 DoS，建议升级到 1.27.2+。</li>
<li>推荐使用 OpenSSL 3.5.1+ 或 BoringSSL 构建 HTTP/3 支持。</li>
<li>支持通过 <code>OSSL_STORE</code> 加载密钥（1.29.0+）。</li>
</ul>

<h3 id="nginx-alternatives-2024">现代替代方案对比</h3>
<table>
<thead><tr><th>服务器</th><th>语言</th><th>特点</th><th>适用场景</th></tr></thead>
<tbody>
<tr><td>Nginx</td><td>C</td><td>高性能、HTTP/3、生态成熟</td><td>通用 Web 服务器/反向代理</td></tr>
<tr><td>Caddy</td><td>Go</td><td>自动 HTTPS、配置简洁</td><td>个人项目、快速部署</td></tr>
<tr><td>Traefik</td><td>Go</td><td>动态配置、容器原生</td><td>Docker/K8s 环境</td></tr>
<tr><td>BoringProxy</td><td>Go</td><td>基于 boringtun 的隧道代理</td><td>内网穿透</td></tr>
</tbody>
</table>
'''


# --- Docker ---
UPDATES['/other/docker/'] = '''
<hr>
<h2 id="docker-2024-update">Docker 2024-2026 更新</h2>

<h3 id="compose-v2">Docker Compose v2（已替代 v1）</h3>
<p>Docker Compose v2 使用 Go 重写，已成为默认的 compose 工具（命令为 <code>docker compose</code>，不再是 <code>docker-compose</code>）。截至 2026 年最新版本为 v2.37+。</p>

<pre><code class="language-yaml"># docker-compose.yml（v2 格式，无需 version 字段）
services:
  web:
    image: nginx:alpine
    ports:
      - "8080:80"
    depends_on:
      - api
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost"]
      interval: 30s
      timeout: 10s
      retries: 3

  api:
    build:
      context: ./api
      dockerfile: Dockerfile
    environment:
      - DB_HOST=db
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '1.0'
          memory: 512M

  db:
    image: postgres:16
    volumes:
      - db_data:/var/lib/postgresql/data
    environment:
      POSTGRES_PASSWORD: secret

volumes:
  db_data:</code></pre>

<h3 id="compose-bake">Bake 构建引擎（v2.37+ 默认启用）</h3>
<p>Bake 是 Docker 的新型构建引擎，支持并行构建、多目标构建和优化缓存：</p>
<pre><code class="language-bash"># Bake 并行构建多个服务
docker compose build --print  # 输出等效 Bakefile
docker compose build --platform linux/amd64,linux/arm64  # 多架构构建

# 直接使用 bake
docker buildx bake web api db  # 并行构建三个目标</code></pre>

<h3 id="buildkit">BuildKit / buildx</h3>
<p>BuildKit 是 Docker 的新一代构建引擎，支持并行构建、缓存挂载、密钥管理：</p>
<pre><code class="language-dockerfile"># Dockerfile with BuildKit features
# syntax=docker/dockerfile:1.7

FROM golang:1.24 AS builder

# 缓存挂载 - 加速依赖下载
RUN --mount=type=cache,target=/go/pkg/mod \
    --mount=type=cache,target=/root/.cache/go-build \
    go build -o /app ./...

# 密钥挂载 - 安全使用私有仓库
RUN --mount=type=secret,id=npmrc,target=/root/.npmrc \
    npm install

FROM alpine:3.20
COPY --from=builder /app /app
ENTRYPOINT ["/app"]</code></pre>

<h3 id="docker-2024-features">2024-2025 新特性</h3>
<ul>
<li><strong>外部服务（External Services）</strong>：Compose 中可引用外部服务（如云数据库）。</li>
<li><strong>镜像卷（volume.type=image）</strong>：使用镜像作为卷内容源，适合数据库初始化。</li>
<li><strong>静默模式</strong>：<code>--quiet</code> 和 <code>--quiet-build</code> 选项，适合 CI/CD。</li>
<li><strong>多架构构建</strong>：<code>docker compose build --platform linux/amd64,linux/arm64</code>。</li>
<li><strong>Model Runner</strong>：Docker Desktop 内置 AI 模型运行能力。</li>
<li><strong>containerd 集成</strong>：Docker Engine 可直接使用 containerd 作为运行时。</li>
</ul>

<h3 id="docker-alternatives">现代替代方案</h3>
<table>
<thead><tr><th>工具</th><th>特点</th><th>适用场景</th></tr></thead>
<tbody>
<tr><td>Podman</td><td>无守护进程、Rootless</td><td>安全敏感环境</td></tr>
<tr><td>containerd</td><td>轻量运行时</td><td>K8s 节点</td></tr>
<tr><td>Kaniko</td><td>K8s 内构建镜像</td><td>CI/CD 流水线</td></tr>
<tr><td>Buildah</td><td>脚本化构建</td><td>无 Dockerfile 构建</td></tr>
</tbody>
</table>
'''


# --- Git ---
UPDATES['/git/'] = '''
<hr>
<h2 id="git-2024-update">Git 新特性（2024-2026 更新）</h2>

<h3 id="git-features">Git 2.40+ 新特性</h3>
<ul>
<li><strong><code>git switch</code> / <code>git restore</code></strong>：分离 <code>checkout</code> 的功能，语义更清晰。
<pre><code class="language-bash">git switch feature-branch  # 切换分支
git switch -c new-feature  # 创建并切换
git restore file.txt       # 恢复文件
git restore --staged file.txt  # 取消暂存</code></pre>
</li>
<li><strong><code>--force-with-lease</code></strong>：比 <code>--force</code> 更安全的强制推送，如果远程有新提交会拒绝。
<pre><code class="language-bash">git push --force-with-lease  # 安全的强制推送</code></pre>
</li>
<li><strong>稀疏检出（Sparse Checkout）</strong>：只检出部分目录，适合大型仓库。
<pre><code class="language-bash">git sparse-checkout init --cone
git sparse-checkout set src/api src/web  # 只检出这两个目录</code></pre>
</li>
<li><strong>部分克隆（Partial Clone）</strong>：按需下载对象，减少初始克隆时间。
<pre><code class="language-bash">git clone --filter=blob:none --no-checkout https://github.com/repo.git</code></pre>
</li>
<li><strong><code>git merge-tree</code></strong>：无需实际合并即可预览合并结果。</li>
<li><strong>SCM 管理的 hook</strong>：<code>core.hooksPath</code> 可以指定 hook 目录，便于团队共享。</li>
</ul>

<h3 id="git-workflows">现代 Git 工作流</h3>
<table>
<thead><tr><th>工作流</th><th>特点</th><th>适用团队</th></tr></thead>
<tbody>
<tr><td>GitHub Flow</td><td>main + feature 分支，PR 合并</td><td>小团队、持续部署</td></tr>
<tr><td>Git Flow</td><td>main/develop/feature/release/hotfix</td><td>有版本发布的产品</td></tr>
<tr><td>Trunk-Based</td><td>所有人提交到 main，feature flag 控制</td><td>高频部署的团队</td></tr>
<tr><td>GitLab Flow</td><td>环境分支（production/staging）</td><td>多环境部署</td></tr>
</tbody>
</table>

<h3 id="git-config-modern">推荐现代配置</h3>
<pre><code class="language-bash"># 推荐的全局配置
git config --global init.defaultBranch main
git config --global pull.rebase true        # pull 时 rebase 而非 merge
git config --global push.autoSetupRemote true  # 自动设置远程跟踪
git config --global core.editor "code --wait"  # 使用 VS Code 编辑
git config --global commit.gpgsign true      # 签名提交
git config --global rerere.enabled true      # 记住冲突解决

# 行尾符配置
git config --global core.autocrlf input      # macOS/Linux
git config --global core.autocrlf true       # Windows</code></pre>

<h3 id="git-tools">现代 Git 工具</h3>
<ul>
<li><strong><code>lazygit</code></strong>：终端 Git TUI，可视化操作。</li>
<li><strong><code>gh</code></strong>：GitHub CLI，直接命令行操作 PR/Issue。</li>
<li><strong><code>gitui</code></strong>：Rust 编写的 Git TUI。</li>
<li><strong><code>tig</code></strong>：文本模式 Git 仓库浏览器。</li>
<li><strong><code>pre-commit</code></strong>：多语言 Git hook 管理框架。</li>
</ul>
'''


# --- Elasticsearch ---
UPDATES['/elastic/'] = '''
<hr>
<h2 id="es-2024-update">Elasticsearch 8.x 更新（2024-2026）</h2>

<h3 id="es-8-features">Elasticsearch 8.x 关键特性</h3>
<ul>
<li><strong>向量搜索（kNN）</strong>：原生支持近似最近邻搜索，支持 HNSW 算法。
<pre><code class="language-json">// 创建向量索引
PUT /products {
  "mappings": {
    "properties": {
      "name": { "type": "text" },
      "embedding": {
        "type": "dense_vector",
        "dims": 768,
        "index": true,
        "similarity": "cosine"
      }
    }
  }
}

// 向量搜索
POST /products/_search {
  "knn": {
    "field": "embedding",
    "query_vector": [0.1, 0.2, ...],
    "k": 10,
    "num_candidates": 100
  }
}</code></pre>
</li>
<li><strong>ES|QL</strong>：新的管道查询语言，比 DSL 更简洁。
<pre><code class="language-text">POST /_query
{
  "query": "FROM logs | WHERE status >= 400 | STATS count = COUNT(*) BY status | SORT count DESC"
}</code></pre>
</li>
<li><strong>语义搜索</strong>：内置 ELSER 模型，无需自行生成 embedding。</li>
<li><strong>安全默认开启</strong>：8.x 默认启用 TLS 和安全认证。</li>
<li><strong>处理大型数据集</strong>：支持 frozen tier 和 searchable snapshots。</li>
</ul>

<h3 id="es-alternatives">搜索引擎对比（2026年）</h3>
<table>
<thead><tr><th>引擎</th><th>语言</th><th>特点</th><th>向量搜索</th></tr></thead>
<tbody>
<tr><td>Elasticsearch 8.x</td><td>Java</td><td>全文+向量+日志分析</td><td>✅ dense_vector</td></tr>
<tr><td>Meilisearch</td><td>Rust</td><td>轻量、易用、毫秒搜索</td><td>✅（1.x+）</td></tr>
<tr><td>Typesense</td><td>C++</td><td>纯内存、高性能</td><td>✅</td></tr>
<tr><td>OpenSearch</td><td>Java</td><td>ES 开源分支</td><td>✅</td></tr>
<tr><td>Zinc</td><td>Go</td><td>轻量级 ES 替代</td><td>有限</td></tr>
<tr><td>Quickwit</td><td>Rust</td><td>日志搜索、对象存储</td><td>✅</td></tr>
</tbody>
</table>
'''


# --- gRPC ---
UPDATES['/grpc/'] = '''
<hr>
<h2 id="grpc-2024-update">gRPC 更新（2024-2026）</h2>

<h3 id="grpc-features">现代 gRPC 特性</h3>
<ul>
<li><strong>gRPC-Web</strong>：浏览器直接调用 gRPC 服务，无需 HTTP 代理。</li>
<li><strong>xDS 支持</strong>：通过 xDS API 实现服务网格集成（Istio、Envoy）。</li>
<li><strong>Protobuf Editions</strong>：替代 proto2/proto3 的新版本模型。</li>
<li><strong>Connect 协议</strong>：Buf 推出的 Connect-RPC，兼容 gRPC 和 HTTP/JSON。</li>
</ul>

<h3 id="grpc-buf">Buf 工具链（推荐）</h3>
<p><code>buf</code> 是现代 Protobuf 管理工具，替代 <code>protoc</code> + 各种插件：</p>
<pre><code class="language-bash"># 安装 buf
brew install bufbuild/buf/buf

# buf.gen.yaml - 代码生成配置
version: v2
plugins:
  - local: protoc-gen-go
    out: gen/go
  - local: protoc-gen-go-grpc
    out: gen/go
  - local: protoc-gen-connect-go
    out: gen/go

# 生成代码
buf generate

# 检查兼容性
buf breaking --against .git#branch=main</code></pre>

<h3 id="grpc-connect">Connect-RPC（推荐替代传统 gRPC）</h3>
<p>Connect-RPC 兼容 gRPC 协议，同时支持 HTTP/JSON 客户端，无需 gRPC 代理：</p>
<pre><code class="language-go">// Go 服务端
import "connectrpc.com/connect"

func main() {
    mux := http.NewServeMux()
    handler := connect.NewHandler(
        pingv1connect.NewPingServiceHandler(&PingServer{}),
    )
    mux.Handle(pingv1connect.NewPingServiceHandler(
        &PingServer{},
    ))
    http.ListenAndServe(":8080", mux)
}

// 客户端可以直接用 HTTP/JSON 调用
// curl -H 'Content-Type: application/json' \
//   -d '{"name":"world"}' \
//   http://localhost:8080/ping.v1.PingService/Ping</code></pre>
'''


# --- Rust ---
UPDATES['/other/rust/'] = '''
<hr>
<h2 id="rust-2024-update">Rust 2024 Edition 更新</h2>

<h3 id="rust-2024-edition">Rust Edition 2024</h3>
<p>Rust 2024 Edition 是继 2015、2018、2021 之后的第四个 Edition，带来多项语言改进：</p>
<ul>
<li><strong>async 闭包</strong>：原生支持 <code>async ||</code> 闭包语法。
<pre><code class="language-rust">// Rust 2024: async 闭包
let fetcher = async || {
    let data = fetch_data().await;
    process(data).await
};
// 调用
let result = fetcher().await;</code></pre>
</li>
<li><strong>gen 块</strong>：生成器块，简化迭代器编写。
<pre><code class="language-rust">// Rust 2024: gen 块
fn fibonacci() -> impl Iterator<Item = u64> {
    gen {
        let mut a = 0;
        let mut b = 1;
        loop {
            yield a;
            let next = a + b;
            a = b;
            b = next;
        }
    }
}</code></pre>
</li>
<li><strong>生命周期捕获规则变更</strong>：<code>impl Trait</code> 返回类型默认捕获所有生命周期。</li>
<li><strong><code>unsafe_op_in_unsafe_fn</code> 默认启用</strong>：unsafe 函数内的 unsafe 操作需要显式标注。</li>
<li><strong><code>cfg_select!</code></strong>：编译时条件选择宏。</li>
</ul>

<h3 id="rust-ecosystem">Rust 生态系统（2026年）</h3>
<table>
<thead><tr><th>领域</th><th>推荐 crate</th><th>说明</th></tr></thead>
<tbody>
<tr><td>Web 框架</td><td><code>axum</code></td><td>基于 tokio，类型安全</td></tr>
<tr><td>异步运行时</td><td><code>tokio</code></td><td>事实标准</td></tr>
<tr><td>序列化</td><td><code>serde</code></td><td>JSON/YAML/TOML</td></tr>
<tr><td>HTTP 客户端</td><td><code>reqwest</code></td><td>基于 hyper</td></tr>
<tr><td>数据库</td><td><code>sqlx</code></td><td>编译时 SQL 检查</td></tr>
<tr><td>CLI</td><td><code>clap</code></td><td>命令行解析</td></tr>
<tr><td>日志</td><td><code>tracing</code></td><td>结构化日志+分布式追踪</td></tr>
<tr><td>包管理</td><td><code>cargo</code></td><td>内置工具链</td></tr>
</tbody>
</table>

<pre><code class="language-bash"># Rust 安装（2026 推荐方式）
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# 使用 Rust 2024 Edition
# Cargo.toml
# [package]
# edition = "2024"

# 工具链管理
rustup default stable
rustup component add rustfmt clippy
cargo install cargo-watch  # 文件变更自动重编译</code></pre>
'''


# --- WebAssembly ---
UPDATES['/other/wasm/'] = '''
<hr>
<h2 id="wasm-2024-update">WebAssembly 更新（2024-2026）</h2>

<h3 id="wasi-preview">WASI Preview 2 & Component Model</h3>
<p>WebAssembly System Interface (WASI) Preview 2 引入了 Component Model，使不同语言编译的 Wasm 模块可以互相调用：</p>
<ul>
<li><strong>Component Model</strong>：跨语言 Wasm 模块互操作，共享接口定义。</li>
<li><strong>WIT（Wasm Interface Type）</strong>：声明式接口定义语言。</li>
<li><strong>wasm-tools</strong>：用于组件操作的工具链。</li>
</ul>

<pre><code class="language-wit">// example.wit - Wasm 接口定义
package example:greeter;

interface api {
    greet: func(name: string) -> string;
}

world greeter-world {
    export api;
}</code></pre>

<h3 id="wasm-runtimes">运行时对比</h3>
<table>
<thead><tr><th>运行时</th><th>语言</th><th>特点</th><th>WASI</th></tr></thead>
<tbody>
<tr><td>WasmEdge</td><td>C++</td><td>轻量、AI 友好</td><td>Preview 2</td></tr>
<tr><td>Wasmtime</td><td>Rust</td><td>Bytecode Alliance 官方</td><td>Preview 2</td></tr>
<tr><td>Wasmer</td><td>Rust</td><td>支持多语言 SDK</td><td>Preview 2</td></tr>
<tr><td>browser</td><td>-</td><td>浏览器内置</td><td>Preview 1</td></tr>
</tbody>
</table>

<h3 id="wasm-use-cases">Wasm 应用场景</h3>
<ul>
<li><strong>边缘计算</strong>：Cloudflare Workers、Fastly Compute@Edge 使用 Wasm。</li>
<li><strong>Serverless</strong>：轻量级冷启动，比容器快 100 倍。</li>
<li><strong>插件系统</strong>：应用支持用户用任意语言编写 Wasm 插件。</li>
<li><strong>AI 推理</strong>：WasmEdge 支持 WASI-NN，在 Wasm 中运行 AI 模型。</li>
</ul>
'''


# --- Shell ---
UPDATES['/other/shell/'] = '''
<hr>
<h2 id="shell-2024-update">现代 Shell 工具更新（2024-2026）</h2>

<h3 id="modern-unix-2024">Modern Unix 工具链</h3>
<table>
<thead><tr><th>现代工具</th><th>替代</th><th>说明</th></tr></thead>
<tbody>
<tr><td><code>bat</code></td><td>cat</td><td>语法高亮、行号、Git 集成</td></tr>
<tr><td><code>eza</code></td><td>ls</td><td>exa 的继任者，Git 集成</td></tr>
<tr><td><code>zoxide</code></td><td>cd</td><td>智能目录跳转，频率排序</td></tr>
<tr><td><code>ripgrep</code> (<code>rg</code>)</td><td>grep</td><td>极速搜索，尊重 .gitignore</td></tr>
<tr><td><code>fd</code></td><td>find</td><td>友好的文件查找</td></tr>
<tr><td><code>delta</code></td><td>diff</td><td>美化 Git diff 输出</td></tr>
<tr><td><code>dust</code></td><td>du</td><td>磁盘使用可视化</td></tr>
<tr><td><code>procs</code></td><td>ps</td><td>彩色进程列表</td></tr>
<tr><td><code>btop</code></td><td>top/htop</td><td>系统监控可视化</td></tr>
<tr><td><code>jq</code> / <code>yq</code></td><td>-</td><td>JSON/YAML 处理</td></tr>
<tr><td><code>fzf</code></td><td>-</td><td>模糊查找器</td></tr>
<tr><td><code>starship</code></td><td>-</td><td>跨 shell 提示符</td></tr>
</tbody>
</table>

<h3 id="fish-nushell">现代 Shell</h3>
<ul>
<li><strong>Nushell（nu）</strong>：结构化数据 Shell，管道传递表格数据而非纯文本。
<pre><code class="language-bash"># Nushell 示例
ls | where size > 10MB | sort-by size | select name size
open data.json | get users | where age > 18 | count</code></pre>
</li>
<li><strong>Fish Shell</strong>：开箱即用的自动补全和语法高亮。</li>
<li><strong>Zsh + Oh My Zsh</strong>：最流行的 shell 配置框架。</li>
</ul>
'''


# --- Flutter ---
UPDATES['/flutter/'] = '''
<hr>
<h2 id="flutter-2024-update">Flutter 更新（2024-2026）</h2>

<h3 id="flutter-3x">Flutter 3.x 新特性</h3>
<ul>
<li><strong>Impeller 渲染引擎</strong>：替代 Skia，预先编译着色器，消除卡顿。</li>
<li><strong>Material 3</strong>：全面支持 Material Design 3 设计规范。</li>
<li><strong>Dart 3</strong>：空安全、记录类型（Records）、模式匹配。
<pre><code class="language-dart">// Dart 3 记录类型
var record = ('first', a: 2, b: true, 'last');
print(record.$1);    // first
print(record.a);     // 2

// 模式匹配
switch (status) {
  case 200:
    print('OK');
  case >= 400 && < 500:
    print('Client error');
  case >= 500:
    print('Server error');
}</code></pre>
</li>
<li><strong>Flutter Web 改进</strong>：CanvasKit 渲染器、Wasm 编译支持。</li>
<li><strong>Widget 状态管理</strong>：官方推荐 Riverpod / Provider / Bloc。</li>
</ul>

<h3 id="flutter-state">状态管理方案对比</h3>
<table>
<thead><tr><th>方案</th><th>复杂度</th><th>特点</th></tr></thead>
<tbody>
<tr><td>Provider</td><td>低</td><td>官方推荐入门方案</td></tr>
<tr><td>Riverpod</td><td>中</td><td>编译时安全、可测试</td></tr>
<tr><td>Bloc/Cubit</td><td>高</td><td>事件驱动、适合大型应用</td></tr>
<tr><td>GetX</td><td>低</td><td>一站式（路由+状态+依赖）</td></tr>
<tr><td>Signal</td><td>低</td><td>响应式、类似 SolidJS</td></tr>
</tbody>
</table>
'''


# --- Memcached ---
UPDATES['/memcached/'] = '''
<hr>
<h2 id="memcached-2024-update">Memcached 更新（2024-2026）</h2>

<h3 id="memcached-features">现代 Memcached</h3>
<ul>
<li><strong>Memcached 1.6.x</strong>：支持 EXTSTORE（SSD 扩展存储）、自动故障转移。</li>
<li><strong>Meta 协议</strong>：新的二进制协议，支持更丰富的操作。</li>
<li><strong>简化部署</strong>：内置集群支持（需客户端一致性哈希）。</li>
</ul>

<h3 id="memcached-vs-redis">Memcached vs Redis（2026年对比）</h3>
<table>
<thead><tr><th>特性</th><th>Memcached</th><th>Redis</th></tr></thead>
<tbody>
<tr><td>数据结构</td><td>仅 KV 字符串</td><td>String/List/Hash/Set/Stream/Vector</td></tr>
<tr><td>持久化</td><td>无</td><td>RDB + AOF</td></tr>
<tr><td>集群</td><td>客户端分片</td><td>原生集群</td></tr>
<tr><td>内存效率</td><td>更高（更简单）</td><td>稍低（更多功能）</td></tr>
<tr><td>多线程</td><td>✅ 原生</td><td>6.0+（IO 多线程）</td></tr>
<tr><td>向量搜索</td><td>❌</td><td>✅ 7.2+</td></tr>
<tr><td>Pub/Sub</td><td>❌</td><td>✅</td></tr>
<tr><td>适用场景</td><td>纯缓存</td><td>缓存+数据库+消息队列</td></tr>
</tbody>
</table>
'''


# --- macOS ---
UPDATES['/mac/'] = '''
<hr>
<h2 id="mac-2024-update">macOS 工具更新（2024-2026）</h2>

<h3 id="mac-sonoma-sequoia">macOS 14-15 新特性</h3>
<ul>
<li><strong>Apple Silicon（M3/M4）</strong>：性能大幅提升，Go/Rust/Python 原生 ARM64 支持。</li>
<li><strong>Homebrew on ARM</strong>：<code>/opt/homebrew</code>（ARM）与 <code>/usr/local</code>（Intel）分离。</li>
<li><strong>Shortcuts 自动化</strong>：替代 Automator，支持命令行调用。</li>
</ul>

<h3 id="mac-dev-tools">推荐开发工具</h3>
<table>
<thead><tr><th>工具</th><th>用途</th><th>安装</th></tr></thead>
<tbody>
<tr><td><code>homebrew</code></td><td>包管理</td><td>brew.sh</td></tr>
<tr><td><code>orbstack</code></td><td>Docker/Linux 替代</td><td>比 Docker Desktop 轻量</td></tr>
<tr><td><code>raycast</code></td><td>启动器</td><td>替代 Spotlight</td></tr>
<tr><td><code>iterm2</code> / <code>warp</code></td><td>终端</td><td>Warp 有 AI 辅助</td></tr>
<tr><td><code>zed</code></td><td>编辑器</td><td>Rust 编写，极速</td></tr>
<tr><td><code>utm</code></td><td>虚拟机</td><td>支持 ARM/Linux/Windows</td></tr>
</tbody>
</table>
'''


# --- Go sub-pages ---
UPDATES['/golang/gin/'] = '''
<hr>
<h2 id="gin-2024-update">Gin 框架更新（2024-2026）</h2>
<p>Gin v1.10+ 的主要变化：</p>
<ul>
<li>支持 Go 泛型中间件。</li>
<li><code>context.Value</code> 性能优化。</li>
<li>内置 OpenAPI/Swagger 文档生成。</li>
<li>改进的 JSON 序列化（支持 <code>encoding/json/v2</code> 实验）。</li>
<li>推荐使用 <code>go-playground/validator/v10</code> 进行请求验证。</li>
</ul>
<pre><code class="language-go">// Gin v1.10+ 泛型中间件
func AuthMiddleware[T User]() gin.HandlerFunc {
    return func(c *gin.Context) {
        user := GetUserFromContext[T](c)
        if !user.HasPermission() {
            c.AbortWithStatus(403)
            return
        }
        c.Next()
    }
}</code></pre>
'''

UPDATES['/golang/echo/'] = '''
<hr>
<h2 id="echo-2024-update">Echo 框架更新（2024-2026）</h2>
<p>Echo v4.12+ 的主要变化：</p>
<ul>
<li>改进的 Binder 支持泛型。</li>
<li>内置 Prometheus 指标中间件。</li>
<li>支持 HTTP/2 服务端推送。</li>
<li>推荐替代方案：如果需要更现代的框架，可考虑 <code>Fiber</code>（基于 fasthttp）或 <code>Huma</code>（OpenAPI 优先）。</li>
</ul>
'''

UPDATES['/golang/log/'] = '''
<hr>
<h2 id="golog-2024-update">Go 日志更新（2024-2026）</h2>
<p>Go 1.21 引入了 <code>log/slog</code> 结构化日志标准库，推荐替代 <code>log</code> 包：</p>
<pre><code class="language-go">import "log/slog"

// 基本使用
slog.Info("user logged in", "user_id", 123, "ip", "10.0.0.1")
// 输出: 2026/08/25 10:00:00 INFO user logged in user_id=123 ip=10.0.0.1

// JSON 格式
logger := slog.New(slog.NewJSONHandler(os.Stdout, nil))
logger.Info("request completed",
    "method", "GET",
    "path", "/api/users",
    "status", 200,
    "duration_ms", 15,
)

// 自定义 Handler
handler := slog.NewTextHandler(os.Stdout, &slog.HandlerOptions{
    Level: slog.LevelDebug,
    AddSource: true,
})
logger := slog.New(handler)</code></pre>
'''

UPDATES['/golang/sort/'] = '''
<hr>
<h2 id="gosort-2024-update">Go 排序更新（2024-2026）</h2>
<p>Go 1.21 引入了 <code>slices</code> 包，提供泛型排序函数，比旧的 <code>sort</code> 包更安全、更高效：</p>
<pre><code class="language-go">import "slices"

// 泛型排序
slices.Sort(nums)                    // 升序
slices.SortFunc(nums, func(a, b int) int {
    return b - a                    // 降序
})
slices.SortStable(nums, cmp)        // 稳定排序

// 搜索
idx, found := slices.BinarySearch(nums, 42)

// 其他常用操作
slices.Contains(nums, 42)
slices.Reverse(nums)
slices.Min(nums)
slices.Max(nums)</code></pre>
'''

UPDATES['/golang/generic/'] = '''
<hr>
<h2 id="gogeneric-2024-update">Go 泛型更新</h2>
<p>Go 泛型自 1.18 引入以来不断改进。1.21 引入 <code>cmp</code> 包，1.24 支持泛型类型别名。详见 <a href="/golang/generics-update/">泛型进阶</a> 页面。</p>
'''

UPDATES['/golang/io/'] = '''
<hr>
<h2 id="goio-2024-update">Go IO 更新（2024-2026）</h2>
<p>Go 1.21+ IO 相关改进：</p>
<ul>
<li><code>io/fs</code> 包稳定，支持虚拟文件系统。</li>
<li>新增 <code>errors.Join</code> 多错误合并。</li>
<li><code>log/slog</code> 结构化日志集成 IO。</li>
</ul>
'''

UPDATES['/golang/package/'] = '''
<hr>
<h2 id="gopackage-2024-update">Go 常用包更新（2024-2026）</h2>
<p>Go 1.21-1.24 新增标准库：</p>
<table>
<thead><tr><th>包</th><th>版本</th><th>用途</th></tr></thead>
<tbody>
<tr><td><code>log/slog</code></td><td>1.21</td><td>结构化日志</td></tr>
<tr><td><code>slices</code></td><td>1.21</td><td>泛型切片操作</td></tr>
<tr><td><code>maps</code></td><td>1.21</td><td>泛型 map 操作</td></tr>
<tr><td><code>cmp</code></td><td>1.21</td><td>比较约束</td></tr>
<tr><td><code>iter</code></td><td>1.23</td><td>迭代器类型</td></tr>
<tr><td><code>structs</code></td><td>1.23</td><td>结构体工具</td></tr>
<tr><td><code>unique</code></td><td>1.23</td><td>值驻留</td></tr>
<tr><td><code>crypto/mlkem</code></td><td>1.24</td><td>后量子密码</td></tr>
<tr><td><code>crypto/sha3</code></td><td>1.24</td><td>SHA-3 哈希</td></tr>
<tr><td><code>weak</code></td><td>1.24</td><td>弱指针</td></tr>
</tbody>
</table>
'''

UPDATES['/golang/iris/'] = '''
<hr>
<h2 id="iris-2024-update">Iris 框架更新</h2>
<p>Iris v12.2+ 持续更新。但如果考虑新项目，推荐评估以下替代方案：</p>
<ul>
<li><code>net/http</code>（标准库 1.22+ 路由增强后已足够简单场景使用）</li>
<li><code>chi</code>（轻量、兼容标准库）</li>
<li><code>Echo</code> / <code>Gin</code>（生态更活跃）</li>
</ul>
'''

UPDATES['/golang/stringer/'] = '''
<hr>
<h2 id="stringer-2024-update">Go Stringer 更新</h2>
<p><code>stringer</code> 工具用于自动生成枚举类型的 String() 方法。Go 1.24 的 <code>go tool</code> 指令简化了工具调用：</p>
<pre><code class="language-bash"># Go 1.24+ go.mod 中声明工具依赖
go get -tool golang.org/x/tools/cmd/stringer
go tool stringer -type=Pill</code></pre>
'''

UPDATES['/golang/shell/'] = '''
<hr>
<h2 id="goshell-2024-update">Go 调用 Shell 更新</h2>
<p>Go 1.21+ 改进的命令执行方式：</p>
<pre><code class="language-go">// 使用 context 控制超时
ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
defer cancel()

cmd := exec.CommandContext(ctx, "git", "status")
output, err := cmd.CombinedOutput()
if err != nil {
    log.Printf("命令执行失败: %v, 输出: %s", err, output)
}</code></pre>
'''

UPDATES['/golang/code/'] = '''
<hr>
<h2 id="gocode-2024-update">Go 代码片段更新（2024-2026）</h2>
<p>常用现代 Go 代码模式：</p>
<pre><code class="language-go">// 1. 结构化错误
type AppError struct {
    Code    string
    Message string
    Cause   error
}

func (e *AppError) Error() string { return e.Message }
func (e *AppError) Unwrap() error { return e.Cause }

// 2. 泛型选项模式
type Option[T any] func(*T)
func WithName[T any](name string) Option[T] {
    return func(t *T) { /* set name */ }
}

// 3. slog 日志
slog.Info("processing", "input", input, "duration", time.Since(start))

// 4. slices 包
slices.SortFunc(items, func(a, b Item) int {
    return cmp.Compare(a.Priority, b.Priority)
})</code></pre>
'''

UPDATES['/golang/go-git/'] = '''
<hr>
<h2 id="gogit-2024-update">go-git 更新</h2>
<p><code>go-git</code> v5.12+ 支持 Go 泛型和新的 transport 层。对于简单 Git 操作，也可考虑使用 <code>os/exec</code> 调用系统 git。</p>
'''

UPDATES['/golang/freetype/'] = '''
<hr>
<h2 id="gofreetype-2024-update">FreeType 更新</h2>
<p>Go 的 <code>freetype</code> 库主要用于字体渲染。对于现代项目，推荐使用 <code>golang.org/x/image/font</code> + <code>github.com/golang/freetype/truetype</code>。</p>
'''

UPDATES['/golang/groupby/'] = '''
<hr>
<h2 id="gogroupby-2024-update">切片分组更新</h2>
<p>Go 1.21 的 <code>slices</code> 和 <code>maps</code> 包简化了分组操作：</p>
<pre><code class="language-go">import "slices"
import "maps"

// 泛型分组函数
func GroupBy[T any, K comparable](items []T, keyFn func(T) K) map[K][]T {
    result := make(map[K][]T)
    for _, item := range items {
        k := keyFn(item)
        result[k] = append(result[k], item)
    }
    return result
}

// 使用
type Order struct{ ID string; Status string }
orders := []Order{{"1", "paid"}, {"2", "pending"}, {"3", "paid"}}
grouped := GroupBy(orders, func(o Order) string { return o.Status })
// grouped["paid"] = [{1 paid}, {3 paid}]
// grouped["pending"] = [{2 pending}]</code></pre>
'''


# --- Nginx sub-pages ---
UPDATES['/nginx/use/'] = '''
<hr>
<h2 id="nginx-use-2024-update">Nginx 常用技巧更新（2024-2026）</h2>
<pre><code class="language-nginx"># HTTP/3 + HTTP/2 双监听
server {
    listen 443 ssl;
    listen 443 quic reuseport;
    http3 on;
    add_header Alt-Svc 'h3=":443"; ma=86400';
    
    ssl_protocols TLSv1.3;
    ssl_early_data on;
}

# gRPC 反向代理
location /greet.Greeter {
    grpc_pass grpc://grpc-backend:50051;
}

# WebSocket 代理
location /ws {
    proxy_pass http://backend;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
}

# 限流
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
location /api {
    limit_req zone=api burst=20 nodelay;
    proxy_pass http://backend;
}</code></pre>
'''

UPDATES['/nginx/install/'] = '''
<hr>
<h2 id="nginx-install-2024-update">Nginx 安装更新</h2>
<p>2026 年推荐安装方式：</p>
<pre><code class="language-bash"># Ubuntu/Debian - 官方仓库
sudo apt install -y curl gnupg2 ca-certificates lsb-release
curl -fsSL https://nginx.org/keys/nginx_signing.key | sudo gpg --dearmor -o /usr/share/keyrings/nginx-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/nginx-archive-keyring.gpg] http://nginx.org/packages/mainline/ubuntu $(lsb_release -cs) nginx" | sudo tee /etc/apt/sources.list.d/nginx.list
sudo apt update && sudo apt install nginx

# macOS
brew install nginx

# Docker
docker run -d --name nginx -p 80:80 -p 443:443 -v ./nginx.conf:/etc/nginx/nginx.conf nginx:mainline

# 启用 HTTP/3 需要从源码编译
./configure --with-http_v3_module --with-debug
make && make install</code></pre>
'''

UPDATES['/nginx/http/'] = '''
<hr>
<h2 id="nginx-http-2024-update">HTTP 模块更新</h2>
<p>Nginx 1.25+ 新增 HTTP/3 和 Early Hints 支持。核心 HTTP 模块改进：</p>
<ul>
<li><code>http3 on|off</code> 指令（1.27+）</li>
<li><code>quic_retry</code>、<code>quic_gso</code>、<code>ssl_early_data</code> 指令</li>
<li><code>add_before_body</code> 支持 103 Early Hints（1.29+）</li>
</ul>
'''

UPDATES['/nginx/rtmp/'] = '''
<hr>
<h2 id="nginx-rtmp-2024-update">RTMP 模块更新</h2>
<p>Nginx RTMP 模块（<code>nginx-rtmp-module</code>）仍在社区维护。对于现代直播场景，推荐评估：</p>
<ul>
<li><strong>SRS（Simple Realtime Server）</strong>：Go 编写，支持 RTMP/HLS/WebRTC/FLV。</li>
<li><strong>MediaMTX</strong>：Go 编写，轻量级流媒体服务器。</li>
</ul>
'''


# --- Other pages ---
UPDATES['/other/github/'] = '''
<hr>
<h2 id="github-2024-update">GitHub 更新（2024-2026）</h2>
<ul>
<li><strong>GitHub Copilot</strong>：AI 代码助手，支持代码补全、PR 审查、安全修复。</li>
<li><strong>GitHub Actions</strong>：CI/CD 平台，支持矩阵构建、缓存、并发。</li>
<li><strong>GitHub CLI（gh）</strong>：命令行操作 PR/Issue/Actions。</li>
<li><strong>GitHub Codespaces</strong>：云端开发环境。</li>
<li><strong>GitHub Models</strong>：在 GitHub 上直接运行 AI 模型。</li>
</ul>
<pre><code class="language-bash"># gh CLI 常用命令
gh pr create --title "feat: add X" --body "description"
gh pr merge --squash --delete-branch
gh issue list --assignee @me
gh run watch  # 监控 Actions 运行</code></pre>
'''

UPDATES['/other/gitlab/'] = '''
<hr>
<h2 id="gitlab-2024-update">GitLab 更新（2024-2026）</h2>
<p>GitLab 16-17 主要更新：</p>
<ul>
<li><strong>GitLab Duo</strong>：AI 辅助代码建议、MR 摘要、聊天。</li>
<li><strong>CI/CD 组件</strong>：可复用 CI 组件，替代 include 模板。</li>
<li><strong>Fleet 规模管理</strong>：管理多个 GitLab 实例。</li>
</ul>
'''

UPDATES['/other/harbor/'] = '''
<hr>
<h2 id="harbor-2024-update">Harbor 更新（2024-2026）</h2>
<p>Harbor v2.11+ 主要更新：</p>
<ul>
<li>支持 Cosign 签名验证。</li>
<li>支持 OCI Artifact（非容器镜像制品）。</li>
<li>改进的机器人账户和 Webhook。</li>
</ul>
'''

UPDATES['/other/hugo/'] = '''
<hr>
<h2 id="hugo-2024-update">Hugo 更新（2024-2026）</h2>
<p>本博客已从 Hugo 迁移为纯静态 HTML，但 Hugo 本身仍在活跃发展：</p>
<ul>
<li><strong>Hugo v0.130+</strong>：改进的模板系统、更快的构建。</li>
<li><strong>推荐的现代主题</strong>：Hugo Modules、PaperMod、Blowfish。</li>
<li>但静态站点的趋势是向 SSG + 组件化发展（Astro、Next.js SSG）。</li>
</ul>
'''

UPDATES['/other/vim/'] = '''
<hr>
<h2 id="vim-2024-update">Vim/Neovim 更新（2024-2026）</h2>
<p>Neovim 是现代 Vim 分支，推荐使用：</p>
<ul>
<li><strong>Neovim 0.10+</strong>：内置 LSP 完善、Tree-sitter 语法高亮。</li>
<li><strong>LazyVim</strong>：基于 lazy.nvim 的现代化配置发行版。</li>
<li><strong>替代编辑器</strong>：Zed（Rust 编写，极速）、VS Code、Helix。</li>
</ul>
<pre><code class="language-bash"># 安装 Neovim
brew install neovim

# 安装 LazyVim
git clone https://github.com/LazyVim/starter ~/.config/nvim
nvim  # 自动安装插件</code></pre>
'''

UPDATES['/other/markdown/'] = '''
<hr>
<h2 id="markdown-2024-update">Markdown 更新（2024-2026）</h2>
<p>Markdown 生态变化：</p>
<ul>
<li><strong>CommonMark</strong>：标准化 Markdown 语法。</li>
<li><strong>GFM（GitHub Flavored Markdown）</strong>：表格、任务列表、删除线。</li>
<li><strong>MDX</strong>：Markdown + JSX 组件，用于现代文档站点。</li>
<li><strong>Obsidian / Logseq</strong>：基于 Markdown 的知识管理工具。</li>
</ul>
'''

UPDATES['/other/web/'] = '''
<hr>
<h2 id="web-2024-update">Web 技术更新（2024-2026）</h2>
<ul>
<li><strong>View Transitions API</strong>：原生页面过渡动画。</li>
<li><strong>Container Queries</strong>：基于容器尺寸的响应式设计。</li>
<li><strong><code>:has()</code> 选择器</strong>：父选择器，改变 CSS 编写方式。</li>
<li><strong>Bun</strong>：极速 JS 运行时和包管理器。</li>
<li><strong>HTMX</strong>：无需 JS 框架的 AJAX 交互。</li>
</ul>
'''

UPDATES['/other/makefile/'] = '''
<hr>
<h2 id="makefile-2024-update">Makefile 更新</h2>
<p>现代替代方案：</p>
<ul>
<li><strong>Taskfile（go-task）</strong>：YAML 格式，跨平台，更易读。</li>
<li><strong>Just</strong>：Rust 编写的命令运行器。</li>
<li><strong>Mage</strong>：Go 编写的 Make 替代，用 Go 写构建脚本。</li>
</ul>
'''

UPDATES['/other/search/'] = '''
<hr>
<h2 id="search-2024-update">搜索技巧更新</h2>
<p>2026 年搜索建议：</p>
<ul>
<li>使用 AI 搜索（Perplexity、ChatGPT 搜索）获取综合答案。</li>
<li>代码搜索用 <code>grep.app</code>、<code>sourcegraph.com</code>。</li>
<li>GitHub 代码搜索已大幅改进，支持正则和语义搜索。</li>
</ul>
'''

UPDATES['/other/brew/'] = '''
<hr>
<h2 id="brew-2024-update">Homebrew 更新（2024-2026）</h2>
<pre><code class="language-bash"># Apple Silicon (M1/M2/M3/M4)
# Homebrew 安装在 /opt/homebrew

# 常用命令
brew install ripgrep fd bat eza zoxide fzf
brew install --cask raycast orbstack warp zed

# Brewfile 管理依赖
brew bundle dump    # 导出当前安装列表
brew bundle install # 从 Brewfile 安装</code></pre>
'''

UPDATES['/other/tesseract/'] = '''
<hr>
<h2 id="tesseract-2024-update">OCR 技术更新（2024-2026）</h2>
<p>Tesseract 仍在维护，但现代 OCR 选择更多：</p>
<ul>
<li><strong>PaddleOCR</strong>：百度开源，中文识别强。</li>
<li><strong>Surya</strong>：基于 Transformer，多语言。</li>
<li><strong>云服务</strong>：阿里云/腾讯云/Azure OCR API。</li>
</ul>
'''

UPDATES['/other/firefox/'] = '''
<hr>
<h2 id="firefox-2024-update">浏览器更新（2024-2026）</h2>
<ul>
<li><strong>Arc Browser</strong>：创新标签管理和侧边栏设计。</li>
<li><strong>Zen Browser</strong>：基于 Firefox，隐私优先。</li>
<li><strong>Brave</strong>：内置广告拦截和 Tor 支持。</li>
</ul>
'''

UPDATES['/grpc/golang/'] = '''
<hr>
<h2 id="grpc-go-2024-update">gRPC Go 示例更新</h2>
<p>现代 gRPC Go 推荐使用 buf 管理proto文件，详见 <a href="/grpc/">gRPC 主页</a>。Connect-RPC 是更简单的替代方案，兼容 HTTP/JSON。</p>
'''

UPDATES['/other/mermaid/'] = '''
<hr>
<h2 id="mermaid-2024-update">Mermaid 更新（2024-2026）</h2>
<p>Mermaid v10.9+ 新特性：</p>
<ul>
<li>支持思维导图（Mindmap）和架构图（Architecture）。</li>
<li>改进的交互式图表（点击事件）。</li>
<li>支持 ELK 布局引擎。</li>
</ul>
'''

UPDATES['/other/wireshark/'] = '''
<hr>
<h2 id="wireshark-2024-update">Wireshark 更新</h2>
<p>Wireshark 4.2+ 支持 HTTP/3(QUIC) 解析，改进了 TLS 1.3 解密。</p>
'''

UPDATES['/other/aliyun/'] = '''
<hr>
<h2 id="aliyun-2024-update">阿里云更新（2024-2026）</h2>
<p>阿里云主要变化：</p>
<ul>
<li><strong>通义千问（Qwen）</strong>：开源大模型系列，Qwen2.5 支持多语言。</li>
<li><strong>百炼平台</strong>：一站式 AI 应用开发平台。</li>
<li><strong>PAI</strong>：机器学习平台，支持模型训练和部署。</li>
</ul>
'''

UPDATES['/other/opensource/'] = '''
<hr>
<h2 id="opensource-2024-update">优秀开源软件推荐（2024-2026）</h2>
<table>
<thead><tr><th>项目</th><th>语言</th><th>用途</th></tr></thead>
<tbody>
<tr><td><code>uv</code></td><td>Rust</td><td>极速 Python 包管理</td></tr>
<tr><td><code>ripgrep</code></td><td>Rust</td><td>极速文本搜索</td></tr>
<tr><td><code>fd</code></td><td>Rust</td><td>友好的 find 替代</td></tr>
<tr><td><code>bat</code></td><td>Rust</td><td>cat 替代</td></tr>
<tr><td><code>zoxide</code></td><td>Rust</td><td>智能 cd</td></tr>
<tr><td><code>starship</code></td><td>Rust</td><td>跨 shell 提示符</td></tr>
<tr><td><code>lazygit</code></td><td>Go</td><td>Git TUI</td></tr>
<tr><td><code>gh</code></td><td>Go</td><td>GitHub CLI</td></tr>
<tr><td><code>SRS</code></td><td>Go</td><td>流媒体服务器</td></tr>
<tr><td><code>Ollama</code></td><td>Go</td><td>本地 LLM 运行</td></tr>
</tbody>
</table>
'''

UPDATES['/other/unity/'] = '''
<hr>
<h2 id="unity-2024-update">Unity 更新（2024-2026）</h2>
<p>Unity 6（2024年发布）主要变化：</p>
<ul>
<li>新的渲染管线（URP/HDRP）改进。</li>
<li>WebGPU 支持。</li>
<li>AI 导航和物体放置工具。</li>
</ul>
'''

UPDATES['/other/machinelearn/'] = '''
<hr>
<h2 id="ml-2024-update">机器学习更新（2024-2026）</h2>
<p>机器学习领域已被大语言模型（LLM）深刻改变。详见 <a href="/ai/llm/">LLM 页面</a> 和 <a href="/ai/rag/">RAG 页面</a>。</p>
<ul>
<li><strong>PyTorch 2.x</strong>：编译模式 <code>torch.compile</code>。</li>
<li><strong>Hugging Face</strong>：模型仓库生态，Transformers 5.x。</li>
<li><strong>本地推理</strong>：Ollama、vLLM、llama.cpp。</li>
</ul>
'''

UPDATES['/other/rpc/'] = '''
<hr>
<h2 id="rpc-2024-update">RPC 更新（2024-2026）</h2>
<p>RPC 生态变化：</p>
<ul>
<li><strong>Connect-RPC</strong>：Buf 推出，兼容 gRPC 和 HTTP/JSON。</li>
<li><strong>Twirp</strong>：简单 RPC 协议，基于 HTTP/1.1。</li>
<li><strong>Cap'n Proto</strong>：零拷贝序列化，极低延迟。</li>
</ul>
'''

UPDATES['/other/svn/'] = '''
<hr>
<h2 id="svn-2024-update">SVN 更新</h2>
<p>SVN 在 2024-2026 年已基本退出主流开发。建议迁移到 Git。如需迁移：</p>
<pre><code class="language-bash"># 使用 git-svn 迁移
git svn clone -s http://svn.example.com/repo
git remote add origin git@github.com:user/repo.git
git push -u origin main</code></pre>
'''

UPDATES['/other/windows/'] = '''
<hr>
<h2 id="windows-2024-update">Windows 开发环境更新（2024-2026）</h2>
<ul>
<li><strong>WSL2</strong>：Windows Subsystem for Linux 2，接近原生 Linux 性能。</li>
<li><strong>Windows Terminal</strong>：支持多标签、GPU 加速。</li>
<li><strong>PowerShell 7</strong>：跨平台，基于 .NET。</li>
<li><strong>WinGet</strong>：Windows 包管理器。</li>
</ul>
'''

UPDATES['/other/geocode/'] = '''
<hr>
<h2 id="geocode-2024-update">地理编码更新</h2>
<p>推荐使用百度地图 API 或高德地图 API 进行地理编码。详见 <code>baidu-ai-map</code> 技能。</p>
'''

UPDATES['/other/tencent/'] = '''
<hr>
<h2 id="tencent-2024-update">腾讯云更新（2024-2026）</h2>
<p>腾讯云 AI 相关服务：</p>
<ul>
<li>混元大模型（Hunyuan）系列。</li>
<li>TI 平台（TencentCloud AI）。</li>
<li>OCR、语音识别等 AI 能力。</li>
</ul>
'''

UPDATES['/categories/'] = ''
UPDATES['/tags/'] = ''


def main():
    data = load_data()
    pages = data['pages']
    
    updated = 0
    for url_path, update_content in UPDATES.items():
        if not update_content:
            continue
        if url_path in pages:
            old_content = pages[url_path].get('content', '')
            # Check if already updated (avoid duplicate)
            if '2024-2026 更新' in old_content or '2026 更新' in old_content:
                continue
            pages[url_path]['content'] = old_content + update_content
            updated += 1
            print(f"Updated {url_path}: +{len(update_content)} chars")
        else:
            print(f"WARNING: {url_path} not found")
    
    save_data(data)
    print(f"\nTotal pages updated: {updated}")
    print(f"Total pages: {len(pages)}")


if __name__ == '__main__':
    main()
