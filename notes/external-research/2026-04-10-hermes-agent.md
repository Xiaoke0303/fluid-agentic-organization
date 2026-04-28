---
source: file
verified: true
confidence: medium
timestamp: 2026-04-17
access_count: 1
last_accessed: 2026-04-17T01:04:18.032451
---

# Hermes Agent 观察：自改进循环与程序性记忆的工程实现

**来源**：NousResearch/hermes-agent  
** stars**：43.3k+ (截至 2026-04-09)  
**关键文档**：
- [GitHub README](https://github.com/NousResearch/hermes-agent)
- [Persistent Memory 文档](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory)
- [Skills System 文档](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills)

---

## 一、核心架构速览

Hermes Agent 于 2026 年 2 月由 NousResearch 开源，定位是 "The self-improving AI agent"——强调**内置学习闭环（built-in learning loop）**。其设计可直接映射到 FAO 关注的 memory、identity、runtime stability 三个维度。

### 1. 记忆双文件结构

与 FAO 当前实践高度一致：

| 文件 | 用途 | 硬上限 |
|------|------|--------|
| `MEMORY.md` | Agent 个人笔记（环境、约定、教训） | 2,200 chars (~800 tokens) |
| `USER.md` | 用户画像（偏好、沟通风格、期望） | 1,375 chars (~500 tokens) |

- 注入方式：**frozen snapshot**（会话启动时一次性注入 system prompt，之后不再变更，以保留 prefix cache）
- 管理工具：`memory(action="add/replace/remove")`，无 read 动作，因为 agent 已在 context 中"看到"
- 安全扫描：注入前会检测 prompt injection、凭证外泄、隐形 Unicode 等威胁模式

### 2. 程序性记忆 = Skills

Hermes 将 skills 定义为 **"on-demand knowledge documents"**，并进一步升级为 **procedural memory**：

- **Agent 自主创建 skill**：在完成复杂任务（5+ tool calls）、 corrected by user、或发现非平凡工作流后，自动调用 `skill_manage(action="create")`
- **Skills 自我改进**：使用中被 patch/rewrite
- **开放标准**：兼容 [agentskills.io](https://agentskills.io/specification)
- **Hub 生态**：集成 OpenAI skills、Anthropics skills、Vercel skills.sh、ClawHub、LobeHub 等

### 3. 二级记忆：Session Search

所有 CLI 和消息会话存入 SQLite (`~/.hermes/state.db`)，使用 FTS5 全文索引：
- 需要时调用 `session_search`
- 结果经 Gemini Flash 摘要后返回
- **定位**：用于 "did we discuss X last week?"，而非高频实时调用

### 4. 外部记忆提供者（Pluggable Memory）

内置 8 个外部 memory provider 插件：Honcho、OpenViking、Mem0、Hindsight、Holographic、RetainDB、ByteRover、Supermemory。
- **与内置记忆并行运行**，永不替代
- Honcho 主打 **dialectic user modeling**（辩证用户建模）

### 5. 与 OpenClaw 的关系

Hermes 提供 `hermes claw migrate` 命令，直接承接 OpenClaw 用户迁移。这意味着：
- **生态竞争已实质化**：Hermes 在争夺同一批"自托管 AI agent"用户
- **技术路径趋同**：两者都选择 Markdown 文件注入、skills 机制、多平台 gateway、cron 调度

---

## 二、对 FAO 的影响与启发

### 1. 设计趋同的验证

Hermes 的 `MEMORY.md + USER.md` frozen snapshot 模式，与 FAO 当前的记忆主入口设计几乎一致。这是**独立的工程验证**：将记忆文件化、并作为 system prompt 的固定前缀，是低成本且有效的跨会话记忆方案。

**FAO 启示**：该方向无需否定，但需明确与 Hermes 的差异点——FAO 更强调"记忆不是能力仓库，而是责任锚定点"。

### 2. 程序性记忆的边界张力

Hermes 的 agent 可**自主创建 skill**，这是 procedural memory 的自动化版本。对 FAO 提出关键问题：

> 当智能体自主生成新能力（skill）时，能力的"所有权"归谁？如果 skill 出错，责任是否能追溯到生成它的那次会话？

FAO 的核心立场是"能力可以下放，责任不能消失"。Hermes 的自主学习循环如果缺少**责任签名机制**（如：每个 auto-created skill 绑定生成会话 ID、生成时间、生成原因），就会在 long tail 中积累"无主之错"。

**FAO 启示**：若 FAO 未来引入自动 skill 创建，必须配套 **"skill 来源锚定"** 与 **"能力-责任双向链路"**。

### 3. 记忆硬上限的启示

Hermes 对记忆有严格字符上限（总计约 1,300 tokens）。其理由是：保持 system prompt 边界可控，避免性能衰减。

FAO 当前的记忆文件没有同等硬约束。随着孵化笔记、外部观察、共识文件的累积，system prompt 的 memory block 会自然膨胀。

**FAO 启示**：需要评估是否引入**软容量管理规则**。例如：
- P0 核心共识永久保留
- 时间衰减规则（observation 卡片在 60/90 天后降级或归档）
- 记忆文件的主动压缩/合并机制

### 4. Session Search 作为记忆的 fallback

FAO 目前主要依赖 memory 文件和 changelog，没有系统性的"历史会话全文检索"层。Hermes 的 SQLite + FTS5 + LLM 摘要提供了一个低成本的补充方案。

**FAO 启示**：可以考虑将会话摘要（或关键决策点）写入可搜索的二级存储，而不仅依赖手工维护的 memory 文件。这对"渐进式真相收敛"有帮助。

### 5. 生态竞争信号

Hermes 直接支持 `claw migrate`，且集成 ClawHub。说明 NousResearch 将 OpenClaw 生态视为存量市场。

FAO 的理论差异化在于：
- Hermes 强调 "self-improving agent"（能力自生）
- FAO 强调 "routing and responsibility anchoring"（路由与责任锚定）

随着技术实现层面的趋同，**理论叙事将成为核心护城河**。FAO 需要加速将 "route, not layer" 的框架从白皮书转化为可操作的 runtime 约束（如 AGENTS.md 中的最小嫁接条款）。

### 6. Honcho 的 dialectic user modeling

Honcho 作为外部 memory provider，引入"辩证用户建模"——不是静态标签，而是通过对立问题的交互来刻画用户。这与 FAO 的"异质主体"视角有潜在对话空间：
- FAO 认为人类主体是"带宽窄、计算慢、承担最终责任"
- Honcho 式的建模如果过度"预测"人类偏好，可能滑向**隐性代理决策**（即 agent 替用户做了"用户会想要什么"的假设）

**FAO 启示**：任何用户画像系统都必须设置"不可流动的边界"——agent 可以记录偏好，但不能以画像为由替用户承担对外后果。

---

## 三、建议行动

1. **将 Hermes 纳入定期外部观察扫描**：每月检查其 release notes（尤其是 `RELEASE_v0.x.0.md`），关注 memory provider 和 skill auto-creation 的演进。
2. **在 FAO 内部讨论"技能生成的责任锚定"**：如果未来 OpenClaw 或 FAO 引入 auto-skill-creation，提前设计签名与回滚机制。
3. **评估记忆容量管理**：是否给 observation 卡片设置时效性？是否引入 session-level search fallback？
4. **强化理论差异化传播**：技术同质化不可避免，需持续将 FAO 的"路由 vs 层级""位责不僭"等概念固化为工程约束（如 AGENTS.md 中的真实性约束、任务准入检查），而不仅是白皮书文字。

---

*记录时间：2026-04-10*  
*记录者：外部观察节点*  
*状态：待进一步跟踪*
