#!/usr/bin/env python3
"""Update incomplete pages and add new tech content."""

import json
import os
import re
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
# Content for incomplete pages
# ============================================================

GOLANG_CONTEXT_CONTENT = '''<h3 id="golang-context">Go context.Context 详解</h3>

<p><code>context.Context</code> 是 Go 语言中用于控制 goroutine 生命周期、传递请求元数据和实现超时/取消机制的核心接口。从 Go 1.7 开始引入，是编写健壮并发程序的基础。</p>

<h4 id="context-interface">Context 接口定义</h4>
<pre><code class="language-go">type Context interface {
    // Deadline 返回 context 的截止时间和是否设置了截止时间
    Deadline() (deadline time.Time, ok bool)

    // Done 返回一个 channel，当 context 被取消或超时时关闭
    Done() <-chan struct{}

    // Err 返回 context 被取消的原因
    Err() error

    // Value 返回 context 中关联的键值
    Value(key any) any
}</code></pre>

<h4 id="context-creation">创建 Context</h4>
<p>Go 提供了两种创建根 context 的方式：</p>
<pre><code class="language-go">// 1. context.Background() - 通常用于 main 函数、初始化和测试
ctx := context.Background()

// 2. context.TODO() - 当不确定使用什么 context 时占位
ctx := context.TODO()</code></pre>

<h4 id="context-derive">派生 Context</h4>
<p>从根 context 可以派生出子 context，形成树状结构：</p>
<pre><code class="language-go">// 带超时的 context
ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
defer cancel()

// 带截止时间的 context
deadline := time.Now().Add(10 * time.Second)
ctx, cancel := context.WithDeadline(context.Background(), deadline)
defer cancel()

// 带取消信号的 context
ctx, cancel := context.WithCancel(context.Background())
defer cancel()

// 带键值对的 context
ctx := context.WithValue(context.Background(), "userID", 12345)</code></pre>

<h4 id="context-usage">典型使用场景</h4>

<h5>1. HTTP 请求超时控制</h5>
<pre><code class="language-go">func handler(w http.ResponseWriter, r *http.Request) {
    ctx, cancel := context.WithTimeout(r.Context(), 3*time.Second)
    defer cancel()

    result, err := fetchFromDB(ctx, query)
    if err != nil {
        if ctx.Err() == context.DeadlineExceeded {
            http.Error(w, "Request timeout", http.StatusGatewayTimeout)
            return
        }
        http.Error(w, err.Error(), http.StatusInternalServerError)
        return
    }
    json.NewEncoder(w).Encode(result)
}</code></pre>

<h5>2. Goroutine 取消传播</h5>
<pre><code class="language-go">func worker(ctx context.Context, id int) {
    for {
        select {
        case <-ctx.Done():
            fmt.Printf("Worker %d stopped: %v\\n", id, ctx.Err())
            return
        default:
            // 执行工作
            time.Sleep(500 * time.Millisecond)
        }
    }
}

func main() {
    ctx, cancel := context.WithCancel(context.Background())

    // 启动多个 worker
    for i := 1; i <= 3; i++ {
        go worker(ctx, i)
    }

    // 运行 2 秒后取消所有 worker
    time.Sleep(2 * time.Second)
    cancel()
    time.Sleep(500 * time.Millisecond) // 等待 worker 退出
}</code></pre>

<h5>3. 请求链路追踪</h5>
<pre><code class="language-go">type contextKey string

const (
    RequestIDKey contextKey = "requestID"
    UserIDKey    contextKey = "userID"
)

func middleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        requestID := generateID()
        ctx := context.WithValue(r.Context(), RequestIDKey, requestID)
        next.ServeHTTP(w, r.WithContext(ctx))
    })
}

func getFromContext(ctx context.Context, key contextKey) string {
    if v, ok := ctx.Value(key).(string); ok {
        return v
    }
    return ""
}</code></pre>

<div class="mermaid">
graph TD
    A[Background] --> B[WithTimeout 5s]
    A --> C[WithCancel]
    B --> D[WithValue: userID]
    B --> E[WithValue: traceID]
    C --> F[WithDeadline 10s]
    D --> G[HTTP Handler]
    E --> H[DB Query]
    F --> I[Worker Goroutine]
</div>

<h4 id="context-rules">最佳实践</h4>
<ol>
<li><strong>总是调用 cancel()</strong>：即使 context 会超时，也要调用 cancel 函数来释放资源。使用 <code>defer cancel()</code>。</li>
<li><strong>不要将 context 存储在 struct 中</strong>：context 应该作为函数的第一个参数传递：<code>func DoSomething(ctx context.Context, ...)</code>。</li>
<li><strong>不要传递 nil context</strong>：如果不确定用什么，使用 <code>context.TODO()</code>。</li>
<li><strong>使用自定义类型作为 key</strong>：避免键冲突，使用 <code>type contextKey string</code>。</li>
<li><strong>context.Value 只用于请求范围的数据</strong>：不要用它传递函数参数，它只适合传递 trace ID、认证信息等。</li>
</ol>

<h4 id="context-go121">Go 1.21+ 新特性</h4>
<p>Go 1.21 引入了 <code>context.WithoutCancel</code> 和 <code>context.AfterFunc</code>：</p>
<pre><code class="language-go">// WithoutCancel 返回一个不会因父 context 取消而取消的 context
// 适用于需要在请求取消后继续执行清理逻辑的场景
ctx := context.WithoutCancel(parentCtx)

// AfterFunc 在 context 取消后执行回调
stop := context.AfterFunc(ctx, func() {
    // 清理逻辑
    log.Println("Context cancelled, cleaning up...")
})
// 如果需要停止监听，调用 stop()
// stop()</code></pre>

<p>Go 1.22 进一步优化了 context 的性能，减少了内存分配。在 HTTP 请求中，<code>r.Context()</code> 现在会在客户端断开连接时自动取消。</p>'''


