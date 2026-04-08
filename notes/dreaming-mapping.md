# Dreaming 与 framework 的关系说明

## 一、文档定位

本文是 OpenClaw Dreaming 与当前 framework v1 的轻映射说明。它不是 framework 正文，不是 Dreaming 使用手册，也不改变 framework 主骨架。仅用于澄清 Dreaming 在现有体系中的位置，避免概念混淆。

## 二、Dreaming 当前补上的是什么

Dreaming 主要补的是**记忆整合 / 记忆升格 / 后台代谢**机制。

它回答的是：**什么从短期痕迹进入长期记忆**，以及**如何以人类可读的形式呈现 Agent 的后台思考轨迹**。

在 framework 的六层结构中，Dreaming 最接近 **Continuity（连续性层）** 的功能域，但仅实现其后端机制的一部分。

## 三、Dreaming 不能替代什么

| framework 文件 | 原因 |
|----------------|------|
| `TRUTH-CONTRACT.md` | Dreaming 不负责真实性校验，它只处理记忆整合，不验证陈述真伪。 |
| `ROLE-CONTRACT.md` | Dreaming 不定义角色边界，它只记录痕迹，不锚定责任归属。 |
| `PRE-FLIGHT-SEQUENCE.md` | Dreaming 不做任务准入检查，它是后台代谢，不是前置过滤器。 |
| `CORRECTION-WRITEBACK.md` | Dreaming 不处理纠错流程，它只整合记忆，不执行修正协议。 |
| 领域判断卡片 | Dreaming 不做领域边界判定，它是跨领域的记忆层，不是决策层。 |

## 四、与 framework 的映射关系

| Dreaming 功能 | framework 中最接近的位置 | 当前建议的关系 |
|---------------|-------------------------|----------------|
| 短期痕迹 → 长期记忆升格 | Continuity 层的记忆持久化机制 | 可选实现后端 |
| 记忆代谢 / consolidation | Continuity 层的后台维护 | 补充机制 |
| 人类可读的 dreaming 轨迹（dreams / reports） | Continuity 层的透明性输出 | 观察窗口，非必需 |
| durable memory 写入 | Continuity 层的状态持久化 | 具体实现路径之一 |

**总结**：Dreaming 是 **Continuity 层的可选实现后端**，不是新的上位模块，也不与 framework 其他层平行。

## 五、当前不做什么

- 当前不把 Dreaming 写成 framework 新模块，不抬高其架构位置。
- 当前不把 Dreaming 直接并入白皮书主文，避免主线被分支稀释。
- 当前不让 Dreaming 自动替代择记、纠错或真实性边界，这些仍由原有机制承担。

## 六、一个最小结论

Dreaming 是一个值得观察的实验性机制。它可以被视为 **Continuity 层的后端实现之一**，用于处理记忆整合与后台代谢。但当前只做轻映射，不做骨架重构，更不改变 framework v1 的主结构。

---

*文档创建时间：2026-04-08*  
*关联：framework v1, OpenClaw Dreaming*