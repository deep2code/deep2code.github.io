#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

# 读取JSON文件
with open('/Users/junjunyi/src-code/deep2code.github.io/extracted_content.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

mysql_content = data['pages']['/mysql/']['content']

# 1. 在SQL基础部分添加SQL标准及进化
sql_evolution_addition = '''
<h4 id="sql标准进化">SQL 标准及进化</h4>
<p>SQL 作为关系型数据库的标准语言，经历了多个版本的演进：</p>

<table>
<thead>
<tr><th>标准</th><th>年份</th><th>主要特性</th><th>MySQL 支持</th></tr>
</thead>
<tbody>
<tr><td>SQL-86</td><td>1986</td><td>基础 SELECT、INSERT</td><td>✅</td></tr>
<tr><td>SQL-89</td><td>1989</td><td>完整性约束、触发器</td><td>✅</td></tr>
<tr><td>SQL-92</td><td>1992</td><td>JOIN、CASE、SET 操作</td><td>✅</td></tr>
<tr><td>SQL:1999</td><td>1999</td><td>递归查询、OLAP、正则</td><td>✅ 部分</td></tr>
<tr><td>SQL:2003</td><td>2003</td><td>XML 支持、窗口函数</td><td>✅ 部分</td></tr>
<tr><td>SQL:2006</td><td>2006</td><td>XQuery、XML 函数</td><td>✅ 部分</td></tr>
<tr><td>SQL:2008</td><td>2008</td><td>ORDER BY 增强</td><td>✅</td></tr>
<tr><td>SQL:2011</td><td>2011</td><td>时序数据、PERIOD</td><td>✅ 部分</td></tr>
<tr><td>SQL:2016</td><td>2016</td><td>JSON、行模式识别</td><td>✅</td></tr>
<tr><td>SQL:2019</td><td>2019</td><td>多维数组、图查询</td><td>🚧 规划中</td></tr>
<tr><td>SQL:2023</td><td>2023</td><td>AI/ML 原生支持、向量类型</td><td>🚧 发展中</td></tr>
</tbody>
</table>

<div class="echart-container" data-option="{&quot;type&quot;: &quot;line&quot;, &quot;title&quot;: {&quot;text&quot;: &quot;SQL 标准演进历程&quot;}, &quot;categories&quot;: [&quot;1986&quot;, &quot;1992&quot;, &quot;1999&quot;, &quot;2003&quot;, &quot;2011&quot;, &quot;2016&quot;, &quot;2023&quot;], &quot;series&quot;: [{&quot;name&quot;: &quot;特性数量&quot;, &quot;value&quot;: [5, 15, 35, 45, 55, 70, 90]}]}"></div>

<p><strong>MySQL 扩展</strong>：MySQL 在标准 SQL 基础上增加了许多特有功能：</p>
<ul>
<li><code>REPLACE</code>：插入或更新</li>
<li><code>INSERT ... ON DUPLICATE KEY UPDATE</code>：冲突更新</li>
<li><code>INSERT IGNORE</code>：忽略重复</li>
<li><code>GROUP_CONCAT</code>：字符串聚合</li>
<li><code>EXPLAIN FORMAT=JSON</code>：详细执行计划</li>
<li><code>WITH RECURSIVE</code>：递归 CTE (8.0+)</li>
</ul>
'''

# 在"基本规则"之后插入SQL标准进化
mysql_content = mysql_content.replace(
    '<h4 id="sql注释">注释</h4>',
    sql_evolution_addition + '\n<h4 id="sql注释">注释</h4>'
)

# 2. 添加完整的CRUD示例（在数据类型之前）
crud_example = '''
<h2 id="完整示例">📋 完整示例：数据表增删改查</h2>

<h3 id="crud概述">CRUD 概述</h3>
<p>CRUD 代表 Create（创建）、Read（读取）、Update（更新）、Delete（删除），是数据库操作的核心。</p>

<h3 id="创建表">1. 创建数据表</h3>
<pre><code class="language-sql">-- 创建数据库
CREATE DATABASE IF NOT EXISTS shop_db
    DEFAULT CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE shop_db;

-- 创建用户表
CREATE TABLE IF NOT EXISTS users (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE COMMENT '用户名',
    email VARCHAR(100) NOT NULL COMMENT '邮箱',
    password_hash VARCHAR(255) NOT NULL COMMENT '密码哈希',
    status TINYINT DEFAULT 1 COMMENT '状态:1正常 0禁用',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_username (username),
    INDEX idx_email (email),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='用户表';

-- 创建商品表
CREATE TABLE IF NOT EXISTS products (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    category_id BIGINT UNSIGNED COMMENT '分类ID',
    name VARCHAR(200) NOT NULL COMMENT '商品名',
    description TEXT COMMENT '商品描述',
    price DECIMAL(10,2) NOT NULL COMMENT '价格',
    stock INT UNSIGNED DEFAULT 0 COMMENT '库存',
    status TINYINT DEFAULT 1 COMMENT '状态',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FULLTEXT INDEX ft_name (name, description),
    INDEX idx_category (category_id),
    INDEX idx_price (price),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='商品表';

-- 创建订单表
CREATE TABLE IF NOT EXISTS orders (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT UNSIGNED NOT NULL COMMENT '用户ID',
    order_no VARCHAR(32) NOT NULL UNIQUE COMMENT '订单号',
    total_amount DECIMAL(12,2) NOT NULL DEFAULT 0 COMMENT '订单总额',
    status TINYINT DEFAULT 1 COMMENT '1:待支付 2:已支付 3:已发货 4:已完成 5:已取消',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_user (user_id),
    INDEX idx_order_no (order_no),
    INDEX idx_status (status),
    INDEX idx_created (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='订单表';

-- 创建订单明细表
CREATE TABLE IF NOT EXISTS order_items (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    order_id BIGINT UNSIGNED NOT NULL COMMENT '订单ID',
    product_id BIGINT UNSIGNED NOT NULL COMMENT '商品ID',
    product_name VARCHAR(200) NOT NULL COMMENT '商品名称(快照)',
    price DECIMAL(10,2) NOT NULL COMMENT '购买单价',
    quantity INT UNSIGNED NOT NULL COMMENT '购买数量',
    subtotal DECIMAL(12,2) NOT NULL COMMENT '小计',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_order (order_id),
    INDEX idx_product (product_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='订单明细表';

-- 查看表结构
DESCRIBE users;
SHOW CREATE TABLE users\\G
</code></pre>

<h3 id="插入数据">2. 插入数据 (Create)</h3>
<pre><code class="language-sql">-- 插入单条数据
INSERT INTO users (username, email, password_hash)
VALUES ('zhangsan', 'zhangsan@example.com', '$2b$12$abcdefghijklmnopqrstuvwxyz');

-- 插入多条数据
INSERT INTO users (username, email, password_hash, status) VALUES
    ('lisi', 'lisi@example.com', '$2b$12$xxxx', 1),
    ('wangwu', 'wangwu@example.com', '$2b$12$yyyy', 1),
    ('zhaoliu', 'zhaoliu@example.com', '$2b$12$zzzz', 0);

-- 插入或更新 (ON DUPLICATE KEY UPDATE)
INSERT INTO users (username, email, password_hash)
VALUES ('zhangsan', 'zhangsan_new@example.com', '$2b$12$new')
ON DUPLICATE KEY UPDATE
    email = VALUES(email),
    password_hash = VALUES(password_hash);

-- 插入商品数据
INSERT INTO products (category_id, name, description, price, stock) VALUES
    (1, 'iPhone 15 Pro', 'Apple 最新旗舰手机', 7999.00, 100),
    (1, 'MacBook Pro 14', 'Apple 笔记本电脑', 14999.00, 50),
    (2, 'AirPods Pro', '主动降噪无线耳机', 1999.00, 200),
    (3, 'iPad Pro 12.9', '专业级平板电脑', 8999.00, 80);

-- 插入订单
INSERT INTO orders (user_id, order_no, total_amount, status) VALUES
    (1, 'ORD20240912001', 9998.00, 2),
    (1, 'ORD20240912002', 1999.00, 1),
    (2, 'ORD20240912003', 14999.00, 3);

-- 插入订单明细
INSERT INTO order_items (order_id, product_id, product_name, price, quantity, subtotal) VALUES
    (1, 1, 'iPhone 15 Pro', 7999.00, 1, 7999.00),
    (1, 3, 'AirPods Pro', 1999.00, 1, 1999.00),
    (2, 3, 'AirPods Pro', 1999.00, 1, 1999.00),
    (3, 2, 'MacBook Pro 14', 14999.00, 1, 14999.00);

-- 使用 REPLACE（先删除再插入）
REPLACE INTO products (id, name, price) VALUES (1, 'iPhone 15', 7499.00);
</code></pre>

<h3 id="查询数据">3. 查询数据 (Read)</h3>
<pre><code class="language-sql">-- 基本查询
SELECT * FROM users;
SELECT id, username, email FROM users WHERE status = 1;

-- 条件查询
SELECT * FROM products WHERE price > 5000;
SELECT * FROM products WHERE price BETWEEN 1000 AND 5000;
SELECT * FROM products WHERE category_id IN (1, 2);

-- 模糊搜索
SELECT * FROM products WHERE name LIKE '%iPhone%';
SELECT * FROM products WHERE MATCH(name, description) AGAINST('手机' IN NATURAL LANGUAGE MODE);

-- 排序与分页
SELECT * FROM products ORDER BY price DESC LIMIT 10;
SELECT * FROM products ORDER BY created_at DESC LIMIT 20, 10;

-- 聚合统计
SELECT
    COUNT(*) as total_users,
    SUM(CASE WHEN status = 1 THEN 1 ELSE 0 END) as active_users
FROM users;

SELECT
    category_id,
    COUNT(*) as product_count,
    AVG(price) as avg_price,
    MAX(price) as max_price,
    MIN(price) as min_price
FROM products
GROUP BY category_id
HAVING product_count > 0;

-- 多表连接查询
SELECT
    o.id as order_id,
    o.order_no,
    u.username,
    u.email,
    o.total_amount,
    o.status,
    o.created_at
FROM orders o
INNER JOIN users u ON o.user_id = u.id
WHERE o.status >= 2
ORDER BY o.created_at DESC;

-- 子查询
SELECT * FROM products
WHERE price > (SELECT AVG(price) FROM products);

SELECT * FROM users
WHERE id IN (SELECT DISTINCT user_id FROM orders WHERE status = 2);

-- 窗口函数 (MySQL 8.0+)
SELECT
    p.*,
    ROW_NUMBER() OVER (PARTITION BY category_id ORDER BY price DESC) as rank_in_category,
    RANK() OVER (ORDER BY price DESC) as rank_overall,
    LAG(name, 1) OVER (ORDER BY price DESC) as prev_product,
    LEAD(name, 1) OVER (ORDER BY price DESC) as next_product
FROM products p;

-- 公共表表达式 CTE (MySQL 8.0+)
WITH user_orders AS (
    SELECT user_id, COUNT(*) as order_count, SUM(total_amount) as total_spent
    FROM orders
    GROUP BY user_id
)
SELECT
    u.username,
    u.email,
    COALESCE(o.order_count, 0) as order_count,
    COALESCE(o.total_spent, 0) as total_spent
FROM users u
LEFT JOIN user_orders o ON u.id = o.user_id
ORDER BY o.total_spent DESC;
</code></pre>

<h3 id="更新数据">4. 更新数据 (Update)</h3>
<pre><code class="language-sql">-- 基本更新
UPDATE users SET email = 'newemail@example.com' WHERE id = 1;

-- 批量更新
UPDATE products SET price = price * 0.9 WHERE category_id = 1 AND stock > 50;

-- 条件更新
UPDATE orders SET status = 5, updated_at = NOW()
WHERE status = 1 AND created_at < DATE_SUB(NOW(), INTERVAL 7 DAY);

-- 关联更新
UPDATE orders o
INNER JOIN users u ON o.user_id = u.id
SET o.status = 4
WHERE u.status = 0;

-- 使用 CASE 进行条件更新
UPDATE products SET
    price = CASE
        WHEN price > 10000 THEN price * 0.95
        WHEN price > 5000 THEN price * 0.97
        ELSE price
    END,
    updated_at = NOW();

-- 更新限制
UPDATE products SET stock = stock - 1
WHERE id = 1 AND stock > 0;

-- 原子更新（防止并发问题）
UPDATE products SET stock = stock - 1, updated_at = NOW()
WHERE id = 1 AND stock > 0;
SELECT ROW_COUNT();
</code></pre>

<h3 id="删除数据">5. 删除数据 (Delete)</h3>
<pre><code class="language-sql">-- 基本删除
DELETE FROM users WHERE id = 1;

-- 条件删除
DELETE FROM orders WHERE status = 5 AND created_at < DATE_SUB(NOW(), INTERVAL 1 YEAR);

-- 关联删除
DELETE o FROM orders o
INNER JOIN users u ON o.user_id = u.id
WHERE u.status = 0;

-- 截断表（快速删除所有数据）
TRUNCATE TABLE order_items;

-- 使用 LIMIT 删除
DELETE FROM logs WHERE created_at < DATE_SUB(NOW(), INTERVAL 30 DAY)
ORDER BY created_at LIMIT 1000;

-- 软删除（推荐）
ALTER TABLE users ADD COLUMN deleted_at DATETIME DEFAULT NULL;
UPDATE users SET deleted_at = NOW() WHERE id = 1;
SELECT * FROM users WHERE deleted_at IS NULL;
</code></pre>

<h3 id="事务操作">6. 事务操作</h3>
<pre><code class="language-sql">-- 开启事务
START TRANSACTION;

-- 扣减库存
UPDATE products SET stock = stock - 1 WHERE id = 1;

-- 创建订单
INSERT INTO orders (user_id, order_no, total_amount, status) VALUES
    (1, 'ORD20240913001', 7999.00, 1);

-- 获取订单ID
SET @order_id = LAST_INSERT_ID();

-- 添加订单明细
INSERT INTO order_items (order_id, product_id, product_name, price, quantity, subtotal) VALUES
    (@order_id, 1, 'iPhone 15 Pro', 7999.00, 1, 7999.00);

-- 提交事务
COMMIT;

-- 回滚示例
START TRANSACTION;
    UPDATE products SET stock = stock - 1 WHERE id = 999;
    -- 发现商品不存在
ROLLBACK;

-- 保存点
START TRANSACTION;
    INSERT INTO users (username, email) VALUES ('a', 'a@test.com');
    SAVEPOINT sp1;
    INSERT INTO users (username, email) VALUES ('b', 'b@test.com');
    ROLLBACK TO SAVEPOINT sp1;
COMMIT;
-- 只保留了用户 a
</code></pre>

<h3 id="事务隔离级别">7. 事务隔离级别</h3>
<pre><code class="language-sql">-- 查看当前隔离级别
SELECT @@transaction_isolation;

-- 设置隔离级别
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
SET SESSION transaction_isolation = 'READ-COMMITTED';
SET GLOBAL transaction_isolation = 'READ-COMMITTED';

-- 隔离级别测试
-- READ UNCOMMITTED: 脏读
-- READ COMMITTED: 不可重复读
-- REPEATABLE READ: 幻读 (MySQL 默认)
-- SERIALIZABLE: 最高隔离级别
</code></pre>

<h3 id="完整示例小结">小结</h3>
<p>以上展示了 MySQL 完整的数据表操作流程：</p>
<ul>
<li>使用合适的字段类型和索引设计表结构</li>
<li>熟练运用 INSERT、REPLACE、ON DUPLICATE KEY UPDATE</li>
<li>掌握 SELECT 的各种用法：条件、排序、分页、聚合、连接、子查询、窗口函数</li>
<li>UPDATE 时注意条件，避免全表更新</li>
<li>DELETE 前先备份或使用软删除</li>
<li>事务保证数据一致性，合理使用保存点</li>
</ul>
'''

# 在数据类型之前插入完整示例
mysql_content = mysql_content.replace(
    '<h3 id="数据类型">',
    crud_example + '\n<h3 id="数据类型">'
)

# 3. 添加 InnoDB 架构内容（在存储引擎对比之后）
innodb_architecture = '''
<h2 id="innodb架构">🗄️ InnoDB 架构深度解析</h2>

<h3 id="innodb体系结构">InnoDB 体系结构</h3>
<p>InnoDB 是 MySQL 默认的存储引擎，采用 MVCC（多版本并发控制）实现事务隔离，支持行级锁和外键约束。</p>

<div class="echart-container" data-option="{&quot;type&quot;: &quot;graph&quot;, &quot;title&quot;: {&quot;text&quot;: &quot;InnoDB 架构图&quot;}, &quot;nodes&quot;: [{&quot;name&quot;: &quot;Buffer Pool&quot;, &quot;x&quot;: 100, &quot;y&quot;: 200}, {&quot;name&quot;: &quot;Redo Log&quot;, &quot;x&quot;: 300, &quot;y&quot;: 100}, {&quot;name&quot;: &quot;Undo Log&quot;, &quot;x&quot;: 300, &quot;y&quot;: 300}, {&quot;name&quot;: &quot;Change Buffer&quot;, &quot;x&quot;: 100, &quot;y&quot;: 100}, {&quot;name&quot;: &quot;Adaptive Hash&quot;, &quot;x&quot;: 100, &quot;y&quot;: 300}, {&quot;name&quot;: &quot;Doublewrite&quot;, &quot;x&quot;: 300, &quot;y&quot;: 200}, {&quot;name&quot;: &quot;Data Files&quot;, &quot;x&quot;: 500, &quot;y&quot;: 200}], &quot;links&quot;: [{&quot;source&quot;: &quot;Buffer Pool&quot;, &quot;target&quot;: &quot;Data Files&quot;}, {&quot;source&quot;: &quot;Redo Log&quot;, &quot;target&quot;: &quot;Data Files&quot;}, {&quot;source&quot;: &quot;Undo Log&quot;, &quot;target&quot;: &quot;Buffer Pool&quot;}, {&quot;source&quot;: &quot;Change Buffer&quot;, &quot;target&quot;: &quot;Buffer Pool&quot;}, {&quot;source&quot;: &quot;Doublewrite&quot;, &quot;target&quot;: &quot;Data Files&quot;}]}"></div>

<h4 id="内存结构">1. 内存结构</h4>

<h5 id="buffer-pool">Buffer Pool（缓冲池）</h5>
<p>缓冲池是 InnoDB 最重要的内存结构，用于缓存表数据和索引，减少磁盘 I/O。</p>
<pre><code class="language-sql">-- 查看缓冲池大小
SHOW VARIABLES LIKE 'innodb_buffer_pool_size';
-- 默认: 128MB，建议设置为可用内存的 50-70%

-- 查看缓冲池状态
SHOW ENGINE INNODB STATUS\\G
-- 查找 Buffer pool size 相关信息

-- 动态调整缓冲池大小 (MySQL 8.0+)
SET GLOBAL innodb_buffer_pool_size = 2147483648; -- 2GB

-- 缓冲池实例（多实例提升并发）
SHOW VARIABLES LIKE 'innodb_buffer_pool_instances';
</code></pre>

<ul>
<li><strong>Page（页）</strong>：InnoDB 最小存储单位，默认 16KB</li>
<li><strong>Chunk</strong>：缓冲池块，默认 128MB</li>
<li><strong>Instance</strong>：缓冲池实例，用于减少锁竞争</li>
<li><strong>LRU List</strong>：最近最少使用列表，管理页面淘汰</li>
<li><strong>Flush List</strong>：脏页列表，需要刷新到磁盘的页面</li>
<li><strong>Free List</strong>：空闲页面列表</li>
</ul>

<h5 id="change-buffer">Change Buffer（变更缓冲区）</h5>
<p>对非唯一索引的 DML 操作先缓存，减少随机 I/O。</p>
<pre><code class="language-sql">-- 查看变更缓冲配置
SHOW VARIABLES LIKE 'innodb_change_buffering';
-- all: 缓存所有操作
-- none: 不缓存
-- inserts: 只缓存插入
-- deletes: 只缓存删除
-- changes: 缓存插入和删除
-- purges: 缓存后台purge

-- 查看变更缓冲使用情况
SHOW ENGINE INNODB STATUS\\G
-- 查找 INSERT BUFFER AND ADAPTIVE HASH INDEX
</code></pre>

<h5 id="adaptive-hash">Adaptive Hash Index（自适应哈希索引）</h5>
<p>InnoDB 根据查询模式自动构建哈希索引，加速等值查询。</p>
<pre><code class="language-sql">-- 查看自适应哈希索引状态
SHOW ENGINE INNODB STATUS\\G
-- 查找 hash table size, node heap

-- 启用/禁用自适应哈希
SHOW VARIABLES LIKE 'innodb_adaptive_hash_index';
SET GLOBAL innodb_adaptive_hash_index = ON;
</code></pre>

<h4 id="磁盘结构">2. 磁盘结构</h4>

<h5 id="system-tablespace">System Tablespace（系统表空间）</h5>
<p>包含 InnoDB 数据字典、Undo 空间、修改缓冲、双写缓冲区。</p>
<pre><code class="language-sql">-- 查看系统表空间配置
SHOW VARIABLES LIKE 'innodb_data_file_path';
-- ibdata1:12M:autoextend

-- 查看表空间使用
SELECT
    FILE_ID,
    FILE_NAME,
    TABLESPACE_NAME,
    ENGINE,
    INITIAL_SIZE,
    TOTAL_EXTENTS*EXTENT_SIZE as USED_SIZE,
    MAXIMUM_SIZE
FROM information_schema.FILES
WHERE FILE_TYPE = 'TABLESPACE';
</code></pre>

<h5 id="undo-tablespace">Undo Tablespace（Undo 表空间）</h5>
<p>存储事务的回滚段，用于实现 MVCC 和事务回滚。</p>
<pre><code class="language-sql">-- 创建独立的 Undo 表空间 (MySQL 8.0+)
CREATE UNDO TABLESPACE undo_tblsp ADD DATAFILE 'undo_001.ibu';

-- 查看 Undo 表空间
SELECT * FROM information_schema.INNODB_TABLESPACES
    WHERE SPACE_TYPE = 'Undo';

-- 配置 Undo 日志数量
SHOW VARIABLES LIKE 'innodb_undo_tablespaces';
-- 默认: 2
</code></pre>

<h5 id="redo-log">Redo Log（重做日志）</h5>
<p>记录数据页的物理修改，用于崩溃恢复。</p>
<pre><code class="language-sql">-- 查看 Redo Log 配置
SHOW VARIABLES LIKE 'innodb_log_file_size';
SHOW VARIABLES LIKE 'innodb_log_files_in_group';
SHOW VARIABLES LIKE 'innodb_log_group_home_dir';

-- Redo Log 容量计算
-- 建议: innodb_log_file_size * innodb_log_files_in_group >= 缓冲池的 50%
-- 例如: 缓冲池 4GB, 日志文件 2 * 1GB = 2GB (50%)

-- 强制刷新日志
SET GLOBAL innodb_flush_log_at_trx_commit = 1; -- 最安全，每事务刷新
-- 0: 每秒刷新，性能最高
-- 1: 每事务刷新（默认）
-- 2: 提交时刷新到操作系统缓存
</code></pre>

<h5 id="doublewrite">Doublewrite Buffer（双写缓冲区）</h5>
<p>防止部分页写入问题，确保数据页的完整性。</p>
<pre><code class="language-sql">-- 查看双写缓冲
SHOW VARIABLES LIKE 'innodb_doublewrite';
-- ON: 启用双写

-- 查看双写缓冲文件
SHOW VARIABLES LIKE 'innodb_doublewrite_file';
-- 默认: #ib_16384_0.dblwr
</code></pre>

<h5 id="general-tablespace">General Tablespace（通用表空间）</h5>
<p>支持多个表共享一个表空间文件。</p>
<pre><code class="language-sql">-- 创建通用表空间
CREATE TABLESPACE ts1 ADD DATAFILE 'ts1.ibd';

-- 在通用表空间创建表
CREATE TABLE t1 (id INT) TABLESPACE ts1;

-- 移动表到通用表空间
ALTER TABLE t1 TABLESPACE ts1;
</code></pre>

<h5 id="file-per-table">File-Per-Table Tablespace（独立表空间）</h5>
<p>每个表独立的 .ibd 文件，便于管理和备份。</p>
<pre><code class="language-sql">-- 查看独立表空间配置
SHOW VARIABLES LIKE 'innodb_file_per_table';
-- ON: 每个表一个文件

-- 收缩独立表空间
ALTER TABLE t1 ENGINE=InnoDB;
-- 或
OPTIMIZE TABLE t1;
</code></pre>

<h3 id="innodb工作原理">InnoDB 工作原理</h3>

<h4 id="mvcc">MVCC（多版本并发控制）</h4>
<p>InnoDB 通过为每行记录添加两个隐藏列实现 MVCC：</p>
<ul>
<li><strong>DB_TRX_ID</strong>：最近修改的事务 ID</li>
<li><strong>DB_ROLL_PTR</strong>：指向 Undo 日志的指针</li>
</ul>
<p>读取时根据事务的隔离级别决定读取哪个版本的数据。</p>

<h4 id="锁机制">锁机制</h4>
<pre><code class="language-sql">-- 查看当前锁
SELECT * FROM information_schema.INNODB_LOCKS;
SELECT * FROM information_schema.INNODB_LOCK_WAITS;

-- 查看事务锁信息
SHOW ENGINE INNODB STATUS\\G
-- 查找 TRANSACTIONS 部分

-- 死锁检测
SHOW VARIABLES LIKE 'innodb_deadlock_detect';
-- ON: 启用死锁检测
</code></pre>

<table>
<thead>
<tr><th>锁类型</th><th>说明</th><th>粒度</th></tr>
</thead>
<tbody>
<tr><td>S Lock</td><td>共享锁，多事务可同时持有</td><td>行</td></tr>
<tr><td>X Lock</td><td>排他锁，独占访问</td><td>行</td></tr>
<tr><td>IS Lock</td><td>意向共享锁</td><td>表</td></tr>
<tr><td>IX Lock</td><td>意向排他锁</td><td>表</td></tr>
<tr><td>AUTO-INC Lock</td><td>自增锁</td><td>表</td></tr>
</tbody>
</table>

<h4 id="崩溃恢复">崩溃恢复流程</h4>
<ol>
<li><strong>Redo Log 重做</strong>：重做已提交事务的修改</li>
<li><strong>Undo Log 回滚</strong>：回滚未提交事务的修改</li>
<li><strong>Doublewrite 修复</strong>：修复不完整的页写入</li>
<li><strong>Master Thread</strong>：后台定期刷新脏页</li>
</ol>

<h3 id="innodb配置优化">InnoDB 配置优化</h3>
<pre><code class="language-sql">-- 核心参数配置示例
[mysqld]
innodb_buffer_pool_size = 4G          # 缓冲池大小
innodb_buffer_pool_instances = 4      # 缓冲池实例数
innodb_log_file_size = 1G             # Redo 日志大小
innodb_log_files_in_group = 2         # Redo 日志文件数
innodb_flush_log_at_trx_commit = 1    # 日志刷新策略
innodb_flush_method = O_DIRECT        # 刷新方式
innodb_file_per_table = 1             # 独立表空间
innodb_io_capacity = 2000             # I/O 容量
innodb_io_capacity_max = 4000         # 最大 I/O 容量
innodb_read_io_threads = 4            # 读线程数
innodb_write_io_threads = 4           # 写线程数
innodb_page_cleaners = 4              # 页面清理线程
</code></pre>

<h3 id="innodb监控">InnoDB 监控</h3>
<pre><code class="language-sql">-- 缓冲池命中率
SHOW ENGINE INNODB STATUS\\G
-- 查找 Buffer pool hit rate

-- 关键指标查询
SELECT
    variable_name,
    variable_value
FROM performance_schema.global_status
WHERE variable_name LIKE 'Innodb%'
ORDER BY variable_name;

-- 监控脏页比例
SHOW VARIABLES LIKE 'innodb_max_dirty_pages_pct';
-- 默认: 90%

-- 监控检查点
SHOW ENGINE INNODB STATUS\\G
-- 查找 LOG 部分
</code></pre>

<h3 id="innodb小结">小结</h3>
<p>InnoDB 是 MySQL 最核心的存储引擎，理解其架构对于数据库调优至关重要：</p>
<ul>
<li>Buffer Pool 是性能关键，合理配置大小</li>
<li>Redo Log 保证事务持久性，配置合理容量</li>
<li>Undo Log 支持 MVCC 和事务回滚</li>
<li>Doublewrite 确保数据页完整性</li>
<li>锁机制和 MVCC 支撑并发控制</li>
</ul>
'''

# 在存储引擎对比之后插入 InnoDB 架构
mysql_content = mysql_content.replace(
    '<h2 id="进阶技能">',
    innodb_architecture + '\n<h2 id="进阶技能">'
)

# 4. 扩展 AI 时代部分
ai_enhancement = '''
<h3 id="llm优化">LLM 大模型优化</h3>
<p>在 AI 时代，MySQL 通过向量搜索功能支持大语言模型的本地部署和 RAG 应用。</p>

<h4 id="向量存储">向量存储与搜索</h4>
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

<h4 id="rag实现">RAG 架构实现</h4>
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

<h4 id="ai模型调优">AI 模型调优技巧</h4>
<ul>
<li><strong>向量维度选择</strong>：OpenAI ada-002 使用 1536 维，BGE 使用 1024 维</li>
<li><strong>索引类型</strong>：HNSW 适合中等规模数据，FLAT 适合精确搜索</li>
<li><strong>批量处理</strong>：使用 LOAD DATA 批量导入向量数据</li>
<li><strong>分块策略</strong>：文档分块大小影响检索精度，建议 512-1024 字符</li>
<li><strong>混合搜索</strong>：结合关键词搜索和向量搜索提升召回率</li>
</ul>

<h4 id="性能优化">向量搜索性能优化</h4>
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

# 5. 扩展 MySQL 9.x 新特性（重点 Geo 地理位置）
mysql9_enhancement = '''
<h3 id="mysql9新特性">MySQL 9.x 新特性详解</h3>

<h4 id="geo地理位置">🌍 Geo 地理位置（重点）</h4>
<p>MySQL 9.x 对地理空间功能进行了重大增强，支持更丰富的空间数据类型和操作。</p>

<h5 id="新增空间函数">新增空间函数</h5>
<pre><code class="language-sql">-- 创建包含空间数据的表
CREATE TABLE locations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    position POINT NOT NULL SRID 4326,
    area POLYGON,
    route LINESTRING,
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    SPATIAL INDEX (position),
    INDEX (name)
);

