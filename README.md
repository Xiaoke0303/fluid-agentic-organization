# FAO (Fluid Agentic Organization)

**任务可以流动，但责任未必能流动。**

FAO（Fluid Agentic Organization，流态代理组织）关注人类主体与智能体主体共存时，任务如何在不同主体之间流转，以及这种流转对责任边界、真实性与治理结构提出的要求。

FAO 不是又一个 agent 编排框架、业务自动化方案或某个 runtime 的配置模板。它不追求让 agent 跑得更快，而是追问：当任务流动时，责任如何保持可追溯，真实性如何保持可验证，边界如何不被模糊的"协作"掩盖。

## 当前阶段说明

白皮书（`whitepaper/FAO-Whitepaper.md`）承载组织分析主线。framework v1 承载通用工作节点最小骨架。mapping 承载框架在真实 runtime 中的验证记录。三者并行，成熟度不同。

`framework/` 是通用工作节点框架，与白皮书并行，不是白皮书的附属实现。

`notes/cost-line.md` 与 `notes/memory-line.md` 是 sidecar working notes，不是 framework 本体，对外正式口径以白皮书正文为准。

---

## 当前结构

| 目录 | 说明 |
|------|------|
| **[framework/](framework/)** | 通用工作节点框架。当前新的上位骨架候选，包含框架定义、元动作、OpenClaw 映射、角色、真实性、运行规则、前置检查、薄记忆、纠错协议、迁移计划等核心文件。 |
| **[toolkit/](toolkit/)** | 旧分组仍保留。[minimal-core/](toolkit/minimal-core/) 与 [governance/](toolkit/governance/) 当前作为 legacy grouping / implementation source，后续按迁移计划逐步映射。 |
| **[domains/](domains/)** | 领域包占位。预留 framework 向具体专业域的扩展接口，当前无已展开的活跃领域包。 |

---

## framework 骨架

`framework/` 是通用工作节点框架。以下为核心文件索引：

- [core/UNIVERSAL-WORK-NODE-FRAMEWORK.md](framework/core/UNIVERSAL-WORK-NODE-FRAMEWORK.md) — 框架总定义，六个功能模块说明
- [core/META-ACTIONS.md](framework/core/META-ACTIONS.md) — 14 个元动作表，骨架的元操作层
- [mapping/OPENCLAW-MAPPING.md](framework/mapping/OPENCLAW-MAPPING.md) — 与 OpenClaw 默认 bootstrap 规则的映射文档
- [assurance/TRUTH-CONTRACT.md](framework/assurance/TRUTH-CONTRACT.md) — 真实性合同
- [runtime/OPERATING-RULES.md](framework/runtime/OPERATING-RULES.md) — 运行母规则
- [runtime/CONTEXT-BUDGET.md](framework/runtime/CONTEXT-BUDGET.md) — 运行时成本量化接口
- [continuity/MEMORY-INDEX.md](framework/continuity/MEMORY-INDEX.md) — 长期连续性薄索引
- [continuity/CORRECTION-WRITEBACK.md](framework/continuity/CORRECTION-WRITEBACK.md) — 纠错写回协议

其余文件在此骨架下展开：角色契约、前置检查序列、判断卡片接口、迁移计划等。

---

## toolkit 退位说明

[toolkit/minimal-core/](toolkit/minimal-core/) 与 [toolkit/governance/](toolkit/governance/) 继续保留，主要作为：

- 旧分组的历史记录
- 实现来源与参考
- 迁移计划的映射来源

当前不直接删除，不宣布作废。后续以 [framework/mapping/MIGRATION-PLAN.md](framework/mapping/MIGRATION-PLAN.md) 为准，逐步完成内容级映射。

---

## 主线笔记入口

以下 working notes 作为 sidecar 保留，不替代白皮书主文，也不直接构成 framework 的一部分。

- `notes/cost-line.md` —— 成本主线：人力成本、token 成本、组织成本结构、算法套利与生态位
- `notes/memory-line.md` —— 记忆主线：薄记忆、纠错写回、判断卡、长期连续性与跨节点沉淀

---

## 阅读入口

本项目当前有三个并行入口：

- `whitepaper/` —— 组织分析层
- `framework/` —— 通用工作节点框架
- `framework/mapping/verification/` —— 映射与实例验证层

读者可按需求进入对应入口，无需强制单一路径。

### 组织分析层

面向 FAO 的组织分析与核心论述。

- `whitepaper/FAO-Whitepaper.md` —— FAO 组织分析主文
- `whitepaper/README.md` —— 白皮书目录与章节入口

### 通用工作节点框架

面向通用工作节点的框架定义、元动作与运行规则。与白皮书并行，不是白皮书的附属实现。

- `framework/core/UNIVERSAL-WORK-NODE-FRAMEWORK.md` —— 框架总定义
- `framework/README.md` —— 框架目录与全部文件索引

### 映射与实例验证层

面向框架在真实运行时中的映射衔接与验证记录。当前已启动，尚处早期。

- `framework/mapping/verification/` —— 实例验证记录（第一条 OpenClaw 样本已落盘）
- `framework/mapping/MIGRATION-PLAN.md` —— framework 迁移计划与阶段定义
- `framework/mapping/OPENCLAW-MAPPING.md` —— OpenClaw 映射文档

### 参考目录

以下目录不作为当前主入口，仅供参考。

- `toolkit/` —— 早期实验与 legacy 分组，历史记录与实现来源
- `whitepaper/cases/` —— 白皮书配套案例与观察材料，随白皮书正文阅读
- `notes/` —— sidecar working notes，见上方「主线笔记入口」节

---

## 当前状态

- **白皮书**：组织分析主线与核心论证基本成型，细节、案例、量化与成本约束仍在补充
- **framework v1**：通用工作节点最小骨架已完成，mapping verification、增强层协议与跨 runtime 验证仍在早期
- **mapping**：已启动，第一条 OpenClaw 实例已落盘，尚处早期验证阶段
- **当前重点**：入口对齐、mapping 验证推进、白皮书细节补充
- **参与方式**：提修正 / 补案例 / 指出不清楚之处

---

## 实践来源

FAO 的部分判断与框架文件，来自一个持续进行的人类主体与智能体节点协作过程。当前 `mapping/verification/` 中的部分记录，是从真实讨论、纠错与写回中沉淀下来的。

这不表示 FAO 已被证明，也不表示当前协作节点是其唯一实现或指定 runtime。它只说明：framework 中关于责任边界、路由、真实性与记忆的判断，正在接受真实协作场景的检验。

---

## 当前如何参与

本仓库由组织分析层（whitepaper）、通用工作节点框架（framework）与映射验证层（mapping）三层并行构成。欢迎围绕文档清晰度、接口边界、框架与 runtime 的映射衔接提出修正。
