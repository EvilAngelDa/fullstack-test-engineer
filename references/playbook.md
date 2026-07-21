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

## Process

1. Always list **待补充信息** instead of inventing business fixtures.
2. Export both human-readable summary and template-compatible xlsx when a template exists.
3. Run privacy scrub before any public share.
4. After delivery, write 2–8 generalized memory patterns via `scripts/memory.py update`.

## Suggested future upgrades (agents may add below)

<!-- AUTO-UPGRADE: append dated bullets, no secrets -->

- 2026-07-21: Initial playbook from FE expand/collapse + API conclusion-module style work (sanitized).
