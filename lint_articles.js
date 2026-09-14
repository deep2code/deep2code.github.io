const TurndownService = require('turndown');
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// 初始化 Turndown
const turndownService = new TurndownService({
  headingStyle: 'atx',
  codeBlockStyle: 'fenced'
});

// 读取 extracted_content.json
const data = JSON.parse(fs.readFileSync('extracted_content.json', 'utf8'));
const pages = data.pages;

// 过滤出实际的文章
const articles = Object.entries(pages).filter(([url, page]) => {
  if (url === '/' || url === '/_mtest/') return false;
  if (!page.content || page.content.length < 100) return false;
  return true;
});

console.log(`找到 ${articles.length} 篇文章待审核\n`);

// 创建临时目录
const tempDir = path.join(__dirname, 'temp_lint');
if (!fs.existsSync(tempDir)) {
  fs.mkdirSync(tempDir, { recursive: true });
}

// 清理旧文件
const existingFiles = fs.readdirSync(tempDir);
existingFiles.forEach(f => fs.unlinkSync(path.join(tempDir, f)));

// 转换并保存文章
const results = [];
articles.forEach(([url, page]) => {
  const filename = (page.url_path || url).replace(/^\//, '').replace(/\//g, '_') || 'index';
  const mdPath = path.join(tempDir, `${filename}.md`);
  let markdown = turndownService.turndown(page.content);
  markdown = `# ${page.title}\n\n${markdown}`;
  fs.writeFileSync(mdPath, markdown, 'utf8');
  results.push({ url, title: page.title, mdPath, filename: `${filename}.md` });
});

console.log(`已转换 ${results.length} 篇文章到 Markdown\n`);

// 运行 textlint 并收集输出
let textlintOutput = '';
try {
  const files = fs.readdirSync(tempDir).filter(f => f.endsWith('.md')).map(f => `"${path.resolve(tempDir, f)}"`).join(' ');
  textlintOutput = execSync(`cd zh-blog-lint && npx textlint --config .textlintrc.json ${files} 2>&1`, {
    encoding: 'utf8',
    maxBuffer: 100 * 1024 * 1024,
    shell: '/bin/bash'
  });
} catch (e) {
  textlintOutput = e.stdout || e.stderr || '';
}

// 解析 textlint 输出
const errorStats = {
  byFile: {},
  byRule: {},
  totalErrors: 0,
  longSentences: []
};

const lines = textlintOutput.split('\n');
let currentFile = '';

lines.forEach(line => {
  // 检测文件行 - textlint 输出格式: /full/path/to/file.md
  const fileMatch = line.match(/^\/(?:.*\/temp_lint\/)?(.+?\.md)$/);
  if (fileMatch && !line.includes('error') && !line.includes('warning')) {
    currentFile = fileMatch[1];
    return;
  }

  // 格式1: "    5:73    error    Line 5 sentence length(108)..."
  let errorMatch = line.match(/^\s*(\d+):(\d+)\s+.*?error\s+Line\s+(\d+)\s+(.+)$/);
  if (errorMatch && currentFile) {
    const lineNum = errorMatch[1];
    const errorMessage = errorMatch[4];

    if (!errorStats.byFile[currentFile]) {
      errorStats.byFile[currentFile] = { count: 0, errors: [] };
    }
    errorStats.byFile[currentFile].count++;
    errorStats.totalErrors++;

    if (errorMessage.includes('sentence length')) {
      const match = errorMessage.match(/sentence length\((\d+)\)/);
      if (match) {
        errorStats.longSentences.push({
          file: currentFile,
          line: lineNum,
          length: parseInt(match[1])
        });
      }
      if (!errorStats.byRule['sentence-length']) errorStats.byRule['sentence-length'] = 0;
      errorStats.byRule['sentence-length']++;
    } else {
      if (!errorStats.byRule['其他']) errorStats.byRule['其他'] = 0;
      errorStats.byRule['其他']++;
    }
    return;
  }

  // 格式2: "   10:30     ✓ error  中文与英文之间需要添加空格   zh-technical-writing"
  errorMatch = line.match(/^\s*(\d+):(\d+)\s+.*?✓ error\s+(.+?)(?:\s{2,}|\s+zh-technical-writing)/);
  if (errorMatch && currentFile) {
    const lineNum = errorMatch[1];
    const errorMessage = errorMatch[3].trim();

    if (!errorStats.byFile[currentFile]) {
      errorStats.byFile[currentFile] = { count: 0, errors: [] };
    }
    errorStats.byFile[currentFile].count++;
    errorStats.totalErrors++;

    if (errorMessage.includes('中文与英文之间需要添加空格')) {
      if (!errorStats.byRule['中英空格']) errorStats.byRule['中英空格'] = 0;
      errorStats.byRule['中英空格']++;
    } else if (errorMessage.includes('全角标点')) {
      if (!errorStats.byRule['全角标点空格']) errorStats.byRule['全角标点空格'] = 0;
      errorStats.byRule['全角标点空格']++;
    } else if (errorMessage.includes('terminology')) {
      if (!errorStats.byRule['术语']) errorStats.byRule['术语'] = 0;
      errorStats.byRule['术语']++;
    } else if (errorMessage.includes('中文与数字')) {
      if (!errorStats.byRule['中文数字空格']) errorStats.byRule['中文数字空格'] = 0;
      errorStats.byRule['中文数字空格']++;
    } else if (errorMessage.includes('多余的空格')) {
      if (!errorStats.byRule['多余空格']) errorStats.byRule['多余空格'] = 0;
      errorStats.byRule['多余空格']++;
    } else {
      if (!errorStats.byRule['其他']) errorStats.byRule['其他'] = 0;
      errorStats.byRule['其他']++;
    }
  }
});

// 运行 markdownlint
let mdlintOutput = '';
try {
  mdlintOutput = execSync('cd zh-blog-lint && npx markdownlint-cli2 --config .markdownlint.json "../temp_lint/*.md" 2>&1', {
    encoding: 'utf8',
    maxBuffer: 50 * 1024 * 1024,
    shell: '/bin/bash'
  });
} catch (e) {
  mdlintOutput = e.stdout || e.stderr || '';
}

// 解析 markdownlint 输出
const mdStats = {
  byFile: {},
  totalErrors: 0
};

mdlintOutput.split('\n').forEach(line => {
  const match = line.match(/^.*\/temp_lint\/(.+?\.md):(\d+):\d+ error (.+?) /);
  if (match) {
    const file = match[1];
    const rule = match[3];
    if (!mdStats.byFile[file]) {
      mdStats.byFile[file] = { count: 0, rules: {} };
    }
    mdStats.byFile[file].count++;
    mdStats.totalErrors++;
    if (!mdStats.byFile[file].rules[rule]) {
      mdStats.byFile[file].rules[rule] = 0;
    }
    mdStats.byFile[file].rules[rule]++;
  }
});

// 打印报告
console.log('='.repeat(60));
console.log('📊 审核报告汇总');
console.log('='.repeat(60));

console.log('\n📝 textlint 错误统计:');
console.log(`  总错误数: ${errorStats.totalErrors}`);
console.log('\n  按规则类型:');
Object.entries(errorStats.byRule)
  .sort((a, b) => b[1] - a[1])
  .forEach(([rule, count]) => {
    console.log(`    - ${rule}: ${count}`);
  });

console.log('\n  🔴 长句 (超过100字):');
if (errorStats.longSentences.length > 0) {
  errorStats.longSentences.sort((a, b) => b.length - a.length).slice(0, 10).forEach(s => {
    console.log(`    - ${s.file}:${s.line} (${s.length}字)`);
  });
} else {
  console.log('    无');
}

console.log('\n📋 markdownlint 错误统计:');
console.log(`  总错误数: ${mdStats.totalErrors}`);

console.log('\n  🔴 错误最多的文件 (前10):');
Object.entries(mdStats.byFile)
  .sort((a, b) => b[1].count - a[1].count)
  .slice(0, 10)
  .forEach(([file, data]) => {
    console.log(`    - ${file}: ${data.count}个错误`);
    Object.entries(data.rules).forEach(([rule, count]) => {
      console.log(`        ${rule}: ${count}`);
    });
  });

console.log('\n' + '='.repeat(60));
console.log('✅ 审核完成');
console.log('='.repeat(60));

// 保存详细报告
const report = {
  textlint: {
    total: errorStats.totalErrors,
    byRule: errorStats.byRule,
    longSentences: errorStats.longSentences,
    byFile: errorStats.byFile
  },
  markdownlint: {
    total: mdStats.totalErrors,
    byFile: mdStats.byFile
  }
};

fs.writeFileSync('lint_report.json', JSON.stringify(report, null, 2), 'utf8');
console.log('\n📄 详细报告已保存到 lint_report.json');