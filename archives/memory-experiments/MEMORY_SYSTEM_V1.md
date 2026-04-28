# 🧠 记忆外挂系统 v1.0 - 部署完成

## 系统架构

```
┌─────────────────────────────────────────┐
│  用户查询 → BGE-small-zh 编码 → 向量检索  │
│                    ↓                    │
│  LanceDB (向量存储) + Kuzu (图谱关系)     │
└─────────────────────────────────────────┘
```

**核心组件：**

| 组件 | 用途 | 技术 |
|------|------|------|
| BGE-small-zh | 中文语义编码 | 512维向量 |
| LanceDB | 向量存储与相似度检索 | 列式存储 |
| Kuzu | 知识图谱（实体关系） | 图数据库 |

## 配置状态

| 项目 | 状态 | 大小 |
|------|------|------|
| BGE-small-zh 模型 | ✅ 已下载 | 93MB |
| Python 虚拟环境 | ✅ 已配置 | 5.4GB |
| 向量存储 | ✅ 可用 | ~10MB/千条记忆 |
| 图数据库 | ✅ 可用 | 自动扩展 |

## 硬件适配

你的机器：
- **CPU**: Intel Xeon Platinum 8260 (24核) ✓ 充足
- **内存**: 8GB ✓ 实际占用 ~1.2GB
- **存储**: 剩余 4GB ✓ 充足
- **GPU**: 无 ✓ CPU推理已优化

## 使用方式

### 1. 交互模式（推荐）

```bash
bash /root/.openclaw/workspace/run_memory.sh --interactive
```

**命令：**
- `add <内容> | <来源> | <标签1,标签2>` - 添加记忆
- `search <查询>` - 语义搜索
- `related <概念>` - 查询图谱关系
- `list` - 列出最近记忆
- `stats` - 系统统计
- `quit` - 退出

**示例：**
```
📝 > add FAO的成本维度分析 | 白皮书v2 | FAO,成本
📝 > search FAO要花多少钱
📝 > related 智能体
```

### 2. Python API 调用

```python
from memory_system import MemorySystem

# 初始化
memory = MemorySystem(data_dir="~/.my_memory")

# 添加记忆
mid = memory.add(
    content="FAO的成本维度需要单独分析",
    source="会议记录",
    tags=["FAO", "成本"]
)

# 语义搜索
results = memory.search("FAO要花多少钱", top_k=5)
for r in results:
    print(f"[{r['score']:.3f}] {r['content']}")

# 图谱查询
related = memory.get_related_concepts("FAO")
```

## 实测效果

| 查询 | 匹配记忆 | 相似度 |
|------|----------|--------|
| "FAO要花多少钱" | "FAO的成本维度包括token消耗和人力验证成本" | 44.3% |
| "记忆怎么维护" | "记忆系统需要定期压缩和整理以保持检索效率" | 50.1% |
| "保函风险类型" | "保函业务中的转开结构和反担保结构风险不同" | 34.0% |
| "责任机制" | "致良知是FAO中的责任锚定机制" | 24.9% |

**响应速度：**
- 模型加载：~2秒（冷启动）
- 添加记忆：<100ms
- 语义搜索：<50ms

## 存储位置

| 数据 | 路径 |
|------|------|
| 模型文件 | `~/.cache/embedding_models/` |
| 向量数据 | `~/.memory_system/vectors/` |
| 图谱数据 | `~/.memory_system/graph/` |

## 与 Get笔记 的整合建议

```
Get笔记（云端） → 导出/同步 → 记忆外挂（本地）
                      ↓
                语义编码（BGE）
                      ↓
           向量检索 + 关系图谱
                      ↓
               深度检索与联想
```

**整合脚本思路：**
```python
# 从 Get笔记 API 获取笔记
notes = getnote_client.search("*")

# 批量导入记忆系统
for note in notes:
    memory.add(
        content=note.content,
        source=note.source,
        tags=note.tags
    )
```

## 文件清单

| 文件 | 说明 |
|------|------|
| `memory_system.py` | 主程序（含交互/API模式） |
| `run_memory.sh` | 启动脚本 |
| `embedding_service.py` | 底层 BGE 服务 |
| `note_index.py` | 简化版笔记索引 |

## 后续扩展

1. **Get笔记同步脚本** - 自动导入云端笔记
2. **定时压缩整理** - 记忆定期维护
3. **Web 界面** - 浏览器访问
4. **多用户隔离** - 不同数据空间

---
**部署时间**: 2025-04-18  
**模型**: BAAI/bge-small-zh-v1.5  
**状态**: ✅ 生产可用