AI_INDEX_CONTENT = '''<h3 id="ai-overview">人工智能技术笔记</h3>

<p>本分类涵盖人工智能、机器学习与深度学习相关的技术笔记，包括大语言模型（LLM）、检索增强生成（RAG）、Fine-tuning 微调、Agent 智能体等方向。</p>

<h4 id="ai-topics">主题列表</h4>
<ul>
<li><a href="/ai/llm/">大语言模型（LLM）</a> - GPT、Claude、Llama 等大模型的原理与应用</li>
<li><a href="/ai/rag/">检索增强生成（RAG）</a> - 结合知识库的 LLM 增强方案</li>
<li><a href="/ai/agent/">AI Agent 智能体</a> - 基于大模型的自主代理架构</li>
<li><a href="/ai/__index/">Fine-tuning 微调</a> - 深度学习模型微调技术</li>
</ul>

<h4 id="ai-ecosystem">AI 生态速览（2024-2026）</h4>
<p>近年来 AI 领域发展迅速，以下是关键趋势：</p>
<table>
<thead><tr><th>方向</th><th>代表性技术/产品</th><th>典型应用</th></tr></thead>
<tbody>
<tr><td>大语言模型</td><td>GPT-4o, Claude 3.5, Llama 3, DeepSeek</td><td>对话、代码生成、文档摘要</td></tr>
<tr><td>多模态模型</td><td>GPT-4V, Gemini, DALL-E 3</td><td>图文理解、图片生成</td></tr>
<tr><td>RAG</td><td>LangChain, LlamaIndex, Milvus</td><td>企业知识库问答</td></tr>
<tr><td>AI Agent</td><td>AutoGPT, CrewAI, OpenAI Agents</td><td>自动化任务执行</td></tr>
<tr><td>代码生成</td><td>Copilot, Cursor, Claude Code</td><td>编程辅助、代码审查</td></tr>
<tr><td>本地推理</td><td>Ollama, vLLM, llama.cpp</td><td>私有化部署、边缘推理</td></tr>
</tbody>
</table>'''


