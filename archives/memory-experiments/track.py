#!/usr/bin/env python3
"""
FAO 记忆活跃度追踪
在访问记忆时自动更新访问计数
"""
import re
from datetime import datetime
from pathlib import Path

def update_access_count(file_path: Path):
    """更新记忆的访问计数"""
    try:
        content = file_path.read_text(encoding="utf-8")
        
        # 解析 frontmatter
        if not content.startswith("---"):
            # 没有 frontmatter，创建一个
            now = datetime.now().isoformat()
            new_content = f"""---
source: file
verified: true
confidence: medium
timestamp: {now}
access_count: 1
last_accessed: {now}
---

{content}"""
            file_path.write_text(new_content, encoding="utf-8")
            return {"access_count": 1, "last_accessed": now}
        
        # 有 frontmatter，更新计数
        parts = content.split("---", 2)
        if len(parts) >= 3:
            fm_text = parts[1]
            body = parts[2]
            
            # 提取当前计数
            count_match = re.search(r'access_count:\s*(\d+)', fm_text)
            current_count = int(count_match.group(1)) if count_match else 0
            
            # 更新计数和时间
            new_count = current_count + 1
            now = datetime.now().isoformat()
            
            # 替换或添加字段
            if 'access_count:' in fm_text:
                fm_text = re.sub(r'access_count:\s*\d+', f'access_count: {new_count}', fm_text)
            else:
                fm_text += f"\naccess_count: {new_count}"
            
            if 'last_accessed:' in fm_text:
                fm_text = re.sub(r'last_accessed:\s*[^\n]*', f'last_accessed: {now}', fm_text)
            else:
                fm_text += f"\nlast_accessed: {now}"
            
            new_content = f"---{fm_text}---{body}"
            file_path.write_text(new_content, encoding="utf-8")
            
            return {"access_count": new_count, "last_accessed": now}
            
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        result = update_access_count(Path(sys.argv[1]))
        print(result)