-- 插入点数据 (WGS84 坐标系)
INSERT INTO locations (name, position) VALUES
    ('天安门', ST_GeomFromText('POINT(116.397128 39.916527)', 4326)),
    ('故宫', ST_GeomFromText('POINT(116.397469 39.916668)', 4326)),
    ('长城', ST_GeomFromText('POINT(116.573067 40.431908)', 4326));

-- 插入区域数据
INSERT INTO locations (name, area) VALUES
    ('北京市', ST_GeomFromText('POLYGON((116.2 39.8, 116.6 39.8, 116.6 40.2, 116.2 40.2, 116.2 39.8))', 4326)),
    ('上海市', ST_GeomFromText('POLYGON((121.3 31.1, 121.7 31.1, 121.7 31.4, 121.3 31.4, 121.3 31.1))', 4326));

-- 插入路径数据
INSERT INTO locations (name, route) VALUES
    ('京沪高速', ST_GeomFromText('LINESTRING(116.397128 39.916527, 116.4 39.92, 117.2 39.1, 118.0 38.4, 119.0 37.5, 120.0 36.8, 121.0 31.2)', 4326));

-- 距离计算（米）
SELECT
    name,
    ST_Distance_Sphere(
        ST_GeomFromText('POINT(116.397128 39.916527)', 4326),
        position
    ) as distance_meters
