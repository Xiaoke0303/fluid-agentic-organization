# scripts/ — 辅助工具目录

> 辅助脚本，**不代表默认运行路径**，**不会自动执行**。

---

## 目录说明

`scripts/` 下的脚本为**人工触发的辅助工具**，不是周期任务，不是默认加载技能，不自动运行。

---

## 当前脚本

| 文件 | 用途 | 依赖关系 | 执行方式 |
|------|------|---------|---------|
| `diagram.sh` | 技术图解生成器包装脚本 | 调用 `tech_diagram.py` | 人工执行：`bash scripts/diagram.sh <type> -o <output>` |
| `tech_diagram.py` | 技术图解生成器主体 | 被 `diagram.sh` 调用；依赖 diagrams、graphviz | 人工执行或通过 `diagram.sh` 调用 |
| `github_fao_patrol_stage1.py` | GitHub FAO 巡检数据获取脚本 | 独立运行 | 人工执行，**不代表已恢复周期巡检** |
| `openclaw_observer_stage1.py` | OpenClaw issue 观察脚本 | 独立运行 | 人工执行，**不代表已恢复周期巡检** |

---

## 重要声明

1. **非默认运行路径**：这些脚本不会被自动加载或执行。
2. **不自动执行**：不等于已启用 cron/task，不等于已配置周期巡检。
3. `github_fao_patrol_stage1.py` 和 `openclaw_observer_stage1.py` 是**历史/阶段性巡检脚本**，不代表当前已恢复周期巡检。
4. **执行前需人工确认**：任何脚本运行前必须由操作者确认目标和参数。
5. **禁止从 scripts/ 自动加载任务**：不得将脚本内容自动注入 agent 上下文或自动调用。

---

## 文档引用

- `diagram.sh` / `tech_diagram.py`：被 `docs/tech-diagram-guide.md` 引用
- `github_fao_patrol_stage1.py` / `openclaw_observer_stage1.py`：被 `framework/mapping/MIGRATION-PLAN.md` 引用

---

*辅助工具。不自动激活。*
