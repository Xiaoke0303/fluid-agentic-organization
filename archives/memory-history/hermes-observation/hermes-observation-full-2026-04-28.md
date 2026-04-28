## 2026-04-19 Hermes Agent 观察

### 扫描来源
- NousResearch/hermes-agent issues (open, per_page=10)
- NousResearch/hermes-agent releases (per_page=3)

### 值得关注的进展（最多3条）
- #12436 | feat(orchestration): DAG TaskGraph + delegate bridge + A2A bus + reflex hints | https://github.com/NousResearch/hermes-agent/pull/12436
  - 摘要：Hermes 引入 DAG TaskGraph 编排、委托桥、A2A 总线和反射提示，重构 agent 协同架构。
  - 值得理由：这是 Hermes 向"agentic orchestration"迈出的关键一步，与 FAO 框架的异质主体协同理念形成可对比的实现路径。
  - FAO 关联（如有）：FAO 强调异质主体间的路由与代理，Hermes 的 DAG + A2A bus 提供了一个具体的工程参照——可作为 FAO 理论落地的对照样本。

- #12446 | fix(session_search): avoid dense-match CPU spin | https://github.com/NousResearch/hermes-agent/pull/12446
  - 摘要：修复 session_search 中的密集匹配导致 CPU 空转问题。
  - 值得理由：上周刚记录 session 泄漏问题，本周即见 session_search 的性能修复，显示 Hermes 正在集中治理 session 子系统的稳定性。
  - FAO 关联（如有）：延续上周的 session 生命周期关注，可追踪 Hermes 的 session 治理进展，为 FAO 的 Failure/Correction 分离设计提供实证。

- #12440 | [BUG] Sub-agent model configuration is ignored, causing persistent context window errors | https://github.com/NousResearch/hermes-agent/issues/12440
  - 摘要：子代理模型配置被忽略，导致上下文窗口错误持续发生。
  - 值得理由：子代理配置失效直接影响多 agent 系统的可靠性，是 agentic 架构中的关键基础设施问题。
  - FAO 关联（如有）：与 FAO 的 Role-Contract 设计相关——若主体间契约无法正确传递配置，则异质主体协同将出现系统性失效。

### 是否计划深入
- [ ] 无 / [x] 建议记录到 FAO 笔记（DAG orchestration 模式值得对比）

### 备注
本周命中 3 条，涵盖 orchestration 新特性、session 稳定性修复、agent 配置失效三类问题。与上周单一 session 泄漏问题相比，本周呈现更广泛的 agentic 架构治理图景。releases 无新命中。

---

## 2026-04-20 Hermes Agent 观察

### 扫描来源
- NousResearch/hermes-agent issues (open, per_page=10)
- NousResearch/hermes-agent releases (per_page=3)

### 值得关注的进展（最多3条）
- #12883 | [Memory System] No importance-scoring mechanism — what should be remembered vs. forgotten? | https://github.com/NousResearch/hermes-agent/issues/12883
  - 摘要：Hermes 的 Memory System 缺少重要性评分机制，无法区分什么该记住、什么该遗忘。
  - 值得理由：记忆系统的"选择性保留"是 agent 长期运行的核心难题，直接关乎 identity 的连续性。
  - FAO 关联（如有）：FAO 将 Memory 与 Judgment 分离设计，但 Hermes 的实践表明"什么值得记住"仍是未解决的通用问题——可作为 FAO Memory 接口设计的反向验证。

- #12877 | [Skills System] Serious systemic defects in the skills system: no pruning, island isolation, and missing conflict detection | https://github.com/NousResearch/hermes-agent/issues/12877
  - 摘要：Skills 系统存在严重缺陷：无修剪机制、技能岛隔离、缺少冲突检测。
  - 值得理由：技能膨胀与冲突是任何可扩展 agent 框架的必遇瓶颈，Hermes 将其暴露为系统性问题而非边缘 bug。
  - FAO 关联（如有）：与 FAO 的 Role-Contract 和 Judgment-Card 设计形成对照——FAO 通过角色契约限定技能边界，而 Hermes 的"技能岛"问题说明无边界约束的技能增长必然失控。

