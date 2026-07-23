# Default Coverage Matrix

Use as a checklist. Drop rows that do not apply. Do not invent expects for unchecked rows.

## Layer: API

| Area | Examples |
|------|----------|
| Happy path | Legal params → success code + body shape |
| Required params | Missing / empty string each required field |
| Type / enum | Wrong type; out-of-range enum (note if doc only lists happy enums) |
| Boundary | Min/max length; zero/negative numbers if numeric |
| Error codes | Only codes documented as hard expects |
| Method/path | Wrong verb; typo path |
| Idempotency | Repeat safe methods |
| Concurrency | Parallel reads no cross-talk |
| Auth | With/without credential if product requires |
| Security light | Injection chars, XSS payloads in params (no exploit kit) |
| Scenario taxonomy | Risk/policy empty-success vs network vs 4xx/5xx vs wrong data vs business empty — **split** (see response-scenario-taxonomy.md) |

## Layer: Frontend functional

| Area | Examples |
|------|----------|
| Placement | Relative to sibling modules |
| Structure | Title, icon, container vs design |
| Content binding | Current entity only; switch resets stale data |
| Truncation | Max N lines + expand entry |
| Expand/collapse | Full text; control label swap; restore |
| Short content | No expand control |
| Empty / fail | Hide module or empty-state per PRD |
| No navigation | Body text not a link unless designed |
| Interaction stress | Multi toggle; rapid click |
| Layout | Expand grows card; no overlap; scroll ok |
| Width | Line clamp still correct on narrow/wide |

## Layer: Display-field abnormal (API fields shown on UI) — **required when applicable**

Detail: `display-field-abnormal-matrix.md`.  
**Refined per-field overlay:** `field-refined-case-rules.md` (one field + one scene per case; dual expects on FE).

| Type | Must-cover abnormal set |
|------|-------------------------|
| int / number | negative, 0, positive |
| string | empty (`""` and `null` separate), very long, special chars; safe render of `<>&` |
| array `[]` | empty, 1, few, many (~10), normal multi; order matches API; nest drill-down |
| object `{}` | empty, fewer keys, extra unknown keys (not shown), full keys; nest drill-down |
| single-line UI | overflow → `...` (cite UI稿) |
| multi-line UI | clamp / expand (cite UI稿) |
| scroll / modal | fixed height + vertical scroll for long body |
| empty strategies | hide module vs hide row vs FE fallback copy (PRD overrides defaults) |
| case granularity | **no batch-by-type**; name field path + scene + UI/PRD basis |

## Layer: Content quality (only if requested)

| Area | Examples |
|------|----------|
| Required semantic parts | Advantage / audience / risk if PRD requires |
| Forbidden wording | Absolute marketing phrases |
| Evidence insufficient | Message vs hide — follow acceptance |

## Layer: Non-functional (light by default)

| Area | Examples |
|------|----------|
| Perf smoke | Single-request latency baseline note |
| Compatibility | Browsers / OS / resolution list from product matrix |
| Security checklist | Authz, injection, XSS, plaintext, unauthenticated surface |