AI_FINETUNING_CONTENT = '''<h3 id="fine-tuning">深度学习 Fine-tuning 微调技术</h3>

<p>Fine-tuning（微调）是深度学习中迁移学习的核心技术。其原理是利用已知的网络结构和预训练参数，修改 output 层为自定义层，微调最后一层前的所有层参数，同时加大最后一层的学习率（因为需要重新学习），这样既有效利用了深度神经网络强大的泛化能力，又免去了设计复杂模型和耗时良久的训练。</p>

<h4 id="fine-tuning-types">微调的主要方式</h4>

<h5>1. Full Fine-tuning（全量微调）</h5>
<p>更新模型所有参数，效果最好但计算成本高，需要大量 GPU 显存。</p>
<pre><code class="language-python">from transformers import AutoModelForSequenceClassification, Trainer, TrainingArguments

model = AutoModelForSequenceClassification.from_pretrained("bert-base-chinese", num_labels=10)

training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=16,
    learning_rate=5e-5,
    weight_decay=0.01,
)

trainer = Trainer(model=model, args=training_args, train_dataset=train_ds)
trainer.train()</code></pre>

<h5>2. LoRA（Low-Rank Adaptation）</h5>
<p>LoRA 通过在权重矩阵旁增加低秩分解矩阵来实现高效微调，只训练少量参数（通常 <1%），极大降低显存需求。</p>
<pre><code class="language-python">from peft import LoraConfig, get_peft_model, TaskType

lora_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    r=8,                    # 低秩矩阵的秩
    lora_alpha=32,          # 缩放因子
    lora_dropout=0.1,
    target_modules=["q_proj", "v_proj"],  # 应用 LoRA 的层
)

model = get_peft_model(base_model, lora_config)
model.print_trainable_parameters()
# 输出示例: trainable params: 1,474,560 || all params: 7,000,000,000 || trainable%: 0.02%</code></pre>

<h5>3. QLoRA（Quantized LoRA）</h5>
<p>QLoRA 在 LoRA 基础上对基础模型进行 4-bit 量化，使得在单张消费级显卡上微调 70B 参数模型成为可能。</p>
<pre><code class="language-python">from transformers import BitsAndBytesConfig
import torch

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True,
)

model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-7b",
    quantization_config=bnb_config,
    device_map="auto",
)</code></pre>

<h4 id="fine-tuning-comparison">微调方式对比</h4>
<table>
<thead><tr><th>方式</th><th>训练参数量</th><th>显存需求</th><th>效果</th><th>适用场景</th></tr></thead>
<tbody>
<tr><td>Full Fine-tuning</td><td>100%</td><td>高</td><td>最好</td><td>有充足 GPU 资源</td></tr>
<tr><td>LoRA</td><td>0.1%-1%</td><td>中</td><td>接近全量</td><td>资源受限场景</td></tr>
<tr><td>QLoRA</td><td>0.1%-1%</td><td>低</td><td>略低于 LoRA</td><td>单卡微调大模型</td></tr>
<tr><td>P-Tuning v2</td><td>0.1%</td><td>低</td><td>中等</td><td>自然语言理解任务</td></tr>
</tbody>
</table>

<h4 id="fine-tuning-tips">实践建议</h4>
<ol>
<li><strong>数据质量 > 数据量</strong>：1,000 条高质量样本比 10,000 条低质量样本效果好。</li>
<li><strong>学习率选择</strong>：LoRA 通常用 1e-4 到 5e-4，全量微调用 1e-5 到 5e-5。</li>
<li><strong>评估指标</strong>：除了 loss，还要关注 BLEU、ROUGE 等任务相关指标。</li>
<li><strong>防止过拟合</strong>：使用 early stopping、dropout 和 weight decay。</li>
<li><strong>数据格式</strong>：使用 ChatML 或 Alpaca 格式，保持与推理时一致的 prompt 模板。</li>
</ol>'''