- #12885 | [Feature Request] Add video content learning — ingest, transcribe, and learn from video content | https://github.com/NousResearch/hermes-agent/issues/12885
  - 摘要：请求增加视频内容学习功能，支持摄入、转录并从视频内容中学习。
  - 值得理由：扩展 agent 感知输入维度（从文本到视频）意味着 learning-loop 的数据来源质变，可能影响记忆与技能系统的负载。
  - FAO 关联（如有）：FAO 的异质主体框架中，信息输入维度扩展会直接影响 Memory 的存储策略和 Judgment 的处理负荷——可作为 FAO 信息论维度的延伸思考。

### 是否计划深入
- [ ] 无 / [x] 建议记录到 FAO 笔记（Memory importance-scoring 与 Skills 系统性缺陷均值得对比）

### 备注
本周命中 3 条，从上周的 session/orchestration 基础设施问题转向 memory/skills/learning-loop 认知层问题。releases 无新命中（v2026.4.16 为常规版本迭代）。

---

## 2026-04-21 Hermes Agent 观察

### 扫描来源
- NousResearch/hermes-agent issues (open, per_page=10)
- NousResearch/hermes-agent releases (per_page=3)

### 值得关注的进展（最多3条）
- #13373 | feat: add context-engine runtime identity diagnostics | https://github.com/NousResearch/hermes-agent/pull/13373
  - 摘要：为 context engine 添加运行时身份诊断能力，暴露配置引擎、活跃引擎、会话绑定关系及漂移警告。
  - 值得理由：首次将「运行时身份」作为可观测对象，使 engine/session/plugin 之间的对齐状态可见，直接回应了 agent 长期运行中的身份漂移盲区。
  - FAO 关联（如有）：与 FAO 的 Identity/Role 分离设计高度呼应——Hermes 用诊断接口暴露 runtime identity 状态，FAO 则用契约约束其边界，两者互补。

- #13383 | [Bug]: MCP server session expires during long-running gateway — no auto-reconnect | https://github.com/NousResearch/hermes-agent/issues/13383
  - 摘要：长时间运行的 gateway 中 MCP 会话过期后无法自动重连，导致工具调用持续失败，唯一恢复方式是重启 gateway。
  - 值得理由：长运行稳定性是 agent 基础设施的底线问题，session 过期无自愈路径会中断所有已连接平台，影响生产可用性。
  - FAO 关联（如有）：与 FAO 的 Failure/Correction 分离设计相关——MCP session 失效属于 Failure 检测范畴，而「tear down + re-initialize + retry」正是 Correction 的最小闭环。

- #13384 | feat(skills): expose absolute skill dir and ${HERMES_SKILL_DIR} templates in SKILL.md | https://github.com/NousResearch/hermes-agent/pull/13384
  - 摘要：Skill 激活消息现在暴露绝对路径并支持 `${HERMES_SKILL_DIR}` 模板变量替换，agent 无需额外推理路径即可直接调用捆绑脚本。
  - 值得理由：上周刚记录 Skills 系统性缺陷（无修剪、岛隔离、缺冲突检测），本周即见技能路径与模板化改进，显示 Hermes 正在从「技能发现」层着手修复。
  - FAO 关联（如有）：与 FAO 的 Role-Contract 设计形成对照——FAO 通过角色契约限定技能边界，Hermes 则通过路径暴露降低技能调用摩擦，两者从不同方向解决「技能如何被正确调用」问题。

### 是否计划深入
- [ ] 无 / [x] 建议记录到 FAO 笔记（runtime identity 诊断模式可作为 FAO Identity 接口的参照实现）

### 备注
本周命中 3 条，涵盖 runtime identity 诊断、长运行 session 稳定性、skill 系统改进。与上周的 memory/skills/learning-loop 认知层问题相比，本周重新聚焦 runtime 基础设施与 identity 可观测性。releases 无新命中（v2026.4.16 为常规版本迭代）。

---

## 2026-04-24 Hermes Agent 观察

### 扫描来源
- NousResearch/hermes-agent issues (open, per_page=10)
- NousResearch/hermes-agent releases (per_page=3)