FROM locations
WHERE position IS NOT NULL;

-- 附近搜索（10公里范围内）
SELECT
    name,
    ST_Distance_Sphere(
        ST_GeomFromText('POINT(116.397128 39.916527)', 4326),
        position
    ) as distance_meters
FROM locations
WHERE ST_Distance_Sphere(
    ST_GeomFromText('POINT(116.397128 39.916527)', 4326),
    position
) <= 10000
ORDER BY distance_meters;

-- 包含判断（点是否在区域内）
SELECT
    name,
    ST_Contains(
        ST_GeomFromText('POLYGON((116.2 39.8, 116.6 39.8, 116.6 40.2, 116.2 40.2, 116.2 39.8))', 4326),
        ST_GeomFromText('POINT(116.397128 39.916527)', 4326)
    ) as is_in_beijing
FROM locations;

-- 交叉判断（路径是否穿过区域）
SELECT
    name,
    ST_Crosses(
        route,
        ST_GeomFromText('POLYGON((116.2 39.8, 116.6 39.8, 116.6 40.2, 116.2 40.2, 116.2 39.8))', 4326)
    ) as crosses
FROM locations
WHERE route IS NOT NULL;

-- 缓冲区分析（路径周边1公里范围）
SELECT
    ST_AsText(
        ST_Buffer(
            ST_GeomFromText('LINESTRING(116.397128 39.916527, 116.4 39.92)', 4326),
            0.01
        )
    ) as buffer_area;
