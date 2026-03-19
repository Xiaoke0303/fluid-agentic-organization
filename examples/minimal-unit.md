# FAO Minimal Unit (Example)

一个最小的 FAO 协作单元示例。

---

## Task
goal: 更新 Minimal Core 文档

## Agents

kimi_claw:
role: 执行修改、提交 PR
authority:
- 修改文件
- 提交 commit
- 创建 PR
limit:
- 不可直接 merge

human:
role: review、merge、承担结果
authority:
- 审核变更
- 决定是否 merge
- 对最终结果负责

## Trace
- Git commit
- Pull Request

## Lifecycle
- 创建任务
- agent 执行修改
- 提交 PR
- human review
- merge 后结束

## Notes
- 这是一个最小单元，不包含多 agent 协作
- 不涉及任务编排或自动化系统
- 仅用于说明如何分配权限与责任
