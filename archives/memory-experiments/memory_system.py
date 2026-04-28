#!/usr/bin/env python3
"""
记忆外挂系统 v1.0
BGE-small-zh + LanceDB + Kuzu

完全本地运行，无需外部 API
"""

import os
import sys
import json
import asyncio
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

# 环境设置
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
VENV_PATH = Path.home() / ".venvs" / "embedding"
if str(VENV_PATH / "lib" / "python3.12" / "site-packages") not in sys.path:
    sys.path.insert(0, str(VENV_PATH / "lib" / "python3.12" / "site-packages"))

from sentence_transformers import SentenceTransformer
import lancedb

@dataclass
class MemoryItem:
    """记忆项"""
    id: int
    content: str
    source: str
    tags: List[str]
    vector: Optional[List[float]] = None
    created: str = ""
    
    def __post_init__(self):
        if not self.created:
            self.created = datetime.now().isoformat()


class BGEEmbedder:
    """BGE-small-zh 嵌入模型"""
    
    def __init__(self):
        print("Loading BGE-small-zh...")
        self.model = SentenceTransformer(
            "BAAI/bge-small-zh-v1.5",
            device='cpu',
            trust_remote_code=True
        )
        self.dim = self.model.get_embedding_dimension()
        print(f"✓ BGE ready. Dim: {self.dim}")
    
    def encode(self, texts: List[str]) -> np.ndarray:
        """编码文本"""
        instruction = "为这个句子生成表示以用于检索相关文章："
        texts = [f"{instruction}{t}" for t in texts]
        return self.model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=False
        )


class VectorStore:
    """LanceDB 向量存储"""
    
    def __init__(self, data_dir: Path):
        self.db = lancedb.connect(str(data_dir / "vectors"))
        self.table_name = "memories"
    
    def add(self, items: List[MemoryItem]):
        """添加记忆"""
        data = [
            {
                "id": item.id,
                "content": item.content,
                "source": item.source,
                "tags": json.dumps(item.tags),
                "vector": item.vector,
                "created": item.created
            }
            for item in items
        ]
        
        try:
            if self.table_name in self.db.list_tables():
                table = self.db.open_table(self.table_name)
                table.add(data)
            else:
                self.db.create_table(self.table_name, data)
        except Exception as e:
            # LanceDB 可能版本差异，尝试兼容
            try:
                table = self.db.open_table(self.table_name)
                table.add(data)
            except:
                raise e
    
    def search(self, query_vec: np.ndarray, top_k: int = 5) -> List[Dict]:
        """向量搜索"""
        if self.table_name not in self.db.list_tables():
            return []
        
        table = self.db.open_table(self.table_name)
        results = table.search(query_vec).limit(top_k).to_list()
        
        # 解析 tags
        for r in results:
            r['tags'] = json.loads(r.get('tags', '[]'))
        
        return results
    
    def list_all(self) -> List[Dict]:
        """列出所有"""
        if self.table_name not in self.db.list_tables():
            return []
        
        table = self.db.open_table(self.table_name)
        return table.to_pandas().to_dict('records')


class GraphStore:
    """Kuzu 图数据库存储"""
    
    def __init__(self, data_dir: Path):
        self.db_path = data_dir / "graph"
        self._init_db()
    
    def _init_db(self):
        """初始化数据库"""
        try:
            import kuzu
            self.db = kuzu.Database(str(self.db_path))
            self.conn = kuzu.Connection(self.db)
            
            # 创建 schema
            self._create_schema()
        except Exception as e:
            print(f"Graph init warning: {e}")
            self.db = None
            self.conn = None
    
    def _create_schema(self):
        """创建图谱结构"""
        if not self.conn:
            return
        
        try:
            # 实体节点
            self.conn.execute("CREATE NODE TABLE IF NOT EXISTS Entity(name STRING PRIMARY KEY, type STRING, doc_id INT64)")
            # 关系边
            self.conn.execute("CREATE REL TABLE IF NOT EXISTS Relates(FROM Entity TO Entity, relation STRING, weight DOUBLE DEFAULT 1.0)")
        except:
            pass  # 已存在
    
    def add_entities(self, doc_id: int, entities: List[Dict[str, str]]):
        """添加实体"""
        if not self.conn:
            return
        
        for entity in entities:
            name = entity.get('name', '').replace('"', '\\"')
            etype = entity.get('type', 'unknown')
            try:
                self.conn.execute(f'CREATE (e:Entity {{name: "{name}", type: "{etype}", doc_id: {doc_id}}})')
            except:
                pass  # 已存在
    
    def add_relations(self, relations: List[tuple]):
        """添加关系"""
        if not self.conn:
            return
        
        for src, rel, dst in relations:
            src = src.replace('"', '\\"')
            dst = dst.replace('"', '\\"')
            try:
                self.conn.execute(f'''
                    MATCH (a:Entity), (b:Entity) 
                    WHERE a.name = "{src}" AND b.name = "{dst}" 
                    CREATE (a)-[:Relates {{relation: "{rel}", weight: 1.0}}]->(b)
                ''')
            except:
                pass
    
    def query_related(self, entity: str) -> List[Dict]:
        """查询相关实体"""
        if not self.conn:
            return []
        
        entity = entity.replace('"', '\\"')
        try:
            result = self.conn.execute(f'''
                MATCH (e:Entity)-[r:Relates]->(other:Entity)
                WHERE e.name = "{entity}"
                RETURN other.name, other.type, r.relation, r.weight
            ''')
            return result.get_as_df().to_dict('records')
        except:
            return []


