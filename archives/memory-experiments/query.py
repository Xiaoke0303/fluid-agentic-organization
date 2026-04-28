#!/usr/bin/env python3
"""
FAO 云端薄记忆查询工具
轻量级关键词搜索 + 元数据提取
无需外部依赖
"""
import os
import re
import sys
from datetime import datetime
from pathlib import Path

MEMORY_DIR = Path("/root/.openclaw/workspace/memory")

def parse_frontmatter(content):
    """解析 YAML frontmatter"""
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            fm_text = parts[1].strip()
            body = parts[2].strip()
            
            # 简单解析 key: value
            metadata = {}
            for line in fm_text.split("\n"):
                if ":" in line:
                    key, val = line.split(":", 1)
                    metadata[key.strip()] = val.strip()
            return metadata, body
    return {}, content

def search_memories(query: str, n: int = 5, verified_only: bool = False):
    """搜索记忆文件
    
    Args:
        query: 关键词（支持多个，空格分隔）
        n: 返回数量
        verified_only: 只返回 verified: true 的记忆
    """
    keywords = query.lower().split()
    results = []
    
    for md_file in MEMORY_DIR.glob("*.md"):
        if md_file.name == "TEMPLATE.md":
            continue
            
        try:
            content = md_file.read_text(encoding="utf-8")
            metadata, body = parse_frontmatter(content)
            
            # 过滤未验证的记忆
            if verified_only and metadata.get("verified") != "true":
                continue
            
            # 计算匹配度（简单关键词匹配）
            text_lower = (body + " " + str(metadata)).lower()
            match_count = sum(1 for kw in keywords if kw in text_lower)
            
            if match_count > 0:
                results.append({
                    "file": md_file.name,
                    "title": body.split("\n")[0].replace("# ", ""),
                    "match": match_count,
                    "verified": metadata.get("verified", "unknown"),
                    "timestamp": metadata.get("timestamp", "unknown"),
                    "preview": body[:100].replace("\n", " ") + "..."
                })
        except Exception as e:
            continue
    
    # 按匹配度排序
    results.sort(key=lambda x: x["match"], reverse=True)
    return results[:n]

def format_output(results, fmt="table"):
    """格式化输出"""
    if fmt == "json":
        import json
        return json.dumps(results, ensure_ascii=False, indent=2)
    
    # table 格式
    lines = ["📚 查询结果", "=" * 70]
    for i, r in enumerate(results, 1):
        v_mark = "✓" if r["verified"] == "true" else "?"
        lines.append(f"\n{i}. [{v_mark}] {r['title']}")
        lines.append(f"   文件: {r['file']}")
        lines.append(f"   匹配: {r['match']} | 时间: {r['timestamp']}")
        lines.append(f"   预览: {r['preview']}")
    lines.append("\n" + "=" * 70)
    lines.append(f"共 {len(results)} 条结果")
    return "\n".join(lines)

def main():
    import argparse
    parser = argparse.ArgumentParser(description="FAO 云端薄记忆查询")
    parser.add_argument("query", help="搜索关键词")
    parser.add_argument("-n", type=int, default=5, help="返回数量")
    parser.add_argument("--verified", action="store_true", help="只返回已验证记忆")
    parser.add_argument("--format", choices=["table", "json"], default="table", help="输出格式")
    
    args = parser.parse_args()
    
    results = search_memories(args.query, args.n, args.verified)
    print(format_output(results, args.format))

if __name__ == "__main__":
    main()