GOLANG_REGEXP_CONTENT = '''<h3 id="golang-regexp">Go regexp 正则表达式包</h3>

<p>Go 的 <code>regexp</code> 包实现了 RE2 语法正则表达式，支持 Unicode 字符类，但不支持回溯引用（backreferences）和零宽断言（lookaround）。</p>

<h4 id="regexp-basic">基本用法</h4>
<pre><code class="language-go">package main

import (
    "fmt"
    "regexp"
)

func main() {
    // 编译正则表达式（ MustCompile 遇到错误会 panic）
    // 连续的汉字字母数字
    maxHanDigitAlphaReg := regexp.MustCompile(`[\p{Han}[:digit:][:alpha:]]+`)
    // 单个汉字字母数字（非贪婪）
    minHanDigitAlphaReg := regexp.MustCompile(`[\p{Han}[:digit:][:alpha:]]+?`)

    text := "Hello世界123!"

    // 查找所有匹配
    matches := maxHanDigitAlphaReg.FindAllString(text, -1)
    fmt.Println(matches) // [Hello世界123]

    // 查找第一个匹配
    first := minHanDigitAlphaReg.FindString(text)
    fmt.Println(first) // H
}</code></pre>

<h4 id="regexp-compile">Compile vs MustCompile</h4>
<pre><code class="language-go">// Compile 返回错误，适合正则来自用户输入
re, err := regexp.Compile(`[invalid`)
if err != nil {
    log.Fatal(err)
}

// MustCompile 遇到错误时 panic，适合正则是硬编码的场景
re = regexp.MustCompile(`\d+`)</code></pre>

<h4 id="regexp-operations">常用操作</h4>
<pre><code class="language-go">re := regexp.MustCompile(`(\w+)@(\w+)\.(\w+)`)
email := "user@example.com"

// 1. 匹配测试
matched := re.MatchString(email) // true

// 2. 提取子匹配
submatch := re.FindStringSubmatch(email)
// ["user@example.com", "user", "example", "com"]

// 3. 提取命名子匹配
namedRe := regexp.MustCompile(`(?P<user>\w+)@(?P<domain>\w+)\.(?P<tld>\w+)`)
result := namedRe.FindStringSubmatch(email)
names := namedRe.SubexpNames()
for i, name := range names {
    if name != "" {
        fmt.Printf("%s: %s\n", name, result[i])
    }
}

// 4. 替换
replaced := re.ReplaceAllString(email, "$1 at $2 dot $3")
// "user at example dot com"

// 5. 分割
splitRe := regexp.MustCompile(`[,\s]+`)
parts := splitRe.Split("a, b, c d", -1)
// ["a", "b", "c", "d"]</code></pre>

<h4 id="regexp-unicode">Unicode 支持</h4>
<pre><code class="language-go">// 匹配中文字符
hanRe := regexp.MustCompile(`[\p{Han}]+`)
fmt.Println(hanRe.FindAllString("Hello世界，你好", -1)) // [世界 你好]

// 匹配中文、字母、数字
allRe := regexp.MustCompile(`[\p{Han}\p{L}\p{N}]+`)

// 匹配日文假名
jpRe := regexp.MustCompile(`[\p{Hiragana}\p{Katakana}]+`)</code></pre>

<h4 id="regexp-tips">常见模式速查</h4>
<table>
<thead><tr><th>用途</th><th>正则</th><th>说明</th></tr></thead>
<tbody>
<tr><td>邮箱</td><td><code>[\w.]+@[\w]+\.[a-zA-Z]+</code></td><td>基本邮箱格式</td></tr>
<tr><td>手机号</td><td><code>1[3-9]\d{9}</code></td><td>中国大陆手机号</td></tr>
<tr><td>IP 地址</td><td><code>(\d{1,3}\.){3}\d{1,3}</code></td><td>IPv4 地址</td></tr>
<tr><td>URL</td><td><code>https?://[\w./?-]+</code></td><td>HTTP/HTTPS URL</td></tr>
<tr><td>日期</td><td><code>\d{4}-\d{2}-\d{2}</code></td><td>YYYY-MM-DD 格式</td></tr>
<tr><td>中文</td><td><code>[\p{Han}]+</code></td><td>连续中文字符</td></tr>
</tbody>
</table>

<h4 id="regexp-performance">性能建议</h4>
<ol>
<li><strong>预编译</strong>：在函数外部或 init 中编译正则，避免每次调用都重新编译。</li>
<li><strong>使用 <code>regexp.Compile</code></strong>：用户输入的正则用 Compile 检查错误。</li>
<li><strong>避免贪婪匹配</strong>：使用 <code>+?</code> 或 <code>*?</code> 避免不必要的回溯。</li>
<li><strong>RE2 限制</strong>：Go 的 RE2 不支持回溯引用和零宽断言，如需这些功能可用 <code>github.com/dlclark/regexp2</code>。</li>
</ol>'''


# ============================================================
# New tech content pages (2023-2026)
# ============================================================

