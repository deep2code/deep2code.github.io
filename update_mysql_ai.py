#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

with open('/Users/junjunyi/src-code/deep2code.github.io/extracted_content.json', 'r') as f:
    data = json.load(f)

content = data['pages']['/mysql/']['content']

# 添加AI增强内容 - 在向量搜索示例之后添加
ai_enhancement = '''

<h4 id="llm优化">LLM 大模型优化</h4>
<p>在 AI 时代，MySQL 通过向量搜索功能支持大语言模型的本地部署和 RAG 应用。</p>

<h5 id="向量存储">向量存储与搜索</h5>
<pre><code class="language-sql">-- 创建向量表 (MySQL 8.0.31+)
CREATE TABLE document_embeddings (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    doc_id BIGINT NOT NULL,
    chunk_text TEXT NOT NULL,
    embedding VECTOR(1536) NOT NULL COMMENT 'OpenAI ada-002 维度',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_vector (embedding) VECTOR_INDEX_TYPE HNSW
);

-- 插入向量数据
INSERT INTO document_embeddings (doc_id, chunk_text, embedding) VALUES
    (1, 'MySQL 是最流行的开源关系数据库', '[0.1, 0.2, ...]'),
    (2, 'InnoDB 是 MySQL 默认存储引擎', '[0.2, 0.3, ...]');

-- 向量相似度搜索
SELECT
    id,
    doc_id,
    chunk_text,
    vector_distance(embedding, '[0.1, 0.2, ...]' , COSINE) as distance
FROM document_embeddings
ORDER BY distance ASC
LIMIT 5;
</code></pre>

<h5 id="rag实现">RAG 架构实现</h5>
<pre><code class="language-python"># Python RAG 示例
import mysql.connector
from openai import OpenAI
import numpy as np

# 连接 MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="rag_db"
)

# 获取用户问题
question = "MySQL 如何优化查询性能?"

# 1. 将问题转为向量
client = OpenAI()
question_embedding = client.embeddings.create(
    model="text-embedding-ada-002",
    input=question
).data[0].embedding

# 2. 向量相似度搜索
cursor = conn.cursor()
query = """
    SELECT chunk_text, vector_distance(embedding, %s, COSINE) as distance
    FROM document_embeddings
    ORDER BY distance ASC
    LIMIT 3
"""
cursor.execute(query, (str(question_embedding),))
results = cursor.fetchall()

# 3. 构建上下文
context = "\\n".join([r[0] for r in results])

# 4. 调用 LLM 生成回答
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "基于以下上下文回答用户问题"},
        {"role": "context", "content": context},
        {"role": "user", "content": question}
    ]
)

print(response.choices[0].message.content)
</code></pre>

<h5 id="ai模型调优">AI 模型调优技巧</h5>
<ul>
<li><strong>向量维度选择</strong>：OpenAI ada-002 使用 1536 维，BGE 使用 1024 维</li>
<li><strong>索引类型</strong>：HNSW 适合中等规模数据，FLAT 适合精确搜索</li>
<li><strong>批量处理</strong>：使用 LOAD DATA 批量导入向量数据</li>
<li><strong>分块策略</strong>：文档分块大小影响检索精度，建议 512-1024 字符</li>
<li><strong>混合搜索</strong>：结合关键词搜索和向量搜索提升召回率</li>
</ul>

<h5 id="性能优化">向量搜索性能优化</h5>
<pre><code class="language-sql">-- 查看向量索引信息
SHOW INDEX FROM document_embeddings;

-- 调整 HNSW 参数
ALTER TABLE document_embeddings
    DROP INDEX idx_vector,
    ADD INDEX idx_vector (embedding) VECTOR_INDEX_TYPE HNSW
    WITH (m = 16, ef_construction = 200);

-- 查询优化
SET SESSION otel_instrumentation_ai = 1;
EXPLAIN ANALYZE
SELECT * FROM document_embeddings
ORDER BY vector_distance(embedding, '[0.1, 0.2, ...]', COSINE)
LIMIT 5;
</code></pre>
'''

# 在向量搜索示例之后添加
old_text = '''</pre>

<h4 id="混合搜索">混合搜索架构</h4>'''

new_text = '''</pre>''' + ai_enhancement + '''
<h4 id="混合搜索">混合搜索架构</h4>'''

content = content.replace(old_text, new_text)

data['pages']['/mysql/']['content'] = content

with open('/Users/junjunyi/src-code/deep2code.github.io/extracted_content.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("AI 增强内容已添加！")
print(f"内容长度: {len(content)} 字符")