</code></pre>

<h5 id="geo索引优化">空间索引优化</h5>
<pre><code class="language-sql">-- 查看空间索引
SHOW INDEX FROM locations;

-- 优化查询
EXPLAIN SELECT * FROM locations
WHERE ST_Distance_Sphere(
    ST_GeomFromText('POINT(116.397128 39.916527)', 4326),
    position
) <= 10000;

-- 使用 MBR 快速过滤
SELECT * FROM locations
WHERE MBRContains(
    ST_Buffer(ST_GeomFromText('POINT(116.397128 39.916527)', 4326), 0.1),
    position
);
</code></pre>

<h5 id="geo应用场景">地理应用场景</h5>
<ul>
<li><strong>位置服务</strong>：附近商家、用户推荐</li>
<li><strong>物流配送</strong>：路径规划、区域划分</li>
<li><strong>物联网</strong>：设备追踪、地理围栏</li>
<li><strong>智慧城市</strong>：交通分析、灾害预警</li>
</ul>

<h4 id="json增强">JSON 增强</h4>
<pre><code class="language-sql">-- JSON 多路径查询
SELECT
    JSON_QUERY(data, '$.store.book[*].author') as authors,
    JSON_VALUE(data, '$.store.book[0].price') as first_price
FROM documents;

-- JSON 合并
SELECT JSON_MERGE_PATCH(
    '{"a": 1, "b": 2}',
    '{"b": 3, "c": 4}'
) as merged;
-- 结果: {"a":1,"b":3,"c":4}

