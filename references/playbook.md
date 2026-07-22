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

## Frontend functional cases

1. Truncation rules depend on **font/line-height/width** — assert line count behavior, not character counts, unless PRD gives chars.
2. Expand/collapse: verify **label swap**, **full text equality to source**, **layout reflow**, **state reset on entity switch**.
3. Empty/fail: assert **whole module absence** (title+body+control), not only empty body.
4. “一段文本无跳转” → click body must not route; only expand/collapse controls act.
5. Do not mix **content wording quality** cases into FE-only requests.

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

## Process

1. Always list **待补充信息** instead of inventing business fixtures.
2. Export both human-readable summary and template-compatible xlsx when a template exists.
3. Run privacy scrub before any public share.
4. After delivery, write 2–8 generalized memory patterns via `scripts/memory.py update`.
5. When API+UI both present, deliver 外显字段映射表 in 交付说明.

## Suggested future upgrades (agents may add below)

<!-- AUTO-UPGRADE: append dated bullets, no secrets -->

- 2026-07-21: Initial playbook from FE expand/collapse + API conclusion-module style work (sanitized).
- 2026-07-22: Display-field abnormal matrix (int/string/array/object + single-line/scroll/modal patterns).