### 值得关注的进展（最多3条）
- #14957 | fix: stabilization fixes and architectural enhancements | https://github.com/NousResearch/hermes-agent/pull/14957
  - 摘要：针对多个子系统（agent/cli/gateway/cron）的稳定性修复与架构增强。
  - 值得理由：在大量 provider/平台适配涌入的背景下，集中处理 stability 是避免技术债堆积的关键动作，直接影响生产可用性。
  - FAO 关联（如有）：与 FAO 的 Failure/Correction 分离设计呼应——stabilization 属于 Failure 检测与遏制，architectural enhancements 则属于 Correction 的结构化改进。

### 是否计划深入
- [ ] 无 / [ ] 建议记录到 FAO 笔记（未执行）

### 备注
本周命中 1 条（stability）。其余 9 个 open issues 及 3 个 releases 无匹配。与昨日相比，今日 open issues 列表以 Google Chat 适配、图像生成、provider 注册等特性/修复为主，FAO 核心关注领域（memory/session/identity/skills/bootstrap/injection）无新增条目。

### 扫描来源
- NousResearch/hermes-agent issues (open, per_page=10)
- NousResearch/hermes-agent releases (per_page=3)

### 值得关注的进展（最多3条）
- #13904 | feat(skills): add ecommerce-data-analysis to optional skills | https://github.com/NousResearch/hermes-agent/pull/13904
  - 摘要：新增电商数据分析可选技能，支持通过 EcCompass AI 搜索分析超过 1000 万电商店铺数据。
  - 值得理由：延续上周技能系统改进趋势，显示 Hermes 正在扩展技能生态而非仅修复缺陷。
  - FAO 关联（如有）：与 FAO Role-Contract 设计形成持续对照——技能增加的速度超过边界治理能力时，膨胀问题会重演。

- #13905 | Context compressor summary fallback retry passes wrong arguments | https://github.com/NousResearch/hermes-agent/issues/13905
  - 摘要：上下文压缩器的 summary model 回退重试路径传递错误参数，导致 focus_topic 丢失甚至 NameError。
  - 值得理由：上下文压缩直接决定 agent 的会话记忆窗口质量，回退路径的 bug 意味着记忆系统在故障时反而降级。
  - FAO 关联（如有）：与 FAO Memory/Judgment 分离设计相关——记忆子系统的故障回退机制必须被显式设计，而非依赖隐式行为。

- #13898 | fix: correct delegation tool trace error detection | https://github.com/NousResearch/hermes-agent/pull/13898
  - 摘要：修复委托工具将成功的终端 JSON 载荷（如 `{"error": null, "exit_code": 0}`）误判为错误的缺陷。
  - 值得理由：子代理委托的错误分类是 agentic 系统的关键可观测性，误报会直接破坏对异质主体协同状态的判断。
  - FAO 关联（如有）：与 FAO Failure/Correction 分离设计呼应——正确识别「什么算失败」是启动修正流程的前提。

### 是否计划深入
- [ ] 无 / [x] 建议记录到 FAO 笔记（上下文压缩故障回退机制可作为 Memory 接口的反面教材）

### 备注
本周命中 3 条，涵盖 skills 扩展、session memory 压缩稳定性、agentic delegation 可观测性。与上周的 runtime identity 诊断和 session 长运行稳定性相比，本周聚焦更细粒度的子系统故障。releases 无新命中（v2026.4.16 已在上次扫描中记录）。

## 2026-04-23 Hermes Agent 观察

### 扫描来源
- NousResearch/hermes-agent issues (open, per_page=10)
- NousResearch/hermes-agent releases (per_page=3)

### 值得关注的进展（最多3条）
- #14432 | feat(skills): support eager prompt injection | https://github.com/NousResearch/hermes-agent/pull/14432
  - 摘要：在技能系统层支持「主动式提示注入」，将 prompt injection 从漏洞模式转变为可控特性。
  - 值得理由：把 injection 从被动防御转为主动能力，是 agentic 框架中对「注入」概念的范式级重新定义。
  - FAO 关联（如有）：FAO 关注 injection 作为系统外部输入边界，Hermes 的 eager injection 设计提供了一个反向参照——若 injection 被显性化为一等公民，则防御逻辑需前置到 skill 注册层而非运行时过滤层。