class MemorySystem:
    """
    记忆外挂系统
    
    整合向量存储（语义检索）+ 图谱存储（关系推理）
    """
    
    def __init__(self, data_dir: str = "~/.memory_system"):
        self.data_dir = Path(data_dir).expanduser()
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # 初始化组件
        print("="*60)
        print("🧠 记忆外挂系统启动")
        print("="*60)
        
        self.embedder = BGEEmbedder()
        self.vector_store = VectorStore(self.data_dir)
        self.graph_store = GraphStore(self.data_dir)
        
        # 计数器
        self._id_counter = self._get_max_id()
        
        print(f"✓ 系统就绪")
        print(f"  数据目录: {self.data_dir}")
        print(f"  已有记忆: {self._id_counter} 条")
    
    def _get_max_id(self) -> int:
        """获取当前最大ID"""
        records = self.vector_store.list_all()
        if not records:
            return 0
        return max(r.get('id', 0) for r in records) + 1
    
    def add(self, content: str, source: str = "manual", tags: List[str] = None) -> int:
        """
        添加记忆
        
        Args:
            content: 记忆内容
            source: 来源
            tags: 标签列表
        
        Returns:
            记忆ID
        """
        tags = tags or []
        
        # 生成向量
        vec = self.embedder.encode([content])[0]
        
        # 创建记忆项
        item = MemoryItem(
            id=self._id_counter,
            content=content,
            source=source,
            tags=tags,
            vector=vec.tolist()
        )
        
        # 存储
        self.vector_store.add([item])
        
        # 提取简单实体到图谱（基于关键词）
        self._extract_to_graph(item)
        
        self._id_counter += 1
        print(f"✓ 记忆 #{item.id} 已存储")
        return item.id
    
    def _extract_to_graph(self, item: MemoryItem):
        """简单实体提取"""
        # 预定义关键词库
        keywords = {
            "FAO": "framework", "成本": "concept", "token": "concept",
            "记忆": "concept", "智能体": "entity", "人类": "entity",
            "路由": "mechanism", "保函": "business", "层级": "structure",
            "责任": "concept", "锚定": "mechanism", "致良知": "concept",
            "王阳明": "person", "四句教": "concept", "事上磨练": "concept",
        }
        
        # 提取实体
        entities = []
        found_keywords = []
        
        for kw, ktype in keywords.items():
            if kw in item.content:
                entities.append({"name": kw, "type": ktype})
                found_keywords.append(kw)
        
        if entities:
            self.graph_store.add_entities(item.id, entities)
            
            # 添加共现关系
            for i in range(len(found_keywords)):
                for j in range(i+1, len(found_keywords)):
                    self.graph_store.add_relations([
                        (found_keywords[i], "cooccurs", found_keywords[j])
                    ])
    
    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        语义搜索
        
        Args:
            query: 查询文本
            top_k: 返回数量
        
        Returns:
            结果列表
        """
        query_vec = self.embedder.encode([query])[0]
        results = self.vector_store.search(query_vec, top_k)
        
        # 计算相似度分数（转换为 0-1 范围）
        for r in results:
            distance = r.get('_distance', 0)
            r['score'] = 1 - distance  # LanceDB 返回的是距离
        
        return results
    
    def get_related_concepts(self, concept: str) -> List[Dict]:
        """获取相关概念"""
        return self.graph_store.query_related(concept)
    
    def list_recent(self, n: int = 10) -> List[Dict]:
        """列出最近记忆"""
        all_memories = self.vector_store.list_all()
        # 按时间排序
        sorted_memories = sorted(
            all_memories,
            key=lambda x: x.get('created', ''),
            reverse=True
        )
        return sorted_memories[:n]
    
    def stats(self) -> Dict:
        """统计信息"""
        memories = self.vector_store.list_all()
        return {
            "total_memories": len(memories),
            "storage_path": str(self.data_dir),
            "embedding_dim": self.embedder.dim
        }


def interactive_mode():
    """交互式命令行"""
    memory = MemorySystem()
    
    print("\n" + "="*60)
    print("命令: add <内容> | search <查询> | related <概念> | list | stats | quit")
    print("="*60)
    
    while True:
        try:
            cmd = input("\n📝 > ").strip()
            if not cmd:
                continue
            
            parts = cmd.split(maxsplit=1)
            action = parts[0].lower()
            
            if action in ("quit", "q", "exit"):
                break
            
            elif action == "add" and len(parts) > 1:
                # 解析可选的 source 和 tags
                content = parts[1]
                source = "manual"
                tags = []
                
                # 简单解析: content | source | tag1,tag2
                if " | " in content:
                    segments = content.split(" | ")
                    content = segments[0]
                    if len(segments) > 1:
                        source = segments[1]
                    if len(segments) > 2:
                        tags = [t.strip() for t in segments[2].split(",")]
                
                memory.add(content, source=source, tags=tags)
            
            elif action == "search" and len(parts) > 1:
                results = memory.search(parts[1])
                if results:
                    print(f"\n找到 {len(results)} 条相关记忆:")
                    for r in results:
                        score = r.get('score', 0)
                        content = r.get('content', '')[:50]
                        sid = r.get('id', '?')
                        print(f"  [{score:.3f}] #{sid}: {content}...")
                else:
                    print("  无相关记忆")
            
            elif action == "related" and len(parts) > 1:
                related = memory.get_related_concepts(parts[1])
                if related:
                    print(f"\n'{parts[1]}' 相关概念:")
                    for r in related[:5]:
                        name = r.get('other.name', '?')
                        rtype = r.get('other.type', '?')
                        print(f"  → {name} ({rtype})")
                else:
                    print("  无相关概念")
            
            elif action == "list":
                recent = memory.list_recent()
                print(f"\n最近 {len(recent)} 条记忆:")
                for m in recent:
                    content = m.get('content', '')[:40]
                    sid = m.get('id', '?')
                    source = m.get('source', '?')
                    print(f"  #{sid} [{source}]: {content}...")
            
            elif action == "stats":
                s = memory.stats()
                print(f"\n系统统计:")
                for k, v in s.items():
                    print(f"  {k}: {v}")
            
            else:
                print("未知命令")
                
        except KeyboardInterrupt:
            print("\n")
            break
        except Exception as e:
            print(f"Error: {e}")
    
    print("\n记忆系统已关闭")


def demo():
    """演示模式"""
    print("="*60)
    print("🧠 记忆外挂系统 - 完整演示")
    print("="*60)
    
    # 初始化
    memory = MemorySystem(data_dir="~/.memory_demo")
    
    # 添加示例记忆
    print("\n--- 添加记忆 ---")
    test_memories = [
        ("FAO的成本维度包括token消耗和人力验证成本", "FAO白皮书", ["成本", "FAO"]),
        ("记忆系统需要定期压缩和整理以保持检索效率", "技术笔记", ["记忆", "维护"]),
        ("智能体可以执行但不可以承担后果", "FAO核心", ["智能体", "责任"]),
        ("致良知是FAO中的责任锚定机制", "王阳明哲学", ["致良知", "责任"]),
        ("事上磨练强调任务路由在具体事务中的实践检验", "王阳明哲学", ["事上磨练", "路由"]),
        ("保函业务中的转开结构和反担保结构风险不同", "金融笔记", ["保函", "风险"]),
    ]
    
    for content, source, tags in test_memories:
        memory.add(content, source=source, tags=tags)
    
    # 语义搜索测试
    print("\n--- 语义搜索 ---")
    queries = [
        "FAO要花多少钱",
        "记忆怎么维护",
        "保函风险类型",
        "责任机制是什么",
    ]
    
    for query in queries:
        print(f"\n🔍 '{query}':")
        results = memory.search(query, top_k=2)
        for r in results:
            print(f"  → [{r['score']:.3f}] {r['content'][:35]}...")
    
    # 图谱查询
    print("\n--- 知识图谱 ---")
    for concept in ["FAO", "记忆", "致良知"]:
        print(f"\n📊 '{concept}' 相关:")
        related = memory.get_related_concepts(concept)
        for r in related[:3]:
            print(f"  → {r.get('other.name', '?')}")
    
    # 统计
    print("\n--- 系统统计 ---")
    s = memory.stats()
    for k, v in s.items():
        print(f"  {k}: {v}")
    
    print("\n" + "="*60)
    print("✅ 演示完成")
    print("使用: python memory_system.py --interactive 进入交互模式")
    print("="*60)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        interactive_mode()
    else:
        demo()
