#!/usr/bin/env python3
"""
FAO 云端薄记忆 - 统一查询接口
结合小克方案，提供轻量级记忆查询 + 活跃度追踪

使用示例:
    python3 /root/.openclaw/workspace/memory/recall.py "FAO 责任" -n 5
    python3 /root/.openclaw/workspace/memory/recall.py "厚记忆验证" --format json
"""
import os
import re
import sys
import json
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
            
            metadata = {}
            for line in fm_text.split("\n"):
                if ":" in line and not line.strip().startswith("-"):
                    key, val = line.split(":", 1)
                    metadata[key.strip()] = val.strip()
            return metadata, body
    return {}, content

def update_access_metadata(file_path):
    """更新访问计数和最后访问时间"""
    try:
        content = file_path.read_text(encoding="utf-8")
        now = datetime.now().isoformat()
        
        if not content.startswith("---"):
            # 无 frontmatter，创建
            new_content = f"""---
source: file
verified: true
confidence: medium
timestamp: {now[:10]}
access_count: 1
last_accessed: {now}
---

{content}"""
            file_path.write_text(new_content, encoding="utf-8")
            return 1
        
        # 更新现有 frontmatter
        parts = content.split("---", 2)
        fm_text = parts[1]
        body = parts[2]
        
        # 更新计数
        count_match = re.search(r'access_count:\s*(\d+)', fm_text)
        current = int(count_match.group(1)) if count_match else 0
        new_count = current + 1
        
        if 'access_count:' in fm_text:
            fm_text = re.sub(r'access_count:\s*\d+', f'access_count: {new_count}', fm_text)
        else:
            fm_text += f"\naccess_count: 1"
        
        if 'last_accessed:' in fm_text:
            fm_text = re.sub(r'last_accessed:\s*[^\n]*', f'last_accessed: {now}', fm_text)
        else:
            fm_text += f"\nlast_accessed: {now}"
        
        new_content = f"---{fm_text}---{body}"
        file_path.write_text(new_content, encoding="utf-8")
        return new_count
    except Exception as e:
        return 0

def recall(query, n=5, verified_only=False, format="table"):
    """
    云端薄记忆查询接口（对标小克的 recall）
    
    功能:
    - 关键词搜索
    - 自动更新访问计数
    - 支持 verified 过滤
    - table/json 两种输出
    """
    keywords = query.lower().split()
    results = []
    
    for md_file in sorted(MEMORY_DIR.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True):
        if md_file.name in ["TEMPLATE.md", "query.py", "track.py", "recall.py"]:
            continue
            
        try:
            content = md_file.read_text(encoding="utf-8")
            metadata, body = parse_frontmatter(content)
            
            # 过滤
            if verified_only and metadata.get("verified") != "true":
                continue
            
            # 匹配计算
            text_lower = (body + " " + str(metadata)).lower()
            match_count = sum(1 for kw in keywords if kw in text_lower)
            
            if match_count > 0:
                # 更新访问计数
                access_count = update_access_metadata(md_file)
                
                results.append({
                    "id": md_file.stem,
                    "title": body.split("\n")[0].replace("# ", "").replace("#", ""),
                    "match_score": match_count,
                    "verified": metadata.get("verified", "unknown"),
                    "timestamp": metadata.get("timestamp", str(datetime.fromtimestamp(md_file.stat().st_mtime))[:10]),
                    "access_count": access_count,
                    "preview": body[body.find("\n")+1:body.find("\n")+100].replace("\n", " ") + "..."
                })
        except Exception as e:
            continue
    
    # 排序: 匹配度 > 访问计数 > 时间
    results.sort(key=lambda x: (x["match_score"], x["access_count"]), reverse=True)
    return results[:n]

def format_table(results):
    """表格格式输出"""
    if not results:
        return "📭 未找到匹配的记忆"
    
    lines = ["📚 云端薄记忆查询结果", "=" * 75]
    for i, r in enumerate(results, 1):
        v_mark = "✓" if r["verified"] == "true" else "?"
        lines.append(f"\n{i}. [{v_mark}] {r['title']}")
        lines.append(f"   ID: {r['id']} | 匹配: {r['match_score']} | 访问: {r['access_count']}次")
        lines.append(f"   时间: {r['timestamp']} | 验证: {r['verified']}")
        lines.append(f"   {r['preview']}")
    lines.append("\n" + "=" * 75)
    lines.append(f"共 {len(results)} 条结果 | 查询时间: {datetime.now().isoformat()[:19]}")
    return "\n".join(lines)

def format_json(results):
    """JSON 格式输出"""
    return json.dumps({
        "query_time": datetime.now().isoformat(),
        "count": len(results),
        "results": results
    }, ensure_ascii=False, indent=2)

def main():
    import argparse
    parser = argparse.ArgumentParser(description="FAO 云端薄记忆查询（recall）")
    parser.add_argument("query", nargs="?", default="FAO", help="搜索关键词")
    parser.add_argument("-n", type=int, default=5, help="返回数量")
    parser.add_argument("--verified", action="store_true", help="只返回已验证记忆")
    parser.add_argument("--format", choices=["table", "json"], default="table", help="输出格式")
    
    args = parser.parse_args()
    
    results = recall(args.query, args.n, args.verified, args.format)
    
    if args.format == "json":
        print(format_json(results))
    else:
        print(format_table(results))

if __name__ == "__main__":
    main()
