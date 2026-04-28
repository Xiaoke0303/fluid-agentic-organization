#!/usr/bin/env python3
"""Fetch and digest GitHub data for FAO patrol. Writes to /tmp/github_fao_patrol_digest.md"""
import json, urllib.request, sys, subprocess, os

REPO = "Xiaoke0303/FAO_Fluid-Agentic-Organization"

def get_token():
    try:
        return subprocess.check_output(["gh", "auth", "token"], text=True).strip()
    except Exception:
        return os.environ.get("GITHUB_TOKEN", "")

GH_TOKEN = get_token()

def fetch(url):
    headers = {"Accept": "application/vnd.github+json"}
    if GH_TOKEN:
        headers["Authorization"] = f"Bearer {GH_TOKEN}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.load(resp)
    except Exception as e:
        return [{"error": str(e)}]

def fmt_pr(item):
    num = item.get("number", "?")
    title = item.get("title", "N/A")
    author = item.get("user", {}).get("login", "N/A")
    state = item.get("state", "N/A")
    merged = item.get("merged_at")
    return f"#{num} | {title} | {author} | state:{state} | merged_at:{merged or 'N/A'}"

open_prs = fetch(f"https://api.github.com/repos/{REPO}/pulls?state=open&per_page=5")
closed_prs = fetch(f"https://api.github.com/repos/{REPO}/pulls?state=closed&per_page=5")
issues = fetch(f"https://api.github.com/repos/{REPO}/issues?state=open&per_page=5")

lines = ["## FAO GitHub 数据摘要", f"仓库: {REPO}", ""]

lines.append("### 开放 PR（最多5条）")
if isinstance(open_prs, list):
    lines.extend([fmt_pr(i) for i in open_prs] or ["无"])
else:
    lines.append(str(open_prs))
lines.append("")

lines.append("### 最近关闭 PR（最多5条）")
if isinstance(closed_prs, list):
    lines.extend([fmt_pr(i) for i in closed_prs] or ["无"])
else:
    lines.append(str(closed_prs))
lines.append("")

lines.append("### 开放 Issues（最多5条）")
if isinstance(issues, list):
    lines.extend([f"#{i.get('number','?')} | {i.get('title','N/A')} | {i.get('user',{}).get('login','N/A')}" for i in issues] or ["无"])
else:
    lines.append(str(issues))
lines.append("")

out_path = "/tmp/github_fao_patrol_digest.md"
with open(out_path, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print(out_path)
