# 笔记软件市场分析与本地笔记系统设计

## 一、市场分析：主流笔记软件对比

### 1. 软件分类矩阵

| 类型 | 代表 | 优点 | 缺点 | 适合人群 |
|------|------|------|------|---------|
| **知识图谱型** | Obsidian | 本地优先、双向链接、图谱可视化、插件丰富 | 移动端弱、同步付费 | PKM重度用户 |
| **大纲/outliner型** | Logseq | 大纲结构、双向链接、开源免费、本地优先 | 长文写作不适、移动端弱 | 思维整理者 |
| **数据库型** | Notion | 强大的数据库、协作、模板 | 非本地、无离线、隐私风险 | 团队协作 |
| **隐私安全型** | Joplin | 开源、端到端加密、跨平台 | UI较简陋、移动端弱 | 隐私优先 |
| **对象型** | Anytype/Capacities | 对象关联、P2P同步 | 新兴产品、生态不成熟 | 结构化思维 |
| **简单型** | Apple/Google Notes | 开箱即用、生态集成 | 功能受限、不可移植 | 轻度用户 |

### 2. 关键趋势 (2025-2026)

1. **Local-first回归**：Obsidian、Logseq、Anytype都主打本地优先
2. **Markdown标准**：成为知识管理的事实标准
3. **双向链接普及**：从Roam Research开始，已成标配
4. **AI集成**：Notion AI、Obsidian Copilot等
5. **隐私重视**：端到端加密成为卖点

### 3. 痛点总结

- **Obsidian**：同步贵、移动端差、插件依赖
- **Notion**：数据不自主、离线差、越来越臃肿
- **Logseq**：大纲限制、性能问题
- **Joplin**：体验差、生态弱
- **通用**：跨平台同步要么贵要么复杂

---

## 二、本地笔记系统设计方案

### 核心理念

**"文件即笔记，文件夹即分类，Git即历史"**

- 纯Markdown文件，无任何锁定
- 文件系统原生组织
- Git版本控制
- 简单脚本增强

### 系统架构

```
~/notes/                          # 笔记根目录
├── inbox/                        # 收件箱（临时存放）
├── daily/                        # 日记（YYYY-MM-DD.md）
├── projects/                     # 项目笔记
│   ├── active/                   # 进行中
│   ├── backlog/                  # 待办
│   └── archive/                  # 已完成
├── areas/                        # 领域（长期关注）
│   ├── tech/                     # 技术
│   ├── health/                   # 健康
│   ├── finance/                  # 财务
│   └── ...
├── resources/                    # 参考资料
│   ├── books/                    # 读书笔记
│   ├── articles/                 # 文章收藏
│   └── tools/                    # 工具/软件
├── zettelkasten/                 # 卡片盒（原子笔记）
│   └── {YYYY}{MM}{DD}{HH}{MM}.md # 时间戳命名
└── templates/                    # 模板
    ├── daily.md
    ├── project.md
    └── zettel.md
```

### 命名规范

| 类型 | 命名规则 | 示例 |
|------|---------|------|
| 日记 | `YYYY-MM-DD.md` | `2026-03-29.md` |
| 项目 | `project-slug.md` | `fao-whitepaper.md` |
| 卡片 | `YYYYMMDDHHMM.md` | `202603290105.md` |
| 主题 | `kebab-case.md` | `local-first-principle.md` |

### 文件格式标准

```markdown
---
title: "笔记标题"
date: 2026-03-29
tags: [tag1, tag2]
status: # seedling / growing / evergreen
source: # 可选：来源链接
---

# 笔记标题

正文内容...

## 相关链接

- [[202603290103]] 相关笔记1
- [[another-note]] 相关笔记2

## 反向链接

*自动生成的链接到此的笔记*
```

### 工具链

| 功能 | 工具 | 说明 |
|------|------|------|
| **编辑** | VS Code + Foam / Vim / Obsidian(可选) | 首选VS Code + 插件 |
| **搜索** | `rg` (ripgrep) | 命令行全文搜索 |
| **链接** | 自定义脚本 | 双向链接解析 |
| **同步** | Git + GitHub/GitLab | 版本控制+备份 |
| **发布** | MkDocs / Hugo | 静态站点生成 |
| **移动端** | Working Copy (iOS) / Git Journal | Git移动端 |