AI_LLM_CONTENT = '''<h3 id="llm-overview">大语言模型（LLM）技术概览</h3>

<p>大语言模型（Large Language Model）是基于 Transformer 架构、使用海量文本数据训练的深度学习模型，具备文本生成、代码编写、逻辑推理、多语言理解等能力。2022 年 ChatGPT 的发布标志着 LLM 时代的到来。</p>

<h4 id="llm-architecture">核心架构</h4>
<p>现代 LLM 基于 Transformer 的 Decoder-only 架构，核心机制是自注意力（Self-Attention）：</p>
<pre><code class="language-python"># Self-Attention 简化示意
import torch
import torch.nn.functional as F

def attention(Q, K, V):
    """Scaled Dot-Product Attention
    Q: query  (batch, seq_len, d_k)
    K: key    (batch, seq_len, d_k)
    V: value  (batch, seq_len, d_v)
    """
    d_k = Q.size(-1)
    scores = torch.matmul(Q, K.transpose(-2, -1)) / (d_k ** 0.5)
    # Causal mask: 只看当前及之前的 token
    mask = torch.tril(torch.ones(scores.size(-2), scores.size(-1)))
    scores = scores.masked_fill(mask == 0, float('-inf'))
    weights = F.softmax(scores, dim=-1)
    return torch.matmul(weights, V)</code></pre>

<h4 id="llm-training">训练流程</h4>
<div class="mermaid">
flowchart LR
    A[预训练 Pre-training] --> B[指令微调 SFT]
    B --> C[人类反馈强化学习 RLHF]
    C --> D[对齐 Alignment]
    A --> E[万亿 tokens 文本数据]
    B --> F[高质量问答对]
    C --> G[偏好排序数据]
</div>

<table>
<thead><tr><th>阶段</th><th>目标</th><th>数据量</th><th>代表方法</th></tr></thead>
<tbody>
<tr><td>预训练</td><td>学习语言规律和世界知识</td><td>万亿 tokens</td><td>自回归下一词预测</td></tr>
<tr><td>SFT</td><td>学会遵循指令</td><td>万-百万条</td><td>指令微调</td></tr>
<tr><td>RLHF/DPO</td><td>对齐人类偏好</td><td>万-十万条偏好对</td><td>PPO, DPO</td></tr>
</tbody>
</table>

<h4 id="llm-models">主流开源模型（2024-2026）</h4>
<table>
<thead><tr><th>模型</th><th>参数量</th><th>开发者</th><th>特点</th></tr></thead>
<tbody>
<tr><td>Llama 3</td><td>8B/70B/405B</td><td>Meta</td><td>多语言支持强，生态丰富</td></tr>
<tr><td>DeepSeek-V3</td><td>671B (MoE)</td><td>DeepSeek</td><td>MoE 架构，推理高效</td></tr>
<tr><td>Qwen2.5</td><td>0.5B-72B</td><td>阿里巴巴</td><td>中文能力突出</td></tr>
<tr><td>Mistral</td><td>7B/8x7B MoE</td><td>Mistral AI</td><td>轻量高效</td></tr>
<tr><td>Gemma 2</td><td>2B/9B/27B</td><td>Google</td><td>研究友好</td></tr>
</tbody>
</table>

<h4 id="llm-inference">推理优化技术</h4>
<ul>
<li><strong>KV Cache</strong>：缓存已计算的 Key/Value 矩阵，避免重复计算。</li>
<li><strong>量化（Quantization）</strong>：将 FP16 权重降为 INT8/INT4，减少显存占用。</li>
<li><strong>PagedAttention</strong>：vLLM 的核心创新，分页管理 KV Cache 显存。</li>
<li><strong>推测解码（Speculative Decoding）</strong>：用小模型快速生成草稿，大模型验证。</li>
<li><strong>Flash Attention</strong>：优化 GPU 显存访问模式，加速注意力计算。</li>
</ul>

<pre><code class="language-bash"># 使用 Ollama 本地运行 LLM
ollama pull llama3:8b
ollama run llama3:8b "用 Go 写一个 HTTP 服务器"

# 使用 vLLM 部署 OpenAI 兼容 API
pip install vllm
vllm serve meta-llama/Llama-3-8B-Instruct --port 8000

# 使用 llama.cpp 进行 CPU/GPU 推理
./main -m llama-3-8b.gguf -p "Hello, how are you?" -n 256</code></pre>

<h4 id="llm-api">调用 LLM API</h4>
<pre><code class="language-go">// Go 调用 OpenAI 兼容 API
package main

import (
    "context"
    "fmt"
    "os"
    openai "github.com/sashabaranov/go-openai"
)

func main() {
    client := openai.NewClient(os.Getenv("OPENAI_API_KEY"))
    resp, err := client.CreateChatCompletion(context.Background(),
        openai.ChatCompletionRequest{
            Model: openai.GPT4oMini,
            Messages: []openai.ChatCompletionMessage{
                {Role: openai.ChatMessageRoleUser, Content: "用一句话解释 Go 的 goroutine"},
            },
            MaxTokens: 100,
        },
    )
    if err != nil {
        panic(err)
    }
    fmt.Println(resp.Choices[0].Message.Content)
}</code></pre>'''


