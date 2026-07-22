# Playbook — Curated Patterns (Auto-Upgradeable)

This file holds **stable, generalized** lessons. Agents may propose append-only updates after ≥3 similar runs. Keep entries privacy-safe.

## Requirements analysis

1. Split every requirement line into `FE` / `API` / `CONTENT` / `NF` / `UNCLEAR` before writing cases.
2. When **约束条件** and **验收标准** conflict, **prefer 验收标准** for expected results and record the conflict in 需求疑问清单.
3. “证据不足展示文案” vs “不展示模块” is a common product ambiguity — never silently pick without labeling 待确认 if both appear.

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

## Frontend functional cases

1. Truncation rules depend on **font/line-height/width** — assert line count behavior, not character counts, unless PRD gives chars.
2. Expand/collapse: verify **label swap**, **full text equality to source**, **layout reflow**, **state reset on entity switch**.
3. Empty/fail: assert **whole module absence** (title+body+control), not only empty body.
4. “一段文本无跳转” → click body must not route; only expand/collapse controls act.
5. Do not mix **content wording quality** cases into FE-only requests.
6. **Do not merge hide scenarios:** risk empty-success, network error, 4xx/5xx, wrong data, business empty lists need **separate** FE cases (preconditions differ: toast, recovery, sibling modules).
7. Show-if-has-data: both `data:{}` and structured empty lists count as no-data; still separate mocks/cases from server error.

## Display fields from API (前端外显) — mandatory

Full matrix: `references/display-field-abnormal-matrix.md`.

1. Map every UI-visible response field → type + surface + empty strategy before writing cases.
2. **int**: negative, zero, positive (minimum set for each displayed number).
3. **string**: empty, oversize, special characters; XSS-ish payloads must render as text.
4. **array**: empty, 1 item, few, many (~10), normal multi.
5. **object**: empty `{}`, fewer keys than schema, extra unknown keys (ignore extras), full keys.
6. **Layout shapes**: single-line + ellipsis; multi-line clamp; fixed-height scroll; modal with FE-fixed title + API body.
7. Partial object metrics: no crash; show only returned keys; typically one row left-aligned.
8. Empty core object often means **hide whole module**; empty leaf string often means **hide that row only**.
9. Empty modal body when title is FE-fixed: fallback copy vs blank → always 产品确认.

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

## Suggested future upgrades (agents may add below)

<!-- AUTO-UPGRADE: append dated bullets, no secrets, no case libraries -->

- 2026-07-21: Initial playbook from FE expand/collapse + API conclusion-module style work (sanitized).
- 2026-07-22: Display-field abnormal matrix (int/string/array/object + single-line/scroll/modal patterns).
- 2026-07-22: Memory isolation + CrossModule patterns; cases stay in user workspace only.
- 2026-07-22: Response scenario taxonomy — risk control ≠ network ≠ 4xx/5xx ≠ wrong data ≠ empty business data.
