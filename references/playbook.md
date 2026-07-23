# Playbook — Curated Patterns (Auto-Upgradeable)

This file holds **stable, generalized** lessons. Agents may propose append-only updates after ≥3 similar runs. Keep entries privacy-safe.

## Requirements analysis

1. Split every requirement line into `FE` / `API` / `CONTENT` / `NF` / `UNCLEAR` before writing cases.
2. When **约束条件** and **验收标准** conflict, **prefer 验收标准** for expected results and record the conflict in 需求疑问清单.
3. “证据不足展示文案” vs “不展示模块” is a common product ambiguity — never silently pick without labeling 待确认 if both appear.

## Layer split (API vs FE) — do not mix

| Layer | Source of truth | Write | Do **not** write |
|-------|-----------------|-------|------------------|
| **API** | 模块/需求描述的**数据要求** + 接口文档 | 入参、错误码、字段类型、**需求规定的指标/字段集合**、列表规则、空数据形态、鉴权 | 吸顶、横滑、展开行数、卡片样式、布局适配 |
| **FE** | **UI 设计稿** + 需求**交互/显隐** | 有数据怎么展示/交互；空/异常数据怎么展示/交互；样式与设计一致 | 登录与否；「接口必须返回哪几项」的契约清单（完整集合放 API） |

1. **接口按需求返回数据**；前端 **返回什么展示什么、几条展几条**（样式适配）。二者不矛盾：契约在 API，渲染在 FE。  
2. 完整有数据场景缺需求指标 → **API/数据缺陷**；不完整 mock 少项 → FE **容错有几条展几条**，不要求前端补齐。  
3. 禁止把「单行省略 / 吸顶 / 卡片样式」写进接口预期结果。

## API cases

1. Cover **missing param** and **empty string** separately for each required query field.
2. Documented error messages are hard expects; undocumented type-coercion failures are “记录实际行为”.
3. Mock-stage APIs: prioritize **contract** (codes, types, echo ids) over business copy correctness.
4. After real DB wiring, re-run injection + not-found entity cases.
5. **Scenario taxonomy (mandatory when risk/empty/fail all appear):**  
   **风控 ≠ 网络异常 ≠ 接口内部错误(4xx/5xx) ≠ 错误数据(串号等) ≠ 数据为空(业务空/`[]`/`data:{}`)。**  
   Full table: `references/response-scenario-taxonomy.md`. Split cases even if UI all hides the module.
6. Risk/policy offline often = **success code + empty body** (e.g. `data:{}`) by entity id — not 500, not param 400.
7. Empty success body may be **minimal `{}`** or **structured empty** (keys present, empty arrays) — cover both; neither is transport failure.
8. Auth/anonymous access belongs in **API** cases only.

## Frontend functional cases

1. **Data-driven only:** FE cares about **是否有数据、数据是否正常** — not login state. 有数据→展示与交互；空数据→不展示/对应交互；异常数据→兼容展示与交互。
2. Structure FE suites as: **正常数据展示** | **正常数据交互** | **空数据展示/交互** | **异常/失败展示/交互**.
3. Styles follow **UI mockups**; interactions follow **PRD**; field values follow **API response**.
4. Truncation/expand depend on font/line-height/width — assert behavior, not magic char counts unless PRD says so.
5. Expand/collapse: label swap, full text = source, reflow, reset on entity switch.
6. Empty/fail: whole module absence when no displayable data; partial field missing must not break other blocks.
7. Hardcoded tab **labels** may be FE-fixed; **visibility** is data-driven (show tab only if that section has data).
8. **Do not merge hide scenarios:** risk empty-success, network, 4xx/5xx, wrong data, business empty — separate FE cases.
9. Do not mix content-generation quality suites into pure FE unless user asks; light content checks OK as P2.
10. Never put “anonymous/login can browse” as FE case if show/hide is purely API-data-driven — put auth on API side.

## Display fields from API (前端外显) — mandatory

Full matrix: `references/display-field-abnormal-matrix.md`.  
**Field-refined overlay (also mandatory):** `references/field-refined-case-rules.md`.

1. Map every UI-visible response field → type + surface + empty strategy before writing cases.
2. **int**: negative, zero, positive (minimum set for each displayed number).
3. **string**: empty, oversize, special characters; XSS-ish payloads must render as text.
4. **array**: empty, 1 item, few, many (~10), normal multi.
5. **object**: empty `{}`, fewer keys than schema, extra unknown keys (ignore extras), full keys.
6. **Layout shapes**: single-line + ellipsis; multi-line clamp; fixed-height scroll; modal with FE-fixed title + API body.
7. Partial object metrics: no crash; show only returned keys; typically one row left-aligned.
8. Empty core object often means **hide whole module**; empty leaf string often means **hide that row only**.
9. Empty modal body when title is FE-fixed: fallback copy vs blank → always 产品确认.
10. **Per-field independent cases** (no batch-by-type); one field + one scene per case.
11. FE field cases must state **【接口返回预期】** + **【前端页面渲染预期】** and cite UI稿 or PRD.
12. Split **API return cases** and **client display cases** into separate lists/files; do not merge multi-scenes into one case.
13. Nested structures: drill every leaf; empty `""` vs `null` as separate cases.
14. **Module PRD overrides** generic defaults (e.g. hide stats when 0) — annotate 备注; do not delete global matrix rules.

## Cross-module (same page / product family)

1. List sibling modules before scoping cases; note layout order and shared entity id.
2. Entity switch: all modules that bind the entity must refresh; no cross-talk of stale UI.
3. Sibling APIs often share `version` / `deviceType` (or equivalent) — reuse required-param matrices.
4. One module API fail may hide only that module; do not assume whole page fails unless PRD says so.
5. Memory category `CrossModule` is for these links — not for dumping multi-module case sheets.
6. Sibling isolation: **risk empty-data on module A** and **500/network on module A** are two FE cases — both may leave module B visible.

## Process

1. Always list **待补充信息** instead of inventing business fixtures.
2. Export both human-readable summary and template-compatible xlsx when a template exists — **into user workspace only**.
3. Run privacy scrub before any public share.
4. After delivery, **mandatory** `scripts/memory.py update` with 2–8 **generalized** patterns (no case xlsx, no case IDs).
5. When API+UI both present, deliver 外显字段映射表 in 交付说明.
6. Never commit local memory or real project cases into the skill repository.
7. First `snapshot` empty on a new machine is normal.
8. **Append-only experience (strict):** new lessons that do **not** conflict with old playbook/memory → **add only, never delete old**. If they **conflict** → **ask the user**; do not auto-drop prior rules. Checklist rewrites must keep prior mandatory detail bullets.

## Suggested future upgrades (agents may add below)

<!-- AUTO-UPGRADE: append dated bullets, no secrets, no case libraries -->

- 2026-07-21: Initial playbook from FE expand/collapse + API conclusion-module style work (sanitized).
- 2026-07-22: Display-field abnormal matrix (int/string/array/object + single-line/scroll/modal patterns).
- 2026-07-22: Memory isolation + CrossModule patterns; cases stay in user workspace only.
- 2026-07-22: Response scenario taxonomy — risk control ≠ network ≠ 4xx/5xx ≠ wrong data ≠ empty business data.
- 2026-07-22: Strict API vs FE layer split; FE data-driven only (no login); API owns PRD metric sets, FE owns design+interaction.
- 2026-07-22: Append-only memory/playbook — never delete non-conflicting prior experience; conflicts escalate to user.
- 2026-07-23: Field-refined case rules overlay — per-field cases, dual expects, no batch-by-type; PRD overrides defaults.