-- JSON 表函数
SELECT * FROM JSON_TABLE(
    '[{"id":1,"name":"Alice"},{"id":2,"name":"Bob"}]',
    '$[*]' COLUMNS (
        id INT PATH '$.id',
        name VARCHAR(50) PATH '$.name'
    )
) AS t;
</code></pre>

<h4 id="sql增强">SQL 增强</h4>
<pre><code class="language-sql">-- 递归 CTE 增强
WITH RECURSIVE org_chart AS (
    -- 基础查询
    SELECT id, name, manager_id, 1 as level
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    -- 递归部分
    SELECT e.id, e.name, e.manager_id, oc.level + 1
    FROM employees e
    INNER JOIN org_chart oc ON e.manager_id = oc.id
    WHERE oc.level < 10
)
SELECT * FROM org_chart;

-- WINDOW 窗口函数增强
SELECT
    name,
    department,
    salary,
    AVG(salary) OVER (PARTITION BY department) as dept_avg,
    salary - AVG(salary) OVER (PARTITION BY department) as diff_from_avg
FROM employees;
</code></pre>

<h4 id="性能优化增强">性能优化增强</h4>
<ul>
<li><strong>查询优化器改进</strong>：更准确的代价估算</li>
<li><strong>并行查询</strong>：支持更多场景的并行执行</li>
<li><strong>不可见索引</strong>：在线测试索引效果</li>
<li><strong>降序索引</strong>：优化 DESC 排序</li>
<li><strong>JSON 索引</strong>：原生 JSON 列索引</li>
</ul>