AI_RAG_CONTENT = '''<h3 id="rag-overview">检索增强生成（RAG）</h3>

<p>RAG（Retrieval-Augmented Generation）将信息检索与大语言模型结合，通过从外部知识库检索相关文档来增强 LLM 的回答，解决幻觉问题并提供可溯源的知识。</p>

<h4 id="rag-architecture">RAG 架构</h4>
<div class="mermaid">
flowchart TD
    A[用户提问] --> B[Query Embedding]
    B --> C[向量检索 Vector Search]
    C --> D[Top-K 相关文档]
    D --> E[构建 Prompt: 问题 + 检索到的上下文]
    E --> F[LLM 生成回答]
    F --> G[输出: 答案 + 来源引用]

    subgraph 离线建库
        H[文档库] --> I[分块 Chunking]
        I --> J[Embedding 向量化]
        J --> K[向量数据库]
    end
    C -.-> K
</div>

<h4 id="rag-components">核心组件</h4>

<h5>1. 文档处理</h5>
<pre><code class="language-python">from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import DirectoryLoader

# 加载文档
loader = DirectoryLoader("./docs", glob="**/*.md")
docs = loader.load()

# 文档分块
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,        # 每块最大 500 字符
    chunk_overlap=50,      # 块之间重叠 50 字符
    separators=["\\n\\n", "\\n", "。", "！", "？", " "],
)
chunks = splitter.split_documents(docs)
print(f"共 {len(chunks)} 个文档块")</code></pre>

<h5>2. 向量化与存储</h5>
<pre><code class="language-python">from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma

# 使用中文 embedding 模型
embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-zh-v1.5",
    encode_kwargs={"normalize_embeddings": True},
)

# 存入向量数据库
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db",
)
vectorstore.persist()</code></pre>

<h5>3. 检索与生成</h5>
<pre><code class="language-python">from langchain.chains import RetrievalQA
from langchain.llms import Ollama

# 初始化 LLM
llm = Ollama(model="llama3", temperature=0.3)

# 构建 RAG 链
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever(search_kwargs={"k": 5}),
    return_source_documents=True,
)

# 提问
result = qa_chain({"query": "Go 语言中 context 的作用是什么？"})
print(result["result"])
for doc in result["source_documents"]:
    print(f"来源: {doc.metadata['source']}")</code></pre>

<h4 id="rag-vector-db">向量数据库选型</h4>
<table>
<thead><tr><th>数据库</th><th>类型</th><th>特点</th><th>适用场景</th></tr></thead>
<tbody>
<tr><td>Milvus</td><td>专用向量库</td><td>分布式、高性能</td><td>大规模生产环境</td></tr>
<tr><td>Chroma</td><td>轻量向量库</td><td>嵌入式、易用</td><td>原型开发、小规模</td></tr>
<tr><td>Qdrant</td><td>专用向量库</td><td>Rust 实现、过滤强</td><td>需要复杂过滤</td></tr>
<tr><td>Pgvector</td><td>PostgreSQL 扩展</td><td>SQL 生态</td><td>已有 PG 基础设施</td></tr>
<tr><td>Elasticsearch</td><td>搜索引擎</td><td>全文+向量混合检索</td><td>已有 ES 基础设施</td></tr>
</tbody>
</table>

<h4 id="rag-advanced">进阶技巧</h4>
<ul>
<li><strong>混合检索</strong>：结合 BM25 全文检索 + 向量检索，取两者并集再重排。</li>
<li><strong>Query 重写</strong>：用 LLM 将用户查询重写为更利于检索的表达。</li>
<li><strong>重排序（Reranking）</strong>：用 Cross-Encoder 对检索结果二次排序，提高精度。</li>
<li><strong>多路召回</strong>：同时从多个知识源检索，合并结果。</li>
<li><strong>动态 chunk</strong>：根据文档结构（段落、标题）动态分块，而非固定长度。</li>
</ul>'''


