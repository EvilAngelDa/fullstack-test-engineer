# Case Template Semantics

Default import-oriented columns (Chinese headers common in domestic QA platforms):

| Column | Required | Notes |
|--------|----------|-------|
| 用例名称 | Yes | Start with layer tag: `【正常】` `【异常】` `【边界】` `【展示】` `【交互】` `【显隐】` `【安全】` |
| 所属模块 | Yes | Hierarchical, e.g. `/Product/Module/API/xxx` or `/Product/Module/Frontend/xxx` |
| 标签 | No | `;` or `,` separated: `接口;正向;P0` / `前端;展开;交互` |
| 前置条件 | Prefer | Env, data, account role — **no secrets** |
| 步骤描述 | Yes | Single action per step when using STEP mode |
| 预期结果 | Yes | Observable, assertable; mark 待确认 if doc gap |
| 编辑模式 | Prefer | `STEP` multi-step / `TEXT` narrative |
| 备注 | No | Doc gaps, mock notes, conflict flags |
| 用例状态 | No | `Prepare` / `Underway` / `Completed` |
| 责任人 | No | Platform user id — leave empty if unknown |
| 用例等级 | Yes | `P0` smoke · `P1` core · `P2` extended · `P3` low |

## Priority guidance

| Level | Meaning |
|-------|---------|
| P0 | Smoke / release blockers (happy path + critical hide/fail + key contract) |
| P1 | Core rules (enums, expand/collapse, binding, main negatives) |
| P2 | Boundaries, multi-env consistency, rapid click, multi-width |
| P3 | Nice-to-have, rare paths |

## STEP multi-row rule

When exporting xlsx compatible with multi-row STEP templates:

- Merge all columns **except** 步骤描述 / 预期结果 across step rows
- One logical case id per merged block (name is unique)
