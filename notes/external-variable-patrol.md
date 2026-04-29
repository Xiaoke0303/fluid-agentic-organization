# External Variable Patrol

> FAO 外部变量巡检的 sidecar 工作笔记。不是新闻摘要，不是白皮书草稿，不是自动研究档案。

---

## Status

- **state**: template
- **cron/task enabled**: no
- **default execution**: manual only
- **output type**: sidecar observation
- **relation to HEARTBEAT.md**: implements the pending fao-external-variable-patrol output format

---

## Purpose

This file records external-variable observations that may affect FAO assumptions.

It is **not**:
- a news digest
- a whitepaper draft
- an automatic research archive
- an argument for changing FAO mainline
- evidence that cron/task has been enabled

---

## Scope

External patrol may observe:

1. **Agent Runtime**
   - OpenClaw, Claude Code, Codex, Kimi / GLM / Zhipu, OpenAI agent runtime
   - tool execution boundaries, session stability

2. **Agent Memory**
   - long-term memory, context engineering, RAG
   - LoRA / internalized memory, memory consolidation, cross-session continuity

3. **Agent Governance**
   - approval, audit, permission, truthfulness, failure reporting, human-in-the-loop

4. **Multi-Agent Orchestration**
   - agent mesh, workflow agent, DAG orchestration, A2A bus, delegation

5. **Enterprise Adoption**
   - AI employee, AI analyst, AI coding agent, enterprise deployment, actual ROI

6. **Cost / Context Budget**
   - token cost, inference cost, human review cost, context budget, resource routing

7. **Regulation / Liability**
   - AI liability, agent governance regulation, financial AI compliance, responsibility boundary

---

## Entry Template

### YYYY-MM-DD External Variable Patrol

#### Scan Scope

- **Sources checked**:
  - 
- **Domains checked**:
  - Agent Runtime:
  - Agent Memory:
  - Agent Governance:
  - Multi-Agent Orchestration:
  - Enterprise Adoption:
  - Cost / Context Budget:
  - Regulation / Liability:

#### Hits

Maximum 3 hits per patrol.

##### Hit 1

- **title**:
- **source**:
- **date**:
- **factual summary**:
- **FAO relevance**:
- **impacted FAO assumption**:
- **suggested line**: whitepaper / toolkit / cost sidecar / memory sidecar / guarantee line / ignore for now
- **truth-state**: 已执行 / 已验证 / 未命中 / 失败 / 推断 / 未确认
- **human confirmation needed**: yes / no

##### Hit 2

- **title**:
- **source**:
- **date**:
- **factual summary**:
- **FAO relevance**:
- **impacted FAO assumption**:
- **suggested line**:
- **truth-state**:
- **human confirmation needed**:

##### Hit 3

- **title**:
- **source**:
- **date**:
- **factual summary**:
- **FAO relevance**:
- **impacted FAO assumption**:
- **suggested line**:
- **truth-state**:
- **human confirmation needed**:

#### No-hit Record

Use this section if no meaningful external variable was found.

- **result**: no hit
- **reason**:
- **truth-state**: 未命中
- **next action**: no frequency increase

#### Reflection

Only answer these four questions:

1. Did any external variable affect a FAO assumption?
2. Which FAO line may be affected?
3. Is this worth entering a sidecar?
4. Does this require human confirmation?

---

## Red Lines

- Do not treat news as conclusions.
- Do not auto-modify whitepaper/.
- Do not auto-modify framework/.
- Do not auto-create theory terms.
- Do not auto-open PR.
- Do not auto-merge.
- Do not increase frequency because of no-hit results.
- Do not write long-form research into memory/.
- Distinguish fact / inference / unverified / guessed.
- Maximum 3 hits per patrol.

---

## Activation

- This file does not activate patrol.
- Real cron/task activation requires explicit human confirmation.
- First patrol must be manual.
- Output format must be validated before any recurring task is considered.