GOLANG_GENERICS_UPDATE_CONTENT = '''<h3 id="generics-update">Go 泛型进阶（1.18-1.22）</h3>

<p>Go 1.18 引入了泛型（Type Parameters），这是 Go 语言自 1.0 以来最大的语法变更。本文总结泛型的核心概念和实际应用。</p>

<h4 id="generics-basic">基本语法</h4>
<pre><code class="language-go">// 泛型函数：T 是类型参数，any 是约束（等同 interface{}）
func Reverse[T any](s []T) []T {
    result := make([]T, len(s))
    for i, v := range s {
        result[len(s)-1-i] = v
    }
    return result
}

// 使用
nums := []int{1, 2, 3, 4, 5}
fmt.Println(Reverse(nums)) // [5 4 3 2 1]

strs := []string{"a", "b", "c"}
fmt.Println(Reverse(strs)) // [c b a]</code></pre>

<h4 id="generics-constraints">类型约束</h4>
<pre><code class="language-go">// 使用 constraints 包（Go 1.21+ 移入标准库）
import "cmp"

// Ordered 约束：支持 < <= > >= 的类型
func Min[T cmp.Ordered](a, b T) T {
    if a < b {
        return a
    }
    return b
}

// 自定义约束
type Number interface {
    int | int8 | int16 | int32 | int64 |
    float32 | float64
}

func Sum[T Number](nums []T) T {
    var total T
    for _, n := range nums {
        total += n
    }
    return total
}

// 使用 ~ 表示底层类型
type StringList []string
func Process[T ~[]string](v T) {
    // T 可以是 []string 或 StringList
}</code></pre>

<h4 id="generics-map-filter">泛型工具函数</h4>
<pre><code class="language-go">// Map: 对切片每个元素应用函数
func Map[T, U any](s []T, f func(T) U) []U {
    result := make([]U, len(s))
    for i, v := range s {
        result[i] = f(v)
    }
    return result
}

// Filter: 过滤切片
func Filter[T any](s []T, pred func(T) bool) []T {
    result := make([]T, 0, len(s))
    for _, v := range s {
        if pred(v) {
            result = append(result, v)
        }
    }
    return result
}

// Reduce: 聚合
func Reduce[T, U any](s []T, init U, f func(U, T) U) U {
    result := init
    for _, v := range s {
        result = f(result, v)
    }
    return result
}

// 使用示例
nums := []int{1, 2, 3, 4, 5}
doubled := Map(nums, func(n int) int { return n * 2 })
evens := Filter(nums, func(n int) bool { return n%2 == 0 })
sum := Reduce(nums, 0, func(acc, n int) int { return acc + n })</code></pre>

<h4 id="generics-struct">泛型类型</h4>
<pre><code class="language-go">// 泛型栈
type Stack[T any] struct {
    items []T
}

func (s *Stack[T]) Push(v T) {
    s.items = append(s.items, v)
}

func (s *Stack[T]) Pop() (T, bool) {
    var zero T
    if len(s.items) == 0 {
        return zero, false
    }
    v := s.items[len(s.items)-1]
    s.items = s.items[:len(s.items)-1]
    return v, true
}

// 泛型 Map
type Map[K comparable, V any] struct {
    data map[K]V
}

func (m *Map[K, V]) Set(key K, value V) {
    if m.data == nil {
        m.data = make(map[K]V)
    }
    m.data[key] = value
}

func (m *Map[K, V]) Get(key K) (V, bool) {
    v, ok := m.data[key]
    return v, ok
}</code></pre>

<h4 id="generics-122">Go 1.22+ 改进</h4>
<p>Go 1.22 对泛型类型推断做了显著改进：</p>
<pre><code class="language-go">// Go 1.22 前需要显式指定类型
func Compare[T cmp.Ordered](a, b T) int { ... }
result := Compare[int](1, 2)

// Go 1.22+ 可以推断
result := Compare(1, 2) // 自动推断 T=int

// 支持从函数参数推断类型参数
func NewSet[T comparable](items ...T) *Set[T] { ... }
s := NewSet(1, 2, 3) // 自动推断 T=int</code></pre>

<h4 id="generics-notes">使用建议</h4>
<ol>
<li><strong>不要为了泛型而泛型</strong>：只在需要多类型复用代码时使用。</li>
<li><strong>优先使用标准库</strong>：<code>slices</code>、<code>maps</code> 包（Go 1.21+）已提供常用泛型工具。</li>
<li><strong>约束越宽越好</strong>：除非需要特定操作，否则用 <code>any</code> 或 <code>comparable</code>。</li>
<li><strong>注意编译速度</strong>：过度使用泛型会减慢编译速度。</li>
<li><strong>泛型不适合所有场景</strong>：如果只有 2-3 种类型，直接写具体类型可能更清晰。</li>
</ol>'''


