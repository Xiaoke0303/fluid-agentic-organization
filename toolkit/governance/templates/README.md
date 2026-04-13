# Templates

> 节点接入模板，不是运行内核。

---

## 文件说明

| 文件 | 用途 |
|------|------|
| `identity-cloud-node.md` | 内网云节点的身份锚点模板 |
| `user.md` | 接口另一端角色模型占位（观察期，有意保留） |

---

## 迁移状态

`templates/` 当前应理解为历史实现来源，新接入请优先参考 `framework/` 下的对应文件。

- `identity-cloud-node.md` — 当前保留为新框架分层前的历史实现参考。其真实性约束部分已由 [`framework/assurance/TRUTH-CONTRACT.md`](../../framework/assurance/TRUTH-CONTRACT.md) 承接，角色边界相关内容请参考 [`framework/runtime/ROLE-CONTRACT.md`](../../framework/runtime/ROLE-CONTRACT.md)。其中 "Cloud Node / 组织节点" 身份定位尚无 framework 内一对一正式承接，不应视为已迁移完成。
- `user.md` — 当前仍保留为 legacy 来源，与根目录 `USER.md` 的定位并不等价，暂不做正式迁移判断。

---

## 与内核的关系

- `toolkit/minimal-core/` — 运行内核（方向、记忆、节律）
- `toolkit/governance/` — 治理护栏（真实性约束、失败报告、最小自主排查）
- `templates/` — 接入模板（身份锚点、用户接口占位）

模板层不替代内核，只提供节点接入时的初始结构。
