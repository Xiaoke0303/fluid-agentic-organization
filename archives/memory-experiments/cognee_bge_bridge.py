#!/usr/bin/env python3
"""
Cognee + BGE-small-zh 整合配置
使用本地 BGE 模型替代外部 API 的 embedding
"""

import os
import sys
import json
import asyncio
import numpy as np
from pathlib import Path
from typing import List

# 环境设置
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'

# 路径配置
COGNEE_ENV = Path("/root/cognee-env")
EMBEDDING_VENV = Path.home() / ".venvs" / "embedding"

def setup_paths():
    """设置 Python 路径"""
    # cognee 环境
    cognee_site = COGNEE_ENV / "lib" / "python3.12" / "site-packages"
    if str(cognee_site) not in sys.path:
        sys.path.insert(0, str(cognee_site))
    
    # embedding 环境
    emb_site = EMBEDDING_VENV / "lib" / "python3.12" / "site-packages"
    if str(emb_site) not in sys.path:
        sys.path.insert(0, str(emb_site))

setup_paths()

# 导入 BGE
from sentence_transformers import SentenceTransformer

# cognee 核心库（简化导入）
import cognee
from cognee.infrastructure.databases.vector import get_vector_db_client

class BGEEmbedder:
    """BGE-small-zh 封装，适配 cognee 接口"""
    
    def __init__(self):
        print("Loading BGE-small-zh for cognee...")
        self.model = SentenceTransformer(
            "BAAI/bge-small-zh-v1.5",
            device='cpu',
            trust_remote_code=True
        )
        self.dim = self.model.get_embedding_dimension()
        print(f"✓ BGE ready. Dim: {self.dim}")
    
    def embed_text(self, text: str) -> List[float]:
        """单文本编码"""
        instruction = "为这个句子生成表示以用于检索相关文章："
        vec = self.model.encode(
            f"{instruction}{text}",
            normalize_embeddings=True,
            show_progress_bar=False
        )
        return vec.tolist()
    
    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """批量编码"""
        instruction = "为这个句子生成表示以用于检索相关文章："
        texts = [f"{instruction}{t}" for t in texts]
        vecs = self.model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=False
        )
        return vecs.tolist()


