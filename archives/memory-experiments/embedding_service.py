#!/usr/bin/env python3
"""
BGE-small-zh Embedding 服务（国内镜像版）
用于 Get笔记 语义检索的本地轻量级向量模型
"""

import os
import sys
import json
import numpy as np
from pathlib import Path

# 设置国内镜像
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'

# 虚拟环境路径
VENV_PATH = Path.home() / ".venvs" / "embedding"
if str(VENV_PATH / "lib" / "python3.12" / "site-packages") not in sys.path:
    sys.path.insert(0, str(VENV_PATH / "lib" / "python3.12" / "site-packages"))

from sentence_transformers import SentenceTransformer

# 模型配置
MODEL_NAME = "BAAI/bge-small-zh-v1.5"
MODEL_CACHE = Path.home() / ".cache" / "embedding_models"

class BGEEmbedder:
    """BGE-small-zh 嵌入模型封装"""
    
    def __init__(self):
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """加载模型（首次会自动下载）"""
        print(f"Loading {MODEL_NAME} from hf-mirror.com...")
        os.makedirs(MODEL_CACHE, exist_ok=True)
        
        self.model = SentenceTransformer(
            MODEL_NAME,
            cache_folder=str(MODEL_CACHE),
            device='cpu',  # 明确使用CPU
            trust_remote_code=True
        )
        print(f"✓ Model loaded. Dim: {self.model.get_sentence_embedding_dimension()}")
    
    def encode(self, texts, normalize=True):
        """
        编码文本为向量
        
        Args:
            texts: str 或 List[str]，要编码的文本
            normalize: 是否归一化向量（用于余弦相似度）
        
        Returns:
            numpy array: 向量或向量列表
        """
        if isinstance(texts, str):
            texts = [texts]
        
        # BGE模型需要在中文前加指令前缀以获得更好效果
        instruction = "为这个句子生成表示以用于检索相关文章："
        texts = [f"{instruction}{t}" for t in texts]
        
        embeddings = self.model.encode(
            texts,
            normalize_embeddings=normalize,
            show_progress_bar=False
        )
        return embeddings
    
    def similarity(self, query, documents):
        """
        计算查询与文档列表的相似度
        
        Returns:
            List[tuple]: (index, score) 按相似度排序
        """
        query_vec = self.encode([query], normalize=True)
        doc_vecs = self.encode(documents, normalize=True)
        
        # 余弦相似度（已归一化，直接点积）
        scores = np.dot(doc_vecs, query_vec.T).flatten()
        
        # 排序返回
        indexed_scores = [(i, float(scores[i])) for i in range(len(documents))]
        return sorted(indexed_scores, key=lambda x: x[1], reverse=True)


def demo():
    """演示：语义搜索测试"""
    print("="*50)
    print("BGE-small-zh 语义检索演示")
    print("="*50)
    
    embedder = BGEEmbedder()
    
    # 模拟笔记数据
    notes = [
        "FAO的成本维度包括token消耗和人力验证成本",
        "记忆系统需要定期压缩和整理",
        "Claude Code的自动Dream功能可以夜间自主工作",
        "保函业务中的转开和反担保结构需要仔细区分",
        "路由机制是FAO的核心，不是层级结构",
        " yesterday's meeting discussed the quarterly roadmap",
    ]
    
    print(f"\n笔记库 ({len(notes)} 条):")
    for i, note in enumerate(notes, 1):
        print(f"  {i}. {note}")
    
    # 测试查询
    queries = [
        "FAO要花多少钱",
        "记忆外挂怎么维护",
        "保函有哪些类型",
        "自动运行功能",
    ]
    
    print("\n" + "="*50)
    for query in queries:
        print(f"\n查询: '{query}'")
        results = embedder.similarity(query, notes)
        print("  最相关:")
        for idx, score in results[:2]:
            print(f"    → [{score:.3f}] {notes[idx]}")
    
    print("\n" + "="*50)
    print("✓ 测试完成")
    
    return embedder


def server_mode():
    """简单服务端模式：读取stdin，输出向量json"""
    embedder = BGEEmbedder()
    print(json.dumps({"status": "ready", "dim": 512}), flush=True)
    
    for line in sys.stdin:
        try:
            data = json.loads(line.strip())
            texts = data.get("texts", [])
            embeddings = embedder.encode(texts, normalize=True)
            
            result = {
                "vectors": embeddings.tolist(),
                "count": len(texts)
            }
            print(json.dumps(result), flush=True)
        except Exception as e:
            print(json.dumps({"error": str(e)}), flush=True)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--server":
        server_mode()
    else:
        demo()
