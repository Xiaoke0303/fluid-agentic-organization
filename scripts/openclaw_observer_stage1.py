#!/usr/bin/env python3
"""Fetch and digest openclaw issues. Writes to /tmp/openclaw_observer_digest.md"""
import json, urllib.request, subprocess, os

REPO = "openclaw/openclaw"
KEYWORDS = ["memory", "identity", "bootstrap", "injection", "runtime", "stability", "timeout", "pairing", "cron", "session", "agentic", "memory-consolidation"]

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

def matches(item):
    title = item.get("title", "").lower()
    labels = [l.get("name", "").lower() for l in item.get("labels", [])]
    return any(k in title for k in KEYWORDS) or any(any(k in l for k in KEYWORDS) for l in labels)

issues = fetch(f"https://api.github.com/repos/{REPO}/issues?state=open&per_page=20")
if not isinstance(issues, list):
    issues = [{"error": str(issues)}]

matched = [i for i in issues if matches(i)][:5]
other = [i for i in issues if not matches(i)][:3]

lines = ["## OpenClaw GitHub 数据摘要", f"仓库: {REPO}", ""]

lines.append(f"### 匹配关键主题的前 {len(matched)} 条 issues")
for i in matched:
    if "error" in i:
        lines.append(str(i))
        continue
    num = i.get("number", "?")
    title = i.get("title", "N/A")
    labels = ", ".join([l.get("name", "") for l in i.get("labels", [])]) or "无标签"
    created = i.get("created_at", "N/A")
    lines.append(f"#{num} | {title} | labels:{labels} | created_at:{created}")
if not matched:
    lines.append("无")
lines.append("")

lines.append("### 其他最新 issues（最多3条）")
for i in other:
    num = i.get("number", "?")
    title = i.get("title", "N/A")
    created = i.get("created_at", "N/A")
    lines.append(f"#{num} | {title} | created_at:{created}")
if not other:
    lines.append("无")
lines.append("")

out_path = "/tmp/openclaw_observer_digest.md"
with open(out_path, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print(out_path)