# ============================================================
# Main update logic
# ============================================================

def update_content():
    """Update extracted_content.json with new and improved content."""
    data = load_data()
    pages = data['pages']
    nav_items = data['navigation']

    # 1. Update incomplete pages
    updates = {
        '/golang/context/': GOLANG_CONTEXT_CONTENT,
        '/ai/__index/': AI_FINETUNING_CONTENT,
        '/ai/': AI_INDEX_CONTENT,
        '/golang/regexp/': GOLANG_REGEXP_CONTENT,
    }

    for url_path, content in updates.items():
        if url_path in pages:
            old_len = len(pages[url_path].get('content', ''))
            pages[url_path]['content'] = content
            pages[url_path]['title'] = clean_title_from_content(content)
            print(f"Updated {url_path}: {old_len} -> {len(content)} chars")
        else:
            print(f"WARNING: {url_path} not found in pages")

    # 2. Add new pages
    new_pages = {
        '/ai/llm/': {
            'title': '大语言模型 LLM',
            'content': AI_LLM_CONTENT,
            'filepath': str(BASE_DIR / 'ai' / 'llm' / 'index.html'),
        },
        '/ai/rag/': {
            'title': 'RAG 检索增强生成',
            'content': AI_RAG_CONTENT,
            'filepath': str(BASE_DIR / 'ai' / 'rag' / 'index.html'),
        },
        '/golang/generics-update/': {
            'title': 'Go 泛型进阶',
            'content': GOLANG_GENERICS_UPDATE_CONTENT,
            'filepath': str(BASE_DIR / 'golang' / 'generics-update' / 'index.html'),
        },
    }

    for url_path, page_data in new_pages.items():
        pages[url_path] = page_data
        # Ensure directory exists
        filepath = Path(page_data['filepath'])
        filepath.parent.mkdir(parents=True, exist_ok=True)
        print(f"Added new page {url_path}: {len(page_data['content'])} chars")

    # 3. Update navigation
    # Add new items to AI section
    ai_item = None
    for item in nav_items:
        if item.get('href', '').rstrip('/') == '/ai':
            ai_item = item
            break

    if ai_item:
        # Check if children exist, if not create
        if 'children' not in ai_item:
            ai_item['children'] = []
        existing = {c.get('href') for c in ai_item['children']}
        if '/ai/llm/' not in existing:
            ai_item['children'].append({
                'href': '/ai/llm/',
                'text': 'LLM 大语言模型',
            })
        if '/ai/rag/' not in existing:
            ai_item['children'].append({
                'href': '/ai/rag/',
                'text': 'RAG 检索增强',
            })
        # Update AI nav title
        ai_item['text'] = 'AI 人工智能'

    # Add generics-update to golang section
    golang_item = None
    for item in nav_items:
        if item.get('href', '').rstrip('/') == '/golang':
            golang_item = item
            break

    if golang_item:
        if 'children' not in golang_item:
            golang_item['children'] = []
        existing = {c.get('href') for c in golang_item['children']}
        if '/golang/generics-update/' not in existing:
            golang_item['children'].append({
                'href': '/golang/generics-update/',
                'text': '泛型进阶',
            })
        # Update golang nav title
        golang_item['text'] = 'Golang'

    # Save updated data
    save_data(data)
    print(f"\nTotal pages: {len(pages)}")
    print(f"Total nav items: {len(nav_items)}")


def clean_title_from_content(content):
    """Extract title from HTML content."""
    match = re.search(r'<h[23][^>]*id="([^"]+)"[^>]*>([^<]+)</h[23]>', content)
    if match:
        return match.group(2)
    match = re.search(r'<h[23][^>]*>([^<]+)</h[23]>', content)
    if match:
        return match.group(1)
    return 'Untitled'


if __name__ == '__main__':
    update_content()