### 是否计划深入
- [ ] 无 / [x] 建议记录到 FAO 笔记（eager prompt injection 模式可作为 FAO injection 接口设计的反向参照）

### 备注
本周命中 1 条（skills + injection），其余 9 个 open issues 无匹配。releases 无新命中（v2026.4.16 已在历次扫描中记录）。与上周相比，本周 open issues 列表呈现大量 RouterMint/ACP/copilot 相关的热修复。

---

## 2026-04-24 Hermes Agent 观察

### 扫描来源
- NousResearch/hermes-agent issues (open, per_page=10)
- NousResearch/hermes-agent releases (per_page=3)

### 值得关注的进展（最多3条）
- #14957 | fix: stabilization fixes and architectural enhancements | https://github.com/NousResearch/hermes-agent/pull/14957
  - 摘要：针对多个子系统（agent/cli/gateway/cron）的稳定性修复与架构增强。
  - 值得理由：在大量 provider/平台适配涌入的背景下，集中处理 stability 是避免技术债堆积的关键动作，直接影响生产可用性。
  - FAO 关联（如有）：与 FAO 的 Failure/Correction 分离设计呼应——stabilization 属于 Failure 检测与遏制，architectural enhancements 则属于 Correction 的结构化改进。

### 是否计划深入
- [ ] 无 / [ ] 建议记录到 FAO 笔记（未执行）

### 备注
本周命中 1 条（stability）。其余 9 个 open issues 及 3 个 releases 无匹配。与昨日相比，今日 open issues 列表以 Google Chat 适配、图像生成、provider 注册等特性/修复为主，FAO 核心关注领域（memory/session/identity/skills/bootstrap/injection）无新增条目。

---

## 2026-04-25 Hermes Agent 观察

### 扫描来源
- NousResearch/hermes-agent issues (open, per_page=10)
- NousResearch/hermes-agent releases (per_page=3)

### 值得关注的进展（最多3条）
- #15538 | [Feishu] Session titles in /sessions and /resume expose private conversation content | https://github.com/NousResearch/hermes-agent/issues/15538
  - 摘要：飞书平台的 /sessions 和 /resume 命令泄露会话标题中的私人对话内容。
  - 值得理由：Session 元数据未做隐私隔离即暴露于平台接口，是 session 边界治理的敏感缺口。
  - FAO 关联（如有）：与 FAO Identity/Session 边界设计相关——会话标题携带的身份上下文若未隔离，则异质主体间的信息边界即被穿透。

- #15539 | fix: prevent concurrent gateway updates from clobbering shared IPC state | https://github.com/NousResearch/hermes-agent/pull/15539
  - 摘要：阻止并发 gateway 更新破坏共享 IPC 状态，避免多路写入导致的状态覆盖。
  - 值得理由：共享 IPC 状态在并发更新下被覆盖是典型的运行时稳定性漏洞，直接影响多会话/多代理共存可靠性。
  - FAO 关联（如有）：与 FAO Failure/Correction 分离设计呼应——并发写入冲突属于 Failure 范畴，修复动作则是 Correction 的最小闭环示例。

- #15535 | fix(gateway): invalidate agent cache on session changes | https://github.com/NousResearch/hermes-agent/pull/15535
  - 摘要：当 session 发生变更时，使 agent cache 失效，防止旧会话状态污染新上下文。
  - 值得理由：Agent cache 未随 session 生命周期同步失效会导致记忆/状态残留，是 session 治理的常见隐蔽缺陷。
  - FAO 关联（如有）：与 FAO Memory/Session 分离设计相关——记忆载体必须绑定会话生命周期，否则将产生跨会话的状态漂移。

### 是否计划深入
- [ ] 无 / [ ] 建议记录到 FAO 笔记（未执行）