class CogneeBGE:
    """Cognee + BGE 整合封装"""
    
    def __init__(self, data_dir: str = "/root/cognee-data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        # 初始化 BGE
        self.embedder = BGEEmbedder()
        
        # 配置 cognee
        self._setup_cognee()
        
        print(f"✓ Cognee+BGE initialized")
        print(f"  Data: {self.data_dir}")
    
    def _setup_cognee(self):
        """配置 cognee 环境"""
        os.environ["COGNEE_DIRECTORY"] = str(self.data_dir)
        
        # 创建 cognee 配置
        config_path = self.data_dir / "config.json"
        config = {
            "llm_provider": "custom",  # 使用自定义 embedding
            "vector_db": "lancedb",
            "graph_db": "kuzu",
            "embedding_dim": self.embedder.dim
        }
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
    
    async def add_documents(self, texts: List[str], source: str = "manual"):
        """添加文档到记忆系统"""
        print(f"\nAdding {len(texts)} documents...")
        
        # 生成向量
        embeddings = self.embedder.embed_texts(texts)
        
        # 存储到 lancedb
        import lancedb
        db = lancedb.connect(str(self.data_dir / "vector_store"))
        
        # 准备数据
        data = []
        for i, (text, emb) in enumerate(zip(texts, embeddings)):
            data.append({
                "id": i,
                "text": text,
                "vector": emb,
                "source": source,
                "timestamp": str(np.datetime64('now'))
            })
        
        # 创建/追加表
        if "documents" in db.table_names():
            table = db.open_table("documents")
            table.add(data)
        else:
            table = db.create_table("documents", data)
        
        print(f"✓ Stored in LanceDB: {len(data)} docs")
        
        # 同时尝试简单的图谱关系（知识三元组提取）
        await self._build_simple_graph(texts)
    
    async def _build_simple_graph(self, texts: List[str]):
        """构建简单知识图谱"""
        import kuzu
        
        db_path = self.data_dir / "graph_store"
        db = kuzu.Database(str(db_path))
        conn = kuzu.Connection(db)
        
        # 初始化 schema（如果不存在）
        try:
            conn.execute("CREATE NODE TABLE Concept(name STRING PRIMARY KEY, type STRING)")
            conn.execute("CREATE REL TABLE Related(FROM Concept TO Concept, weight DOUBLE)")
        except:
            pass  # 表已存在
        
        # 简单提取实体和关系（关键词匹配）
        concepts = set()
        relations = []
        
        keywords = {
            "FAO": "framework",
            "成本": "concept", "token": "concept", "人力": "concept",
            "记忆": "concept", "压缩": "action", "整理": "action",
            "智能体": "entity", "人类": "entity",
            "路由": "mechanism", "层级": "structure",
            "保函": "business", "转开": "operation", "反担保": "operation",
        }
        
        for text in texts:
            found = []
            for kw, ktype in keywords.items():
                if kw in text:
                    found.append((kw, ktype))
                    concepts.add((kw, ktype))
            
            # 简单的共现关系
            for i in range(len(found)):
                for j in range(i+1, len(found)):
                    relations.append((found[i][0], found[j][0]))
        
        # 写入节点
        for name, ctype in concepts:
            try:
                conn.execute(f'CREATE (c:Concept {{name: "{name}", type: "{ctype}"}})')
            except:
                pass  # 节点已存在
        
        # 写入关系
        for src, dst in relations:
            try:
                conn.execute(f'MATCH (a:Concept), (b:Concept) WHERE a.name = "{src}" AND b.name = "{dst}" CREATE (a)-[:Related {{weight: 1.0}}]->(b)')
            except:
                pass
        
        print(f"✓ Graph: {len(concepts)} concepts, {len(relations)} relations")
    
    async def search(self, query: str, top_k: int = 5):
        """语义搜索"""
        import lancedb
        
        query_vec = self.embedder.embed_text(query)
        
        db = lancedb.connect(str(self.data_dir / "vector_store"))
        if "documents" not in db.table_names():
            return []
        
        table = db.open_table("documents")
        results = table.search(query_vec).limit(top_k).to_list()
        
        return results
    
    async def query_graph(self, concept: str):
        """查询知识图谱"""
        import kuzu
        
        db_path = self.data_dir / "graph_store"
        if not db_path.exists():
            return []
        
        db = kuzu.Database(str(db_path))
        conn = kuzu.Connection(db)
        
        result = conn.execute(f'''
            MATCH (c:Concept)-[r:Related]->(other:Concept)
            WHERE c.name = "{concept}"
            RETURN other.name, other.type, r.weight
            ORDER BY r.weight DESC
        ''')
        
        return result.get_as_df().to_dict('records')


async def demo():
    """完整演示"""
    print("="*60)
    print("Cognee + BGE-small-zh 记忆系统演示")
    print("="*60)
    
    # 初始化
    memory = CogneeBGE()
    
    # 添加测试文档
    documents = [
        "FAO的成本维度包括token消耗和人力验证成本",
        "记忆系统需要定期压缩和整理以保持检索效率",
        "Claude Code的自动Dream功能可以在夜间自主工作",
        "保函业务中的转开结构和反担保结构需要仔细区分",
        "路由机制是FAO的核心，不是层级结构",
        "异质主体协作意味着人类判断与智能体执行的分工",
        "致良知是FAO中的责任锚定机制",
        "事上磨练强调任务路由在具体事务中的实践检验",
    ]
    
    await memory.add_documents(documents, source="FAO白皮书")
    
    # 语义搜索测试
    print("\n" + "="*60)
    print("语义搜索测试")
    print("="*60)
    
    queries = [
        "FAO要花多少钱",
        "记忆怎么维护",
        "保函有哪些类型",
        "自动运行功能",
        "责任机制是什么",
    ]
    
    for query in queries:
        print(f"\n🔍 查询: '{query}'")
        results = await memory.search(query, top_k=3)
        for r in results:
            score = r.get('_distance', 0)
            text = r.get('text', '')[:40]
            print(f"  → [{1-score:.3f}] {text}...")
    
    # 图谱查询
    print("\n" + "="*60)
    print("知识图谱查询")
    print("="*60)
    
    for concept in ["FAO", "记忆", "保函"]:
        print(f"\n📊 '{concept}' 相关概念:")
        related = await memory.query_graph(concept)
        for r in related[:3]:
            print(f"  → {r.get('other.name')} ({r.get('other.type')})")
    
    print("\n" + "="*60)
    print("✅ Cognee + BGE 整合完成")
    print("="*60)


if __name__ == "__main__":
    asyncio.run(demo())
