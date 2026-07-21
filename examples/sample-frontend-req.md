# Sample Frontend Requirement (fictional)

## Module

AI highlight summary card under series basic info.

## Display & interaction

- Show a single paragraph of conclusion text; **no navigation** on body click.
- Default **max 2 lines**; if overflow, show **Expand** control.
- Tap Expand → full text + **Collapse** control.
- Title example: `AI亮点总结` with leading icon; rounded gradient card (see design).

## Abnormal

Hide the entire module when:

- No data
- Request failed
- Data abnormal / insufficient evidence (per acceptance)

## Non-goals for FE-only suite

- Content generation quality (absolute wording bans, multi-part semantic composition) unless separately requested.
- API parameter validation matrix (belongs to API suite).