### 备注
本周命中 3 条，全部围绕 session + gateway stability。与上周的 general stabilization (#14957) 相比，本周聚焦更具体的 session 隐私边界、并发 IPC 状态、agent cache 生命周期三类问题，显示 Hermes 的稳定性治理正从 broad fixes 转向 session 子系统的精细修复。releases 无新命中（v2026.4.23 为常规版本迭代）。

---

## 2026-04-26 Hermes Agent 观察

### 扫描来源
- NousResearch/hermes-agent issues (open, per_page=10)
- NousResearch/hermes-agent releases (per_page=3)

### 值得关注的进展（最多3条）
- #15941 | fix(gateway): avoid cross-user mirror writes in per-user group sessions | https://github.com/NousResearch/hermes-agent/pull/15941
  - 摘要：修复群聊中按用户隔离的会话镜像路由，防止 `send_message` 输出写入错误参与者的会话。
  - 值得理由：跨用户会话污染直接影响多用户场景下的身份边界，是 session 治理的隐蔽缺陷。
  - FAO 关联（如有）：与 FAO Identity/Session 边界设计呼应——当会话路由仅依赖 platform+chat_id 而不区分用户时，异质主体间的信息隔离即被穿透。

- #15933 | bug(delegation): heartbeat stale detector kills healthy child agents on slow LLM providers | https://github.com/NousResearch/hermes-agent/issues/15933
  - 摘要：心跳过期检测阈值（150s）对慢速 LLM 提供商过于激进，导致健康的子代理被误判为僵死并终止。
  - 值得理由：子代理（delegation）是 agentic 架构的关键扩展机制，heartbeat 误杀直接破坏多主体协同的可靠性。
  - FAO 关联（如有）：与 FAO Failure/Correction 分离设计相关——heartbeat 阈值属于 Failure 检测参数，但错误参数会触发不必要的 Correction（终止），需显式校准以避免误判。

- #15940 | hermes-agent: Scrub provider creds from ACP child env | https://github.com/NousResearch/hermes-agent/pull/15940
  - 摘要：在生成 ACP 子进程前剥离 Hermes 托管的提供商凭证，防止父进程环境变量泄露给外部子进程。
  - 值得理由：ACP 子进程继承父进程完整环境会导致密钥泄露，是 agentic 框架中进程边界安全的 P1 级漏洞。
  - FAO 关联（如有）：与 FAO Runtime 安全边界设计相关——异质主体间的进程隔离必须包含凭证隔离，否则协同即引入攻击面。

### 是否计划深入
- [ ] 无 / [ ] 建议记录到 FAO 笔记（未执行）

### 备注
本周命中 3 条，延续上周 session + gateway 主题，但新增 delegation 心跳误判和 ACP 进程安全两个维度。与 04-25 的 session 隐私/IPC 并发/agent cache 相比，今日 issue 更聚焦于「主体间边界」——会话路由边界（#15941）、子进程凭证边界（#15940）、子代理生命边界（#15933）。releases 无新命中（v2026.4.23 已在历次扫描中记录）。
## 2026-04-27 Hermes Agent 观察

### 扫描来源
- NousResearch/hermes-agent issues (open, per_page=10)
- NousResearch/hermes-agent releases (per_page=3)

### 值得关注的进展（最多3条）
- #16415 | fix(memory): cache provider instance in load_memory_provider() | https://github.com/NousResearch/hermes-agent/pull/16415
  - 摘要：为 load_memory_provider() 添加 provider 实例缓存，避免每条 gateway 消息重建 AIAgent 时重复初始化 memory provider。
  - 值得理由：MemPalace 等 provider 的 initialize() 每次耗时 1-4 秒，缓存后显著降低每消息延迟，是 memory 子系统的关键性能修复。
  - FAO 关联（如有）：与 FAO Memory/Judgment 分离设计呼应——memory provider 的初始化成本若不加约束，会直接将 memory 层的开销转嫁到每次交互，缓存策略是 Memory 接口实现的必要考量。

- #16419 | feat(dashboard): add profiles management page | https://github.com/NousResearch/hermes-agent/pull/16419
  - 摘要：Dashboard 新增 profile 管理页面，支持 profile 生命周期 REST 接口及 SOUL.md 读写。
  - 值得理由：首次为 identity/profile 系统提供图形化管理入口，使 SOUL.md 驱动的 agent 身份配置从文件层提升至 UI 层。
  - FAO 关联（如有）：与 FAO Identity/Role 分离设计相关——Hermes 将 profile 视为 dashboard 一级对象，FAO 则将 Identity 与 Role 拆分为独立接口，两者在「身份如何被管理」上提供了不同抽象层级的参照。

- #16424 | feat(plugins): allow pre_tool_call hooks to block tool execution | https://github.com/NousResearch/hermes-agent/pull/16424
  - 摘要：pre_tool_call 插件钩子现在可返回 block 字典以阻断工具执行，使安全/策略插件能在 dispatch 层拦截而非仅事后观察。
  - 值得理由：将插件从「只能看」升级为「可以拦」，是 runtime 安全治理的关键能力缺口补齐，直接影响生产环境中的策略执行可信度。
  - FAO 关联（如有）：与 FAO Runtime 边界设计相关——Hermes 在工具调用分发点引入可阻断的 hook，FAO 则在 META-ACTIONS 中区分「执行」与「约束」，两者的 runtime 治理思路互补。

### 是否计划深入
- [ ] 无 / [ ] 建议记录到 FAO 笔记（未执行）

### 备注
本周命中 3 条，聚焦 memory 性能、identity UI 化、plugin runtime 拦截三个方向。与上周的 session 路由边界 + delegation 心跳 + ACP 安全相比，本周从「主体间边界」转向「主体内部子系统治理」。releases 无新命中（v2026.4.23 为常规版本迭代）。

---

## 2026-04-28 Hermes Agent 观察

### 扫描来源
- NousResearch/hermes-agent issues (open, per_page=10)
- NousResearch/hermes-agent releases (per_page=3)

### 值得关注的进展（最多3条）
- #16866 | fix(state): index tool_calls and tool_name in FTS5 for session_search | https://github.com/NousResearch/hermes-agent/pull/16866
  - 摘要：为 session_search 的 FTS5 全文检索补充 tool_calls 与 tool_name 字段索引，使工具调用历史可被搜索。
  - 值得理由：session 子系统的可搜索性是 agent 长期运行的记忆回溯基础，缺失工具调用索引会直接削弱「会话记忆」的完整性。
  - FAO 关联（如有）：与 FAO Memory/Session 边界相关——若工具调用作为主体间交互记录无法被检索，则 Memory 接口的信息回溯能力将存在结构性缺口。

- #16867 | fix: honor agent.disabled_toolsets in gateway sessions | https://github.com/NousResearch/hermes-agent/pull/16867
  - 摘要：修复 gateway 会话中 agent.disabled_toolsets 配置未被尊重的缺陷，使按会话禁用工具集的约束生效。
  - 值得理由：工具集按会话粒度的启停控制是 runtime 安全与策略执行的基础能力，配置失效意味着安全边界可被绕过。
  - FAO 关联（如有）：与 FAO Role-Contract 设计呼应——角色契约中隐含的能力边界若无法被 runtime 强制执行，则契约本身失去约束效力。

- #16863 | Fix gateway restart handling and config validation | https://github.com/NousResearch/hermes-agent/pull/16863
  - 摘要：修复 gateway 重启时的处理逻辑与配置验证问题，避免重启路径中的状态不一致或配置错误被静默忽略。
  - 值得理由：gateway 是 Hermes 的 runtime 核心枢纽，重启处理与配置验证的缺陷直接影响服务可用性和状态恢复可靠性。
  - FAO 关联（如有）：与 FAO Failure/Correction 分离设计相关——重启是系统级 Correction 动作，若重启路径本身不可靠，则 Failure 后的恢复闭环即被打破。

### 是否计划深入
- [ ] 无 / [ ] 建议记录到 FAO 笔记（未执行）

### 备注
本周命中 3 条，全部围绕 session + gateway runtime 基础设施。与上周的 memory provider 缓存 (#16415)、identity profile UI (#16419)、plugin 拦截 hook (#16424) 相比，本周从「主体内部子系统治理」重新聚焦于「会话层与运行时核心」的稳定性修复。releases 无新命中（v2026.4.23 为常规版本迭代，无 memory/session/identity 等关键词）。