### VS Code 插件配置

必装插件：
- **Foam**：双向链接、图谱
- **Markdown All in One**：Markdown增强
- **Paste Image**：粘贴图片
- **GitLens**：Git历史
- **Todo+**：任务管理

### 核心脚本

```bash
# notes-new: 创建新笔记
notes-new() {
  local name=$1
  local date=$(date +%Y%m%d%H%M)
  local file="${date}-${name}.md"
  cp ~/notes/templates/zettel.md ~/notes/zettelkasten/$file
  code ~/notes/zettelkasten/$file
}

# notes-daily: 创建/打开日记
notes-daily() {
  local date=$(date +%Y-%m-%d)
  local file="~/notes/daily/${date}.md"
  if [ ! -f $file ]; then
    cp ~/notes/templates/daily.md $file
  fi
  code $file
}

# notes-search: 全文搜索
notes-search() {
  cd ~/notes && rg -i "$1" --type md
}

# notes-backlinks: 查找反向链接
notes-backlinks() {
  local note=$1
  cd ~/notes && rg -l "\[\[${note}\]\]" --type md
}

# notes-publish: 发布到GitHub Pages
notes-publish() {
  cd ~/notes && git add . && git commit -m "update: $(date)" && git push
}
```

### 工作流程 (PARA方法)

```
1. 捕获 (Capture)
   → 快速记录到 inbox/ 或 daily/

2. 处理 (Process)
   → 定期整理 inbox/，分类到 projects/ 或 areas/

3. 提炼 (Distill)
   → 从项目笔记中提取原子笔记到 zettelkasten/

4. 表达 (Express)
   → 组合卡片形成文章、文档
```

### 与现有系统集成

| 场景 | 方案 |
|------|------|
| 网页收藏 | 浏览器插件 → Markdown → resources/articles/ |
| Kindle笔记 | Clippings.io → Markdown → resources/books/ |
| 会议笔记 | VS Code快速记录 → daily/ → 整理到 projects/ |
| 代码片段 | VS Code Snippets / Gist → resources/tools/ |
| 图片 | Paste Image插件 → assets/ 目录 |

### Git工作流

```bash
# 每日提交
git add .
git commit -m "daily: $(date +%Y-%m-%d)"
git push

# 周回顾
git log --oneline --since="1 week ago"
```

---

## 三、实施步骤

### Phase 1: 基础设施 (本周)

- [ ] 创建 ~/notes 目录结构
- [ ] 初始化 Git 仓库
- [ ] 配置 VS Code + 插件
- [ ] 编写核心脚本 (notes-new, notes-daily, notes-search)
- [ ] 创建模板文件

### Phase 2: 迁移 (下周)

- [ ] 导入现有笔记
- [ ] 整理标签
- [ ] 建立双向链接
- [ ] 设置 Git 自动提交

### Phase 3: 增强 (持续)

- [ ] 配置 MkDocs 发布
- [ ] 移动端 Git 客户端
- [ ] 浏览器剪藏插件
- [ ] 定期回顾流程

---

## 四、对比：为什么选择自建

| 维度 | 商业软件 (Notion/Obsidian) | 自建系统 |
|------|---------------------------|---------|
| **数据所有权** | 受限/付费 | 完全自主 |
| **长期使用** | 可能涨价/关闭 | 永久可用 |
| **定制性** | 受限于产品 | 完全可控 |
| **学习成本** | 中 | 低（Markdown） |
| **功能丰富度** | 高 | 够用即可 |
| **协作** | 强 | Git协作 |
| **移动端** | 好 | 一般 |

---

## 五、参考资源

- [Foam](https://foambubble.github.io/foam/) - VS Code知识管理
- [PARA方法](https://fortelabs.com/blog/para/) - 组织系统
- [Zettelkasten](https://zettelkasten.de/) - 卡片盒笔记法
- [Markdown](https://commonmark.org/) - 标准语法

---

*分析时间：2026-03-29*  
*系统版本：v0.1*
