# AGENTS.md — Loading `fullstack-test-engineer` on any agent

This file is for **OpenClaw, Codex, Hermes, Claude Code, Cursor, Copilot agents, Grok**, and other LLM coding agents.

## When to activate

Activate when the user asks for any of:

- test cases / 测试用例 / 接口用例 / 前端用例  
- requirement review / 需求疑问 / QA plan  
- bug report template filled from repro  
- `/fullstack-test` `/test-cases` `/qa`  

## Mandatory procedure

1. **Read** `SKILL.md` in this directory before writing cases.
2. **Resolve** `SKILL_ROOT` = this directory’s absolute path.
3. **Run** (best-effort):

   ```bash
   python3 "$SKILL_ROOT/scripts/memory.py" snapshot
   ```

   - Memory path: `$HOME/.fullstack-test-engineer/memory/<workspace-id>.md`
   - **First use: empty is normal** — do not fail the run.
   - Memory is **local to this machine**, not shipped with the skill git repo.

4. **Classify** requirements into FE / API / CONTENT / NF. Honor user filters (e.g. frontend-only).
5. Apply **display-field abnormal** rules and note **cross-module** links when multiple modules share a page.
6. **Do not invent** business fixtures; emit 待补充信息清单.
7. **Write** deliverables only to the **user project workspace** (never as a case library inside `SKILL_ROOT`).
8. **Mandatory after success:** `memory.py update` with **generalized** patterns only (include `CrossModule` when relevant).  
   - No full cases, no case IDs, no xlsx content in memory.
9. If user will publish artifacts: `scrub_privacy.py --path <artifacts> --report`.

See `references/memory-and-isolation.md`.

## Tool permissions needed

| Need | Why |
|------|-----|
| Read files | PRD, API, screenshots, templates |
| Write files | Cases under **user** workspace; memory under `$HOME` |
| Shell | `python3 scripts/*.py` |
| Network | Optional; only if user asks live API probe |

No privileged deploy or secret access required.

## Output contract

Every completed run should include:

1. Paths of generated files  
2. Case counts by priority  
3. Layer filter applied  
4. Open questions list  
5. Memory update summary (new/merged patterns; note if first-run empty)  
6. Privacy scan summary if publishing  

## Anti-patterns (do not)

- Dumping only abstract “test points” without steps/expects  
- Mixing content-generation quality suites into FE-only requests  
- Hardcoding private hostnames, tokens, or personal paths into cases  
- Writing exploits or attack payloads beyond basic injection **strings** for negative input tests  
- Putting real project case xlsx into the skill repository or `examples/`  
- Expecting non-empty memory right after cloning the skill  
- Skipping `memory.py update` after a successful delivery  

## Skill path discovery

```text
<workspace>/fullstack-test-engineer/SKILL.md
~/.grok/skills/fullstack-test-engineer/SKILL.md
```

Prefer the path the user names; otherwise search for `fullstack-test-engineer/SKILL.md`.
