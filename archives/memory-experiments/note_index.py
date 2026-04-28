#!/usr/bin/env python3
"""
Get笔记 本地语义索引工具
配合 BGE-small-zh 实现笔记的本地语义搜索
"""

import os
import sys
import json
import numpy as np
from pathlib import Path
from datetime import datetime

# 环境设置
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
VENV_PATH = Path.home() / ".venvs" / "embedding"
if str(VENV_PATH / "lib" / "python3.12" / "site-packages") not in sys.path:
    sys.path.insert(0, str(VENV_PATH / "lib" / "python3.12" / "site-packages"))

from sentence_transformers import SentenceTransformer

class NoteIndex:
    """简单的笔记语义索引"""
    
    def __init__(self, storage_dir="~/.note_index"):
        self.storage = Path(storage_dir).expanduser()
        self.storage.mkdir(exist_ok=True)
        
        self.notes_file = self.storage / "notes.json"
        self.vectors_file = self.storage / "vectors.npy"
        
        # 加载模型
        print("Loading BGE-small-zh...")
        self.model = SentenceTransformer(
            "BAAI/bge-small-zh-v1.5",
            device='cpu',
            trust_remote_code=True
        )
        self.dim = self.model.get_embedding_dimension()
        
        # 加载或初始化数据
        self.notes = self._load_notes()
        self.vectors = self._load_vectors()
        
        print(f"✓ Index ready. Notes: {len(self.notes)}, Dim: {self.dim}")
    
    def _load_notes(self):
        if self.notes_file.exists():
            with open(self.notes_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def _load_vectors(self):
        if self.vectors_file.exists():
            return np.load(self.vectors_file)
        return np.zeros((0, self.dim))
    
    def _save(self):
        with open(self.notes_file, 'w', encoding='utf-8') as f:
            json.dump(self.notes, f, ensure_ascii=False, indent=2)
        if len(self.vectors) > 0:
            np.save(self.vectors_file, self.vectors)
    
    def add(self, content, source="", tags=None):
        """添加笔记到索引"""
        instruction = "为这个句子生成表示以用于检索相关文章："
        vec = self.model.encode([f"{instruction}{content}"], normalize_embeddings=True)
        
        note = {
            "id": len(self.notes),
            "content": content,
            "source": source,
            "tags": tags or [],
            "created": datetime.now().isoformat()
        }
        
        self.notes.append(note)
        self.vectors = np.vstack([self.vectors, vec]) if len(self.vectors) > 0 else vec
        self._save()
        
        print(f"✓ Added note #{note['id']}")
        return note['id']
    
    def search(self, query, top_k=5):
        """语义搜索笔记"""
        if len(self.notes) == 0:
            return []
        
        instruction = "为这个句子生成表示以用于检索相关文章："
        query_vec = self.model.encode([f"{instruction}{query}"], normalize_embeddings=True)
        
        scores = np.dot(self.vectors, query_vec.T).flatten()
        top_indices = np.argsort(scores)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            if scores[idx] > 0.3:  # 相似度阈值
                results.append({
                    "note": self.notes[int(idx)],
                    "score": float(scores[idx])
                })
        return results
    
    def list_all(self):
        """列出所有笔记"""
        return self.notes


def interactive_mode():
    """交互式命令行界面"""
    index = NoteIndex()
    
    print("\n" + "="*50)
    print("Get笔记 本地语义索引")
    print("="*50)
    print("命令: add <内容> | search <查询> | list | quit")
    
    while True:
        try:
            cmd = input("\n> ").strip()
            if not cmd:
                continue
            
            parts = cmd.split(maxsplit=1)
            action = parts[0].lower()
            
            if action == "quit" or action == "q":
                break
            
            elif action == "add" and len(parts) > 1:
                index.add(parts[1])
            
            elif action == "search" and len(parts) > 1:
                results = index.search(parts[1])
                if results:
                    print(f"\n找到 {len(results)} 条相关笔记:")
                    for r in results:
                        note = r['note']
                        print(f"  [{r['score']:.3f}] #{note['id']}: {note['content'][:60]}...")
                else:
                    print("  无相关笔记")
            
            elif action == "list":
                notes = index.list_all()
                print(f"\n共 {len(notes)} 条笔记:")
                for n in notes[-10:]:  # 显示最近10条
                    print(f"  #{n['id']}: {n['content'][:50]}...")
            
            else:
                print("未知命令")
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")
    
    print("\nBye!")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        interactive_mode()
    else:
        # 快速测试
        index = NoteIndex()
        
        # 添加示例笔记
        test_notes = [
            "FAO框架的成本维度需要单独分析token和人力成本",
            "记忆系统需要定期压缩，否则检索效率会下降",
            "Get笔记可以与本地embedding模型配合实现语义检索",
            "保函业务中的转开结构和反担保结构风险不同",
        ]
        
        print("\n添加测试笔记...")
        for note in test_notes:
            index.add(note)
        
        print("\n搜索测试...")
        queries = ["FAO要花多少钱", "记忆怎么维护", "保函风险"]
        for q in queries:
            print(f"\n查询: '{q}'")
            results = index.search(q, top_k=2)
            for r in results:
                print(f"  → [{r['score']:.3f}] {r['note']['content'][:40]}...")
        
        print("\n✓ 测试完成")
        print("\n使用: python note_index.py --interactive 进入交互模式")