<h4 id="安全增强">安全增强</h4>
<ul>
<li><strong>密码策略</strong>：更灵活的密码复杂度要求</li>
<li><strong>角色管理</strong>：简化权限管理</li>
<li><strong>审计日志</strong>：细粒度审计</li>
<li><strong>防火墙</strong>：SQL 注入防护</li>
</ul>

<h4 id="mysql9升级注意">升级注意事项</h4>
<pre><code class="language-sql">-- 升级前检查
SELECT @@version;

-- 1. 检查不兼容语法
SELECT
    sql_text,
    count(*) as count
FROM mysql.general_log
WHERE command_type = 'Query'
    AND sql_text LIKE '%deprecated%'
GROUP BY sql_text;

-- 2. 检查字符集
SELECT
    table_schema,
    table_name,
    column_name,
    character_set_name
FROM information_schema.columns
WHERE character_set_name NOT IN ('utf8mb4', 'utf8', 'latin1')
LIMIT 10;

-- 3. 检查存储过程
SHOW PROCEDURE STATUS;
SHOW FUNCTION STATUS;

-- 4. 执行升级检查
mysql_upgrade -u root -p --check
</code></pre>
'''

# 在版本现状部分替换新特性内容
mysql_content = mysql_content.replace(
    '''<h4 id="新特性">MySQL 9.x 新特性</h4>
<ul>
<li>向量搜索支持 (8.0.31+)</li>
<li>JSON 增强</li>
<li>性能优化</li>
<li>安全增强</li>
<li>AI/ML 原生支持</li>
</ul>''',
    mysql9_enhancement
)

# 更新 JSON 文件
data['pages']['/mysql/']['content'] = mysql_content

# 写回文件
with open('/Users/junjunyi/src-code/deep2code.github.io/extracted_content.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("MySQL 页面内容已更新完成！")
print(f"新内容长度: {len(mysql_content)} 字符")